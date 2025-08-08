import cv2
import threading
import time
from backend.utils.logger import logger
from backend.config.settings import settings

class Camera:
    def __init__(self, url: str):
        self.url = url
        self.stream = None
        self.frame = None
        self.is_running = False
        self.thread = None
        self.lock = threading.Lock()
        logger.info(f"Instância da câmera criada para a URL: {self.url}")

    def start(self):
        if self.is_running:
            return
        self.is_running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()
        logger.info(f"Thread de captura da câmera iniciada para a URL: {self.url}")

    def _run(self):
        while self.is_running:
            if self.stream is None or not self.stream.isOpened():
                logger.warning(f"Tentando reconectar à câmera em {self.url}...")
                self.stream = cv2.VideoCapture(self.url)
                if self.stream.isOpened():
                    logger.success(f"Conectado com sucesso à câmera em {self.url}.")
                else:
                    logger.error(f"Falha na conexão com a câmera em {self.url}. Tentando novamente em 5 segundos.")
                    time.sleep(5)
                    continue
            ret, frame = self.stream.read()
            if not ret:
                logger.warning(f"Não foi possível ler um frame da câmera em {self.url}. Reconectando...")
                self.stream.release()
                time.sleep(1)
                continue
            with self.lock:
                self.frame = frame
            time.sleep(0.01)
        if self.stream:
            self.stream.release()
        logger.info(f"Thread de captura da câmera para {self.url} finalizada.")

    def get_latest_frame(self):
        with self.lock:
            if self.frame is not None:
                return self.frame.copy()
        return None

    def stop(self):
        if self.is_running:
            self.is_running = False
            self.thread.join()
            logger.info(f"Câmera em {self.url} foi parada.")