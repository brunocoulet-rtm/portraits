# portraits

Ce projet utilise [uv](https://github.com/astral-sh/uv) pour la gestion des dépendances et l'exécution des scripts Python.

## Prérequis

- Python ≥ 3.8
- [uv](https://github.com/astral-sh/uv) installé (voir la doc officielle pour l’installation : `pip install uv` ou suivez les instructions du dépôt)

## Installation des dépendances

```bash
uv pip install -r requirements.txt
```

## Fonctionnement
Actuellement, le script ``main.py`` fait cela :
 
- ouvre le dossier `input/img_raw` qui contient les photos au format 192x248
- essaie de pivoter et recadrer les photos si besoin (format 4/3)
- si l'opération précédente à réussi, il enregistre la photo dans le dossier `output/img_cropped`
- sinon il enregistre la photo dans le dossier `output/img_ko`
 
Puis il faut lancer `process_ko.py` qui fait cela :
- ouvre le dossier ``output/img_ko`` pour traiter les images qu'il contient
- essaie de corriger une éventuelle déformation, de pivoter, de recadrer
- s'il l'opération précédente à réussi, il enregistre la photo dans le dossier ``output/ko_processed``
- sinon la photo reste dans le dossier ``output/img_ko``
 
 
En résumé :
 
en entrée un dossier de photos 192x248 pixels<br>
en sortie 3 dossiers 
- img_cropped  ----- contient les photos considéré ok
- ko_processed ----- contient les photos considéré ok après rattrapage
- img_ko       ----- contient les photos considéré ko
 
2 scripts doivent être lancés l'un après l'autre, on peut les rassembler en un seul script
 
Un œil humain reste nécessaire en fin de parcours, mais le travail est prémâché


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
