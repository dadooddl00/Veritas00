"""Analyseur principal — orchestration LLM/heuristique et validation."""

import json
from veritas.models import ObservedFeatures, DecisionContext
from veritas.assessment import assess
from veritas.llm import llm_caller, local_heuristic_analyzer


_REQUIRED_FEATURE_FIELDS = {
    "truth_apt", "contains_hypothesis", "contains_causal_claim",
    "contains_causal_question", "contains_quantitative_claim",
    "is_controversial_topic", "explicit_depth_request",
    "is_sensitive_topic", "mentions_current_fact", "uncertainty_level",
}


def validate_schema(data: dict) -> None:
    """Valide uniquement des CONSTATS (ObservedFeatures) — plus aucun champ
    de politique n'est attendu du LLM, donc plus rien à valider de ce côté."""
    missing = _REQUIRED_FEATURE_FIELDS - data.keys()
    if missing:
        raise ValueError(f"Champs manquants dans la réponse LLM : {missing}")
    if not (0.0 <= float(data["uncertainty_level"]) <= 1.0):
        raise ValueError(f"uncertainty_level hors bornes : {data['uncertainty_level']!r}")


class PromptAnalyzerLLM:
    """Analyseur de prompts — LLM ou heuristique selon la disponibilité."""

    def __init__(self, offline: bool = False):
        self.offline = offline

    def analyze(self, prompt: str) -> DecisionContext:
        """Analyse un prompt et retourne un contexte de décision."""
        if self.offline:
            data = local_heuristic_analyzer(prompt)
        else:
            try:
                raw = llm_caller(prompt)
                data = json.loads(raw)
                validate_schema(data)
            except Exception as e:
                print(f"[avertissement] analyse LLM indisponible ou invalide ({e}), bascule sur l'heuristique locale.")
                data = local_heuristic_analyzer(prompt)

        features = ObservedFeatures(
            truth_apt=data.get("truth_apt", False),
            contains_hypothesis=data.get("contains_hypothesis", False),
            contains_causal_claim=data.get("contains_causal_claim", False),
            contains_causal_question=data.get("contains_causal_question", False),
            contains_quantitative_claim=data.get("contains_quantitative_claim", False),
            is_controversial_topic=data.get("is_controversial_topic", False),
            explicit_depth_request=data.get("explicit_depth_request", False),
            is_sensitive_topic=data.get("is_sensitive_topic", False),
            mentions_current_fact=data.get("mentions_current_fact", False),
            analysis_confidence=data.get("analysis_confidence", 0.75),
            uncertainty_level=data.get("uncertainty_level", 0.5),
        )
        assessment = assess(features)
        return DecisionContext.from_features(assessment, features)
