// main.js
const { Client, LocalAuth } = require("whatsapp-web.js");
const qrcode = require("qrcode-terminal");
const express = require('express');
const handleMessage = require('./handlers/messageHandler');
const config = require('./config');

// --- INICIALIZAÇÃO DO CLIENTE E API ---
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox'] // Configuração de estabilidade
    }
});
const app = express();
app.use(express.json());

// --- EVENTOS DO CLIENTE WHATSAPP ---
client.on("qr", (qr) => qrcode.generate(qr, { small: true }));
client.on("ready", () => console.log("✅ Bot GT-Vision está pronto e conectado."));
client.on("message", (msg) => handleMessage(client, msg)); // Delega para o handler

// --- API PARA RECEBER ALERTAS DO PYTHON ---
app.post('/send-alert', async (req, res) => {
    const { number, message } = req.body;
    if (!number || !message) {
        return res.status(400).json({ success: false, error: 'Número e mensagem são obrigatórios.' });
    }
    try {
        const chatId = `${number.replace('+', '')}@c.us`;
        await client.sendMessage(chatId, message);
        console.log(`✅ Alerta enviado via API para ${number}`);
        res.status(200).json({ success: true, message: 'Alerta enviado.' });
    } catch (error) {
        console.error('Erro ao enviar alerta via API:', error);
        res.status(500).json({ success: false, error: 'Falha ao enviar mensagem.' });
    }
});

// --- INICIALIZAÇÃO DO SERVIDOR ---
client.initialize().then(() => {
    app.listen(config.API_PORT, () => {
        console.log(`🚀 API de Alertas ouvindo na porta ${config.API_PORT}`);
    });
}).catch(err => {
    console.error("Erro na inicialização do cliente:", err);
});