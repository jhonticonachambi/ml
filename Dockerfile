# Dockerfile para ML Service - Ultra conservador
FROM python:3.11.4-slim

# Establecer directorio de trabajo
WORKDIR /app

# Variables de entorno ultra-estrictas
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_PREFER_BINARY=1
ENV PIP_ONLY_BINARY=":all:"
ENV PIP_NO_BUILD_ISOLATION=1
ENV PIP_NO_COMPILE=1
ENV NUMPY_NO_BUILD=1
ENV SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=False

# NO instalar herramientas de compilación para forzar uso de binarios
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar configuraciones
COPY pip.conf /etc/pip.conf
COPY requirements-minimal.txt .

# Instalar pip estable
RUN python -m pip install --upgrade pip==23.2.1

# Instalación ultra-conservadora paso a paso
RUN pip install --only-binary=:all: --prefer-binary wheel==0.41.2 setuptools==68.2.2 && \
    pip install --only-binary=:all: --prefer-binary numpy==1.24.3 && \
    pip install --only-binary=:all: --prefer-binary scipy==1.10.1 && \
    pip install --only-binary=:all: --prefer-binary joblib==1.2.0 && \
    pip install --only-binary=:all: --prefer-binary scikit-learn==1.2.2 && \
    pip install --only-binary=:all: --prefer-binary fastapi==0.104.1 && \
    pip install --only-binary=:all: --prefer-binary uvicorn==0.24.0 && \
    pip install --only-binary=:all: --prefer-binary pydantic==2.5.0

# Verificar instalaciones críticas
RUN python -c "import sklearn; print(f'✅ scikit-learn {sklearn.__version__}')" && \
    python -c "import fastapi; print('✅ FastAPI OK')"

# Copiar código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p models data

# Exponer puerto
EXPOSE 8000

# Comando optimizado
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
