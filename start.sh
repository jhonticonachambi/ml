#!/bin/bash
# start.sh - Script de inicio para deployment

echo "🚀 Iniciando ML Service..."

# Verificar si existen los directorios necesarios
echo "📁 Creando directorios necesarios..."
mkdir -p models
mkdir -p data
mkdir -p logs

# Verificar si existe el modelo entrenado
if [ ! -f "models/volunteer_model.pkl" ]; then
    echo "⚠️ Modelo no encontrado. Generando datos de entrenamiento..."
    python generate_data.py
    echo "🧠 Entrenando modelo..."
    python -c "from ml_model import VolunteerMLModel; model = VolunteerMLModel(); model.train('data/training_data.csv'); model.save_model()"
    echo "✅ Modelo entrenado y guardado"
fi

# Iniciar la aplicación
echo "🌟 Iniciando FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1
