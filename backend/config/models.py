# backend/config/models.py

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from .settings import settings
from datetime import datetime

# --- Configuração do Banco de Dados com SQLAlchemy ---
DATABASE_URL = settings.database_url
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# --- Modelo da Tabela do Banco de Dados (SQLAlchemy) ---
class Alert(Base):
    __tablename__ = 'alerts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_critical = Column(Boolean, default=False)
    image_path = Column(String, nullable=True)
    video_path = Column(String, nullable=True)