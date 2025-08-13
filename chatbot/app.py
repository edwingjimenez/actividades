from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def procesar_mensaje(texto):
    texto = texto.lower().strip()
    
    if any(palabra in texto for palabra in ['hola', 'buenos días']):
        return "¡Bienvenido! ¿En qué puedo ayudarle?"
    elif 'horario' in texto:
        return "Nuestro horario es de 9:00 a 18:00 hrs"
    elif 'contacto' in texto:
        return "Contáctenos al: 555-1234"
    else:
        return "No entendí su consulta. Por favor reformule."

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/enviar_mensaje', methods=['POST'])
def manejar_mensaje():
    datos = request.json
    respuesta = procesar_mensaje(datos.get('mensaje', ''))
    return jsonify({'respuesta': respuesta})

if __name__ == '__main__':
    app.run(debug=True, port=5000)