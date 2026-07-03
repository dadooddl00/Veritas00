"""Sous-module LLM — callers et heuristiques."""

from veritas.llm.callers import llm_caller
from veritas.llm.heuristic import local_heuristic_analyzer

__all__ = ["llm_caller", "local_heuristic_analyzer"]
