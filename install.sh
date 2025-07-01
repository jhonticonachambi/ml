#!/bin/bash
# Script de instalación alternativo para Render

echo "🔧 Instalando dependencias del sistema..."
apt-get update
apt-get install -y build-essential

echo "🐍 Actualizando pip y herramientas de construcción..."
pip install --upgrade pip wheel setuptools

echo "📦 Instalando dependencias con binarios precompilados..."
pip install --only-binary=:all: --no-compile -r requirements.txt

echo "✅ Instalación completada"
