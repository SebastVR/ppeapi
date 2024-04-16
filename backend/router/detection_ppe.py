from fastapi import APIRouter, HTTPException, UploadFile, File
from controller.detection_ppe import process_image

# Crea una instancia del router
detection_router = APIRouter()


@detection_router.post("/detections/", status_code=200)
async def create_detection(file: UploadFile = File(...)):
    """
    Recibe una imagen, procesa la imagen para detectar elementos de protección personal utilizando YOLO,
    y devuelve los resultados de la detección.
    """
    try:
        # Procesar la imagen subida y obtener los resultados de detección
        detection_results = process_image(file)
        return detection_results
    except Exception as e:
        # En caso de errores en el procesamiento, lanzar un error HTTP
        raise HTTPException(status_code=500, detail=str(e))


@detection_router.get("/detections/{image_path}")
async def get_detection(image_path: str):
    """
    Endpoint para recuperar y mostrar la imagen procesada con los resultados de la detección.
    Esto es solo un ejemplo de cómo podrías manejar la recuperación de imágenes si fuera necesario.
    """
    # Implementa la lógica para recuperar y servir la imagen desde el servidor si es necesario.
    # Aquí simplemente retornamos la ruta como parte del mensaje para ilustrar.
    return {"message": "Imagen procesada disponible en", "path": image_path}
