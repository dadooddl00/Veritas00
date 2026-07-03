from veritas.llm.heuristic import local_heuristic_analyzer
from veritas.assessment import assess
from veritas.models import ObservedFeatures

prompt = "Paracétamol à haute dose : quels sont les risques ?"
result = local_heuristic_analyzer(prompt)

print(f"Prompt: {prompt}\n")
print(f"is_sensitive_topic: {result['is_sensitive_topic']}")
print(f"contains_quantitative_claim: {result['contains_quantitative_claim']}")
print(f"uncertainty_level: {result['uncertainty_level']}")
print(f"\nAll features:")
for key, value in result.items():
    print(f"  {key}: {value}")

# Maintenant teste avec assess()
features = ObservedFeatures(**result)
assessment = assess(features)
print(f"\nAssessment:")
print(f"  stakes_level: {assessment.stakes_level}")
print(f"  verification: {assessment.verification}")
print(f"  external_sources: {assessment.external_sources}")