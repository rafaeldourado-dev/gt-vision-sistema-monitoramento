import cv2
import numpy as np
from backend.utils.logger import logger

def preprocess_for_ocr(image: np.ndarray) -> np.ndarray:
    """
    Aplica técnicas de pré-processamento para melhorar a qualidade da imagem
    antes do reconhecimento OCR.
    
    Args:
        image: O frame do OpenCV (np.ndarray) contendo a placa.

    Returns:
        A imagem pré-processada.
    """
    # Converte para tons de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Aplica um filtro de ruído Gaussiano
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Binarização adaptativa para destacar o texto
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, 11, 2)
                                   
    logger.debug("Imagem pré-processada para OCR.")
    return thresh

def crop_image(image: np.ndarray, bbox: list) -> np.ndarray:
    """
    Recorta uma imagem com base nas coordenadas de uma caixa delimitadora.

    Args:
        image: A imagem original do OpenCV.
        bbox: Uma lista com as coordenadas [x1, y1, x2, y2].

    Returns:
        A imagem recortada.
    """
    x1, y1, x2, y2 = [int(i) for i in bbox]
    cropped = image[y1:y2, x1:x2]
    
    if cropped.size == 0:
        logger.warning(f"Não foi possível recortar a imagem com a bounding box: {bbox}")
        return None
        
    logger.debug(f"Imagem recortada com as coordenadas: {bbox}")
    return cropped