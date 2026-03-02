import os
from pathlib import Path

from PIL import Image, ImageDraw
from huggingface_hub import hf_hub_download
from ultralytics import YOLO


CHECKPOINT = "yasirfaizahmed/license-plate-object-detection"
WEIGHTS_FILE = "best.pt"

# Jednoduché nastavení pro studenty
IMG_PATH = "auto.jpg"
OUTPUT_PATH = "detekce_vysledek.jpg"
THRESHOLD = 0.30

image_path = Path(IMG_PATH)
if not image_path.exists():
    candidates = []
    for ext in ("*.jpg", "*.jpeg", "*.png", "*.bmp"):
        candidates.extend(Path(".").glob(ext))

    if not candidates:
        print("Nenašel jsem obrázek. Přidej sem např. auto.jpg")
        raise SystemExit(1)

    image_path = candidates[0]
    print(f"auto.jpg nenalezen, používám: {image_path}")

print("Načítám model...")
os.environ.setdefault("TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD", "1")
weights_path = hf_hub_download(repo_id=CHECKPOINT, filename=WEIGHTS_FILE)
model = YOLO(weights_path)

image = Image.open(image_path).convert("RGB")
draw = ImageDraw.Draw(image)

print("Hledám SPZ...")
try:
    predictions = model.predict(source=str(image_path), conf=THRESHOLD, verbose=False)
except Exception as e:
    print("Nepodařilo se spustit detekci.")
    print(f"Detail chyby: {e}")
    raise SystemExit(1)

count = 0
if predictions:
    boxes = predictions[0].boxes
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        score = float(box.conf[0])

        draw.rectangle(
            [(x1, y1), (x2, y2)],
            outline="red",
            width=4,
        )

        count += 1
        print(f"Nalezena SPZ s jistotou {score:.2%}")
        print(
            f"Souřadnice boxu: xmin={int(x1)}, ymin={int(y1)}, xmax={int(x2)}, ymax={int(y2)}"
        )

if count == 0:
    print("Žádná SPZ nebyla nalezena.")
else:
    print(f"Počet vykreslených boxů: {count}")

image.save(OUTPUT_PATH)
print(f"Uloženo: {OUTPUT_PATH}")

if os.getenv("DISPLAY"):
    try:
        image.show()
    except Exception as e:
        print(f"Náhled se nepodařilo otevřít: {e}")
else:
    print("Náhled přes image.show() přeskočen (bez GUI).")