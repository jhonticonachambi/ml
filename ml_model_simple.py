import os
import json
import math

class VolunteerMLModel:
    """
    Modelo ML ultra-simple que funciona SIN dependencias externas
    Solo usa la librería estándar de Python
    """
    def __init__(self):
        self.feature_names = [
            'reliability', 'punctuality', 'task_quality', 'success_rate',
            'total_projects', 'completed_projects', 'total_hours',
            'availability_hours', 'project_duration', 'project_complexity',
            'required_hours'
        ]
        self.is_trained = True  # Siempre "entrenado" porque usa reglas fijas
        self.model_type = "RuleBasedClassifier"
        
    def _safe_divide(self, a, b, default=0):
        """División segura que evita división por cero"""
        try:
            return a / b if b != 0 else default
        except:
            return default
    
    def _clamp(self, value, min_val=0, max_val=1):
        """Limita un valor entre min_val y max_val"""
        return max(min_val, min(max_val, value))
    
    def predict(self, volunteer_data, project_data):
        """
        Predicción basada en reglas de negocio simples
        """
        try:
            # Extraer datos del voluntario
            reliability = volunteer_data.get('reliability', 0.5)
            punctuality = volunteer_data.get('punctuality', 0.5)
            task_quality = volunteer_data.get('task_quality', 0.5)
            success_rate = volunteer_data.get('success_rate', 0.5)
            total_projects = volunteer_data.get('total_projects', 0)
            completed_projects = volunteer_data.get('completed_projects', 0)
            total_hours = volunteer_data.get('total_hours', 0)
            availability_hours = volunteer_data.get('availability_hours', 0)
            
            # Extraer datos del proyecto
            project_duration = project_data.get('project_duration', 1)
            project_complexity = project_data.get('project_complexity', 5)
            required_hours = project_data.get('required_hours', 1)
            
            # REGLA 1: Score de performance (40% del peso)
            performance_score = (reliability + punctuality + task_quality + success_rate) / 4
            performance_weight = 0.4
            
            # REGLA 2: Score de experiencia (25% del peso)
            completion_rate = self._safe_divide(completed_projects, total_projects, 0.5)
            experience_factor = min(total_projects / 10, 1.0)  # Máximo a los 10 proyectos
            hours_factor = min(total_hours / 1000, 1.0)  # Máximo a las 1000 horas
            experience_score = (completion_rate * 0.6 + experience_factor * 0.2 + hours_factor * 0.2)
            experience_weight = 0.25
            
            # REGLA 3: Score de disponibilidad (25% del peso)
            availability_ratio = self._safe_divide(availability_hours, required_hours, 0)
            availability_score = min(availability_ratio, 1.0)  # Máximo 1.0
            availability_weight = 0.25
            
            # REGLA 4: Factor de complejidad del proyecto (10% del peso)
            # Proyectos más simples son más fáciles de completar
            complexity_factor = (10 - project_complexity) / 10  # Invertir escala
            complexity_weight = 0.1
            
            # CÁLCULO FINAL
            final_score = (
                performance_score * performance_weight +
                experience_score * experience_weight +
                availability_score * availability_weight +
                complexity_factor * complexity_weight
            )
            
            # Ajustar por duración del proyecto
            if project_duration > 12:  # Proyectos largos requieren más compromiso
                final_score *= 0.9
            elif project_duration < 4:  # Proyectos cortos son más flexibles
                final_score *= 1.1
                
            # Limitar score entre 0 y 1
            final_score = self._clamp(final_score, 0, 1)
            
            # DECISIÓN
            threshold = 0.6
            is_suitable = final_score >= threshold
            
            # CONFIANZA: qué tan lejos está del threshold
            confidence = abs(final_score - threshold) * 2
            confidence = self._clamp(confidence, 0.5, 1.0)  # Mínimo 50% de confianza
            
            return {
                'is_suitable': is_suitable,
                'confidence': float(confidence),
                'probability_suitable': float(final_score)
            }
            
        except Exception as e:
            # Fallback ultra-conservador
            print(f"Error en predicción: {e}")
            return {
                'is_suitable': True,
                'confidence': 0.5,
                'probability_suitable': 0.6
            }
    
    def train(self, data_path=None):
        """
        Simulación de entrenamiento (no hace nada real)
        """
        print("✅ Modelo basado en reglas 'entrenado' (sin ML real)")
        self.is_trained = True
        return 0.75  # Accuracy simulada
    
    def save_model(self, path='models/'):
        """
        Guarda metadatos del modelo
        """
        try:
            os.makedirs(path, exist_ok=True)
            
            metadata = {
                'model_type': self.model_type,
                'feature_names': self.feature_names,
                'is_trained': self.is_trained,
                'note': 'Modelo basado en reglas, no requiere entrenamiento ML'
            }
            
            with open(f'{path}metadata.json', 'w') as f:
                json.dump(metadata, f, indent=2)
                
            print("✅ Metadatos del modelo guardados")
            return True
            
        except Exception as e:
            print(f"Error al guardar: {e}")
            return False
    
    def load_model(self, path='models/'):
        """
        Carga metadatos del modelo
        """
        try:
            metadata_path = f'{path}metadata.json'
            
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                    self.feature_names = metadata.get('feature_names', self.feature_names)
                print("✅ Metadatos del modelo cargados")
            else:
                print("⚠️ No se encontraron metadatos, usando configuración por defecto")
            
            self.is_trained = True
            return True
            
        except Exception as e:
            print(f"Error al cargar: {e}")
            self.is_trained = True  # Aún así funciona
            return True
