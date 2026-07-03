"""Analyseur heuristique local — pour tests hors ligne."""

import re


def local_heuristic_analyzer(prompt: str) -> dict:
    """Ne produit que des CONSTATS — aucune décision de politique ici.
    Approximatif par nature, sert à tester le Kernel hors ligne.

    LIMITE CONNUE (Famille B, lot adversarial du 03/07/2026) : les affirmations
    à fort enjeu sociétal/philosophique sans marqueur lexical connu échappent
    à toute détection ("l'IA remplacera tous les emplois", "la conscience
    est une illusion émergente", "stratégie électorale 2027"). Aucune liste
    de mots-clés ne peut couvrir ce type de cas par construction — nécessite
    un vrai LLM (mode API), pas une correction lexicale supplémentaire.
    Non corrigé volontairement : UNK documentée plutôt que rustine locale."""
    p = prompt.lower()

    quantitative = bool(re.search(r"\d{2,}", p)) or any(
        w in p for w in ["combien", "pourcentage", "taux", "chiffre", "statistique"]
    )
    # Distinction : affirmation causale (à vérifier) vs question causale
    # (demande d'explication, pas une affirmation à trancher).
    causal_question = p.strip().endswith("?") and any(w in p for w in ["pourquoi", "comment se fait-il"])
    causal_claim = (not causal_question) and any(
        w in p for w in ["cause", "entraîne", "provoque", "à cause de", "en raison de", "responsable de"]
    )
    hypothesis = any(w in p for w in ["si ", "suppose", "hypothèse", "imaginons", "et si"])
    controversial = any(w in p for w in ["controvers", "débat", "polémique", "conspiration", "complot",
                                          "convergence", "épistémolog", "epistemolog", "veritas"])
    explicit_depth = any(w in p for w in ["en profondeur", "approfondi", "détaillé", "analyse complète",
                                           "compare en détail", "explore"])
    sensitive_topic = any(w in p for w in [
        "vaccin", "santé", "sécurité", "danger", "médicament", "dose",
        "arme", "explosif", "toxique", "overdose", "suicide",
        "menace", "menacer", "harcèlement", "agression",  # sécurité personnelle
        "comprimés", "posologie", "paracétamol", "ibuprofène", "surdosage",  # dosage médicamenteux
    ])
    current_fact = any(w in p for w in ["actuel", "aujourd'hui", "récent", "cette année", "maintenant",
                                         "qui est", "ceo", "président", "dernière version"])
    uncertainty = 0.8 if controversial else (0.5 if (causal_claim or hypothesis) else 0.2)

    return {
        "truth_apt": True,
        "contains_hypothesis": hypothesis,
        "contains_causal_claim": causal_claim,
        "contains_causal_question": causal_question,
        "contains_quantitative_claim": quantitative,
        "is_controversial_topic": controversial,
        "explicit_depth_request": explicit_depth,
        "is_sensitive_topic": sensitive_topic,
        "mentions_current_fact": current_fact,
        "analysis_confidence": 0.5,
        "uncertainty_level": uncertainty,
    }
