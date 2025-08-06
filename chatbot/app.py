from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def chatbot_response(user_message):
    