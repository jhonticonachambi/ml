#!/bin/bash
# build.sh - Script de build personalizado para Render

echo "🚀 Iniciando build personalizado..."

# Configurar variables de entorno
export PIP_PREFER_BINARY=1
export PIP_ONLY_BINARY=":all:"
export SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=False
export PIP_NO_BUILD_ISOLATION=1

# Verificar versión de Python
echo "📋 Versión de Python: $(python --version)"
echo "📋 Versión de pip: $(pip --version)"

# Actualizar pip y herramientas básicas
echo "🔧 Actualizando herramientas básicas..."
python -m pip install --upgrade pip==23.3.1
pip install wheel==0.41.2 setuptools==68.2.2

# Instalar numpy primero (dependencia crítica)
echo "🔢 Instalando numpy..."
pip install --prefer-binary --only-binary=:all: numpy==1.24.4

# Instalar scipy (si scikit-learn lo necesita)
echo "🧮 Instalando scipy..."
pip install --prefer-binary --only-binary=:all: scipy==1.10.1

# Instalar pandas
echo "🐼 Instalando pandas..."
pip install --prefer-binary --only-binary=:all: pandas==2.0.3

# Instalar joblib
echo "⚙️ Instalando joblib..."
pip install --prefer-binary --only-binary=:all: joblib==1.2.0

# Instalar scikit-learn
echo "🤖 Instalando scikit-learn..."
pip install --prefer-binary --only-binary=:all: scikit-learn==1.2.2

# Instalar el resto de dependencias
echo "📦 Instalando resto de dependencias..."
pip install --prefer-binary fastapi==0.104.1
pip install --prefer-binary uvicorn[standard]==0.24.0
pip install --prefer-binary pydantic==2.5.0
pip install --prefer-binary python-multipart==0.0.6
pip install --prefer-binary gunicorn==21.2.0
pip install --prefer-binary httpx==0.25.2

echo "✅ Build completado exitosamente!"

# Verificar instalaciones
echo "🔍 Verificando instalaciones..."
python -c "import sklearn; print(f'✅ scikit-learn {sklearn.__version__} instalado correctamente')"
python -c "import pandas; print(f'✅ pandas {pandas.__version__} instalado correctamente')"
python -c "import numpy; print(f'✅ numpy {numpy.__version__} instalado correctamente')"
