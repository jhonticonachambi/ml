#!/bin/bash
# fallback-build.sh - Script de instalación mínima de emergencia

echo "🆘 MODO FALLBACK: Instalación mínima..."

# Configurar entorno para solo binarios
export PIP_ONLY_BINARY=":all:"
export PIP_PREFER_BINARY=1
export PIP_NO_BUILD_ISOLATION=1

echo "🔧 Actualizando pip..."
python -m pip install --upgrade pip==23.2.1

echo "📦 Instalando solo dependencias críticas..."

# Instalar solo las dependencias absolutamente necesarias
pip install --only-binary=:all: --prefer-binary wheel==0.41.2
pip install --only-binary=:all: --prefer-binary setuptools==68.2.2
pip install --only-binary=:all: --prefer-binary numpy==1.24.3
pip install --only-binary=:all: --prefer-binary fastapi==0.104.1
pip install --only-binary=:all: --prefer-binary uvicorn==0.24.0
pip install --only-binary=:all: --prefer-binary pydantic==2.5.0

# Intentar scikit-learn como último recurso
echo "🤖 Intentando scikit-learn básico..."
pip install --only-binary=:all: --prefer-binary --no-deps scikit-learn==1.2.2 || {
    echo "❌ scikit-learn falló, usando versión alternativa..."
    pip install --only-binary=:all: --prefer-binary scikit-learn==1.1.3
}

echo "✅ Instalación mínima completada"

# Verificar solo lo crítico
python -c "import fastapi; print('✅ FastAPI OK')" || echo "❌ FastAPI FALLÓ"
python -c "import numpy; print('✅ NumPy OK')" || echo "❌ NumPy FALLÓ"
