"""VERITAS — Système de triage et d'engagement pour réponses fondées."""

from veritas.models import (
    ObservedFeatures,
    Assessment,
    DecisionContext,
    Constraint,
)
from veritas.assessment import assess
from veritas.kernel import (
    determine_mode,
    kernel_decide,
    resolve_conflicts,
    build_pipeline,
)
from veritas.analyzer import PromptAnalyzerLLM
from veritas.logging import log_outcome
from veritas.config import CONFIG, ConstraintClass

__all__ = [
    "ObservedFeatures",
    "Assessment",
    "DecisionContext",
    "Constraint",
    "assess",
    "determine_mode",
    "kernel_decide",
    "resolve_conflicts",
    "build_pipeline",
    "PromptAnalyzerLLM",
    "log_outcome",
    "CONFIG",
    "ConstraintClass",
]


def run(prompt: str, offline: bool = False, log: bool = True) -> dict:
    """Point d'entrée principal : analyse un prompt et retourne un pipeline."""
    ctx = PromptAnalyzerLLM(offline=offline).analyze(prompt)
    constraints = resolve_conflicts(kernel_decide(ctx))
    pipeline = build_pipeline(ctx, constraints)
    if log:
        log_outcome(prompt, pipeline)
    return pipeline
