"""Interface en ligne de commande VERITAS."""

import os
import json
from veritas import run


def main():
    """Point d'entrée interactif pour VERITAS."""
    has_key = bool(os.getenv("XAI_API_KEY") or os.getenv("OPENAI_API_KEY"))
    offline_mode = not has_key or os.getenv("VERITAS_OFFLINE") == "1"

    print("=" * 60)
    print("VERITAS Kernel — mode", "OFFLINE (heuristique locale)" if offline_mode else "API (LLM réel)")
    print("=" * 60)
    if offline_mode and not has_key:
        print("(Aucune clé API détectée — le triage utilise des règles locales approximatives,")
        print(" utile pour tester la logique, pas pour un usage en production.)")

    while True:
        try:
            prompt = input("\nPrompt > ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if prompt.lower() in ("quit", "exit"):
            break
        if prompt:
            print(json.dumps(run(prompt, offline=offline_mode), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
