from ultralytics import YOLO
import cv2
import numpy as np
from backend.utils.logger import logger

class EnhancedYOLO:
    def __init__(self, model_path: str = 'yolov8n.pt'):
        try:
            self.model = YOLO(model_path)
            logger.info(f"Modelo YOLOv8 carregado com sucesso a partir de '{model_path}'.")
        except Exception as e:
            logger.error(f"Falha ao carregar o modelo YOLOv8: {e}")
            self.model = None
        self.class_names = self.model.names if self.model else {}

    def detect(self, frame: np.ndarray, conf_threshold: float = 0.25):
        if self.model is None or frame is None:
            logger.warning("Modelo YOLO não está carregado ou frame é nulo. Pulando detecção.")
            return []
        results = self.model.predict(source=frame, conf=conf_threshold, verbose=False)
        return results

    def get_detections_from_results(self, results, class_ids_to_detect: list = None):
        detections = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                class_id = int(box.cls[0])
                if class_ids_to_detect and class_id not in class_ids_to_detect:
                    continue
                conf = float(box.conf[0])
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                
                detections.append({
                    'class_id': class_id,
                    'class_name': self.class_names.get(class_id),
                    'confidence': conf,
                    'bbox': [x1, y1, x2, y2]
                })
        return detections