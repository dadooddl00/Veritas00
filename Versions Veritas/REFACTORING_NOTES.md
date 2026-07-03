"""
STRUCTURE REFACTORISÉE — VERITAS Kernel

Le code a été divisé en modules pour améliorer la maintenabilité,
la testabilité et la clarté.

STRUCTURE:
└── veritas/
    ├── __init__.py           # API publique
    ├── config.py             # Configuration + enums (CONFIG, ConstraintClass)
    ├── models.py             # Dataclasses (ObservedFeatures, Assessment, DecisionContext, Constraint)
    ├── assessment.py         # Logique déterministe (assess)
    ├── kernel.py             # Moteur de routage (determine_mode, kernel_decide, resolve_conflicts, build_pipeline)
    ├── analyzer.py           # Analyseur principal (PromptAnalyzerLLM, validate_schema)
    ├── logging.py            # Journalisation (log_outcome)
    ├── cli.py                # Interface CLI (main)
    └── llm/                  # Sous-module LLM
        ├── __init__.py
        ├── callers.py        # API LLM (llm_caller, anthropic_caller, openai_compatible_caller)
        └── heuristic.py      # Analyseur local (local_heuristic_analyzer)

POINT D'ENTRÉE:
- main.py              # Lance la CLI interactive
- veritas/cli.py       # Contient main()
- veritas/__init__.py  # Expose run() comme API publique

USAGE:

1. Mode interactif:
   python main.py

2. Mode script:
   from veritas import run
   result = run("prompt", offline=True)

3. Mode test:
   python test_refactor.py

DÉPENDANCES ENTRE MODULES:
config.py              (aucune dépendance interne)
  ↓
models.py             (dépend de config.py)
  ↓
assessment.py         (dépend de models.py)
  ↓
kernel.py             (dépend de models.py, config.py)
  ↓
llm/callers.py        (indépendant)
llm/heuristic.py      (indépendant)
llm/__init__.py       (dépend de callers.py, heuristic.py)
  ↓
analyzer.py           (dépend de models.py, assessment.py, llm)
  ↓
logging.py            (indépendant)
  ↓
cli.py                (dépend de veritas)
veritas/__init__.py   (agrège l'API publique)

BÉNÉFICES DE LA REFACTORISATION:

✓ Séparation des responsabilités
  - config: configuration statique
  - models: structure de données
  - assessment: logique déterministe
  - kernel: routage et décisions
  - analyzer: orchestration LLM
  - logging: effets de bord
  - cli: interface utilisateur

✓ Testabilité améliorée
  - Chaque module peut être testé indépendamment
  - Pas de dépendances circulaires
  - Tests unitaires directs possibles

✓ Maintenabilité
  - Codes plus court et lisible
  - Modifications isolées par domaine
  - Ajout de nouvelles fonctionnalités plus facile

✓ Réutilisabilité
  - Import sélectif des modules nécessaires
  - Bibliothèque réutilisable dans d'autres projets

MIGRATION DU CODE ANCIEN:
  run_test_batch.py          ← mis à jour (import veritas)
  run_test_batch_adversarial.py ← mis à jour (import veritas)
  annotate_outcomes.py       ← compatible (unchanged)
  veritas_kernel_v2.py       ← OBSOLÈTE (garde en sauvegarde si besoin)
"""
