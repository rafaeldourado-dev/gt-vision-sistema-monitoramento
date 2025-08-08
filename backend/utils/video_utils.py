import cv2
import numpy as np
from backend.utils.logger import logger

def convert_frame_to_jpeg(frame: np.ndarray):
    ret, jpeg_frame = cv2.imencode('.jpg', frame)
    if not ret:
        logger.error("Falha ao converter frame para JPEG.")
        return None
    logger.debug("Frame convertido para JPEG com sucesso.")
    return jpeg_frame.tobytes()

def annotate_frame(frame: np.ndarray, text: str, position: tuple, color: tuple = (0, 255, 0)):
    cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    logger.debug(f"Anotação adicionada ao frame: '{text}'")
    return frame

def draw_bounding_box(frame: np.ndarray, box: tuple, color: tuple = (0, 255, 0), thickness: int = 2):
    x1, y1, x2, y2 = box
    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)
    logger.debug(f"Caixa delimitadora desenhada em {box}")
    return frame