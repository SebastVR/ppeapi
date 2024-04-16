from fastapi import FastAPI
from router.detection_ppe import (
    detection_router,
)  # Asegúrate de que la ruta de importación sea correcta

app = FastAPI(
    title="EPP Detection API",
    version="1.0",
    description="API for detecting personal protective equipment in images using YOLO.",
)

# Incluye el router en la aplicación FastAPI
app.include_router(
    detection_router,
    prefix="/api",  # Opcional: Define un prefijo común para todas las rutas en este router
    tags=[
        "detections"
    ],  # Opcional: Ayuda con la organización en la documentación de la API
)
