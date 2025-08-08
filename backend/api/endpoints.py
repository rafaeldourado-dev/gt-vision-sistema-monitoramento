# backend/api/endpoints.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

# Importações corrigidas e organizadas
from backend.storage.database import get_db
from backend.config.models import Alert      # <-- Importa o modelo do banco
from .schemas import AlertSchema            # <-- Importa o modelo da API (schema)

router = APIRouter()

@router.get("/alerts", response_model=List[AlertSchema])
def get_alerts(db: Session = Depends(get_db)):
    """
    Retorna os últimos 50 alertas registrados no banco de dados.
    """
    alerts = db.query(Alert).order_by(Alert.timestamp.desc()).limit(50).all()
    return alerts