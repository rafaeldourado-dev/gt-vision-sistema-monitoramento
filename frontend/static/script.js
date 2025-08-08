// frontend/static/script.js

const API_URL = "http://localhost:8000/api/alerts";
const alertContainer = document.getElementById("alert-container");

// Usamos um Set para guardar os IDs dos alertas que já foram mostrados na tela.
// É uma forma muito eficiente de evitar duplicatas.
const displayedAlertIds = new Set();

/**
 * Cria e exibe um pop-up de alerta na tela.
 * @param {object} alert - O objeto do alerta vindo da API.
 */
function createAlertPopup(alert) {
    const alertElement = document.createElement('div');
    alertElement.className = 'alert-popup';

    const icon = alert.is_critical ? '⚠️' : 'ℹ️';
    const titleColor = alert.is_critical ? '#ff7b72' : '#58a6ff'; // Vermelho para crítico, azul para normal
    const formattedTimestamp = new Date(alert.timestamp).toLocaleTimeString('pt-BR');

    alertElement.innerHTML = `
        <div class="alert-header" style="color: ${titleColor};">
            <span class="alert-icon">${icon}</span>
            <span>${alert.title}</span>
        </div>
        <div class="alert-body">
            ${alert.description}
        </div>
        <div class="alert-timestamp">
            ${formattedTimestamp}
        </div>
    `;

    alertContainer.prepend(alertElement); // Adiciona o novo alerta no início do container

    // Define um tempo para a animação de saída e remoção do elemento
    setTimeout(() => {
        alertElement.classList.add('fade-out');
        // Remove o elemento do DOM após a animação de fade-out terminar
        alertElement.addEventListener('animationend', () => {
            alertElement.remove();
        });
    }, 10000); // O pop-up some após 10 segundos
}

/**
 * Busca alertas da API e exibe apenas os novos.
 */
async function fetchNewAlerts() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) {
            console.error(`Erro na API: ${response.statusText}`);
            return;
        }
        const alerts = await response.json();

        // Itera sobre os alertas recebidos
        alerts.forEach(alert => {
            // Se o ID do alerta ainda NÃO FOI mostrado, exiba-o
            if (!displayedAlertIds.has(alert.id)) {
                displayedAlertIds.add(alert.id); // Adiciona o ID ao nosso registro
                createAlertPopup(alert); // Cria o pop-up
            }
        });
    } catch (error) {
        console.error("Falha ao buscar novos alertas:", error);
    }
}

// Inicia o ciclo de verificação a cada 3 segundos.
setInterval(fetchNewAlerts, 3000);
console.log("Monitoramento de alertas iniciado.");