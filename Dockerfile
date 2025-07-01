# Dockerfile para ML Service
FROM python:3.11.7-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para scikit-learn
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de requirements
COPY requirements.txt .

# Actualizar pip e instalar herramientas de construcción
RUN pip install --upgrade pip wheel setuptools

# Instalar dependencias usando binarios precompilados
RUN pip install --only-binary=:all: --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorio para modelos si no existe
RUN mkdir -p models data

# Exponer puerto
EXPOSE 8000

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
