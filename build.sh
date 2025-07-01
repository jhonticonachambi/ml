#!/bin/bash
# build.sh - Script de build ultra-conservador para Render

echo "🚀 Iniciando build ultra-conservador..."

# Configurar variables de entorno muy estrictas
export PIP_PREFER_BINARY=1
export PIP_ONLY_BINARY=":all:"
export PIP_NO_BUILD_ISOLATION=1
export PIP_NO_COMPILE=1
export SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=False
export NUMPY_NO_BUILD=1

# Verificar versión de Python y fallar si no es 3.11
python_version=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "📋 Versión de Python detectada: $python_version"

if [[ "$python_version" != "3.11" ]]; then
    echo "❌ ERROR: Se requiere Python 3.11, detectado: $python_version"
    echo "🔧 Intentando usar python3.11 explícitamente..."
    if command -v python3.11 &> /dev/null; then
        alias python=python3.11
        alias pip="python3.11 -m pip"
        echo "✅ Usando python3.11 explícitamente"
    else
        echo "❌ FATAL: Python 3.11 no está disponible"
        exit 1
    fi
fi

# Actualizar pip con versión específica estable
echo "🔧 Configurando pip..."
python -m pip install --upgrade pip==23.2.1

# Instalar herramientas de construcción primero
echo "🛠️ Instalando herramientas de construcción..."
pip install --prefer-binary --only-binary=:all: wheel==0.41.2
pip install --prefer-binary --only-binary=:all: setuptools==68.2.2
pip install --prefer-binary --only-binary=:all: "Cython<3.0"

# Instalar dependencias ML en orden muy específico
echo "🔢 Instalando numpy..."
pip install --prefer-binary --only-binary=:all: --index-url https://pypi.org/simple/ numpy==1.24.3

echo "🧮 Instalando scipy..."
pip install --prefer-binary --only-binary=:all: --index-url https://pypi.org/simple/ scipy==1.10.1

echo "⚙️ Instalando joblib..."
pip install --prefer-binary --only-binary=:all: --index-url https://pypi.org/simple/ joblib==1.2.0

echo "🧵 Instalando threadpoolctl..."
pip install --prefer-binary --only-binary=:all: --index-url https://pypi.org/simple/ threadpoolctl==3.1.0

echo "🐼 Instalando pandas..."
pip install --prefer-binary --only-binary=:all: --index-url https://pypi.org/simple/ pandas==2.0.3

echo "🤖 Instalando scikit-learn..."
pip install --prefer-binary --only-binary=:all: --index-url https://pypi.org/simple/ scikit-learn==1.2.2

# Verificar que sklearn se instaló correctamente
python -c "import sklearn; print(f'✅ scikit-learn {sklearn.__version__} instalado')" || {
    echo "❌ FALLÓ la instalación de scikit-learn"
    echo "🔄 Intentando instalación alternativa..."
    pip install --no-deps --prefer-binary --only-binary=:all: scikit-learn==1.2.2
}

# Instalar dependencias FastAPI
echo "� Instalando dependencias FastAPI..."
pip install --prefer-binary fastapi==0.104.1
pip install --prefer-binary "uvicorn[standard]==0.24.0"
pip install --prefer-binary pydantic==2.5.0
pip install --prefer-binary python-multipart==0.0.6
pip install --prefer-binary gunicorn==21.2.0
pip install --prefer-binary httpx==0.25.2

echo "✅ Build completado!"

# Verificaciones finales
echo "🔍 Verificando instalaciones críticas..."
python -c "import numpy; print(f'✅ numpy {numpy.__version__}')" || echo "❌ numpy FALLÓ"
python -c "import pandas; print(f'✅ pandas {pandas.__version__}')" || echo "❌ pandas FALLÓ"
python -c "import sklearn; print(f'✅ scikit-learn {sklearn.__version__}')" || echo "❌ sklearn FALLÓ"
python -c "import fastapi; print(f'✅ fastapi instalado')" || echo "❌ fastapi FALLÓ"

echo "🎉 Proceso de build finalizado"
