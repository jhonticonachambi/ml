#!/bin/bash
# Script de instalación alternativo para Render

echo "🔧 Configurando entorno Python..."
export PIP_PREFER_BINARY=1
export PIP_ONLY_BINARY=":all:"
export SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=False

echo "🐍 Actualizando pip y herramientas básicas..."
python -m pip install --upgrade pip
pip install wheel==0.41.2 setuptools==68.2.2

echo "� Instalando dependencias ML de forma escalonada..."
pip install --prefer-binary --only-binary=:all: numpy==1.24.4
pip install --prefer-binary --only-binary=:all: joblib==1.2.0
pip install --prefer-binary --only-binary=:all: scipy==1.10.1
pip install --prefer-binary --only-binary=:all: pandas==2.0.3
pip install --prefer-binary --only-binary=:all: scikit-learn==1.2.2

echo "🚀 Instalando dependencias FastAPI..."
pip install --prefer-binary fastapi==0.104.1
pip install --prefer-binary uvicorn[standard]==0.24.0
pip install --prefer-binary pydantic==2.5.0
pip install --prefer-binary python-multipart==0.0.6
pip install --prefer-binary gunicorn==21.2.0
pip install --prefer-binary httpx==0.25.2

echo "✅ Instalación completada"
