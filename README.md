# portraits

Ce projet utilise [uv](https://github.com/astral-sh/uv) pour la gestion des dépendances et l'exécution des scripts Python.

## Prérequis

- Python ≥ 3.8
- [uv](https://github.com/astral-sh/uv) installé (voir la doc officielle pour l’installation : `pip install uv` ou suivez les instructions du dépôt)

## Installation des dépendances

```bash
uv pip install -r requirements.txt
```

## Lancer les scripts

### 1. Pour exécuter `main.py` :

```bash
uv python main.py
```

### 2. Pour exécuter `process_ko.py` :

```bash
uv python process_ko.py
```

## Remarques

- En cas de problème avec uv, vérifiez bien votre installation Python et celle d’uv.
