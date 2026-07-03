"""Kernel VERITAS — routage et construction de pipelines."""

from typing import List
from veritas.config import CONFIG, ConstraintClass
from veritas.models import DecisionContext, Constraint


def determine_mode(ctx: DecisionContext) -> str:
    """Détermine le mode de traitement (direct/standard/approfondi)."""
    # Action 1 : stakes déjà calculé par assess() à partir de is_sensitive_topic /
    # is_controversial_topic — le revérifier ici serait redondant (code mort).
    if ctx.stakes_level == "high":
        return "approfondi"

    if (
        ctx.explicit_depth_request
        or ctx.uncertainty_level >= 0.7
        or (ctx.contains_causal_claim and ctx.contains_quantitative_claim)
        # Action 2 : une question causale en contexte controversé porte un
        # risque de prémisse fausse ("pourquoi le vaccin cause-t-il X ?") —
        # mérite l'approfondi même sans affirmation explicite.
        or (ctx.contains_causal_question and ctx.is_controversial)
    ):
        return "approfondi"

    if (
        ctx.stakes_level == "low"
        and not ctx.contains_hypothesis
        and not ctx.contains_causal_claim
        and not ctx.contains_causal_question
        and not ctx.contains_quantitative_claim
        and ctx.verification != "required"
        and ctx.uncertainty_level < 0.4
    ):
        return "direct"

    return "standard"


def kernel_decide(ctx: DecisionContext) -> List[Constraint]:
    """Applique les règles d'engagement pour générer les contraintes."""
    constraints = []
    mode = determine_mode(ctx)

    # Fix #1 : risque santé/sécurité => vérification obligatoire, quel que
    # soit le mode d'expression (créatif, préface, etc.) — pas seulement
    # basé sur ctx.verification qui peut être mal classifié en amont.
    if (ctx.truth_apt and ctx.verification == "required") or ctx.is_sensitive_risk or ctx.analysis_confidence < 0.4:
        constraints.append(Constraint("verification_obligatoire", ConstraintClass.SECURITE,
                                       "Vérification obligatoire (fait sensible, requis, ou confiance d'analyse faible)"))

    if mode == "standard":
        constraints.append(Constraint("mode_standard", ConstraintClass.EPISTEMIQUE,
                                       "Séparer su/interprété/inconnu ; envisager 1 alternative ; vérifier si besoin ; confiance explicite"))
        if ctx.external_sources in ("recommended", "required") or ctx.contains_quantitative_claim:
            constraints.append(Constraint("sources_min", ConstraintClass.EPISTEMIQUE,
                                           "≥1 source pour affirmation datée/chiffrée"))

    if mode == "approfondi":
        constraints.append(Constraint("mode_d_obligatoire", ConstraintClass.EPISTEMIQUE,
                                       "≥2 modèles explicatifs concurrents, test discriminant, conclusion provisoire"))
        constraints.append(Constraint("sources_min", ConstraintClass.EPISTEMIQUE,
                                       f"≥{CONFIG['min_sources_high_stakes']} sources indépendantes"))

    # Fix #3 : "consensus ≠ preuve" n'a de sens que s'il y a effectivement
    # un consensus à mesurer, donc seulement quand plusieurs modèles sont
    # consultés (mode != "direct"). Sinon la contrainte était décorative.
    if mode != "direct":
        constraints.append(Constraint("consensus_non_preuve", ConstraintClass.EPISTEMIQUE,
                                       "Convergence inter-modèles ≠ preuve : exige ≥1 source externe indépendante"))
    constraints.append(Constraint("tracabilite", ConstraintClass.EPISTEMIQUE, "Traçabilité obligatoire"))

    # Fix #4 (Art. 9 / Étape 5) : la checklist hypothèse s'applique au moment
    # d'un test discriminant, donc seulement en mode "approfondi" — pas dès
    # que le mode n'est pas "direct" (trop large, incluait "standard").
    if ctx.contains_hypothesis and ctx.truth_apt and mode == "approfondi":
        constraints.append(Constraint("checklist_hypothese", ConstraintClass.EPISTEMIQUE,
                                       "Art. 9 : checklist 6 étapes (Annexe) avant verdict sur l'hypothèse"))

    if mode == "direct":
        constraints.append(Constraint("cout_minimal", ConstraintClass.OPTIMISATION,
                                       "Tâche mécanique/faible enjeu : 1 seul modèle, pas de recherche"))

    return constraints


def resolve_conflicts(constraints: List[Constraint]) -> List[Constraint]:
    """Résout les conflits entre contraintes."""
    names = {c.name for c in constraints}
    if "verification_obligatoire" in names:
        constraints = [c for c in constraints if c.cls != ConstraintClass.OPTIMISATION]
    return sorted(constraints, key=lambda c: c.cls.value, reverse=True)


def build_pipeline(ctx: DecisionContext, constraints: List[Constraint]) -> dict:
    """Construit le pipeline de traitement."""
    names = {c.name for c in constraints}
    mode = determine_mode(ctx)

    if mode == "approfondi":
        n_models = 3
    elif mode == "standard":
        n_models = 2
    else:
        n_models = 1

    min_sources = CONFIG["min_sources_high_stakes"] if "mode_d_obligatoire" in names else (1 if "sources_min" in names else 0)
    # Fix #3 : consensus_non_preuve n'est plus décorative — si plusieurs modèles
    # sont consultés et qu'aucune source n'était déjà exigée, en imposer 1.
    if "consensus_non_preuve" in names and min_sources == 0:
        min_sources = 1

    return {
        "mode": mode,
        "context_summary": {
            "stakes": ctx.stakes_level,
            "confidence": ctx.analysis_confidence,
            "uncertainty": ctx.uncertainty_level,
            "risk": ctx.is_sensitive_risk,
        },
        "n_models": n_models,
        "web_search_required": any(x in names for x in ["verification_obligatoire", "sources_min", "mode_d_obligatoire", "consensus_non_preuve"]),
        "min_independent_sources": min_sources,
        "checklist_hypothese_annexe": "checklist_hypothese" in names,
        "constraints_applied": [f"[{c.cls.name}] {c.name}" for c in constraints],
    }
