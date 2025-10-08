# Portraits - Traitement et Filtrage de Photos

Ce projet permet de **détecter, analyser et recadrer des portraits** en batch, avec des critères personnalisables : cadrage 4/3, netteté, visage complet, etc.  
Il est conçu pour fonctionner sur Windows 10 ou 11 avec Python 3.11 et des bibliothèques modernes (TensorFlow, MediaPipe, OpenCV).

---

## 1. Prérequis

- Windows 10 ou 11 (64 bits)
- Python 3.11
- Conda ou Miniconda installé
- Git (pour cloner le projet)

---

## 2. Cloner le projet

```bash
git clone https://github.com/<votre-utilisateur>/portraits.git
cd portraits
```

---

## 3. Création de l’environnement Conda

Nous recommandons d’utiliser **Conda** pour gérer les dépendances et éviter les conflits.

```bash
# Créer l'environnement
conda create -n portraits python=3.11 -y

# Activer l'environnement
conda activate portraits

```

## 4. Installer les dépendances

Toutes les dépendances sont listées dans `environment.yml`. Pour installer tout d’un coup :

```bash
conda env update --file environment.yml --prune
```

Si vous préférez `pip` :

```bash
pip install tensorflow==2.15.0
pip install opencv-python pillow numpy scikit-learn
pip install mediapipe==0.10.14 opencv-contrib-python matplotlib sounddevice jax jaxlib
```

⚠️ **Important** : Ne pas installer le package `tensorflow-io-gcs-filesystem` sur Windows, il n’a pas de wheel compatible.

---

## 5. Vérification de l’installation

Pour vérifier que tout fonctionne :

```bash
python -c "import tensorflow as tf; import cv2; import mediapipe as mp; import numpy as np; import PIL; import sklearn; print('OK')"
```

Vous devriez voir `OK` et quelques messages d’information de TensorFlow.

---

## 6. Organisation du projet

```
portraits/
├─ scripts/              # Scripts Python principaux
├─ data/                 # Photos à traiter
│  ├─ ok/                # Portraits valides
│  └─ recadrer/          # Portraits à recadrer ou rejeter
├─ environment.yml       # Définition de l'environnement Conda
└─ README.md
```

---

## 7. Remarques

1. Pour reproduire l’environnement sur une autre machine Windows, utiliser `environment.yml`.
2. Les chemins longs (>260 caractères) ou caractères spéciaux peuvent poser problème sur Windows.
3. Si vous utilisez GPU TensorFlow, installer CUDA et cuDNN compatibles avec Windows et Python 3.11.

---

## 8. Lancer le pipeline

Chaque script est autonome et utilise l’environnement activé `portraits`. Exemple :

```bash
conda activate portraits
python scripts/process_photos.py --input data/incoming --output data/ok
```

Ce script détectera les visages, analysera la qualité et recadrera automatiquement au format 4:3.