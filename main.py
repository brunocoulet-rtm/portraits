"""
Script de traitement automatique de portraits photographiques
===========================================================

Ce script permet de traiter automatiquement des photos de portraits pour :
1. Corriger l'orientation des images selon leurs métadonnées EXIF
2. Détecter les visages dans les images
3. Recadrer les portraits au format 3:4 avec des marges appropriées
4. Gérer les cas d'erreur en déplaçant les images problématiques dans un dossier dédié

Fonctionnement :
---------------
- Le script utilise OpenCV pour la détection de visages (Haar Cascade)
- Les images sont automatiquement orientées selon leurs données EXIF
- Le recadrage est fait avec des marges personnalisables (par défaut 30% en haut et en bas)
- Format de sortie : portrait 3:4
- Les images où aucun visage n'est détecté sont déplacées dans le dossier 'img/img_ko'

Utilisation :
Pour lancer le script, utiliser la commande
uv run main.py

Dépendances :
------------
- OpenCV (cv2)
- NumPy
- Pillow (PIL)
"""

import os
import cv2
import numpy as np
import shutil
from PIL import Image, ExifTags

INPUT_DIRECTORY = "input/img_raw"
OUTUT_DIRECTORY = "output/img_cropped"
KO_DIRECTORY = "output/img_ko"


def auto_orient_image(image_path):
    """
    Corrige l'orientation d'une image selon les métadonnées EXIF.
    Retourne (image OpenCV, True/False selon si une rotation a été appliquée)
    """
    try:
        image_pil = Image.open(image_path)
        exif = image_pil._getexif()
        orientation_key = None

        # Trouver la clé d’orientation dans les tags EXIF
        for key, value in ExifTags.TAGS.items():
            if value == 'Orientation':
                orientation_key = key
                break

        rotated = False
        if exif is not None and orientation_key in exif:
            orientation = exif[orientation_key]

            if orientation == 3:
                image_pil = image_pil.rotate(180, expand=True)
                rotated = True
            elif orientation == 6:
                image_pil = image_pil.rotate(270, expand=True)
                rotated = True
            elif orientation == 8:
                image_pil = image_pil.rotate(90, expand=True)
                rotated = True

        # Conversion PIL → OpenCV
        image_cv = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
        return image_cv, rotated

    except Exception as e:
        print(f"⚠️ Erreur d’orientation pour {image_path}: {e}")
        image_cv = cv2.imread(image_path)
        return image_cv, False

def detect_and_crop_face(image_path, output_path, ko_dir, margin_top=0.2, margin_bottom=0.2):
    """
    Détecte, corrige, recadre et sauvegarde un portrait au format 3:4.
    En cas d'échec, copie l'image dans le dossier 'img/img_ko'.
    """
    image, oriented = auto_orient_image(image_path)
    if image is None:
        print(f"❌ Impossible de charger {image_path}")
        shutil.copy(image_path, os.path.join(ko_dir, os.path.basename(image_path)))
        return False

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

    if len(faces) == 0:
        print(f"⚠️ Aucun visage détecté dans {image_path}")
        shutil.copy(image_path, os.path.join(ko_dir, os.path.basename(image_path)))
        return False

    # Prendre le visage le plus grand
    (x, y, w, h) = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)[0]

    # Marges plus généreuses
    y_top = int(y - h * margin_top)
    y_bottom = int(y + h * (1 + margin_bottom))

    crop_h = y_bottom - y_top
    crop_w = int(crop_h * 3 / 4)
    x_center = x + w // 2
    x_left = int(x_center - crop_w / 2)
    x_right = int(x_center + crop_w / 2)

    # Ajuster si dépassement
    if y_top < 0:
        y_bottom -= y_top
        y_top = 0
    if y_bottom > image.shape[0]:
        diff = y_bottom - image.shape[0]
        y_top = max(0, y_top - diff)
        y_bottom = image.shape[0]
    if x_left < 0:
        x_right -= x_left
        x_left = 0
    if x_right > image.shape[1]:
        diff = x_right - image.shape[1]
        x_left = max(0, x_left - diff)
        x_right = image.shape[1]

    cropped = image[y_top:y_bottom, x_left:x_right]

    if cropped.size == 0:
        print(f"⚠️ Recadrage vide pour {image_path}")
        shutil.copy(image_path, os.path.join(ko_dir, os.path.basename(image_path)))
        return False

    # Redimension en 3:4 portrait — sortie finale 192x248 (largeur x hauteur)
    final_size = (192, 248)
    cropped_resized = cv2.resize(cropped, final_size, interpolation=cv2.INTER_AREA)
    cv2.imwrite(output_path, cropped_resized)

    print(f"✅ {os.path.basename(output_path)} enregistré (orientée={'oui' if oriented else 'non'})")
    return True

def process_directory(input_dir, output_dir, ko_dir):
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(ko_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            detect_and_crop_face(input_path, output_path, ko_dir)
            

process_directory(INPUT_DIRECTORY, OUTUT_DIRECTORY, KO_DIRECTORY)
