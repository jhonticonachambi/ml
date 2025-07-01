#!/usr/bin/env python3
"""
Script de prueba para verificar que la API funciona correctamente
"""
import requests
import json

def test_api(base_url="http://localhost:8000"):
    """Prueba todos los endpoints de la API"""
    print(f"🧪 Probando API en: {base_url}")
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ /health: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ /health falló: {e}")
    
    # Test 2: Root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ /: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ / falló: {e}")
    
    # Test 3: Model info
    try:
        response = requests.get(f"{base_url}/model/info")
        print(f"✅ /model/info: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ /model/info falló: {e}")
    
    # Test 4: Test prediction
    try:
        response = requests.get(f"{base_url}/test")
        print(f"✅ /test: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ /test falló: {e}")
    
    # Test 5: Manual prediction
    try:
        prediction_data = {
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
        }
        
        response = requests.post(
            f"{base_url}/predict", 
            json=prediction_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ /predict: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ /predict falló: {e}")

if __name__ == "__main__":
    # Prueba local
    print("🔧 Probando API localmente...")
    test_api("http://localhost:8000")
    
    print("\n" + "="*50)
    print("📝 Para probar en Render, cambia la URL por la de tu deploy")
    print("Ejemplo: test_api('https://tu-app.onrender.com')")
