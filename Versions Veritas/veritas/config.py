"""Configuration et énumérations VERITAS."""

from enum import Enum


CONFIG = {"min_sources_high_stakes": 2}


class ConstraintClass(Enum):
    """Classification des contraintes par domaine."""
    SECURITE = 3
    EPISTEMIQUE = 2
    OPTIMISATION = 1
