import sys
import subprocess
import requests


def check_python_version():
    print(f"Versión de Python: {sys.version}")


def check_dependencies():
    try:
        import flask
        print(f"Flask instalado: versión {flask.__version__}")
    except ImportError:
        print("Flask no está instalado")

    try:
        import requests
        print(f"Requests instalado: versión {requests.__version__}")
    except ImportError:
        print("Requests no está instalado")


def check_ollama_running():
    try:
        response = requests.get('http://localhost:11434/api/tags')
        if response.status_code == 200:
            print("Ollama está funcionando correctamente")
            print("Modelos disponibles:", response.json())
        else:
            print(f"Ollama está respondiendo, pero con un código de estado inesperado: {
                  response.status_code}")
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar a Ollama. Asegúrate de que esté en ejecución")


def main():
    print("Ejecutando diagnóstico para Ollama Web Interface:")
    check_python_version()
    check_dependencies()
    check_ollama_running()


if __name__ == "__main__":
    main()
