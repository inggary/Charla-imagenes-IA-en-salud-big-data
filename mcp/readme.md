🚀 Cómo Ejecutar tu Demo en Codespace
Abre tu Codespace, crea todos los archivos, sube tu cnn_model.h5 y tu test_image.jpg.

Crea el archivo .env y pon tu GOOGLE_API_KEY.

Abre una terminal y ejecuta pip install -r requirements.txt.

En la Terminal 1 (La API Especialista):

Bash

python app.py
Verás un mensaje de Flask diciendo que el servidor está corriendo en el puerto 5000. Codespaces te preguntará si quieres hacer ese puerto público; di que sí (o ábrelo en la pestaña "Puertos").

Abre una SEGUNDA Terminal (Haz clic en el "+" en la ventana de la terminal).

En la Terminal 2 (El Orquestador):

Bash

python orchestrator.py
Si todo funciona, verás la Terminal 2 imprimir "Consultando al especialista...", luego la Terminal 1 mostrará una petición POST /predict_retina, y finalmente la Terminal 2 imprimirá el reporte completo de Gemini. ¡Y eso es tu demo!