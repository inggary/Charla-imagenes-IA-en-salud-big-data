# guardar_como: servidor_demo.py
#
# Para ejecutar esto, necesitas instalar las librerías:
# pip install tensorflow numpy opencv-python-headless pillow
#
# Y luego (para un servidor local de desarrollo):
# uv run servidor_demo:mcp stdio
#
# (O si quieres conectarlo a Claude/Ollama, la documentación de FastMCP te dice cómo)
#uv run servidor_demo.py --port 8000
import os
import cv2
import numpy as np
import tensorflow as tf
import base64
from io import BytesIO
from PIL import Image
from mcp.server.fastmcp import FastMCP

# --- 1. Cargar tu "Especialista" (El Modelo CNN) ---
# ¡Se carga UNA SOLA VEZ al iniciar el servidor!
print("Cargando modelo CNN 'cnn_model_94.h5' en memoria...")
try:
    # Obtener la ruta absoluta del modelo
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, '..', 'notebooks', 'cnn_model_94.h5')
    model_path = os.path.normpath(model_path)
    
    print(f"Intentando cargar modelo desde: {model_path}")
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"No se encuentra el modelo en: {model_path}")
    
    MODELO_CNN = tf.keras.models.load_model(model_path)
    print("¡Modelo CNN cargado exitosamente!")
except Exception as e:
    print(f"!!! ERROR FATAL: No se pudo cargar 'cnn_model_94.h5'. {e}")
    MODELO_CNN = None

# --- 2. Crear el Servidor "Mesero" ---
mcp = FastMCP("ServidorHibridoDeSalud")
print("Servidor FastMCP 'ServidorHibridoDeSalud' creado.")

# --- 3. Funciones auxiliares para Pre-procesar Imágenes ---
def preprocess_image_for_cnn(image_path: str):
    """Pre-procesa una imagen desde disco para nuestro modelo CNN."""
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"No se pudo leer la imagen: {image_path}")
        
        img = cv2.resize(img, (224, 224))
        img = img.astype('float32') / 255.0
        img = np.expand_dims(img, axis=0) # Crear un batch de 1
        return img
    except Exception as e:
        print(f"Error en preprocess_image_for_cnn: {e}")
        return None

def preprocess_image_from_pil(pil_image):
    """Pre-procesa una imagen PIL para nuestro modelo CNN."""
    try:
        # Convertir PIL a numpy array
        img = np.array(pil_image)
        
        # Si es RGB, OpenCV usa BGR, pero como ya está en RGB de PIL, lo dejamos así
        # Si tiene canal alpha (RGBA), quitarlo
        if img.shape[-1] == 4:
            img = img[:, :, :3]
        
        img = cv2.resize(img, (224, 224))
        img = img.astype('float32') / 255.0
        img = np.expand_dims(img, axis=0) # Crear un batch de 1
        return img
    except Exception as e:
        print(f"Error en preprocess_image_from_pil: {e}")
        return None

# --- 4. Herramienta 1: El Especialista CNN (¡Tu Modelo!) ---
@mcp.tool()
def analizar_retina_cnn(image_path: str) -> dict:
    """
    Analiza una imagen de retina usando el modelo CNN experto para detectar 
    Retinopatía Diabética (DR).
    
    Args:
        image_path: Ruta completa a la imagen (ej: /Users/.../imagen.jpg)
                   Puede ser cualquier imagen accesible en el sistema de archivos.
    
    Returns:
        dict con 'status' ('DR_DETECTADA' o 'NO_DR') y 'confianza' (0.0-1.0)
    """
    global MODELO_CNN
    if MODELO_CNN is None:
        return {"error": "Modelo CNN no está cargado."}
    
    print(f"[Tool: analizar_retina_cnn]: Procesando imagen '{image_path}'...")
    
    try:
        # Verificar que el archivo existe
        if not os.path.exists(image_path):
            return {"error": f"No se encuentra la imagen en: {image_path}"}
        
        # Pre-procesar la imagen
        processed_img = preprocess_image_for_cnn(image_path)
        if processed_img is None:
            return {"error": "No se pudo procesar la imagen."}

        # Realizar la predicción
        prediction = MODELO_CNN.predict(processed_img, verbose=0)
        
        # El modelo binario (clase 0="DR", clase 1="No_DR" según ImageDataGenerator alfabético)
        class_index = np.argmax(prediction[0])
        confidence = float(np.max(prediction[0]))
        
        label = "NO_DR" if class_index == 1 else "DR_DETECTADA"
        
        print(f"[Tool: analizar_retina_cnn]: Resultado: {label} (Conf: {confidence:.2f})")
        
        return {
            "status": label,
            "confianza": confidence,
            "detalles": f"Clase {class_index}: {label} con {confidence*100:.1f}% de confianza"
        }

    except Exception as e:
        print(f"[Tool: analizar_retina_cnn]: Error: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

# --- 5. Herramienta 2: El Sensor de Glucosa (Mock) ---
@mcp.tool()
def obtener_datos_paciente(paciente_id: str) -> dict:
    """
    Obtiene los datos más recientes del sensor de glucosa y smartwatch
    para un ID de paciente específico. (Datos simulados).
    """
    print(f"[Tool: obtener_datos_paciente]: Buscando datos para '{paciente_id}'...")
    # Aquí es donde llamarías a la API del hospital o sensor
    return {
        "glucosa_avg_14d": 185,
        "glucosa_picos": "frecuentes post-comida",
        "smartwatch_pasos_avg": 3200,
        "smartwatch_hr_reposo": 88
    }

# --- 6. El Prompt (La Lógica del Orquestador) ---
@mcp.prompt()
def generar_diagnostico_hibrido(paciente_id: str, image_path: str) -> str:
    """
    Genera un reporte de diagnóstico híbrido completo para un médico,
    combinando los datos del sensor y el análisis de la CNN.
    """
    # 1. Obtenemos los datos del sensor (Herramienta 2)
    datos_sensor = mcp.tools.obtener_datos_paciente(paciente_id=paciente_id)
    
    # 2. Analizamos la retina (Herramienta 1)
    resultado_cnn = mcp.tools.analizar_retina_cnn(image_path=image_path)
    
    # 3. Construimos el prompt final para el "Chef" (Claude/Gemini/Llama)
    prompt_al_chef = f"""
    Eres un Asistente Médico experto en análisis de datos de salud en República Dominicana.
    Tu trabajo es sintetizar múltiples fuentes de datos para darle al doctor un resumen claro y accionable.
    
    Por favor, genera un reporte para el Dr. Pimentel basado en ESTRICTAMENTE la siguiente información:
    
    1. Datos de Sensores del Paciente (ID: {paciente_id}):
       - Glucosa promedio (14 días): {datos_sensor.get('glucosa_avg_14d')} mg/dL
       - Notas de glucosa: {datos_sensor.get('glucosa_picos')}
       - Pasos diarios (promedio): {datos_sensor.get('smartwatch_pasos_avg')}
       - Ritmo cardíaco en reposo: {datos_sensor.get('smartwatch_hr_reposo')} lpm
    
    2. Análisis de Retina (realizado por CNN especialista local):
       - Imagen: {image_path}
       - Resultado: {resultado_cnn.get('status', 'Error')}
       - Confianza del modelo: {resultado_cnn.get('confianza', 0):.2f}
    
    Tarea:
    Sintetiza TODOS estos puntos de datos en un reporte accionable.
    Inicia con 'Reporte Híbrido del Paciente:'
    Finaliza con 'Sugerencias de Próximos Pasos:'.
    """
    
    print(f"\n[Prompt: enviando al 'Chef' (LLM)]:\n{prompt_al_chef}\n")
    
    # Esta variable 'prompt_al_chef' es lo que FastMCP le envía al LLM
    return prompt_al_chef


def main():
    # Initialize and run the server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
