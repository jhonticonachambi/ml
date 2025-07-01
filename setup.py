#!/usr/bin/env python3
"""
Script para configurar y ejecutar el servicio de ML
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Ejecuta un comando y maneja errores"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}")
        print(f"Error: {e.stderr}")
        return False

def setup_ml_service():
    """Configura el servicio de ML"""
    print("🚀 Configurando Servicio de ML para Voluntarios")
    print("=" * 50)
    
    # Verificar Python
    print("🐍 Verificando Python...")
    try:
        import sys
        print(f"✅ Python {sys.version} encontrado")
    except:
        print("❌ Python no encontrado")
        return False
    
    # Instalar dependencias
    if not run_command("pip install -r requirements.txt", "Instalando dependencias"):
        return False
    
    # Generar datos de entrenamiento
    if not os.path.exists('data/training_data.csv'):
        if not run_command("python generate_data.py", "Generando datos de entrenamiento"):
            return False
    else:
        print("✅ Datos de entrenamiento ya existen")
    
    # Entrenar modelo
    if not os.path.exists('models/volunteer_model.pkl'):
        if not run_command("python ml_model.py", "Entrenando modelo"):
            return False
    else:
        print("✅ Modelo ya entrenado")
    
    print("\n🎉 Configuración completada!")
    print("\nPara iniciar el servidor, ejecuta:")
    print("python main.py")
    print("\nO con uvicorn:")
    print("uvicorn main:app --reload --host 127.0.0.1 --port 8000")
    
    return True

def start_server():
    """Inicia el servidor FastAPI"""
    print("🌐 Iniciando servidor FastAPI...")
    run_command("uvicorn main:app --reload --host 127.0.0.1 --port 8000", "Servidor FastAPI")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "start":
        start_server()
    else:
        setup_ml_service()
