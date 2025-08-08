import numpy as np
from .enhanced_yolo import EnhancedYOLO
from backend.utils.logger import logger

class PlateDetector:
    def __init__(self, model_path: str = 'yolov8n.pt'):
        """
        Inicializa o detector de placas usando um modelo YOLOv8.
        Note: O modelo yolov8n.pt padrão possui uma classe 'license plate'.
        Um modelo customizado seria mais preciso.
        """
        self.yolo_model = EnhancedYOLO(model_path)
        
        # ID da classe 'license plate' no modelo YOLOv8n padrão
        # O ID pode variar, mas '3' é um valor comum
        self.plate_class = [3]
        logger.info(f"Detector de placas inicializado com o modelo: {model_path}.")

    def detect_plates(self, frame: np.ndarray):
        """
        Detecta placas em um frame e retorna suas informações.

        Args:
            frame: O frame do OpenCV para detecção.

        Returns:
            Uma lista de dicionários com as detecções de placas.
        """
        if frame is None:
            logger.warning("Frame nulo fornecido para detecção de placas.")
            return []

        results = self.yolo_model.detect(frame, conf_threshold=0.4)
        
        # Filtra os resultados para obter apenas as placas
        detections = self.yolo_model.get_detections_from_results(
            results, 
            class_ids_to_detect=self.plate_class
        )
        
        if detections:
            logger.debug(f"Placas detectadas: {len(detections)}")
        
        return detections

# Exemplo de como usar o PlateDetector (será integrado no main.py)
if __name__ == "__main__":
    from backend.rtsp.stream_manager import StreamManager
    from backend.utils.video_utils import draw_bounding_box, annotate_frame
    import cv2
    import time
    
    stream_manager = StreamManager()
    stream_manager.start_all()

    plate_detector = PlateDetector()

    try:
        while True:
            # Use a câmera LPR para a detecção de placas
            frame = stream_manager.get_frame('lpr')
            if frame is not None:
                detections = plate_detector.detect_plates(frame)
                
                for det in detections:
                    bbox = det['bbox']
                    frame = draw_bounding_box(frame, bbox, color=(255, 255, 0))
                    frame = annotate_frame(frame, "Placa", (int(bbox[0]), int(bbox[1]) - 10), color=(255, 255, 0))
                    
                cv2.imshow('Detecção de Placas', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
            time.sleep(0.01)
    finally:
        stream_manager.stop_all()
        cv2.destroyAllWindows()