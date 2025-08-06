from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def chatbot_response(user_message):
    user_message =user_message.lower().strip()
    if "hola" in user_message or "buenos dias" in user_message:
        return "¡Hola! ¿Cómo puedo ayudarte hoy?"
    elif "como estas" in user_message or "que tal" in user_message:
        return "¡Estoy bien, gracias por preguntar! ¿Y tú?"
    elif "adios" in user_message or "hasta luego" in user_message:
        return "¡Adiós! Que tengas un buen día."
    elif "ayuda" in user_message:
        return "puedo responder a preguntas basicas. Intenta preguntar por 'horario'  'contacto' 0 'ubicacion'."
    elif "horario" in user_message:
        return "nuestro horario de atención es de lunes a viernes de 9:00 a 18:00 de lunes a viernes."
    elif "contacto" in user_message:
        return "puedes contactarnos al 555-1234 o por correo electrónico a info@ejemplo.com"
    elif "ubicacion" in user_message:
        return "estamos ubicados en la calle 123."
    
    