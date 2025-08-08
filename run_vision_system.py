# run_vision_system.py (na pasta raiz do projeto)

import cv2
import time
from datetime import datetime
from backend.rtsp.stream_manager import StreamManager
from backend.detectors.vehicle_detector import VehicleDetector
from backend.detectors.face_detector import FaceDetector
from backend.detectors.plate_detector import PlateDetector
from backend.detectors.motion_detector import MotionDetector
from backend.lpr.plate_recognizer import PlateRecognizer
from backend.alerts.alert_manager import AlertManager
from backend.utils.logger import logger
from backend.utils.video_utils import draw_bounding_box, annotate_frame
from backend.storage.image_storage import ImageStorage
from backend.storage.video_storage import VideoStorage

def main():
    logger.info("Iniciando o sistema GT-VISION (Processo de Visão Computacional)...")
    
    # Inicializa todos os componentes
    stream_manager = StreamManager()
    stream_manager.start_all()
    
    vehicle_detector = VehicleDetector()
    face_detector = FaceDetector()
    plate_detector = PlateDetector()
    motion_detector = MotionDetector()
    plate_recognizer = PlateRecognizer()
    
    image_storage = ImageStorage()
    video_storage = VideoStorage(resolution=(640, 480))
    
    alert_manager = AlertManager(image_storage=image_storage, video_storage=video_storage)
    
    try:
        while True:
            frame_seguranca = stream_manager.get_frame('seguranca')
            frame_lpr = stream_manager.get_frame('lpr')
            
            if frame_seguranca is not None:
                # Lógica de detecção para a câmera de segurança
                detections_faces = face_detector.detect_faces(frame_seguranca)
                for det in detections_faces:
                    bbox = det['bbox']
                    frame_seguranca = draw_bounding_box(frame_seguranca, bbox, color=(255, 0, 0))
                    
                cv2.imshow('GT-VISION - Seguranca', frame_seguranca)

            if frame_lpr is not None:
                # Lógica de detecção para a câmera LPR
                detections_faces_lpr = face_detector.detect_faces(frame_lpr)
                alert_manager.check_for_critical_events('lpr', detections_faces_lpr, frame_lpr)
                
                cv2.imshow('GT-VISION - LPR', frame_lpr)
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        logger.info("Interrupção do usuário. Encerrando o sistema de visão.")
    finally:
        stream_manager.stop_all()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()