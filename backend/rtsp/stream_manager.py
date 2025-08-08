from .camera import Camera
from backend.config.settings import settings
from backend.utils.logger import logger

class StreamManager:
    def __init__(self):
        self.cameras = {}
        self._initialize_cameras()

    def _initialize_cameras(self):
        logger.info("Inicializando gerenciador de streams...")
        
        seguranca_url = settings.camera_seguranca_url
        if seguranca_url:
            self.cameras['seguranca'] = Camera(seguranca_url)
            logger.info("Câmera de segurança adicionada ao gerenciador.")
        else:
            logger.warning("URL da câmera de segurança não configurada.")
        
        lpr_url = settings.camera_lpr_url
        if lpr_url:
            self.cameras['lpr'] = Camera(lpr_url)
            logger.info("Câmera LPR adicionada ao gerenciador.")
        else:
            logger.warning("URL da câmera LPR não configurada.")

    def start_all(self):
        logger.info("Iniciando todos os streams de câmera.")
        for name, camera in self.cameras.items():
            camera.start()
            logger.info(f"Stream da câmera '{name}' iniciado.")
            
    def stop_all(self):
        logger.info("Parando todos os streams de câmera.")
        for name, camera in self.cameras.items():
            camera.stop()
            logger.info(f"Stream da câmera '{name}' parado.")

    def get_frame(self, camera_name: str):
        camera = self.cameras.get(camera_name)
        if camera:
            return camera.get_latest_frame()
        logger.warning(f"Câmera '{camera_name}' não encontrada.")
        return None