document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const typingIndicator = document.getElementById('typingIndicator');
    const apiStatus = document.getElementById('apiStatus');
    const statusIndicator = apiStatus.querySelector('.status-indicator');
    const statusText = apiStatus.querySelector('.status-text');
    
    // Verificar estado de la API al cargar
    checkAPIStatus();
    
    // Función para verificar el estado de la API
    function checkAPIStatus() {
        fetch('/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: 'ping' })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                setAPIStatus('error', 'Error de conexión');
            } else {
                setAPIStatus('connected', 'Conectado');
            }
        })
        .catch(error => {
            setAPIStatus('error', 'Error de conexión');
            console.error('Error:', error);
        });
    }
    
    // Función para establecer el estado de la API
    function setAPIStatus(status, message) {
        statusText.textContent = message;
        if (status === 'connected') {
            statusIndicator.classList.add('connected');
            statusIndicator.style.animation = 'none';
        } else {
            statusIndicator.classList.remove('connected');
            statusIndicator.style.animation = 'pulse 1.5s infinite';
        }
    }
    
    // Función para enviar mensaje
    function sendMessage() {
        const message = userInput.value.trim();
        
        if (message) {
            // Mostrar mensaje del usuario
            addMessage(message, 'user');
            userInput.value = '';
            
            // Mostrar indicador de typing
            typingIndicator.style.display = 'flex';
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            // Deshabilitar botón mientras se procesa
            sendButton.disabled = true;
            userInput.disabled = true;
            
            // Enviar mensaje al servidor
            fetch('/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                // Ocultar indicador de typing
                typingIndicator.style.display = 'none';
                
                if (data.error) {
                    addMessage('Lo siento, ha ocurrido un error. Intenta nuevamente.', 'bot', 'Sistema');
                } else {
                    addMessage(data.bot_response, 'bot', data.source === 'gemini' ? 'Gemini AI' : 'Sistema');
                }
            })
            .catch(error => {
                // Ocultar indicador de typing
                typingIndicator.style.display = 'none';
                
                addMessage('Error de conexión. Intenta nuevamente.', 'bot', 'Sistema');
                console.error('Error:', error);
            })
            .finally(() => {
                // Habilitar botón y input
                sendButton.disabled = false;
                userInput.disabled = false;
                userInput.focus();
            });
        }
    }
    
    // Función para añadir mensaje al chat
    function addMessage(text, type, source = 'Usuario') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        const messageText = document.createElement('p');
        messageText.textContent = text;
        
        const timeSpan = document.createElement('span');
        timeSpan.className = 'timestamp';
        timeSpan.textContent = getCurrentTime();
        
        const sourceSpan = document.createElement('span');
        sourceSpan.className = 'message-source';
        sourceSpan.textContent = source;
        
        contentDiv.appendChild(messageText);
        contentDiv.appendChild(timeSpan);
        contentDiv.appendChild(sourceSpan);
        messageDiv.appendChild(contentDiv);
        
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Función para obtener hora actual
    function getCurrentTime() {
        const now = new Date();
        return `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
    }
    
    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    userInput.addEventListener('input', function() {
        sendButton.disabled = !userInput.value.trim();
    });
    
    // Focus en el input al cargar
    userInput.focus();
});