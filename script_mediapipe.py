import cv2
import script_mediapipe as mp
from PIL import Image

mp_face = mp.solutions.face_detection
detector = mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.5)

def crop_face(image_path, output_path="cropped.jpg"):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = detector.process(image_rgb)
    
    if not results.detections:
        print("Aucun visage détecté.")
        return None

    h, w, _ = image.shape
    for detection in results.detections:
        box = detection.location_data.relative_bounding_box
        x, y, w_box, h_box = box.xmin, box.ymin, box.width, box.height
        x, y, w_box, h_box = int(x*w), int(y*h), int(w_box*w), int(h_box*h)
        face = image[y:y+h_box, x:x+w_box]
        Image.fromarray(cv2.cvtColor(face, cv2.COLOR_BGR2RGB)).save(output_path)
        print(f"Visage recadré : {output_path}")
        return output_path

crop_face("portrait.jpg")
