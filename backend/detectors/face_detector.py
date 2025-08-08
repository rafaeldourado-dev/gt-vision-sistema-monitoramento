import numpy as np
from .enhanced_yolo import EnhancedYOLO
from backend.utils.logger import logger

class FaceDetector:
    def __init__(self, model_path: str = 'yolov8n.pt'):
        """
        Inicializa o detector de faces usando um modelo YOLOv8.
        Note: O modelo yolov8n.pt padrão detecta 'person'.
        Para detecção de face mais precisa, um modelo treinado especificamente seria ideal.
        """
        self.yolo_model = EnhancedYOLO(model_path)
        
        # ID da classe 'person' no modelo YOLOv8n padrão
        self.person_class = [0]
        logger.info(f"Detector de faces inicializado com o modelo: {model_path}.")

    def detect_faces(self, frame: np.ndarray):
        """
        Detecta pessoas em um frame e retorna suas informações.

        Args:
            frame: O frame do OpenCV para detecção.

        Returns:
            Uma lista de dicionários com as detecções de pessoas.
        """
        if frame is None:
            logger.warning("Frame nulo fornecido para detecção de faces.")
            return []

        results = self.yolo_model.detect(frame, conf_threshold=0.4)
        
        # Filtra os resultados para obter apenas as pessoas
        detections = self.yolo_model.get_detections_from_results(
            results, 
            class_ids_to_detect=self.person_class
        )
        
        if detections:
            logger.debug(f"Pessoas detectadas: {len(detections)}")
        
        return detections

# Exemplo de como usar o FaceDetector (será integrado no main.py)
if __name__ == "__main__":
    from backend.rtsp.stream_manager import StreamManager
    from backend.utils.video_utils import draw_bounding_box, annotate_frame
    import cv2
    import time
    
    stream_manager = StreamManager()
    stream_manager.start_all()

    face_detector = FaceDetector()

    try:
        while True:
            frame = stream_manager.get_frame('seguranca')
            if frame is not None:
                detections = face_detector.detect_faces(frame)
                
                for det in detections:
                    bbox = det['bbox']
                    frame = draw_bounding_box(frame, bbox, color=(255, 0, 0))
                    frame = annotate_frame(frame, "Pessoa", (int(bbox[0]), int(bbox[1]) - 10), color=(255, 0, 0))
                    
                cv2.imshow('Detecção de Faces', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
            time.sleep(0.01)
    finally:
        stream_manager.stop_all()
        cv2.destroyAllWindows()