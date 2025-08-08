import requests
import smtplib
from email.mime.text import MIMEText
from backend.config.settings import settings
from backend.utils.logger import logger

class NotificationSender:
    """
    Classe base (interface) para o envio de notificações.
    """
    def send_notification(self, subject: str, message: str):
        raise NotImplementedError("O método send_notification deve ser implementado nas subclasses.")

class TelegramSender(NotificationSender):
    """
    Envia notificações via Telegram usando a API de Bots.
    """
    def __init__(self):
        self.token = settings.telegram_bot_token
        self.chat_id = settings.telegram_chat_id
        if not self.token or not self.chat_id:
            logger.warning("Token ou Chat ID do Telegram não configurados. As notificações não serão enviadas.")
            self.is_configured = False
        else:
            self.is_configured = True
            logger.info("Notificador do Telegram configurado.")

    def send_notification(self, subject: str, message: str):
        if not self.is_configured:
            return

        api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': f"🚨 Alerta GT-VISION - {subject}\n\n{message}"
        }
        
        try:
            response = requests.post(api_url, data=payload)
            response.raise_for_status()
            logger.success("Notificação enviada com sucesso para o Telegram.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao enviar notificação para o Telegram: {e}")

class EmailSender(NotificationSender):
    """
    Envia notificações por e-mail usando SMTP.
    """
    def __init__(self):
        self.sender = settings.email_sender
        self.password = settings.email_password
        self.server = settings.email_server
        self.port = settings.email_port
        
        if not self.sender or not self.password:
            logger.warning("Configurações de e-mail incompletas. As notificações não serão enviadas.")
            self.is_configured = False
        else:
            self.is_configured = True
            logger.info("Notificador de e-mail configurado.")
            
    def send_notification(self, subject: str, message: str, recipient: str):
        if not self.is_configured:
            return
            
        try:
            msg = MIMEText(message)
            msg['Subject'] = f"🚨 Alerta GT-VISION - {subject}"
            msg['From'] = self.sender
            msg['To'] = recipient

            with smtplib.SMTP(self.server, self.port) as smtp_server:
                smtp_server.starttls()
                smtp_server.login(self.sender, self.password)
                smtp_server.sendmail(self.sender, recipient, msg.as_string())
                logger.success(f"Notificação enviada com sucesso para o e-mail: {recipient}.")
        except Exception as e:
            logger.error(f"Erro ao enviar notificação por e-mail: {e}")