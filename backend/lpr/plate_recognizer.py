import easyocr
import numpy as np
from backend.utils.logger import logger
from .ocr_utils import preprocess_for_ocr, crop_image

class PlateRecognizer:
    def __init__(self, languages: list = ['en', 'pt']):
        """
        Inicializa o EasyOCR.
        
        Args:
            languages: Lista de idiomas para o reconhecimento.
                       'en' para inglês, 'pt' para português, etc.
        """
        try:
            self.reader = easyocr.Reader(languages, gpu=True) # Use gpu=False se não tiver uma GPU
            logger.info(f"EasyOCR inicializado com os idiomas: {languages}.")
        except Exception as e:
            logger.error(f"Falha ao inicializar o EasyOCR: {e}")
            self.reader = None

    def recognize_plate(self, frame: np.ndarray, bbox: list) -> str | None:
        """
        Recorta a placa da imagem, a pré-processa e executa o reconhecimento OCR.

        Args:
            frame: O frame do OpenCV.
            bbox: A caixa delimitadora da placa.

        Returns:
            A string da placa reconhecida, ou None se não for encontrada.
        """
        if self.reader is None:
            logger.error("EasyOCR não está inicializado.")
            return None
            
        cropped_plate = crop_image(frame, bbox)
        if cropped_plate is None:
            return None

        # Pré-processa a imagem recortada
        processed_plate = preprocess_for_ocr(cropped_plate)
        
        try:
            results = self.reader.readtext(processed_plate)
            
            # Pega o primeiro resultado com maior confiança
            if results:
                plate_text = results[0][1]
                confidence = results[0][2]
                logger.success(f"Placa reconhecida: '{plate_text}' com confiança de {confidence:.2f}.")
                return plate_text
            
            logger.info("Nenhum texto encontrado na placa.")
            return None

        except Exception as e:
            logger.error(f"Erro durante o reconhecimento OCR: {e}")
            return None