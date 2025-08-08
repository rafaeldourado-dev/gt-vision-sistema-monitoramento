import os
import cv2
from datetime import datetime
from backend.utils.logger import logger
import threading
import time
import queue
import numpy as np # Adicione esta linha!

class VideoStorage:
    def __init__(self, base_dir: str = 'media', fps: int = 20, resolution: tuple = (640, 480)):
        self.base_dir = base_dir
        self.fps = fps
        self.resolution = resolution
        self.writer = None
        self.is_recording = False
        self.queue = queue.Queue()
        self.thread = None
        
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
            logger.info(f"Pasta de mídia '{self.base_dir}' criada.")

    def _writer_thread(self):
        while self.is_recording or not self.queue.empty():
            try:
                frame = self.queue.get(timeout=1)
                if frame is not None and self.writer:
                    # Garantir que a resolução do frame seja compatível
                    if frame.shape[1] != self.resolution[0] or frame.shape[0] != self.resolution[1]:
                        frame_resized = cv2.resize(frame, self.resolution)
                        self.writer.write(frame_resized)
                    else:
                        self.writer.write(frame)
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Erro na thread de gravação: {e}")
                
        if self.writer:
            self.writer.release()
            self.writer = None
        logger.info("Thread de gravação finalizada.")

    def start_recording(self, event_type: str, timestamp: str):
        if self.is_recording:
            logger.warning("Gravação já está em andamento.")
            return

        file_name = f"{event_type}_{timestamp.replace(' ', '_').replace(':', '-')}.avi"
        file_path = os.path.join(self.base_dir, file_name)

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.writer = cv2.VideoWriter(file_path, fourcc, self.fps, self.resolution)
        self.is_recording = True
        
        self.thread = threading.Thread(target=self._writer_thread)
        self.thread.start()
        logger.success(f"Iniciada gravação do evento '{event_type}' em: {file_path}")

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.thread.join()
            logger.success("Gravação encerrada.")
        else:
            logger.info("Nenhuma gravação ativa para ser encerrada.")

    def add_frame(self, frame: np.ndarray):
        if self.is_recording and frame is not None:
            self.queue.put(frame)