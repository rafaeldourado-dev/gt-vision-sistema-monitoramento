// whatsapp-bot/handlers/messageHandler.js

const config = require('../config');
const { db, isAtendimentoAberto, abrirChamado } = require('../services/ticketService');

function getGreeting() {
    const hour = new Date().getHours();
    if (hour >= 5 && hour < 12) return "Bom dia";
    if (hour >= 12 && hour < 18) return "Boa tarde";
    return "Boa noite";
}

async function handleMessage(client, msg) {
    const chatId = msg.from;
    const body = msg.body.trim().toLowerCase();

    // Garante que o usuário sempre tenha um estado, evitando erros.
    if (!db.data.userState[chatId]) {
        db.data.userState[chatId] = 'awaiting_command';
    }

    const currentState = db.data.userState[chatId];
    console.log(`[${new Date().toLocaleTimeString()}] Usuário: ${chatId} | Estado: ${currentState} | Mensagem: "${body}"`);

    // --- LÓGICA DE PRIMEIRO CONTATO ---
    if (currentState === 'awaiting_command' && !['0', '1', '2', '3', '4', '5', 'menu'].includes(body)) {
        const greeting = getGreeting();
        await client.sendMessage(chatId, `${greeting}! ${config.MENSAGENS.boasVindas}`);
        await client.sendMessage(chatId, config.MENSAGENS.menuPrincipal);
        await db.write();
        return;
    }

    // --- LÓGICA PRINCIPAL BASEADA NO ESTADO ---
    switch (currentState) {
        case 'awaiting_command':
            let responseSent = false;

            if (body === '1') {
                await client.sendMessage(chatId, config.MENSAGENS.horarioAtendimento(config.HORA_INICIO, config.HORA_FIM));
                responseSent = true;
            } else if (body === '2') {
                await client.sendMessage(chatId, config.MENSAGENS.informeTipoProblema);
                db.data.userState[chatId] = 'awaiting_tipo_problema';
            } else if (body === '3') {
                await client.sendMessage(chatId, config.MENSAGENS.falarComAtendente);
                responseSent = true;
            } else if (body === '4') {
                await client.sendMessage(chatId, config.MENSAGENS.nossosServicos);
                responseSent = true;
            } else if (body === '5') {
                await client.sendMessage(chatId, config.MENSAGENS.localizacao);
                responseSent = true;
            } else if (body === '0' || body === 'menu') {
                await client.sendMessage(chatId, config.MENSAGENS.menuPrincipal);
            } else {
                await client.sendMessage(chatId, config.MENSAGENS.opcaoInvalida);
                await client.sendMessage(chatId, config.MENSAGENS.menuPrincipal);
            }

            if (responseSent) {
                await client.sendMessage(chatId, "----------------------");
                await client.sendMessage(chatId, config.MENSAGENS.menuPrincipal);
            }
            break;

        case 'awaiting_tipo_problema':
            let tipo;
            if (body === '1') tipo = 'crítico';
            else if (body === '2') tipo = 'não crítico';
            else {
                await client.sendMessage(chatId, "Opção inválida. Por favor, responda com '1' para crítico ou '2' para não crítico.");
                break;
            }

            const chamadoId = await abrirChamado(chatId, tipo);
            const prazoResp = tipo === 'crítico' ? '2 horas' : '8 horas';
            const prazoPres = tipo === 'crítico' ? '4 horas' : '72 horas';
            await client.sendMessage(chatId, config.MENSAGENS.chamadoSucesso(chamadoId, tipo, prazoResp, prazoPres));
            
            if (!isAtendimentoAberto()) {
                await client.sendMessage(chatId, config.MENSAGENS.foraDoHorario);
            }
            
            await client.sendMessage(chatId, "----------------------");
            await client.sendMessage(chatId, config.MENSAGENS.menuPrincipal);
            db.data.userState[chatId] = 'awaiting_command';
            break;

        default:
            await client.sendMessage(chatId, "Ocorreu um erro e reiniciei nossa conversa. Por favor, escolha uma opção do menu.");
            await client.sendMessage(chatId, config.MENSAGENS.menuPrincipal);
            db.data.userState[chatId] = 'awaiting_command';
            break;
    }
    await db.write();
}

module.exports = handleMessage;