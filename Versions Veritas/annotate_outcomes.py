"""
Annotation interactive de .veritas_outcomes.jsonl
Usage : python3 annotate_outcomes.py
Ne touche qu'aux entrées où ground_truth_mode est encore null.
"""
import json

LOG_FILE = ".veritas_outcomes.jsonl"
MODES = ("direct", "standard", "approfondi")


def load():
    with open(LOG_FILE, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def save(entries):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")


def main():
    entries = load()
    # Filtre les entrées d'un ancien schéma (avant ajout du logging actuel)
    valid_entries = [e for e in entries if "prompt_snippet" in e and "mode_predicted" in e]
    skipped = len(entries) - len(valid_entries)
    if skipped:
        print(f"({skipped} ancienne(s) entrée(s) au format incompatible, ignorée(s).)\n")

    todo = [e for e in valid_entries if e.get("ground_truth_mode") is None]
    if not todo:
        print("Rien à annoter.")
        return

    print(f"{len(todo)} décision(s) à annoter. Entrée vide = passer. 'q' = quitter.\n")

    for e in todo:
        print("-" * 60)
        print(f"Prompt   : {e['prompt_snippet']}")
        print(f"Prédit   : {e['mode_predicted']}")
        print(f"Options  : {', '.join(MODES)}")
        choice = input("Mode correct > ").strip().lower()

        if choice == "q":
            break
        if not choice:
            continue
        if choice not in MODES:
            print(f"Ignoré (valeur invalide, attendu : {MODES})")
            continue

        e["ground_truth_mode"] = choice
        e["was_correct"] = (choice == e["mode_predicted"])
        save(entries)  # sauvegarde après chaque annotation, rien n'est perdu

    n_annotated = sum(1 for e in valid_entries if e.get("ground_truth_mode") is not None)
    n_correct = sum(1 for e in valid_entries if e.get("was_correct"))
    print(f"\nTotal annoté : {n_annotated} — dont corrects : {n_correct}")
    if n_annotated:
        print(f"Précision actuelle : {n_correct / n_annotated:.0%}")


if __name__ == "__main__":
    main()
