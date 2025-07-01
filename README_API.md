# 🤖 Volunteer ML API

## ✅ Estado Actual: FUNCIONANDO

La API está desplegada y funcionando correctamente con un sistema de modelos ML robusto que se adapta automáticamente al entorno disponible.

## 🎯 Características

- **Sistema de 3 niveles de modelos**:
  1. **Modelo completo**: Con scikit-learn (si disponible)
  2. **Modelo fallback**: Con numpy (si scikit-learn no está disponible)
  3. **Modelo simple**: Solo Python estándar (funciona en cualquier entorno)

- **API robusta**: Siempre funciona independientemente de las dependencias disponibles
- **Predicciones inteligentes**: Evalúa la idoneidad de voluntarios para proyectos
- **Fácil de usar**: Endpoints RESTful bien documentados

## 🚀 Endpoints Disponibles

### Endpoints Principales
- `GET /` - Información general de la API
- `GET /health` - Estado de salud de la API
- `GET /model/info` - Información del modelo actual
- `GET /test` - Predicción de prueba con datos de ejemplo

### Endpoints Funcionales
- `POST /predict` - Predicción individual
- `POST /predict/batch` - Predicciones en lote
- `POST /retrain` - Re-entrenar modelo (si está disponible)

## 📊 Uso de la API

### Predicción Individual

```bash
curl -X POST "https://tu-app.onrender.com/predict" \
-H "Content-Type: application/json" \
-d '{
  "volunteer": {
    "reliability": 0.8,
    "punctuality": 0.9,
    "task_quality": 0.7,
    "success_rate": 0.8,
    "total_projects": 5,
    "completed_projects": 4,
    "total_hours": 200,
    "availability_hours": 40
  },
  "project": {
    "project_duration": 8,
    "project_complexity": 6,
    "required_hours": 30
  }
}'
```

### Respuesta Ejemplo

```json
{
  "is_suitable": true,
  "confidence": 0.85,
  "probability_suitable": 0.78,
  "message": "Voluntario altamente recomendado para este proyecto"
}
```

## 🔧 Configuración de Desarrollo

### Requisitos Mínimos
- Python 3.8+
- FastAPI
- Uvicorn

### Instalación Local

```bash
# Clonar repositorio
git clone <tu-repo>
cd ml-service

# Instalar dependencias básicas
pip install -r requirements.txt

# Ejecutar API
python main.py
```

### Instalación Completa (con ML)

```bash
# Instalar dependencias ML opcionales
pip install numpy pandas scikit-learn

# La API detectará automáticamente y usará el modelo completo
python main.py
```

## 🌐 Despliegue en Render

### Configuración Actual
- **Runtime**: Python 3.11+ (automático)
- **Build**: Instalación automática de dependencias mínimas
- **Fallback**: Modelo simple si las dependencias ML fallan
- **Puerto**: Configurado automáticamente para Render

### Variables de Entorno
La aplicación detecta automáticamente:
- `PORT` - Puerto del servidor (Render lo configura automáticamente)
- Dependencias ML disponibles
- Tipo de modelo a usar

## 📋 Estructura del Proyecto

```
ml-service/
├── main.py                 # API principal con FastAPI
├── ml_model.py            # Modelo completo (requiere sklearn)
├── ml_model_fallback.py   # Modelo fallback (requiere numpy)
├── ml_model_simple.py     # Modelo simple (solo Python)
├── requirements.txt       # Dependencias mínimas
├── render.yaml           # Configuración de Render
├── runtime.txt           # Versión de Python preferida
├── test_api.py           # Script de pruebas
└── models/               # Modelos entrenados (opcional)
```

## 🎯 Funcionamiento del Sistema

### Cascada de Modelos
1. **Intenta cargar**: `ml_model.py` (modelo completo con scikit-learn)
2. **Si falla, intenta**: `ml_model_fallback.py` (modelo con numpy)
3. **Si falla, usa**: `ml_model_simple.py` (modelo basado en reglas)

### Lógica de Predicción
- **Modelo completo**: RandomForestClassifier entrenado
- **Modelo fallback**: Algoritmo con numpy y reglas complejas
- **Modelo simple**: Sistema de reglas de negocio puras

## 🧪 Pruebas

### Prueba Automática
```bash
python test_api.py
```

### Prueba Manual
1. Visita: `https://tu-app.onrender.com/test`
2. Verifica: `https://tu-app.onrender.com/health`
3. Explora: `https://tu-app.onrender.com/docs` (Swagger UI)

## 📈 Métricas de Calidad

### Modelo Simple (Reglas de Negocio)
- **Factores evaluados**: 
  - Performance del voluntario (40%)
  - Experiencia y historial (25%)
  - Disponibilidad vs requisitos (25%)
  - Complejidad del proyecto (10%)

### Algoritmo de Decisión
```
Score Final = (Performance × 0.4) + (Experiencia × 0.25) + 
              (Disponibilidad × 0.25) + (Factor Complejidad × 0.1)

Apto si: Score Final ≥ 0.6
```

## 🛠️ Solución de Problemas

### La API no inicia
- Verificar que el puerto esté disponible
- Revisar logs en Render dashboard
- Probar localmente con `python main.py`

### Predicciones incorrectas
- Verificar formato de datos de entrada
- Usar endpoint `/test` para validar funcionamiento
- Revisar documentación en `/docs`

### Dependencias ML no disponibles
- ✅ **Es normal**: La API funciona sin dependencias ML
- El modelo simple proporciona predicciones válidas
- Revisar en `/model/info` qué modelo está activo

## 🎉 Estado de Despliegue

- ✅ **Build**: Exitoso
- ✅ **Deploy**: Funcionando
- ✅ **API**: Respondiendo
- ✅ **Modelo**: Cargado (tipo: automático)
- ✅ **Endpoints**: Todos operativos

---

## 📞 Soporte

La API está completamente funcional y preparada para producción. El sistema de fallbacks garantiza que siempre estará disponible, independientemente del entorno de despliegue.

**Última actualización**: Enero 2025  
**Estado**: ✅ PRODUCCIÓN - FUNCIONANDO
