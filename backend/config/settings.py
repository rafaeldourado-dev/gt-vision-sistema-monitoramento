# backend/config/settings.py

from pydantic_settings import BaseSettings
from pathlib import Path

# --- Endereço Exato do Arquivo .env ---
# Esta lógica calcula o caminho absoluto para a pasta raiz do seu projeto (D:\GT-V 2.5)
# e o junta com o nome do arquivo .env.
# Isso remove qualquer ambiguidade.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    database_url: str
    
    camera_seguranca_url: str
    camera_lpr_url: str

    email_sender: str | None = None
    email_password: str | None = None
    email_server: str = "smtp.gmail.com"
    email_port: int = 587
    
    whatsapp_recipient_number: str | None = None

    api_port: int = 8000
    
    api_key_ocr: str | None = None

    class Config:
        # Agora estamos passando o caminho completo e exato para o arquivo
        env_file = ENV_FILE_PATH
        env_file_encoding = "utf-8"

settings = Settings()