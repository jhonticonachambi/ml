import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import joblib
import os

class VolunteerMLModel:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.feature_names = [
            'reliability', 'punctuality', 'task_quality', 'success_rate',
            'total_projects', 'completed_projects', 'total_hours',
            'availability_hours', 'project_duration', 'project_complexity',
            'required_hours'
        ]
        self.is_trained = False
        
    def prepare_features(self, data):
        """
        Prepara las características para el modelo
        """
        if isinstance(data, dict):
            # Convertir dict a DataFrame
            df = pd.DataFrame([data])
        else:
            df = data.copy()
            
        # Asegurar que todas las características necesarias están presentes
        for feature in self.feature_names:
            if feature not in df.columns:
                df[feature] = 0
                
        # Crear características derivadas
        df['experience_score'] = (df['total_projects'] * 0.3 + df['total_hours'] * 0.002)
        df['performance_avg'] = (df['reliability'] + df['punctuality'] + df['task_quality']) / 3
        df['availability_ratio'] = np.minimum(df['availability_hours'] / df['required_hours'], 2)
        df['completion_rate'] = df['completed_projects'] / np.maximum(df['total_projects'], 1)
        
        # Actualizar lista de características
        feature_list = self.feature_names + ['experience_score', 'performance_avg', 'availability_ratio', 'completion_rate']
        
        return df[feature_list]
    
    def train(self, data_path='data/training_data.csv'):
        """
        Entrena el modelo con los datos
        """
        # Cargar datos
        df = pd.read_csv(data_path)
        
        # Preparar características
        X = self.prepare_features(df)
        y = df['is_suitable']
        
        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Escalar características
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Entrenar modelo
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluar
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Accuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Importancia de características
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nFeature Importance:")
        print(feature_importance)
        
        self.is_trained = True
        return accuracy
    
    def predict(self, volunteer_data, project_data):
        """
        Predice si un voluntario es adecuado para un proyecto
        """
        if not self.is_trained:
            raise ValueError("El modelo no ha sido entrenado. Llama a train() primero.")
        
        # Combinar datos del voluntario y proyecto
        combined_data = {
            **volunteer_data,
            **project_data
        }
        
        # Preparar características
        X = self.prepare_features(combined_data)
        X_scaled = self.scaler.transform(X)
        
        # Hacer predicción
        prediction = self.model.predict(X_scaled)[0]
        probability = self.model.predict_proba(X_scaled)[0]
        
        return {
            'is_suitable': bool(prediction),
            'confidence': float(max(probability)),
            'probability_suitable': float(probability[1]) if len(probability) > 1 else float(probability[0])
        }
    
    def save_model(self, model_dir='models'):
        """
        Guarda el modelo entrenado
        """
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
            
        joblib.dump(self.model, f'{model_dir}/volunteer_model.pkl')
        joblib.dump(self.scaler, f'{model_dir}/scaler.pkl')
        
        # Guardar metadatos
        metadata = {
            'feature_names': self.feature_names,
            'is_trained': self.is_trained
        }
        joblib.dump(metadata, f'{model_dir}/metadata.pkl')
        
        print(f"Modelo guardado en {model_dir}/")
    
    def load_model(self, model_dir='models'):
        """
        Carga un modelo previamente entrenado
        """
        try:
            self.model = joblib.load(f'{model_dir}/volunteer_model.pkl')
            self.scaler = joblib.load(f'{model_dir}/scaler.pkl')
            metadata = joblib.load(f'{model_dir}/metadata.pkl')
            
            self.feature_names = metadata['feature_names']
            self.is_trained = metadata['is_trained']
            
            print("Modelo cargado exitosamente")
            return True
        except Exception as e:
            print(f"Error al cargar el modelo: {e}")
            return False

if __name__ == "__main__":
    # Crear y entrenar modelo
    model = VolunteerMLModel()
    
    # Verificar si existen datos de entrenamiento
    if os.path.exists('data/training_data.csv'):
        print("Entrenando modelo...")
        accuracy = model.train()
        
        # Guardar modelo
        model.save_model()
        
        # Ejemplo de predicción
        volunteer_example = {
            'reliability': 8.5,
            'punctuality': 9.0,
            'task_quality': 8.0,
            'success_rate': 0.9,
            'total_projects': 12,
            'completed_projects': 11,
            'total_hours': 150.5,
            'availability_hours': 25.0
        }
        
        project_example = {
            'project_duration': 6.0,
            'project_complexity': 7.0,
            'required_hours': 20.0
        }
        
        result = model.predict(volunteer_example, project_example)
        print(f"\nEjemplo de predicción:")
        print(f"¿Es adecuado? {result['is_suitable']}")
        print(f"Confianza: {result['confidence']:.4f}")
        print(f"Probabilidad de ser adecuado: {result['probability_suitable']:.4f}")
        
    else:
        print("No se encontraron datos de entrenamiento. Ejecuta generate_data.py primero.")
