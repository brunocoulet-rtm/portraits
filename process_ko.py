"""
Script de retraitement des portraits, deuxième passe
==========================================

Retraite les images qui n'ont pas pu être traitées par le script main.py.
Il utilise une approche différente avec MediaPipe pour la détection des visages, plus robuste que
la méthode Haar Cascade dans certains cas difficiles.

Fonctionnement :
--------------
1. FILTRAGE :
   - Rejette les images avec trop de zones blanches (fond)
   - Analyse uniquement la partie centrale de l'image

2. CORRECTION DE DÉFORMATION :
   - Ajuste les images trop étirées en largeur ou en hauteur
   - Normalise les ratios extrêmes

3. DÉTECTION DE VISAGE :
   - Utilise MediaPipe Face Detection
   - Teste plusieurs rotations (0°, 90°, 180°, 270°) pour trouver un visage
   - Sélectionne le plus grand visage si plusieurs sont détectés

4. RECADRAGE :
    - Ajoute des marges autour du visage (40% de la taille du visage)
    - Redimensionne au format standard 192x248 pixels

5. GESTION DES FICHIERS :
   - Déplace les images traitées avec succès
   - Supprime les originaux après traitement réussi

Dépendances :
-----------
- OpenCV (cv2)
- MediaPipe
- NumPy
"""

import os
import cv2
import mediapipe as mp
import numpy as np

KO_DIR = "output/img_ko"
PROCESSED_DIR = "output/ko_processed"

os.makedirs(PROCESSED_DIR, exist_ok=True)

mp_face = mp.solutions.face_detection
detector = mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.6)

# ---------- 1. FILTRAGE ----------
# def is_image_valid(img, min_size=400, white_ratio_thresh=0.75):
#     """Rejette les images trop petites ou quasi blanches"""
#     if img is None:
#         return False
#     h, w = img.shape[:2]
#     if min(h, w) < min_size:
#         return False
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     white_ratio = np.mean(gray > 240)
#     if white_ratio > white_ratio_thresh:
#         return False
#     return True
def is_image_valid(img, white_ratio_thresh=0.30):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    # on ignore les bords (où le fond est souvent blanc)
    margin = int(0.1 * min(h, w))
    cropped = gray[margin:h-margin, margin:w-margin]
    white_ratio = np.mean(cropped > 240)
    return white_ratio <= white_ratio_thresh



# ---------- 2. CORRECTION DE DÉFORMATION ----------
def correct_aspect_ratio(img):
    """Déforme les images très étirées en largeur ou en hauteur"""
    h, w = img.shape[:2]
    ratio = w / h
    if ratio > 1.4:  # trop large → resserrer
        new_w = int(h * 0.9)
        img = cv2.resize(img, (new_w, h))
    elif ratio < 0.7:  # trop haut → élargir
        new_h = int(w * 0.9)
        img = cv2.resize(img, (w, new_h))
    return img

# ---------- 3. DÉTECTION VISAGE ----------
def detect_face(image):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = detector.process(rgb)
    return result.detections

def try_rotations(image_path):
    """Teste plusieurs rotations et renvoie (image, box) si visage trouvé"""
    img = cv2.imread(image_path)
    if img is None:
        return None, None

    rotations = {
        0: img,
        90: cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE),
        180: cv2.rotate(img, cv2.ROTATE_180),
        270: cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    }

    for angle, rotated in rotations.items():
        detections = detect_face(rotated)
        if detections:
            # prendre le visage le plus grand
            det = max(detections, key=lambda d: d.location_data.relative_bounding_box.width)
            box = det.location_data.relative_bounding_box
            return rotated, box
    return None, None

# ---------- 4. RECADRAGE ----------
def crop_face(img, box):
    h, w, _ = img.shape
    x, y, bw, bh = box.xmin, box.ymin, box.width, box.height
    x, y, bw, bh = int(x * w), int(y * h), int(bw * w), int(bh * h)
    pad = int(0.2 * max(bw, bh))
    x1, y1 = max(x - pad, 0), max(y - pad, 0)
    x2, y2 = min(x + bw + pad, w), min(y + bh + pad, h)
    face = img[y1:y2, x1:x2]
    if face.size == 0:
        return None
    # Sortie finale 192x248 (largeur x hauteur) — éviter agrandissement inutile si possible
    return cv2.resize(face, (192, 248))

# ---------- 5. PIPELINE ----------
def process_folder():
    files = [f for f in os.listdir(KO_DIR) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    print(f"🔍 {len(files)} images à retraiter dans {KO_DIR}")

    for file in files:
        path = os.path.join(KO_DIR, file)
        img = cv2.imread(path)

        if not is_image_valid(img):
            print(f"🚫 Image ignorée (fond trop blanc) : {file}")
            continue

        img = correct_aspect_ratio(img)
        corrected, box = try_rotations(path)

        if corrected is not None and box is not None:
            face = crop_face(corrected, box)
            if face is not None:
                out_path = os.path.join(PROCESSED_DIR, file)
                cv2.imwrite(out_path, face)
                os.remove(path)
                print(f"✅ {file} → visage recadré et déplacé")
                continue

        print(f"❌ Aucun visage détecté ou recadrage impossible : {file}")

    print("✅ Traitement terminé.")

if __name__ == "__main__":
    process_folder()
