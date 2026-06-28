# 🛡️ Enterprise Brand-Aligned Visual Generator

![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4o-0078d4?style=flat-square)
![Azure AI](https://img.shields.io/badge/Azure%20AI-DALL--E%203-0078d4?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-UI%20Framework-ff4b4b?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11-3776ab?style=flat-square&logo=python&logoColor=white)
![FinOps](https://img.shields.io/badge/FinOps-Cost%20Control-2ed573?style=flat-square)

Orquestador de activos visuales B2B con arquitectura unificada, asíncrona y segura desplegado en **Azure OpenAI Service**.

Este sistema actúa como un middleware inteligente y una interfaz de usuario avanzada para corporaciones. Permite a los empleados generar material visual publicitario y corporativo garantizando la **consistencia estética de la marca (Brand Guidelines)**, el **control estricto de costos (FinOps)** y la **seguridad de los datos** mediante el aislamiento de la infraestructura cloud en el centro de datos de Polonia Central.

---

## 🚀 Características Clave

* **🧠 Director de Arte Inteligente (Prompt Enrichment):** El sistema utiliza `GPT-4o` para interceptar ideas simples del usuario y transformarlas en instrucciones fotográficas detalladas en inglés, inyectando automáticamente guías de estilo institucionales (`BRAND_STYLES`) y restricciones de seguridad (`negative_prompt`).
* **🔄 Arquitectura Asíncrona (Multi-threading):** Procesamiento en segundo plano mediante hilos independientes (`threading.Thread`). Permite al usuario **cancelar solicitudes en curso** sin congelar la interfaz del navegador y **preservando el historial completo** de imágenes generadas en la sesión.
* **📊 Panel de Control FinOps & Gobierno:**
    * **Monitoreo de Costos en Vivo:** Cálculo dinámico del gasto acumulado basado en volumen y calidad visual seleccionada (Estándar vs HD).
    * **Imputación Contable:** Selector de centros de costos para auditar los gastos por departamento (Marketing, TI, Ventas).
    * **Métricas de Rendimiento:** Medición e indicador en tiempo real de la latencia de la API (viaje de datos ida y vuelta a Polonia Central).
* **⚙️ Calibración del Modelo (Temperature UI):** Slider dinámico en la interfaz que permite regular la temperatura de creatividad de `GPT-4o` según el nivel de disrupción que requiera la campaña publicitaria.
* **🛡️ Enterprise Content Safety & Data Security:** 
    * Manejo elástico de payloads binarios convirtiendo cadenas Base64 a bytes puros directamente en memoria RAM.
    * Políticas estrictas de protección de datos de Azure: las ideas y conceptos comerciales de la empresa no se utilizan para entrenar modelos públicos.

---

## 🛠️ Stack Tecnológico

* **Frontend / UI:** Streamlit (Arquitectura de Chatbot Visual con Estados de Sesión Persistentes).
* **Orquestación de IA:** Azure OpenAI Service (`GPT-4o` y `gpt-image-2` / DALL-E 3).
* **Lenguaje & Concurrencia:** Python 3.x (Threading, Base64 Engine, Tenacity para reintentos elásticos).

---

## 📁 Estructura del Proyecto

```text
enterprise_visual_generator/
│
├── src/
│   ├── __init__.py
│   ├── azure_services.py  # Conectores de API y manejo de hilos thread-safe
│   ├── config.py          # Variables de entorno y configuraciones de Azure
│   └── styles.py          # Diccionario de identidades corporativas (Brand Guidelines)
│
├── .env.example           # Plantilla pública de variables de infraestructura
├── .gitignore             # Filtro de seguridad para evitar fugas de llaves privadas
├── app.py                 # Orquestador principal de la interfaz y lógica de UI
└── requirements.txt       # Congelación de dependencias del entorno de producción
```

---
💻 Instalación y Configuración Local
Sigue estos pasos para levantar el entorno de desarrollo en tu computadora local:

1. Clonar el repositorio
```bash
git clone [https://github.com/Alekhine-Spitfire/enterprise_visual_generator.git](https://github.com/Alekhine-Spitfire/enterprise_visual_generator.git)
cd enterprise_visual_generator
```

2. Configurar el Entorno Virtual
```bash
# Crear entorno virtual
python -m venv .venv

# Activar en Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Activar en Linux/macOS
source .venv/bin/activate
```

3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

4. Configurar Variables de Entorno
Crea un archivo local llamado .env en la raíz del proyecto basándote en el archivo de ejemplo:
```env
AZURE_OPENAI_KEY_TEXT="tu_api_key_de_gpt4o"
AZURE_OPENAI_ENDPOINT_TEXT="tu_endpoint_de_gpt4o"
AZURE_DEPLOYMENT_GPT4O="tu_nombre_de_despliegue"

AZURE_OPENAI_KEY_IMAGE="tu_api_key_de_dalle3"
AZURE_OPENAI_ENDPOINT_IMAGE="tu_endpoint_de_dalle3"
AZURE_DEPLOYMENT_IMAGE_MODEL="tu_nombre_de_despliegue_image_model"
```

5. Ejecutar la Aplicación
```bash
streamlit run app.py
```

📝 Licencia

Este proyecto se distribuye bajo fines de desarrollo interno y portafolio técnico de Ingeniería de Datos / Arquitectura de IA.

Desarrollado por Alejandro Terrazas.

