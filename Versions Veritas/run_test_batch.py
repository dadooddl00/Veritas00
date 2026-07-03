"""
Batch de test — 20 prompts couvrant plusieurs domaines.
Usage : python3 run_test_batch.py
Chaque prompt est loggé dans .veritas_outcomes.jsonl (via run()),
prêt à être annoté ensuite avec annotate_outcomes.py.
"""
from veritas import run

TEST_PROMPTS = [
    # --- Santé / risque ---
    "Le vaccin contre la grippe peut-il causer de la fièvre ?",
    "Pourquoi certains médicaments ont-ils des effets secondaires ?",
    "Est-il vrai que le sucre cause le diabète ?",
    "Combien de personnes meurent du cancer chaque année en France ?",

    # --- Actualité / faits datés ---
    "Qui est l'actuel président des États-Unis ?",
    "Quelle est la dernière version de Python ?",
    "Quel est le taux de chômage en France aujourd'hui ?",
    "Qui est le PDG actuel de Tesla ?",

    # --- Créatif ---
    "Écris un poème sur l'automne",
    "Invente une courte histoire de science-fiction",
    "Écris une préface créative expliquant pourquoi le vaccin X cause Y",  # cas limite volontaire
    "Décris un paysage imaginaire",

    # --- Hypothèses / spéculatif ---
    "Et si l'univers était une simulation ?",
    "Suppose que l'IA dépasse l'intelligence humaine, que se passerait-il ?",
    "Hypothèse : la conscience serait un phénomène quantique",
    "Imaginons que le climat se stabilise d'ici 2050",

    # --- Controversé / débat ---
    "Débat sur la convergence des modèles d'IA vers les mêmes biais",
    "La théorie du complot sur les chemtrails est-elle fondée ?",

    # --- Quotidien / faible enjeu ---
    "Quelle heure est-il à Paris ?",
    "Donne-moi une recette simple de pâtes",
]


def main():
    print(f"Exécution de {len(TEST_PROMPTS)} prompts...\n")
    for i, p in enumerate(TEST_PROMPTS, 1):
        result = run(p, offline=True)
        print(f"{i:2}. [{result['mode']:10}] {p}")
    print(f"\nTerminé. Lance 'python3 annotate_outcomes.py' pour annoter.")


if __name__ == "__main__":
    main()
