# Dockerfile para ML Service
FROM python:3.11.6-slim

# Establecer directorio de trabajo
WORKDIR /app

# Variables de entorno para evitar compilación
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_PREFER_BINARY=1
ENV PIP_ONLY_BINARY=":all:"
ENV SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=False

# Instalar dependencias del sistema solo si es necesario
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de requirements
COPY requirements.txt .
COPY pip.conf /etc/pip.conf

# Instalar dependencias usando estrategia escalonada
RUN python -m pip install --upgrade pip wheel setuptools && \
    pip install --prefer-binary --only-binary=:all: numpy==1.24.4 && \
    pip install --prefer-binary --only-binary=:all: joblib==1.2.0 && \
    pip install --prefer-binary --only-binary=:all: pandas==2.0.3 && \
    pip install --prefer-binary --only-binary=:all: scikit-learn==1.2.2 && \
    pip install --prefer-binary --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorio para modelos si no existe
RUN mkdir -p models data

# Exponer puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
