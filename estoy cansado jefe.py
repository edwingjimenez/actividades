import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import requests
import json

class OpenRouterChatbot:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com",
            "X-Title": "GPT-3.5 Chatbox"
        }
        self.model = "openai/gpt-3.5-turbo"
        self.conversation_history = []
        
    def enviar_mensaje(self, mensaje):
        try:
            self.conversation_history.append({"role": "user", "content": mensaje})
            
            payload = {
                "model": self.model,
                "messages": self.conversation_history,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                respuesta = response.json()['choices'][0]['message']['content']
                self.conversation_history.append({"role": "assistant", "content": respuesta})
                return respuesta
            else:
                error_msg = f"Error API: {response.status_code} - {response.text}"
                print(error_msg)
                return f"Error en la API: {response.status_code}"
            
        except Exception as e:
            print(f"Error de conexión: {e}")
            return "Error de conexión. Intenta nuevamente."

def obtener_api_key():
    root = tk.Tk()
    root.withdraw()
    api_key = simpledialog.askstring(
        "API Key Requerida",
        "Ingresa tu API Key de OpenRouter:",
        parent=root,
        show='*'
    )
    root.destroy()
    return api_key

def enviar_mensaje():
    mensaje = entrada.get()
    if mensaje.strip():
        chat.config(state=tk.NORMAL)
        chat.insert(tk.END, f"Tú: {mensaje}\n", 'usuario')
        chat.insert(tk.END, "Asistente: ", 'asistente')
        chat.see(tk.END)
        chat.config(state=tk.DISABLED)
        
        ventana.after(100, lambda: obtener_respuesta(mensaje))
        entrada.delete(0, tk.END)

def obtener_respuesta(mensaje):
    respuesta = chatbot.enviar_mensaje(mensaje)
    
    chat.config(state=tk.NORMAL)
    chat.insert(tk.END, f"{respuesta}\n\n", 'asistente')
    chat.see(tk.END)
    chat.config(state=tk.DISABLED)


if __name__ == "__main__":
    api_key = obtener_api_key()
    if not api_key:
        messagebox.showerror("Error", "Se requiere API Key para usar esta aplicación")
        exit()
    
    chatbot = OpenRouterChatbot(api_key)
    
    ventana = tk.Tk()
    ventana.title("Chatbox GPT-3.5-turbo (OpenRouter)")
    ventana.geometry("700x550")
    chat = scrolledtext.ScrolledText(
        ventana,
        wrap=tk.WORD,
        width=80,
        height=25,
        font=('Arial', 11),
        padx=15,
        pady=15
    )
    chat.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    chat.tag_config('usuario', foreground='#1E88E5')
    chat.tag_config('asistente', foreground='#43A047')
    chat.config(state=tk.DISABLED)
    
    chat.config(state=tk.NORMAL)
    chat.insert(tk.END, 
        "Asistente: ¡Hola! Soy un asistente con GPT-3.5-turbo. ¿En qué puedo ayudarte hoy?\n\n", 
        'asistente')
    chat.config(state=tk.DISABLED)
    
    frame_entrada = tk.Frame(ventana)
    frame_entrada.pack(pady=10, padx=10, fill=tk.X)
    
    entrada = tk.Entry(
        frame_entrada,
        width=60,
        font=('Arial', 11)
    )
    entrada.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    entrada.focus_set()
    
    boton_enviar = tk.Button(
        frame_entrada,
        text="Enviar",
        command=enviar_mensaje,
        bg='#4CAF50',
        fg='white',
        font=('Arial', 11)
    )
    boton_enviar.pack(side=tk.LEFT)
    
    entrada.bind("<Return>", lambda event: enviar_mensaje())
    
    ventana.mainloop()