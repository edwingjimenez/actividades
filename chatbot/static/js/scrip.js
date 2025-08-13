// Manejar el envío de mensajes
document.getElementById('formulario-entrada').addEventListener('submit', function(e) {
    e.preventDefault();
    const campoTexto = document.getElementById('campo-entrada');
    const texto = campoTexto.value.trim();

    if (texto) {
        // Mostrar mensaje del usuario
        agregarMensaje(texto, 'mensaje-usuario');

        // Enviar al servidor para procesamiento
        enviarPeticion('/obtener-respuesta', {
            contenido: texto
        })
        .then(respuesta => {
            // Mostrar respuesta recibida
            agregarMensaje(respuesta.contenido, 'mensaje-sistema');
        });

        // Limpiar campo de texto
        campoTexto.value = '';
    }
});

// Función para agregar mensajes al historial
function agregarMensaje(contenido, tipo) {
    const historial = document.getElementById('area-mensajes');
    const elementoMensaje = document.createElement('div');
    
    elementoMensaje.classList.add('mensaje', tipo);
    elementoMensaje.textContent = contenido;
    historial.appendChild(elementoMensaje);
    
    // Desplazamiento automático al final
    historial.scrollTop = historial.scrollHeight;
}

// Función genérica para enviar peticiones
function enviarPeticion(url, datos) {
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(datos)
    })
    .then(respuesta => {
        if (!respuesta.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        return respuesta.json();
    })
    .catch(error => {
        console.error('Error:', error);
        return { contenido: 'Hubo un problema al procesar tu mensaje' };
    });
}