# backend/api/main.py

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from . import endpoints

# --- CONFIGURAÇÃO DA APLICAÇÃO ---
app = FastAPI(
    title="GT-VISION",
    description="API e Painel de Controle para o sistema de monitoramento GT-VISION.",
    version="1.0.0"
)

# --- MONTANDO ARQUIVOS ESTÁTICOS E TEMPLATES ---
# 1. Monta a pasta 'static' para servir CSS e JS
# O caminho "frontend/static" é relativo à raiz do projeto onde você roda o uvicorn.
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# 2. Configura o diretório de templates HTML
templates = Jinja2Templates(directory="frontend/templates")


# --- ROTAS DA API ---
# Inclui os endpoints de dados (ex: /api/alerts)
# Esta linha é importante para o seu JavaScript continuar funcionando.
app.include_router(endpoints.router, prefix="/api")


# --- ROTA PARA A PÁGINA PRINCIPAL ---
# ESTA É A GRANDE MUDANÇA:
# A rota raiz "/" agora vai renderizar e retornar nosso arquivo index.html.
@app.get("/", include_in_schema=False)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})