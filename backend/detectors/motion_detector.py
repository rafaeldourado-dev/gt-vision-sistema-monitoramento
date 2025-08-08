import cv2
import numpy as np
from backend.utils.logger import logger

class MotionDetector:
    def __init__(self, min_area: int = 500):
        """
        Inicializa o detector de movimento.

        Args:
            min_area: A área mínima de um contorno (em pixels) para ser considerado movimento.
                      Ajuste este valor para evitar falsos positivos.
        """
        self.min_area = min_area
        self.first_frame = None
        logger.info(f"Detector de movimento inicializado com área mínima de {min_area} pixels.")

    def detect_motion(self, frame: np.ndarray):
        """
        Detecta movimento comparando o frame atual com um frame de referência.

        Args:
            frame: O frame do OpenCV para detecção.

        Returns:
            Uma tupla (bool, list), onde o booleano indica se o movimento foi detectado,
            e a lista contém os contornos do movimento.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.first_frame is None:
            self.first_frame = gray
            logger.debug("Frame de referência para detecção de movimento definido.")
            return False, []

        frame_delta = cv2.absdiff(self.first_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        motion_contours = []

        for contour in contours:
            if cv2.contourArea(contour) > self.min_area:
                motion_detected = True
                motion_contours.append(contour)
                
        if motion_detected:
            logger.info("Movimento detectado no frame.")
            
        return motion_detected, motion_contours