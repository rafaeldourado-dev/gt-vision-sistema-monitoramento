import numpy as np
from .enhanced_yolo import EnhancedYOLO
from backend.utils.logger import logger

class VehicleDetector:
    def __init__(self, model_path: str = 'yolov8n.pt'):
        self.yolo_model = EnhancedYOLO(model_path)
        self.vehicle_classes = [2, 3, 5, 7] # 'car', 'motorcycle', 'bus', 'truck'
        logger.info(f"Detector de veículos inicializado com o modelo: {model_path}.")

    def detect_vehicles(self, frame: np.ndarray):
        if frame is None:
            logger.warning("Frame nulo fornecido para detecção de veículos.")
            return []
        results = self.yolo_model.detect(frame, conf_threshold=0.4)
        detections = self.yolo_model.get_detections_from_results(
            results, 
            class_ids_to_detect=self.vehicle_classes
        )
        if detections:
            logger.debug(f"Veículos detectados: {len(detections)}")
        return detections