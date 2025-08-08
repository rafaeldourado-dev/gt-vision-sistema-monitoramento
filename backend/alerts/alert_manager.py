# backend/alerts/alert_manager.py

import time
from typing import Dict, Any
from datetime import datetime
import numpy as np

from backend.utils.logger import logger
from backend.config.models import Alert
from backend.config.settings import settings
from backend.storage.database import get_db
from backend.storage.image_storage import ImageStorage
from backend.storage.video_storage import VideoStorage

# Importa os notificadores que vamos usar
from .notification import EmailSender
from .whatsapp_api_sender import WhatsAppAPISender

class AlertManager:
    def __init__(self, image_storage: ImageStorage, video_storage: VideoStorage):
        # INICIA OS NOTIFICADORES CORRETOS
        self.whatsapp_sender = WhatsAppAPISender() # <-- Usa o WhatsApp
        self.email_sender = EmailSender()         # <-- Usa o E-mail
        self.email_recipient = settings.email_sender

        self.image_storage = image_storage
        self.video_storage = video_storage

        self.last_alert_time = {}
        self.cooldown_period = 60 # Evita alertas repetidos em menos de 1 minuto

        logger.info("Gerenciador de alertas inicializado com notificações para WhatsApp e E-mail.")

    def check_for_critical_events(self, camera_name: str, detections: list[Dict[str, Any]], frame: np.ndarray):
        current_time = time.time()

        if camera_name == 'lpr':
            for det in detections:
                # A classe 'person' tem ID 0 no modelo YOLOv8
                if det.get('class_id') == 0:
                    if current_time - self.last_alert_time.get(camera_name, 0) > self.cooldown_period:
                        subject = "ALERTA: Pessoa Detectada na Área LPR"
                        message = f"Uma pessoa foi detectada na área restrita da câmera LPR.\nHorário: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"

                        self.send_alert(subject, message, camera_name, frame)
                        self.last_alert_time[camera_name] = current_time
                        return # Sai após o primeiro alerta para evitar spam

    def send_alert(self, subject: str, message: str, camera_name: str, frame: np.ndarray):
        logger.critical(f"ALERTA CRÍTICO: {subject} na câmera '{camera_name}'")

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        image_path = self.image_storage.save_event_image(frame, "alerta_pessoa_lpr", timestamp)

        # --- ENVIO DAS NOTIFICAÇÕES ---
        # 1. Envia para o WhatsApp
        self.whatsapp_sender.send_notification(subject, message)

        # 2. Envia por E-mail
        if self.email_recipient:
            self.email_sender.send_notification(subject, message, self.email_recipient)

        # --- SALVAMENTO NO BANCO DE DADOS ---
        try:
            db_session = next(get_db())
            new_alert = Alert(
                title=subject,
                description=message,
                timestamp=datetime.now(),
                is_critical=True,
                image_path=image_path
            )
            db_session.add(new_alert)
            db_session.commit()
            db_session.refresh(new_alert)
            logger.success(f"Alerta registrado no banco de dados com ID: {new_alert.id}")
        except Exception as e:
            logger.error(f"Erro ao salvar alerta no banco de dados: {e}")
            db_session.rollback()
        finally:
            db_session.close()