import sys
import subprocess
from flask import Flask, render_template, request, jsonify
import requests
import logging
import json
import markdown

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


def check_ollama_version():
    try:
        result = subprocess.run(['ollama', 'version'], capture_output=True,
                                text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return result.stdout.strip()
    except FileNotFoundError:
        return "Ollama no encontrado. Asegúrate de que esté instalado y en el PATH."
    except Exception as e:
        return f"Error al obtener la versión de Ollama: {str(e)}"


@app.route('/')
def home():
    ollama_version = check_ollama_version()
    logging.info(f"Versión de Ollama: {ollama_version}")
    return render_template('chat.html')


@app.route('/chat', methods=['POST'])
def chat():
    message = request.json['message']
    logging.debug(f"Mensaje recibido: {message}")
    try:
        response = requests.post('http://localhost:11434/api/chat', json={
            'model': 'phi3',
            'messages': [{'role': 'user', 'content': message}]
        }, timeout=30)
        response.raise_for_status()

        ollama_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    json_response = json.loads(line)
                    if 'content' in json_response.get('message', {}):
                        ollama_response += json_response['message']['content']
                except json.JSONDecodeError:
                    logging.error(f"Error al decodificar JSON: {line}")

        # Convertir Markdown a HTML
        html_response = markdown.markdown(ollama_response)

        logging.debug(f"Respuesta de Ollama (HTML): {html_response}")
        return jsonify({'response': html_response})
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al comunicarse con Ollama: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print(f"Python version: {sys.version}")
    print(f"Ollama version: {check_ollama_version()}")
    app.run(debug=True)
