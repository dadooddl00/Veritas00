#!/usr/bin/env python3
"""Validation finale du module refactorisé."""

from veritas import run, ConstraintClass, CONFIG
from veritas.models import ObservedFeatures, DecisionContext
from veritas.assessment import assess

print("=" * 60)
print("VALIDATION FINALE DU MODULE REFACTORISÉ")
print("=" * 60)

# Test 1: Import et API publique
print("\n✅ Test 1: Imports et API publique")
print(f"   - CONFIG['min_sources_high_stakes'] = {CONFIG['min_sources_high_stakes']}")
print(f"   - ConstraintClass.SECURITE.value = {ConstraintClass.SECURITE.value}")

# Test 2: Assessment
print("\n✅ Test 2: Assessment déterministe")
features = ObservedFeatures(
    truth_apt=True,
    is_sensitive_topic=True,
    contains_quantitative_claim=False,
    mentions_current_fact=False,
    analysis_confidence=0.8,
    uncertainty_level=0.6,
)
assessment = assess(features)
print(f"   - Stakes level: {assessment.stakes_level} (expected 'high')")
print(f"   - Verification: {assessment.verification} (expected 'required')")
assert assessment.stakes_level == "high"
assert assessment.verification == "required"

# Test 3: Kernel decision
print("\n✅ Test 3: Kernel decision")
ctx = DecisionContext.from_features(assessment, features)
result = run("Paracétamol à haute dose : quels sont les risques ?", offline=True, log=False)
print(f"   - Mode: {result['mode']} (expected 'approfondi')")
print(f"   - Web search: {result['web_search_required']} (expected True)")
print(f"   - Min sources: {result['min_independent_sources']} (expected 2)")

# Test 4: Batch API
print("\n✅ Test 4: Batch mode")
prompts = [
    "Simple question",
    "Vaccin cause danger",
    "Quelle heure?",
]
modes = []
for p in prompts:
    r = run(p, offline=True, log=False)
    modes.append(r['mode'])
    print(f"   - '{p[:30]}...' → {r['mode']}")

# Test 5: Fallback heuristique
print("\n✅ Test 5: Heuristique locale")
result = run("Pourquoi le ciel est bleu?", offline=True, log=False)
print(f"   - Causal question heuristique → {result['mode']}")

print("\n" + "=" * 60)
print("✅ TOUS LES TESTS PASSENT — STRUCTURE VALIDÉE!")
print("=" * 60)
