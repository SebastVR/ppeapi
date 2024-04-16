from pathlib import Path
import shutil
from fastapi import UploadFile
from ultralytics import YOLO
import json

# Configuración del directorio donde se guardan las imágenes y la ruta del modelo YOLO
IMAGE_DIR = Path("data/mediafiles")
IMAGE_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = Path("data/staticfiles/best.pt")

# Lista de todos los posibles elementos de EPP (Equipos de Protección Personal)
EPP_ITEMS = [
    "arnes",
    "barbuquejo",
    "botas",
    "casco",
    "chaleco",
    "eslingas",
    "guantes",
    "personas",
    "proteccion_auditiva",
    "proteccion_respiratoria",
    "proteccion_visual",
]


def save_image(file: UploadFile) -> Path:
    """
    Guarda un archivo cargado y devuelve la ruta al archivo guardado.
    """
    file_name = file.filename
    file_location = IMAGE_DIR / file_name
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_location


def process_image(file: UploadFile) -> dict:
    """
    Procesa una imagen cargada utilizando YOLO para detectar elementos de protección personal,
    y devuelve un diccionario con los resultados de la detección.
    """
    file_path = save_image(file)  # Guardar la imagen
    model = YOLO(MODEL_PATH.as_posix())  # Cargar el modelo YOLO
    results = model.predict([str(file_path)])  # Realizar la detección
    json_data = results[0].tojson()  # Convertir los resultados a JSON
    detections = json.loads(json_data)  # Parsear el JSON a un diccionario de Python
    # Contabilizar los elementos detectados
    detection_counts = {item: 0 for item in EPP_ITEMS}
    for detection in detections:
        if detection["name"] in detection_counts:
            detection_counts[detection["name"]] += 1
    # Devolver los resultados de la detección junto con la ruta de la imagen
    return {"image_path": str(file_path), **detection_counts}
