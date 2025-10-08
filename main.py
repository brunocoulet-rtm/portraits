from pipeline import detect_and_crop, assess_quality, classify_portrait
import os, shutil

INPUT = "input"
OK_DIR = "output/ok"
KO_DIR = "output/rejected"

for file in os.listdir(INPUT):
    path = os.path.join(INPUT, file)
    cropped = detect_and_crop(path)
    if cropped is None:
        shutil.move(path, KO_DIR)
        continue

    if not assess_quality(cropped):
        shutil.move(path, KO_DIR)
        continue

    if not classify_portrait(cropped):
        shutil.move(path, KO_DIR)
        continue

    shutil.move(path, OK_DIR)
