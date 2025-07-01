import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Establecer semilla para reproducibilidad
np.random.seed(42)
random.seed(42)

def generate_training_data(n_samples=1000):
    """
    Genera datos sintéticos de entrenamiento basados en el modelo Volunteer.js
    """
    data = []
    
    for i in range(n_samples):
        # Crear diferentes tipos de voluntarios
        volunteer_type = np.random.choice(['excellent', 'good', 'average', 'poor'], 
                                         p=[0.2, 0.3, 0.3, 0.2])
        
        if volunteer_type == 'excellent':
            reliability = np.random.normal(8.5, 1.0)
            punctuality = np.random.normal(8.5, 1.0)
            task_quality = np.random.normal(8.5, 1.0)
            total_projects = np.random.poisson(15) + 5
            success_rate_base = 0.9
        elif volunteer_type == 'good':
            reliability = np.random.normal(7.0, 1.2)
            punctuality = np.random.normal(7.2, 1.2)
            task_quality = np.random.normal(7.0, 1.2)
            total_projects = np.random.poisson(8) + 2
            success_rate_base = 0.8
        elif volunteer_type == 'average':
            reliability = np.random.normal(5.5, 1.5)
            punctuality = np.random.normal(6.0, 1.5)
            task_quality = np.random.normal(5.8, 1.5)
            total_projects = np.random.poisson(5)
            success_rate_base = 0.6
        else:  # poor
            reliability = np.random.normal(3.5, 1.8)
            punctuality = np.random.normal(4.0, 1.8)
            task_quality = np.random.normal(4.0, 1.8)
            total_projects = np.random.poisson(2)
            success_rate_base = 0.3
        
        # Limitar valores a rangos válidos
        reliability = max(0, min(10, reliability))
        punctuality = max(0, min(10, punctuality))
        task_quality = max(0, min(10, task_quality))
        
        # Experiencia
        completed_projects = int(total_projects * np.random.uniform(success_rate_base-0.2, success_rate_base+0.1))
        completed_projects = max(0, min(completed_projects, total_projects))
        total_hours = np.random.exponential(50) + (total_projects * 8)
        
        # Disponibilidad varía según tipo
        if volunteer_type in ['excellent', 'good']:
            availability_hours = np.random.uniform(15, 40)
        else:
            availability_hours = np.random.uniform(5, 25)
        
        # Calcular success_rate real
        if total_projects > 0:
            success_rate = completed_projects / total_projects
        else:
            success_rate = 0
            
        # Datos del proyecto (simulados)
        project_duration = np.random.uniform(1, 12)  # semanas
        project_complexity = np.random.uniform(1, 10)  # 1-10
        required_hours = np.random.uniform(10, 60)  # horas requeridas        # Calcular si es adecuado (variable objetivo)
        # Lógica mejorada: voluntario es adecuado si tiene buenas métricas Y disponibilidad
        score = (
            reliability * 0.3 + 
            punctuality * 0.2 + 
            task_quality * 0.3 + 
            success_rate * 100 * 0.2
        )
        
        # Ajustar por disponibilidad
        availability_ratio = min(availability_hours / required_hours, 2)
        if availability_ratio >= 0.8:
            score += 1
        elif availability_ratio >= 0.5:
            score += 0.5
        
        # Ajustar por experiencia
        if total_projects >= 5:
            score += 0.8
        if total_hours >= 80:
            score += 0.5
            
        # Determinar si es adecuado basado en tipo y score
        if volunteer_type == 'excellent':
            is_suitable = 1 if score >= 6.5 else 0
        elif volunteer_type == 'good':
            is_suitable = 1 if score >= 7.0 else 0
        elif volunteer_type == 'average':
            is_suitable = 1 if score >= 7.5 else 0
        else:  # poor
            is_suitable = 1 if score >= 8.5 else 0  # Muy difícil para voluntarios pobres
        
        data.append({
            'reliability': round(reliability, 2),
            'punctuality': round(punctuality, 2),
            'task_quality': round(task_quality, 2),
            'success_rate': round(success_rate, 3),
            'total_projects': total_projects,
            'completed_projects': completed_projects,
            'total_hours': round(total_hours, 1),
            'availability_hours': round(availability_hours, 1),
            'project_duration': round(project_duration, 1),
            'project_complexity': round(project_complexity, 1),
            'required_hours': round(required_hours, 1),
            'is_suitable': is_suitable
        })
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    # Generar datos de entrenamiento
    df = generate_training_data(1000)
    
    # Guardar datos
    df.to_csv('data/training_data.csv', index=False)
    
    print("Datos de entrenamiento generados:")
    print(f"Total de muestras: {len(df)}")
    print(f"Distribución de clases:")
    print(df['is_suitable'].value_counts())
    print(f"\nPrimeras 5 filas:")
    print(df.head())
    
    # Estadísticas básicas
    print(f"\nEstadísticas:")
    print(df.describe())
