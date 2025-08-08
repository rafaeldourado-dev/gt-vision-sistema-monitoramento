# run_vision_system.py (na pasta raiz do projeto)

import cv2
import time
from datetime import datetime
from backend.rtsp.stream_manager import StreamManager
from backend.detectors.vehicle_detector import VehicleDetector
from backend.detectors.face_detector import FaceDetector
from backend.detectors.plate_detector import PlateDetector
from backend.lpr.plate_recognizer import PlateRecognizer
from backend.alerts.alert_manager import AlertManager
from backend.utils.logger import logger
from backend.utils.video_utils import draw_bounding_box, annotate_frame
from backend.storage.image_storage import ImageStorage
from backend.storage.video_storage import VideoStorage
# Adicionando o import do get_db para garantir a criação das tabelas
from backend.storage.database import create_database, get_db

def main():
    logger.info("Iniciando o sistema GT-VISION (Processo de Visão Computacional)...")
    
    # --- Passo 1: Inicialização do Banco de Dados ---
    # É uma boa prática tentar criar as tabelas antes de tudo.
    # Isso só irá rodar se as tabelas não existirem.
    create_database()

    # --- Passo 2: Inicialização de todos os componentes ---
    stream_manager = StreamManager()
    stream_manager.start_all()
    
    vehicle_detector = VehicleDetector()
    face_detector = FaceDetector()
    plate_detector = PlateDetector()
    plate_recognizer = PlateRecognizer()
    
    image_storage = ImageStorage()
    video_storage = VideoStorage(resolution=(640, 480))
    
    alert_manager = AlertManager(image_storage=image_storage, video_storage=video_storage)
    
    try:
        while True:
            # Captura os frames das duas câmeras
            frame_seguranca = stream_manager.get_frame('seguranca')
            frame_lpr = stream_manager.get_frame('lpr')
            
            # --- Lógica para a Câmera de Segurança ---
            if frame_seguranca is not None:
                # O detector de faces procura por pessoas (class_id=0)
                detections_faces = face_detector.detect_faces(frame_seguranca)
                
                # Desenha a caixa vermelha em torno das pessoas, como solicitado
                for det in detections_faces:
                    bbox = det['bbox']
                    frame_seguranca = draw_bounding_box(frame_seguranca, bbox, color=(255, 0, 0)) # Vermelho
                    frame_seguranca = annotate_frame(frame_seguranca, "Pessoa", (int(bbox[0]), int(bbox[1]) - 10), color=(255, 0, 0))
                
                cv2.imshow('GT-VISION - Seguranca', frame_seguranca)

            # --- Lógica para a Câmera LPR ---
            if frame_lpr is not None:
                # CORREÇÃO: Removido o detector de faces, agora a lógica busca por veículos e placas.
                detections_vehicles = vehicle_detector.detect_vehicles(frame_lpr)
                
                for vehicle_det in detections_vehicles:
                    vehicle_bbox = vehicle_det['bbox']
                    # Desenha a caixa azul em torno do veículo
                    frame_lpr = draw_bounding_box(frame_lpr, vehicle_bbox, color=(0, 0, 255)) # Azul
                    frame_lpr = annotate_frame(frame_lpr, f"Veiculo", (int(vehicle_bbox[0]), int(vehicle_bbox[1]) - 10), color=(0, 0, 255))
                    
                    # Para cada veículo, tenta detectar placas
                    detections_plates = plate_detector.detect_plates(frame_lpr)
                    
                    for plate_det in detections_plates:
                        plate_bbox = plate_det['bbox']
                        # Desenha a caixa amarela em torno da placa
                        frame_lpr = draw_bounding_box(frame_lpr, plate_bbox, color=(0, 255, 255)) # Amarelo
                        
                        # Reconhece o texto da placa
                        plate_text = plate_recognizer.recognize_plate(frame_lpr, plate_bbox)
                        
                        if plate_text:
                            # Adiciona o texto da placa na anotação
                            frame_lpr = annotate_frame(frame_lpr, f"Placa: {plate_text}", (int(plate_bbox[0]), int(plate_bbox[1]) - 10), color=(0, 255, 255))
                            
                            # CORREÇÃO: Cria um alerta de placa detectada, e não de pessoa
                            subject = f"Placa de Veículo Detectada: {plate_text}"
                            message = f"Uma placa foi detectada na câmera LPR. Placa: {plate_text}"
                            alert_manager.send_alert(subject, message, 'lpr', frame_lpr)

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