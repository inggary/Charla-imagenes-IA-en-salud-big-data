# 🏥 Sistema Híbrido de Diagnóstico con MCP🚀 Cómo Ejecutar tu Demo en Codespace

Abre tu Codespace, crea todos los archivos, sube tu cnn_model.h5 y tu test_image.jpg.

Este directorio contiene tres implementaciones diferentes del sistema de diagnóstico:

Crea el archivo .env y pon tu GOOGLE_API_KEY.

1. **`app.py`** - API REST con Flask (Servidor Especialista)

2. **`orchestrator.py`** - Orquestador con Google GeminiAbre una terminal y ejecuta pip install -r requirements.txt.

3. **`servidor_demo.py`** - Servidor MCP (Model Context Protocol) ⭐ **RECOMENDADO**

En la Terminal 1 (La API Especialista):

---

Bash

## 🚀 Opción 1: Servidor MCP (servidor_demo.py)

python app.py

### Requisitos PreviosVerás un mensaje de Flask diciendo que el servidor está corriendo en el puerto 5000. Codespaces te preguntará si quieres hacer ese puerto público; di que sí (o ábrelo en la pestaña "Puertos").



1. **Instalar dependencias:**Abre una SEGUNDA Terminal (Haz clic en el "+" en la ventana de la terminal).

```bash

pip install -r ../requirements.txtEn la Terminal 2 (El Orquestador):

```

Bash

2. **Asegurarse de tener el modelo CNN:**

   - El archivo `cnn_model_94.h5` debe estar en la carpeta `mcp/` o ajustar la ruta en el códigopython orchestrator.py

   - O copiar desde: `cp ../notebooks/cnn_model_94.h5 ./`Si todo funciona, verás la Terminal 2 imprimir "Consultando al especialista...", luego la Terminal 1 mostrará una petición POST /predict_retina, y finalmente la Terminal 2 imprimirá el reporte completo de Gemini. ¡Y eso es tu demo!

### Iniciar el Servidor MCP

```bash
# Opción 1: Con uv (recomendado para MCP)
uv run servidor_demo.py

# Opción 2: Con Python directamente
python servidor_demo.py
```

### ¿Qué hace el Servidor MCP?

El servidor MCP expone **herramientas** y **prompts** que pueden ser utilizados por Claude Desktop u otros clientes MCP:

**Herramientas disponibles:**
- `analizar_retina_cnn(image_path)` - Analiza imágenes de retina con CNN para detectar Retinopatía Diabética
- `obtener_datos_paciente(paciente_id)` - Obtiene datos simulados del sensor de glucosa y smartwatch

**Prompts disponibles:**
- `generar_diagnostico_hibrido(paciente_id, image_path)` - Genera un reporte completo combinando CNN + datos de sensores

### Conectar con Claude Desktop

Para usar este servidor con Claude Desktop, agrega esta configuración a tu archivo de configuración de Claude:

**En macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "servidor-salud": {
      "command": "python",
      "args": ["/Users/garyjoelpimentelrosario/Desktop/presentacion de salud/proyecto/Charla-imagenes-IA-en-salud-big-data/mcp/servidor_demo.py"]
    }
  }
}
```

---

## 🚀 Opción 2: Demo con Flask + Orchestrator (Método Original)

### Variante A: Con Google Gemini 🆕

**Terminal 1 - Servidor Flask (API Especialista):**
```bash
cd mcp
python app.py
```

**Terminal 2 - Orquestador con Gemini:**

1. Asegúrate de tener tu API key de Google:
```bash
echo "GOOGLE_API_KEY=tu_api_key_aqui" > .env
```

2. Coloca una imagen de retina para probar (ej: `test_image.jpg`)

3. Ejecuta el orquestador:
```bash
python orchestrator_gemini.py
```

**¿Qué hace?**
- Llama al servidor Flask (CNN) para analizar la imagen
- Envía la imagen + resultado CNN + datos de sensores a Gemini
- Gemini genera un reporte médico completo combinando toda la información
- Guarda el reporte en `reporte_gemini.txt`

### Variante B: Con Claude (Original)

**Terminal 1 - Servidor Flask:**
```bash
cd mcp
python app.py
```

**Terminal 2 - Orquestador con Claude:**

1. Crea el archivo `.env` con tu API key de Claude:
```bash
echo "CLAUDE_API_KEY=tu_api_key_aqui" > .env
```

2. Ejecuta:
```bash
python orchestrator.py
```

---

## 🚀 Opción 3: Paso a Paso (Para Codespaces)

### Paso 1: Preparar el entorno

Abre tu Codespace, crea todos los archivos, sube tu `cnn_model_94.h5` y tu `test_image.jpg`.

Crea el archivo `.env` y pon tu `GOOGLE_API_KEY`:

```bash
echo "GOOGLE_API_KEY=tu_api_key_aqui" > .env
```

Abre una terminal y ejecuta:

```bash
pip install -r ../requirements.txt
```

### Paso 2: En la Terminal 1 (La API Especialista):

```bash
python app.py
```

Verás un mensaje de Flask diciendo que el servidor está corriendo en el puerto 5000. Codespaces te preguntará si quieres hacer ese puerto público; di que sí (o ábrelo en la pestaña "Puertos").

### Paso 3: En la Terminal 2 (El Orquestador):

Abre una SEGUNDA Terminal (Haz clic en el "+" en la ventana de la terminal).

```bash
python orchestrator.py
```

Si todo funciona, verás la Terminal 2 imprimir "Consultando al especialista...", luego la Terminal 1 mostrará una petición POST `/predict_retina`, y finalmente la Terminal 2 imprimirá el reporte completo de Gemini. ¡Y eso es tu demo!

---

## 📁 Estructura de Archivos

```
mcp/
├── app.py                 # API REST con Flask
├── orchestrator.py        # Orquestador con Gemini
├── servidor_demo.py       # Servidor MCP ⭐
├── readme.md             # Este archivo
└── cnn_model_94.h5       # Modelo CNN entrenado (copiar desde notebooks/)
```

---

## 🔧 Solución de Problemas

**Error: "No se pudo cargar 'cnn_model_94.h5'"**
- Verifica que el modelo esté en la carpeta `mcp/`
- O copia desde: `cp ../notebooks/cnn_model_94.h5 ./`

**Error: "Module 'mcp' not found"**
- Instala: `pip install mcp fastmcp`

**Error: "Module 'tensorflow' not found"**
- Instala: `pip install tensorflow`

**Error: "Module 'google.generativeai' not found"**
- Instala: `pip install google-generativeai`

---

## 💡 ¿Cuál implementación usar?

- **`servidor_demo.py`** (MCP) → Para integración con Claude Desktop o sistemas MCP modernos
- **`app.py` + `orchestrator.py`** → Para demo tradicional con API REST y Gemini

---

## 📝 Notas Adicionales

- El modelo CNN tiene una precisión del **93.45%** en la detección de Retinopatía Diabética
- El servidor MCP permite que Claude Desktop acceda directamente a tu modelo local
- Los datos del paciente en `obtener_datos_paciente()` son simulados para la demo
