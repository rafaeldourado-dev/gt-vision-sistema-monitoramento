# backend/alerts/whatsapp_api_sender.py

import requests
from backend.utils.logger import logger
from backend.config.settings import settings

class WhatsAppAPISender:
    def __init__(self):
        # O endereço da API do seu bot Node.js
        self.api_url = "http://localhost:3000/send-alert"
        self.recipient_number = settings.whatsapp_recipient_number

        if not self.recipient_number:
            logger.warning("Número do WhatsApp não configurado no .env. Notificações de WhatsApp (API) desativadas.")
            self.is_configured = False
        else:
            self.is_configured = True
            logger.info(f"Notificador de WhatsApp (API) configurado para a URL: {self.api_url}")

    def send_notification(self, subject: str, message: str):
        if not self.is_configured:
            return

        full_message = f"🚨 {subject} 🚨\n\n{message}"
        payload = {
            "number": self.recipient_number,
            "message": full_message
        }

        try:
            # Faz a "ligação" (requisição HTTP POST) para o seu bot Node.js
            response = requests.post(self.api_url, json=payload, timeout=10)

            if response.status_code == 200:
                logger.success("Alerta enviado com sucesso via API para o bot WhatsApp.")
            else:
                logger.error(f"O bot WhatsApp respondeu com erro {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Falha ao conectar com a API do bot WhatsApp: {e}")
            logger.error("Dica: Verifique se o seu bot Node.js (main.js) está rodando no outro terminal.")