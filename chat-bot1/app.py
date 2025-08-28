from flask import Flask, render_template, request, jsonify
import datetime
import google.generativeai as genai
import os
import time

app = Flask(__name__)

# Configurar la API de Gemini
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Inicializar Gemini solo si la API key está disponible
gemini_model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-pro')
        print("✅ Gemini AI configurado correctamente")
    except Exception as e:
        print(f"❌ Error configurando Gemini: {str(e)}")
        gemini_model = None
else:
    print("⚠️  GEMINI_API_KEY no encontrada. Usando modo local.")

class ChatBot:
    def __init__(self):
        self.responses = {
            'saludo': {
                'patterns': ['hola', 'buenos días', 'buenas tardes', 'buenas noches', 'hey', 'hi', 'hello'],
                'responses': [
                    '¡Hola! ¿En qué puedo ayudarte hoy?',
                    '¡Hola! ¿Cómo estás?',
                    '¡Hola! Encantado de hablar contigo.'
                ]
            },
            'despedida': {
                'patterns': ['adiós', 'chao', 'hasta luego', 'nos vemos', 'bye', 'goodbye'],
                'responses': [
                    '¡Hasta luego! Que tengas un buen día.',
                    '¡Adiós! Fue un placer ayudarte.',
                    '¡Nos vemos! No dudes en volver si necesitas más ayuda.'
                ]
            },
            'agradecimiento': {
                'patterns': ['gracias', 'muchas gracias', 'te lo agradezco', 'thanks', 'thank you'],
                'responses': [
                    '¡De nada! Estoy aquí para ayudar.',
                    '¡No hay problema! ¿Necesitas algo más?',
                    '¡Es un placer ayudarte!'
                ]
            },
            'nombre': {
                'patterns': ['cómo te llamas', 'cuál es tu nombre', 'quién eres'],
                'responses': [
                    'Soy ChatBot, tu asistente virtual con tecnología Gemini AI.',
                    'Me llamo ChatBot, ¡encantado de conocerte!',
                    'Soy ChatBot, ¿en qué puedo ayudarte?'
                ]
            },
            'hora': {
                'patterns': ['qué hora es', 'dime la hora', 'hora actual'],
                'responses': [
                    f'La hora actual es: {datetime.datetime.now().strftime("%H:%M:%S")}',
                    f'Son las {datetime.datetime.now().strftime("%H:%M")}',
                    f'La hora es: {datetime.datetime.now().strftime("%H:%M:%S")}'
                ]
            },
            'fecha': {
                'patterns': ['qué día es hoy', 'fecha actual', 'qué fecha es'],
                'responses': [
                    f'Hoy es: {datetime.datetime.now().strftime("%d/%m/%Y")}',
                    f'La fecha actual es: {datetime.datetime.now().strftime("%A, %d de %B de %Y")}',
                    f'Estamos a {datetime.datetime.now().strftime("%d/%m/%Y")}'
                ]
            },
            'gemini': {
                'patterns': ['qué es gemini', 'gemini ai', 'google gemini'],
                'responses': [
                    'Gemini es un modelo de IA de Google. Para usarlo, configura tu API_KEY.',
                    'Gemini AI es la IA avanzada de Google. Necesitas una API key para usarla.',
                    'Google Gemini es muy potente. Configura GEMINI_API_KEY para habilitarlo.'
                ]
            },
            'default': {
                'responses': [
                    'No estoy seguro de entenderte. ¿Podrías reformular tu pregunta?',
                    'Interesante, pero no sé cómo responder a eso.',
                    'Lo siento, no tengo una respuesta para eso todavía.',
                    '¿Podrías intentar preguntar de otra manera?'
                ]
            }
        }

    def get_response(self, user_input):
        user_input = user_input.lower().strip()
        
        # Buscar coincidencia en patrones
        for intent, data in self.responses.items():
            if intent != 'default' and any(pattern in user_input for pattern in data['patterns']):
                return {
                    'response': data['responses'][0],
                    'timestamp': datetime.datetime.now().strftime("%H:%M:%S"),
                    'source': 'local'
                }
        
        # Si no hay coincidencia y Gemini está disponible, usarlo
        if gemini_model:
            try:
                response = gemini_model.generate_content(user_input)
                return {
                    'response': response.text,
                    'timestamp': datetime.datetime.now().strftime("%H:%M:%S"),
                    'source': 'gemini'
                }
            except Exception as e:
                print(f"Error con Gemini AI: {str(e)}")
                # Si falla Gemini, usar respuesta local
                return {
                    'response': "Lo siento, hubo un error con Gemini AI. " + self.responses['default']['responses'][0],
                    'timestamp': datetime.datetime.now().strftime("%H:%M:%S"),
                    'source': 'local'
                }
        
        # Respuesta por defecto
        return {
            'response': self.responses['default']['responses'][0],
            'timestamp': datetime.datetime.now().strftime("%H:%M:%S"),
            'source': 'local'
        }

chatbot = ChatBot()

@app.route('/')
def index():
    return render_template('index.html', gemini_available=gemini_model is not None)

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Mensaje vacío'}), 400
        
        bot_response = chatbot.get_response(user_message)
        
        return jsonify({
            'user_message': user_message,
            'bot_response': bot_response['response'],
            'timestamp': bot_response['timestamp'],
            'source': bot_response['source']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🤖 ChatBot Flask con Gemini AI")
    print("📍 Servidor ejecutándose en: http://localhost:5000")
    if gemini_model:
        print("✅ Modo: Conectado a Gemini AI")
    else:
        print("ℹ️  Modo: Local (sin Gemini AI)")
        print("💡 Para habilitar Gemini AI, establece la variable de entorno GEMINI_API_KEY")
    
    app.run(debug=True, host='0.0.0.0', port=5000)