# VERITAS — Structure Refactorisée

## 📦 Organisation modulaire

Votre code a été réorganisé en **11 modules** avec des responsabilités claires :

```
veritas/
├── config.py          # 📋 Configuration (CONFIG, ConstraintClass)
├── models.py          # 🏗️ Dataclasses (ObservedFeatures, Assessment, DecisionContext)
├── assessment.py      # 🔍 Logique déterministe (assess)
├── kernel.py          # ⚙️ Moteur de routage (determine_mode, kernel_decide, build_pipeline)
├── analyzer.py        # 🔬 Orchestration LLM (PromptAnalyzerLLM, validate_schema)
├── logging.py         # 📝 Journalisation (log_outcome)
├── cli.py             # 💻 Interface interactive (main)
└── llm/
    ├── callers.py     # 🌐 API LLM (Anthropic, xAI, OpenAI)
    └── heuristic.py   # 🧠 Analyseur local (local_heuristic_analyzer)
```

## 🔄 Flux d'exécution

```
User Input
    ↓
cli.py (main)
    ↓
veritas.__init__.py (run)
    ↓
analyzer.py (PromptAnalyzerLLM.analyze)
    ├→ llm/callers.py (llm_caller)
    └→ llm/heuristic.py (local_heuristic_analyzer)
    ↓
assessment.py (assess)
    ↓
kernel.py (kernel_decide, build_pipeline)
    ↓
logging.py (log_outcome)
    ↓
Result → Output
```

## 🎯 Cas d'usage

### 1. CLI interactive
```bash
python main.py
```

### 2. API Python
```python
from veritas import run

result = run("Pourquoi le vaccin cause-t-il X?", offline=True)
print(result['mode'])  # 'approfondi'
```

### 3. Batch processing
```bash
python run_test_batch.py
```

### 4. Tests
```bash
python validate_refactoring.py
python test_refactor.py
```

## ✅ Changements effectués

| Fichier | Avant | Après | Status |
|---------|-------|-------|--------|
| `veritas_kernel_v2.py` | 530 lignes monolithiques | → 11 modules | ✅ Archivé |
| `run_test_batch.py` | `from veritas_kernel_v2 import run` | → `from veritas import run` | ✅ Mis à jour |
| `run_test_batch_adversarial.py` | `from veritas_kernel_v2 import run` | → `from veritas import run` | ✅ Mis à jour |
| `annotate_outcomes.py` | Inchangé | Inchangé | ✅ Compatible |
| `main.py` | N/A | Nouveau launcher | ✅ Créé |
| `cli.py` | N/A | Nouveau module | ✅ Créé |

## 🧪 Validation

✅ Tous les tests passent :
- `test_refactor.py` — 5 prompts offline
- `validate_refactoring.py` — Validation complète
- `run_test_batch.py` — Batch de 20 prompts
- Imports et API publique

## 📚 API Publique

Accessible via `from veritas import ...` :

```python
# Classe principales
from veritas import PromptAnalyzerLLM, ObservedFeatures, Assessment, DecisionContext

# Fonctions
from veritas import run, assess, determine_mode, kernel_decide

# Configuration
from veritas import CONFIG, ConstraintClass

# Logging
from veritas import log_outcome
```

## 🔧 Maintenance

### Ajouter une nouvelle feature

1. Identifier la responsabilité (config? models? kernel?)
2. Ajouter dans le bon module
3. Mettre à jour `veritas/__init__.py` si c'est public
4. Lancer les tests

### Corriger un bug

1. Localiser le module responsable
2. Corriger en isolation
3. Tester avec `validate_refactoring.py`
4. Tester le batch avec `run_test_batch.py`

### Utiliser comme bibliothèque

```bash
# Copier le répertoire veritas/ dans ton projet
# Puis :
from veritas import run
```

## 📊 Bénéfices

| Aspect | Avant | Après |
|--------|-------|-------|
| **Fichiers** | 1 monolithe (530L) | 11 modules (320L total) |
| **Complexité** | Élevée | Basse (separation of concerns) |
| **Testabilité** | Difficile | Facile (modules indépendants) |
| **Maintenabilité** | Moyenne | Haute (code lisible) |
| **Réutilisabilité** | Faible | Haute (import sélectif) |
| **Compréhension** | Longue | Rapide (modules spécialisés) |

---

**Status** : ✅ **Refactorisation complète et validée**
