# backend/storage/database.py

from sqlalchemy.orm import sessionmaker # <-- Importação nova e crucial
from backend.config.models import engine, Base
from backend.utils.logger import logger
from typing import Generator

# --- CONFIGURAÇÃO DA SESSÃO ---
# Aqui nós criamos uma "fábrica" de sessões (SessionLocal) que já vem
# pré-configurada e "ligada" (bind=engine) ao nosso banco de dados.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator:
    """
    Cria e fornece uma nova sessão do banco de dados para uma operação.
    """
    db = SessionLocal() # <-- MUDANÇA AQUI: Agora usamos a nossa fábrica de sessões
    try:
        yield db
    finally:
        db.close()

def create_database():
    """
    Cria as tabelas do banco de dados com base nos modelos definidos.
    """
    logger.info("Tentando criar as tabelas do banco de dados...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.success("Tabelas do banco de dados criadas com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao criar as tabelas do banco de dados: {e}")

# Este bloco continua útil para criar o banco pela primeira vez
if __name__ == "__main__":
    create_database()