from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from contextlib import asynccontextmanager
import uvicorn
import os

# Cascada de imports: intentar modelo completo -> fallback -> simple
try:
    from ml_model import VolunteerMLModel
    print("✅ Usando modelo ML completo con scikit-learn")
    MODEL_TYPE = "full"
except ImportError as e:
    print(f"⚠️ Error importando modelo ML completo: {e}")
    try:
        from ml_model_fallback import VolunteerMLModel
        print("✅ Usando modelo ML fallback con numpy")
        MODEL_TYPE = "fallback"
    except ImportError as e2:
        print(f"⚠️ Error importando modelo fallback: {e2}")
        try:
            from ml_model_simple import VolunteerMLModel
            print("✅ Usando modelo simple basado en reglas (sin dependencias ML)")
            MODEL_TYPE = "simple"
        except ImportError as e3:
            print(f"❌ Error crítico: No se pudo cargar ningún modelo: {e3}")
            raise Exception("No hay modelo ML disponible")

# Cargar modelo al iniciar la aplicación
model = VolunteerMLModel()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manejo del ciclo de vida de la aplicación"""
    # Startup
    if os.path.exists('models/volunteer_model.pkl'):
        success = model.load_model()
        if success:
            print("✅ Modelo cargado exitosamente")
        else:
            print("❌ Error al cargar el modelo")
    else:
        print("⚠️ No se encontró modelo entrenado. Entrena el modelo primero.")
    
    yield
    
    # Shutdown
    print("🔄 Cerrando aplicación...")

app = FastAPI(
    title="Volunteer ML API",
    description="API para predecir la idoneidad de voluntarios para proyectos",
    version="1.0.0",
    lifespan=lifespan
)

# Modelos Pydantic para validación de datos
class VolunteerData(BaseModel):
    reliability: float
    punctuality: float
    task_quality: float
    success_rate: float
    total_projects: int
    completed_projects: int
    total_hours: float
    availability_hours: float

class ProjectData(BaseModel):
    project_duration: float  # en semanas
    project_complexity: float  # 1-10
    required_hours: float  # horas requeridas

class PredictionRequest(BaseModel):
    volunteer: VolunteerData
    project: ProjectData

class PredictionResponse(BaseModel):
    is_suitable: bool
    confidence: float
    probability_suitable: float
    message: str

class RetrainRequest(BaseModel):
    data_path: Optional[str] = "data/training_data.csv"

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "Volunteer ML API",
        "status": "active",
        "model_loaded": model.is_trained,
        "model_type": MODEL_TYPE,
        "note": "API funcionando con modelo disponible"
    }

@app.get("/health")
async def health_check():
    """Verificar estado de la API"""
    return {
        "status": "healthy",
        "model_status": "loaded" if model.is_trained else "not_loaded",
        "model_type": MODEL_TYPE,
        "api_version": "1.0.0",
        "ready": True
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict_volunteer_suitability(request: PredictionRequest):
    """
    Predice si un voluntario es adecuado para un proyecto específico
    """
    if not model.is_trained:
        raise HTTPException(
            status_code=503, 
            detail="Modelo no está entrenado. Contacta al administrador."
        )
    
    try:
        # Convertir datos Pydantic a diccionarios
        volunteer_data = request.volunteer.model_dump()
        project_data = request.project.model_dump()
        
        # Hacer predicción
        result = model.predict(volunteer_data, project_data)
        
        # Generar mensaje descriptivo
        if result['is_suitable']:
            if result['confidence'] > 0.8:
                message = "Voluntario altamente recomendado para este proyecto"
            else:
                message = "Voluntario recomendado para este proyecto"
        else:
            if result['confidence'] > 0.8:
                message = "Voluntario no recomendado para este proyecto"
            else:
                message = "Voluntario posiblemente no adecuado para este proyecto"
        
        return PredictionResponse(
            is_suitable=result['is_suitable'],
            confidence=result['confidence'],
            probability_suitable=result['probability_suitable'],
            message=message
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la predicción: {str(e)}")

@app.post("/retrain")
async def retrain_model(request: RetrainRequest):
    """
    Re-entrena el modelo con nuevos datos
    """
    try:
        if not os.path.exists(request.data_path):
            raise HTTPException(
                status_code=404, 
                detail=f"Archivo de datos no encontrado: {request.data_path}"
            )
        
        # Re-entrenar modelo
        accuracy = model.train(request.data_path)
        
        # Guardar modelo actualizado
        model.save_model()
        
        return {
            "message": "Modelo re-entrenado exitosamente",
            "accuracy": accuracy,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al re-entrenar: {str(e)}")

@app.get("/model/info")
async def get_model_info():
    """
    Obtiene información sobre el modelo actual
    """
    if not model.is_trained:
        return {"status": "not_trained", "message": "Modelo no entrenado"}
    
    return {
        "status": "trained",
        "model_type": MODEL_TYPE,
        "implementation": getattr(model, 'model_type', 'RandomForestClassifier'),
        "feature_names": model.feature_names,
        "is_trained": model.is_trained,
        "note": {
            "full": "Modelo completo con scikit-learn",
            "fallback": "Modelo con numpy (sin scikit-learn)",
            "simple": "Modelo basado en reglas (sin dependencias ML)"
        }.get(MODEL_TYPE, "Tipo desconocido")
    }

@app.post("/predict/batch")
async def predict_batch(requests: list[PredictionRequest]):
    """
    Realizar múltiples predicciones en lote
    """
    if not model.is_trained:
        raise HTTPException(
            status_code=503, 
            detail="Modelo no está entrenado"
        )
    
    results = []
    for req in requests:
        try:
            volunteer_data = req.volunteer.model_dump()
            project_data = req.project.model_dump()
            result = model.predict(volunteer_data, project_data)
            results.append(result)
        except Exception as e:
            results.append({"error": str(e)})
    
    return {"predictions": results}

@app.get("/test")
async def test_prediction():
    """
    Endpoint de prueba con datos de ejemplo
    """
    try:
        # Datos de prueba
        sample_volunteer = {
            "reliability": 0.8,
            "punctuality": 0.9,
            "task_quality": 0.7,
            "success_rate": 0.8,
            "total_projects": 5,
            "completed_projects": 4,
            "total_hours": 200,
            "availability_hours": 40
        }
        
        sample_project = {
            "project_duration": 8,
            "project_complexity": 6,
            "required_hours": 30
        }
        
        # Hacer predicción de prueba
        result = model.predict(sample_volunteer, sample_project)
        
        return {
            "status": "success",
            "test_data": {
                "volunteer": sample_volunteer,
                "project": sample_project
            },
            "prediction": result,
            "model_type": MODEL_TYPE,
            "message": "Predicción de prueba exitosa"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "model_type": MODEL_TYPE,
            "message": "Error en predicción de prueba"
        }

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True,
        log_level="info"
    )
