<!-- # Projeto GT-VISION

Sistema de monitoramento por vídeo inteligente com detecção de eventos, alertas em tempo real e painel de controle web.

## Funcionalidades

* Monitoramento de múltiplos streams de vídeo RTSP.
* Detecção de pessoas, veículos e placas.
* Geração de alertas críticos (ex: pessoa em área restrita).
* Notificações em tempo real via WhatsApp e E-mail.
* Armazenamento de alertas em banco de dados PostgreSQL.
* Painel web minimalista para visualização dos alertas.

## Como Instalar e Configurar

1.  **Clone o repositório.**
2.  **Crie o ambiente virtual:** `python -m venv venv`
3.  **Ative o ambiente:** `.\venv\Scripts\activate`
4.  **Instale as dependências Python:** `pip install -r requirements.txt`
5.  **Instale as dependências do Bot WhatsApp:** `cd whatsapp-bot` e depois `npm install`
6.  **Configure o banco de dados** usando o Docker (use o comando `docker run ...` que definimos).
7.  **Renomeie o arquivo `.env.example` para `.env`** e preencha com suas chaves, URLs e senhas.

## Como Executar

O sistema roda em 3 processos paralelos, em 3 terminais diferentes:

1.  **Terminal 1 (Bot WhatsApp):**
    ```bash
    cd whatsapp-bot
    node main.js
    ```
2.  **Terminal 2 (API e Painel Web):**
    ```bash
    uvicorn backend.api.main:app --reload
    ```
3.  **Terminal 3 (Sistema de Visão):**
    ```bash
    python run_vision_system.py
    ``` -->