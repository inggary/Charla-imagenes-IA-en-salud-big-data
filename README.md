# 🏥 Sistema de Diagnóstico Híbrido con IA para Retinopatía Diabética

Sistema inteligente de diagnóstico médico que combina Inteligencia Artificial (CNN), datos de sensores IoT y Model Context Protocol (MCP) para la detección de Retinopatía Diabética.

## 📋 Descripción

Este proyecto implementa un sistema híbrido de diagnóstico que integra:

- 🧠 **Red Neuronal Convolucional (CNN)** - Precisión del 93.45% en detección de Retinopatía Diabética
- 📊 **Random Forest** - Modelo de clasificación con 90.25% de precisión
- 🔌 **Servidor MCP** - Integración con Claude Desktop para análisis conversacional
- 🌐 **API REST** - Endpoints para análisis de imágenes médicas
- 📡 **Simulación de sensores IoT** - Datos de glucosa y smartwatch

## 🎯 Características

- ✅ Análisis de imágenes de retina con CNN entrenada
- ✅ Detección automática de Retinopatía Diabética (DR/No_DR)
- ✅ Servidor MCP para integración con Claude Desktop
- ✅ API REST con Flask para despliegue
- ✅ Reportes médicos generados con IA (Google Gemini)
- ✅ Notebooks Jupyter con todo el proceso de entrenamiento

## 📁 Estructura del Proyecto

```
Charla-imagenes-IA-en-salud-big-data/
├── notebooks/                  # Jupyter notebooks con análisis y modelos
│   ├── importar_datos.ipynb   # Importación y preparación de datos
│   ├── modelo_cnn.ipynb       # Entrenamiento CNN (93.45% acc)
│   ├── modelo_random_forest.ipynb  # Modelo Random Forest
│   ├── cnn_model_94.h5        # Modelo CNN entrenado
│   └── data_cnn/              # Datasets organizados (train/val/test)
├── mcp/                        # Servidor MCP y APIs
│   ├── servidor_demo.py       # Servidor MCP principal ⭐
│   ├── app.py                 # API REST con Flask
│   ├── orchestrator.py        # Orquestador con Google Gemini
│   ├── pyproject.toml         # Configuración de dependencias
│   └── readme.md              # Documentación MCP detallada
├── requirements.txt            # Dependencias del proyecto
└── README.md                  # Este archivo
```

## 🚀 Instalación Rápida

### Prerrequisitos

- Python 3.10 o superior
- pip o uv (recomendado)

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/inggary/Charla-imagenes-IA-en-salud-big-data.git
cd Charla-imagenes-IA-en-salud-big-data
```

### Paso 2: Instalar dependencias

```bash
# Opción 1: Con pip
pip install -r requirements.txt

# Opción 2: Con uv (recomendado)
cd mcp
uv venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
uv pip install mcp tensorflow "numpy>=1.24.0,<2.0.0" opencv-python-headless pillow
```

## 💻 Uso

### Opción 1: Servidor MCP (Recomendado)

El servidor MCP permite integración directa con Claude Desktop:

```bash
cd mcp
python servidor_demo.py
```

**Configuración en Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "servidor-salud-hibrido": {
      "command": "/ruta/completa/a/.venv/bin/python",
      "args": ["/ruta/completa/a/servidor_demo.py"]
    }
  }
}
```

### Opción 2: API REST + Orchestrator

**Terminal 1 - Servidor Flask:**
```bash
cd mcp
python app.py
```

**Terminal 2 - Orquestador:**
```bash
cd mcp
echo "GOOGLE_API_KEY=tu_api_key" > .env
python orchestrator.py
```

### Opción 3: Notebooks Jupyter

```bash
jupyter notebook notebooks/
```

## 🔧 Herramientas MCP Disponibles

Cuando uses el servidor MCP con Claude Desktop, tendrás acceso a:

1. **`analizar_retina_cnn(image_path)`**
   - Analiza imágenes de retina para detectar DR
   - Retorna: `DR_DETECTADA` o `NO_DR` con nivel de confianza

2. **`obtener_datos_paciente(paciente_id)`**
   - Obtiene datos simulados de sensores IoT
   - Retorna: glucosa, pasos, ritmo cardíaco, etc.

3. **`generar_diagnostico_hibrido(paciente_id, image_path)`**
   - Genera reporte completo combinando CNN + sensores
   - Retorna: Análisis detallado para el médico

## 📊 Resultados del Modelo

### CNN (Red Neuronal Convolucional)
- **Precisión:** 93.45%
- **Arquitectura:** Transfer learning con fine-tuning
- **Input:** Imágenes 224x224 RGB
- **Output:** Clasificación binaria (DR/No_DR)

### Random Forest
- **Precisión:** 90.25%
- **Métricas:**
  - DR: Precision 0.88, Recall 0.94, F1-score 0.91
  - No_DR: Precision 0.93, Recall 0.86, F1-score 0.90

## 🔒 Seguridad y Privacidad

⚠️ **IMPORTANTE:** Este proyecto es para fines educativos y de demostración.

- ❌ **NO** subir archivos `.env` con API keys a GitHub
- ❌ **NO** subir modelos `.h5` grandes al repositorio
- ❌ **NO** incluir datos reales de pacientes
- ✅ Usar `.gitignore` para excluir datos sensibles
- ✅ Variables de entorno para configuraciones

## 📚 Documentación Adicional

- [Documentación MCP](./mcp/readme.md) - Guía completa del servidor MCP
- [Notebooks](./notebooks/) - Análisis exploratorio y entrenamiento
- [FastMCP Documentation](https://github.com/jlowin/fastmcp) - Framework MCP utilizado

## 🤝 Contribuciones

Este proyecto fue desarrollado como material educativo para presentaciones sobre IA en salud y Big Data.

## 👨‍💻 Autor

**Gary Joel Pimentel Rosario**
- GitHub: [@inggary](https://github.com/inggary)
- Proyecto: Sistema Híbrido de Diagnóstico con IA

## 📄 Licencia

Este proyecto está bajo la licencia especificada en el archivo LICENSE.

## ⚕️ Disclaimer Médico

Este software es **ÚNICAMENTE** para propósitos educativos y de investigación. No debe utilizarse como herramienta de diagnóstico médico real. Siempre consulte con profesionales médicos calificados para diagnósticos y tratamientos reales.

---

**Nota:** El modelo CNN (`cnn_model_94.h5`) no está incluido en el repositorio por su tamaño. Debes entrenarlo usando el notebook `modelo_cnn.ipynb` o contactar al autor.

