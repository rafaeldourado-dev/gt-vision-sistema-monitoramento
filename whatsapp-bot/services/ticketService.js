// services/ticketService.js
const { Low } = require('lowdb');
const { JSONFile } = require('lowdb/node');
const config = require('../config');

// Configura o "banco de dados" para usar o arquivo db.json que estará na pasta principal
const adapter = new JSONFile('db.json');
const defaultData = { chamados: {}, userState: {} };
const db = new Low(adapter, defaultData);

// É crucial ler os dados do arquivo para a memória
async function initializeDatabase() {
    await db.read();
    // Se o arquivo db.json não existir, ele será criado com os dados padrão ao escrever
    db.data = db.data || defaultData; 
    await db.write();
    console.log("🗄️ Banco de dados em arquivo (db.json) inicializado.");
}

function isAtendimentoAberto() {
    const now = new Date();
    const diaSemana = now.getDay();
    const hora = now.getHours();
    return config.DIAS_POR_SEMANA.includes(diaSemana) && hora >= config.HORA_INICIO && hora < config.HORA_FIM;
}

async function abrirChamado(chatId, tipoProblema) {
    const chamadoId = `CHAMADO-${Date.now()}`;

    db.data.chamados[chamadoId] = {
        chatId,
        tipo: tipoProblema,
        abertoEm: new Date(),
        status: 'aberto'
    };
    await db.write(); // Salva a alteração no arquivo db.json
    return chamadoId;
}

module.exports = {
    db,
    initializeDatabase,
    isAtendimentoAberto,
    abrirChamado,
};