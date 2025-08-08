import os
import cv2
import numpy as np
from datetime import datetime
from backend.utils.logger import logger

class ImageStorage:
    def __init__(self, base_dir: str = 'media'):
        self.base_dir = base_dir
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
            logger.info(f"Pasta de mídia '{self.base_dir}' criada.")

    def save_event_image(self, frame: np.ndarray, event_type: str, timestamp: str) -> str | None:
        """
        Salva um frame como imagem de um evento.
        
        Args:
            frame: O frame do OpenCV a ser salvo.
            event_type: O tipo do evento (ex: 'alerta_face', 'placa_detectada').
            timestamp: Um timestamp para garantir nomes de arquivos únicos.

        Returns:
            O caminho para a imagem salva, ou None em caso de erro.
        """
        if frame is None:
            logger.warning("Não foi possível salvar a imagem: o frame é nulo.")
            return None

        file_name = f"{event_type}_{timestamp.replace(' ', '_').replace(':', '-')}.jpg"
        file_path = os.path.join(self.base_dir, file_name)

        try:
            cv2.imwrite(file_path, frame)
            logger.success(f"Imagem salva em: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Erro ao salvar a imagem: {e}")
            return None