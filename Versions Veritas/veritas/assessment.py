"""Logique d'assessment — règles déterministes pour évaluer les constats."""

from veritas.models import ObservedFeatures, Assessment


def assess(f: ObservedFeatures) -> Assessment:
    """Règle déterministe unique : aucune valeur de politique ne provient
    directement du LLM. Le LLM/heuristique ne fournit que des constats."""
    reasons = []

    if f.is_sensitive_topic:
        stakes = "high"
        reasons.append("sujet_sensible_sante_securite")
    elif f.is_controversial_topic or f.explicit_depth_request:
        stakes = "high"
        reasons.append("controverse_ou_approfondissement_demande")
    elif f.contains_causal_claim or f.contains_quantitative_claim or f.mentions_current_fact:
        stakes = "medium"
        reasons.append("affirmation_causale_chiffree_ou_fait_date")
    else:
        stakes = "low"

    verification = "required" if (f.is_sensitive_topic or f.contains_quantitative_claim
                                   or f.mentions_current_fact or f.analysis_confidence < 0.4) else "optional"
    external_sources = "required" if (f.is_sensitive_topic or f.is_controversial_topic
                                       or f.mentions_current_fact) else (
        "recommended" if f.contains_quantitative_claim else "none")
    sensitivity = "high" if f.is_sensitive_topic else ("medium" if f.is_controversial_topic else "low")

    return Assessment(verification, external_sources, sensitivity, stakes, reasons)
