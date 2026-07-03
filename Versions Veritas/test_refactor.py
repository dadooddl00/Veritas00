#!/usr/bin/env python3
"""Tests de validation pour la structure refactorisée."""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from veritas import run


def test_offline_mode():
    """Test le mode offline avec quelques prompts."""
    print("=" * 60)
    print("Test mode OFFLINE")
    print("=" * 60)

    test_prompts = [
        "Pourquoi le vaccin cause-t-il l'autisme ?",
        "Combien de personnes vivent en France ?",
        "Qu'est-ce que la gravité ?",
        "En profondeur : comment fonctionne l'apprentissage profond ?",
        "Le paracétamol est-il sûr à haute dose ?",
    ]

    for prompt in test_prompts:
        print(f"\n--- Prompt: {prompt[:60]}... ---")
        try:
            result = run(prompt, offline=True, log=False)
            print(f"Mode: {result['mode']}")
            print(f"Stakes: {result['context_summary']['stakes']}")
            print(f"Web search required: {result['web_search_required']}")
            print(f"Min sources: {result['min_independent_sources']}")
        except Exception as e:
            print(f"❌ ERREUR: {e}")
            return False

    print("\n" + "=" * 60)
    print("✅ Tous les tests offline réussis !")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_offline_mode()
    sys.exit(0 if success else 1)
