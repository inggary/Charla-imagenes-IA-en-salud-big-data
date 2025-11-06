import os
import cv2
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

# --- Configuración de la App ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- Cargar el Modelo Especialista ---
# Asegúrate de tener el archivo "cnn_model.h5" en la misma carpeta
try:
    model = tf.keras.models.load_model('cnn_model.h5')
    print(">>> Modelo CNN cargado exitosamente.")
except Exception as e:
    print(f"!!! Error cargando 'cnn_model.h5': {e}")
    print("!!! Asegúrate de entrenar y guardar tu modelo desde el notebook.")
    model = None

# --- Función de Pre-procesamiento ---
# Esto debe ser IDÉNTICO a como entrenaste en el notebook
def preprocess_image(image_path):
    # El notebook usaba ImageDataGenerator, que re-escala a 1.0/255
    # y redimensiona. Asumiremos el tamaño de 224x224
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0) # Crear un batch de 1
    return img

# --- El Endpoint de la API ---
@app.route('/predict_retina', methods=['POST'])
def predict_retina():
    if model is None:
        return jsonify({"error": "Modelo no cargado"}), 500

    if 'file' not in request.files:
        return jsonify({"error": "No se encontró el archivo"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No se seleccionó archivo"}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Pre-procesar la imagen
        processed_img = preprocess_image(filepath)

        # Realizar la predicción
        prediction = model.predict(processed_img)
        
        # El modelo binario (0="No_DR", 1="DR")
        # El notebook usaba 'categorical_crossentropy' con 2 salidas
        class_index = np.argmax(prediction[0])
        confidence = float(np.max(prediction[0]))
        
        label = "DR_DETECTADA" if class_index == 1 else "NO_DR"

        # Limpiar
        os.remove(filepath)

        return jsonify({
            "status": label,
            "confianza": confidence
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Iniciar el Servidor ---
if __name__ == '__main__':
    # El puerto 5000 es comúnmente abierto por defecto en Codespaces
    app.run(host='0.0.0.0', port=5000, debug=True)