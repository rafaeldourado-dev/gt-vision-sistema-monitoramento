// whatsapp-bot/config.js

module.exports = {
    // Configurações de Horário
    HORA_INICIO: 8,
    HORA_FIM: 18,
    DIAS_POR_SEMANA: [1, 2, 3, 4, 5], // 1=Segunda, 2=Terça, etc.
    API_PORT: 3000,

    // Textos do Bot (Versão Completa)
    MENSAGENS: {
        boasVindas: "Sou o assistente virtual da GT-Vision. Abaixo estão as opções em que posso lhe ajudar:",
        menuPrincipal: `1 - Ver horário de atendimento\n2 - Abrir chamado de suporte técnico\n3 - Falar com atendente\n4 - Ver nossos serviços\n5 - Ver localização`,
        horarioAtendimento: (inicio, fim) => `Nosso horário de atendimento é de Segunda a Sexta, das ${inicio}h às ${fim}h.`,
        foraDoHorario: "Nosso atendimento está fora do horário. Seu chamado será registrado e tratado no próximo dia útil.",
        falarComAtendente: "Certo, Senhor(a). Um de nossos atendentes humanos entrará em contato nesta conversa em breve.",
        nossosServicos: "Nossos serviços incluem: Monitoramento por Câmeras, Reconhecimento de Placas (LPR), Detecção de Movimento e Alertas de Segurança personalizados.",
        localizacao: "Estamos localizados na Rua Juscelino, K. Oliveira, 1145, Itaporã-MS.",
        opcaoInvalida: "Desculpe, Senhor(a), não reconheci este comando. Por favor, escolha uma das opções abaixo.",
        informeTipoProblema: "Entendido. Por favor, informe o tipo do problema:\n\n1 - Crítico (Sistema parado ou falha grave)\n2 - Não crítico (Dúvida ou problema menor)",
        chamadoSucesso: (id, tipo, prazoResp, prazoPres) => `✅ Chamado aberto com sucesso!\n\n*ID do Chamado:* ${id}\n*Tipo:* ${tipo}\n*Prazo de 1ª Resposta:* ${prazoResp}\n*Atendimento Presencial (se necessário):* ${prazoPres}`,
    }
};