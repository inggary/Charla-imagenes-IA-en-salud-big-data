# guardar_como: orchestrator_claude.py
import os
import requests
import anthropic  # <-- ¡La librería de Claude!
import base64
import mimetypes
from dotenv import load_dotenv
from PIL import Image

# --- 1. Cargar Configuración ---
load_dotenv()
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
if not CLAUDE_API_KEY:
    raise ValueError("No se encontró la CLAUDE_API_KEY en el archivo .env")

# Inicializar el cliente de Claude
client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

# --- 2. Definir la URL de tu Especialista Local ---
# Esta debe ser la dirección donde corre 'app.py'
CNN_SERVER_URL = "http://127.0.0.1:5000/predict_retina"

# --- 3. Datos Mock (Simulados) y Archivos ---
IMAGE_FILE_PATH = "test_image.jpg" # Sube una imagen de prueba
if not os.path.exists(IMAGE_FILE_PATH):
    raise FileNotFoundError(f"No se encontró {IMAGE_FILE_PATH}. Sube una imagen de prueba.")

mock_sensor_data = {
    "glucosa_avg_14d": 185, # mg/dL
    "glucosa_picos": "frecuentes post-comida",
    "smartwatch_pasos_avg": 3200,
    "smartwatch_hr_reposo": 88 # lpm
}

# --- 4. Definición de la "Herramienta" (La Magia de Claude) ---
# Aquí le decimos a Claude que TIENE una herramienta llamada 'analizar_retina_cnn'
tools = [
    {
        "name": "analizar_retina_cnn",
        "description": "Ejecuta un análisis de una imagen de retina usando un modelo CNN experto local para detectar Retinopatía Diabética (DR).",
        "input_schema": {
            "type": "object",
            "properties": {
                "motivo": {
                    "type": "string",
                    "description": "El motivo por el cual se solicita el análisis. Ej: 'Analizar imagen del paciente'."
                }
            },
            "required": ["motivo"]
        }
    }
]

# --- 5. Función para llamar a tu CNN local ---
def llamar_al_especialista_cnn(image_path):
    print(f"    > [Orquestador]: Llamando al especialista local en {CNN_SERVER_URL}...")
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (image_path, f, mimetypes.guess_type(image_path)[0])}
            response = requests.post(CNN_SERVER_URL, files=files)
            
            if response.status_code == 200:
                cnn_result = response.json()
                print(f"    > [Especialista CNN]: Respuesta recibida: {cnn_result}")
                # Formateamos la respuesta para Claude
                return cnn_result
            else:
                print(f"    > [Especialista CNN]: Error: {response.text}")
                return {"error": response.text}
    except requests.exceptions.ConnectionError:
        print("\n" + "="*50)
        print("❌ ERROR DE CONEXIÓN: ¿Estás seguro de que 'app.py' se está ejecutando?")
        print("Abre una NUEVA terminal y ejecuta: python app.py")
        print("="*50 + "\n")
        return {"error": "Servidor CNN no disponible"}
    except Exception as e:
        print(f"    > [Orquestador]: Error inesperado: {e}")
        return {"error": str(e)}

# --- 6. Función para convertir la imagen a Base64 (Claude lo prefiere así) ---
def get_image_as_base64(image_path):
    with open(image_path, "rb") as image_file:
        binary_data = image_file.read()
        base64_data = base64.b64encode(binary_data).decode('utf-8')
        media_type = mimetypes.guess_type(image_path)[0]
    return base64_data, media_type

# --- 7. El CEREBRO DE LA DEMO ---
def ejecutar_demo_hibrida():
    print("--- 🧠 Iniciando Demo: Orquestador Híbrido (Claude) ---")

    # --- Preparamos el mensaje para Claude (Multimodal) ---
    print(f"[Paso 1]: Cargando imagen '{IMAGE_FILE_PATH}' y datos del paciente.")
    img_base64, img_media_type = get_image_as_base64(IMAGE_FILE_PATH)
    
    # El prompt del usuario con la imagen y los datos de texto
    user_message_content = [
        {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": img_media_type,
                "data": img_base64,
            },
        },
        {
            "type": "text",
            "text": f"""
            Aquí están los datos de mi paciente:
            - Imagen de retina (adjunta).
            - Glucosa promedio (14 días): {mock_sensor_data['glucosa_avg_14d']} mg/dL
            - Notas de glucosa: {mock_sensor_data['glucosa_picos']}
            - Pasos diarios (promedio): {mock_sensor_data['smartwatch_pasos_avg']}
            - Ritmo cardíaco en reposo: {mock_sensor_data['smartwatch_hr_reposo']} lpm
            
            Por favor, analiza esta información. Primero, usa tu herramienta 'analizar_retina_cnn'
            para obtener el diagnóstico de mi especialista local sobre la imagen. 
            Luego, dame un resumen completo y sugerencias.
            """
        }
    ]

    # --- LLAMADA 1: El Orquestador recibe la petición ---
    print("[Paso 2]: Enviando datos a Claude (Orquestador)...")
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620", # El modelo más nuevo
        max_tokens=2048,
        system="Eres un Asistente Médico experto en análisis de datos de salud en República Dominicana. Tienes acceso a herramientas locales. Tu trabajo es sintetizar múltiples fuentes de datos para darle al doctor un resumen claro y accionable.",
        tools=tools, # <-- Le decimos las herramientas que tiene
        messages=[{"role": "user", "content": user_message_content}]
    )

    print("[Paso 3]: Claude está pensando... ¿Necesitará una herramienta?")

    # --- Claude responde... ¿Pide usar la herramienta? ---
    if message.stop_reason == "tool_use":
        print("    > [Claude]: ¡Sí! Necesito usar una herramienta.")
        
        tool_call = next(block for block in message.content if block.type == "tool_use")
        
        # --- El Orquestador llama al Especialista (Tu CNN) ---
        if tool_call.name == "analizar_retina_cnn":
            print(f"    > [Claude]: Pide usar 'analizar_retina_cnn'.")
            
            # ¡Aquí ocurre la magia! Llamamos a tu app.py local
            cnn_result = llamar_al_especialista_cnn(IMAGE_FILE_PATH)
            
            # --- LLAMADA 2: El Orquestador devuelve el resultado a Claude ---
            print("[Paso 4]: Devolviendo resultado de la CNN a Claude...")
            
            final_message = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=4096,
                system="Eres un Asistente Médico experto en análisis de datos de salud en República Dominicana. Tienes acceso a herramientas locales. Tu trabajo es sintetizar múltiples fuentes de datos para darle al doctor un resumen claro y accionable.",
                tools=tools,
                messages=[
                    {"role": "user", "content": user_message_content},
                    {"role": "assistant", "content": message.content}, # La respuesta anterior de Claude
                    {
                        "role": "user",
                        "type": "tool_result",
                        "tool_use_id": tool_call.id,
                        "content": str(cnn_result) # Resultado de tu CNN
                    }
                ]
            )
            
            print("[Paso 5]: ¡Respuesta final de Claude recibida!")
            print("\n" + "---" * 15)
            print("🏥 REPORTE DEL ORQUESTADOR HÍBRIDO (CLAUDE) 🏥")
            print("---" * 15)
            print(final_message.content[0].text)
            print("---" * 15)
            
        else:
            print(f"Error: Claude pidió una herramienta desconocida: {tool_call.name}")
            
    else:
        # Esto no debería pasar si seguimos el prompt
        print("Error: Claude no usó la herramienta. Respondió directamente:")
        print(message.content[0].text)

# --- Ejecutar la demo ---
if __name__ == "__main__":
    ejecutar_demo_hibrida()