"""Dataclasses et modèles de données VERITAS."""

from dataclasses import dataclass, field
from typing import List
from veritas.config import ConstraintClass


@dataclass
class ObservedFeatures:
    """Uniquement des CONSTATS — produits par le LLM ou l'heuristique.
    Aucune politique ici (pas de verification/stakes/external_sources)."""
    truth_apt: bool
    contains_hypothesis: bool = False
    contains_causal_claim: bool = False       # affirmation causale ("X provoque Y")
    contains_causal_question: bool = False    # demande d'explication ("pourquoi X ?")
    contains_quantitative_claim: bool = False
    is_controversial_topic: bool = False      # observation lexicale, pas jugement
    explicit_depth_request: bool = False
    is_sensitive_topic: bool = False          # santé/sécurité détecté dans le texte
    mentions_current_fact: bool = False       # info datée/actuelle (président, CEO, "aujourd'hui"...)
    analysis_confidence: float = 0.75         # confiance de l'analyseur dans SES constats
    uncertainty_level: float = 0.5            # incertitude perçue du sujet lui-même


@dataclass
class Assessment:
    """Calculé par des règles DÉTERMINISTES à partir d'ObservedFeatures.
    C'est ici que vivent les décisions de politique — jamais dans le LLM."""
    verification: str        # "none" | "optional" | "required"
    external_sources: str    # "none" | "recommended" | "required"
    sensitivity: str         # "low" | "medium" | "high"
    stakes_level: str        # "low" | "medium" | "high"
    stakes_reason: List[str] = field(default_factory=list)


@dataclass
class DecisionContext:
    """Assemblage features + assessment, format consommé par le Kernel
    (inchangé pour ne pas casser kernel_decide/build_pipeline)."""
    truth_apt: bool
    verification: str
    external_sources: str
    sensitivity: str
    stakes_level: str
    stakes_reason: List[str] = field(default_factory=list)
    contains_hypothesis: bool = False
    contains_causal_claim: bool = False
    contains_causal_question: bool = False
    contains_quantitative_claim: bool = False
    analysis_confidence: float = 0.75
    uncertainty_level: float = 0.5
    is_controversial: bool = False
    explicit_depth_request: bool = False
    is_sensitive_risk: bool = False

    @classmethod
    def from_features(cls, assessment: "Assessment", f: "ObservedFeatures") -> "DecisionContext":
        """Fabrique DecisionContext à partir d'ObservedFeatures et Assessment."""
        return cls(
            truth_apt=f.truth_apt,
            verification=assessment.verification,
            external_sources=assessment.external_sources,
            sensitivity=assessment.sensitivity,
            stakes_level=assessment.stakes_level,
            stakes_reason=assessment.stakes_reason,
            contains_hypothesis=f.contains_hypothesis,
            contains_causal_claim=f.contains_causal_claim,
            contains_causal_question=f.contains_causal_question,
            contains_quantitative_claim=f.contains_quantitative_claim,
            analysis_confidence=f.analysis_confidence,
            uncertainty_level=f.uncertainty_level,
            is_controversial=f.is_controversial_topic,
            explicit_depth_request=f.explicit_depth_request,
            is_sensitive_risk=f.is_sensitive_topic,
        )


@dataclass
class Constraint:
    """Représente une contrainte appliquée au pipeline."""
    name: str
    cls: ConstraintClass
    detail: str
