import streamlit as st
import base64
import time
import threading  # 🛡️ Procesa la IA en segundo plano sin congelar la app
from src.azure_services import enrich_prompt_with_gpt4o, generate_image_with_dalle3
from src.styles import BRAND_STYLES

# Configuración de página con identidad Enterprise
st.set_page_config(page_title="Enterprise Visual Generator", layout="centered", page_icon="🛡️")

st.title("🛡️ Enterprise Brand-Aligned Visual Generator")
st.write("Orquestador de activos visuales B2B con arquitectura unificada y segura en Azure.")

# 🧠 INTERFAZ DE MEMORIA AVANZADA (Inicializar estados de sesión)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "generating" not in st.session_state:
    st.session_state.generating = False
if "shared_container" not in st.session_state:
    st.session_state.shared_container = {"done": False, "error": None, "result": None, "latency": 0.0}

# Red de seguridad automática para limpiar la caja de texto
if "should_clear" in st.session_state and st.session_state.should_clear:
    st.session_state.input_text_value = ""
    st.session_state.should_clear = False

if "input_text_value" not in st.session_state:
    st.session_state.input_text_value = ""

if "last_latency" not in st.session_state:
    st.session_state.last_latency = 0.0
    
# 📊 PANEL 1: Panel FinOps en Barra Lateral (Control de Costos y Gobierno)
st.sidebar.markdown("### 📊 Panel FinOps (Control de Costos)")
calidad = st.sidebar.selectbox("Calidad de Cómputo Visual:", ["Estándar ($0.045 / clic)", "Alta Definición HD ($0.085 / clic)"])
st.sidebar.info("Monitoreo de Gobierno activo: Los límites y cuotas duras están configurados por departamento en Azure OpenAI Studio.")

# Cálculo de Gasto Acumulado y Centro de Costos
st.sidebar.markdown("---")
st.sidebar.markdown("### 💳 Facturación de la Sesión")
total_solicitudes = len(st.session_state.chat_history)
precio_por_clic = 0.045 if "Estándar" in calidad else 0.085
gasto_total = total_solicitudes * precio_por_clic

st.sidebar.metric(
    label="Gasto Acumulado en Vivo:", 
    value=f"USD ${gasto_total:.3f}", 
    delta=f"{total_solicitudes} Activos en historial"
)

centro_costos = st.sidebar.selectbox(
    "Imputar Gasto a Departamento:", 
    ["Marketing Digital", "Comunicaciones Internas", "Ventas Corporativas", "Innovación & TI B2B"]
)

# ⚙️ PANEL 2: Configuración de Temperatura 
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Configuración del Modelo")
user_temperature = st.sidebar.slider(
    label="Nivel de Creatividad (Temperature):",
    min_value=0.0, max_value=1.0, value=0.7, step=0.1
)

# ⚡ PANEL 3: Latencia de Infraestructura Cloud (¡CORREGIDO PARA QUE SIEMPRE SE VEA!)
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚡ Rendimiento Cloud")

# Formateo dinámico del texto de la métrica
if st.session_state.last_latency > 0:
    texto_latencia = f"{st.session_state.last_latency:.2f} seg"
else:
    texto_latencia = "0.00 seg (Esperando render)"

st.sidebar.metric(
    label="Latencia del último render:", 
    value=texto_latencia,
    help="Tiempo total de cómputo y viaje de datos de ida y vuelta desde Polonia Central."
)

# 🗑️ PANEL 4: Botón de Reseteo de Sistema
st.sidebar.markdown("---")
st.sidebar.markdown("### 🛠️ Acciones del Sistema")
if st.sidebar.button("🗑️ Borrar Historial de Chat", use_container_width=True):
    st.session_state.chat_history = []
    st.session_state.input_text_value = ""
    st.session_state.last_latency = 0.0
    st.session_state.generating = False
    st.rerun()


# --- 🖼️ FASE 1: RENDERIZADO DEL HISTORIAL DE CHAT ---
st.write("---")
for index, record in enumerate(st.session_state.chat_history):
    with st.chat_message("user"):
        st.write(f"Idea: **{record['user_idea']}**")
        st.write(f"Perfil de Marca: `{record['brand_profile']}` | Creatividad: `{record.get('temperature', 0.7)}`")
        
    with st.chat_message("assistant", avatar="🛡️"):
        st.write("¡Prompt alineado a las directrices de la marca!")
        with st.expander("Ver prompt enriquecido enviado por la API"):
            st.code(record['enriched_prompt'], language="text")
        st.image(record['image_bytes'], caption=f"Activo visual corporativo oficial - Estilo: {record['brand_profile']}", use_column_width=True)
        st.download_button(
            label=f"📥 Descargar Activo Visual {index + 1} (PNG)",
            data=record['image_bytes'],
            file_name=f"activo_{index+1}_{record['brand_profile']}.png",
            mime="image/png",
            key=f"download_{index}"
        )
        st.success("✨ ¡Despliegue visual completado con éxito en el entorno corporativo!")
    st.write("---")


# --- 📥 FASE 2: ENTRADAS DE USUARIO Y CONTROL ASÍNCRONO ---
with st.container():
    st.write("### 🆕 Generar Nuevo Activo")
    brand_profile = st.selectbox("1. Selecciona el perfil de marca institucional (Brand Guidelines):", list(BRAND_STYLES.keys()))
    user_idea = st.text_input("2. Describe la idea de la imagen que necesitas para tu campaña:", placeholder="Ej: Un grupo de ingenieros colaborando en un servidor", key="input_text_value")

    # CONTROL VISUAL DE PROCESAMIENTO
    if st.session_state.generating:
        st.write("---")
        st.markdown("#### ⏳ Procesamiento en Curso con Inteligencia Artificial")
        st.info("🧠 El pipeline está comunicándose con Polonia Central... El historial de arriba está seguro.")
        
        # El Botón de Cancelación que preserva la memoria de la sesión
        if st.button("❌ Cancelar Solicitud en Curso", use_container_width=True, type="primary"):
            st.session_state.generating = False
            st.session_state.should_clear = True
            st.warning("Se ha cancelado la solicitud. Volviendo al estado operativo...")
            st.rerun()
            
        # Oyente del estado del Hilo Secundario
        container = st.session_state.shared_container
        if container["done"]:
            st.session_state.generating = False
            if container["error"]:
                st.error(f"La API de Azure bloqueó la solicitud o error de red: {container['error']}")
            else:
                # Al terminar con éxito, extraemos los datos y la latencia medida de forma segura
                st.session_state.chat_history.append(container["result"])
                st.session_state.last_latency = container["latency"]  # <-- Recibe el tiempo medido de forma limpia
                st.session_state.should_clear = True
            st.rerun()
        else:
            time.sleep(0.4)
            st.rerun()
            
    else:
        # Botón normal de disparo operativo
        if st.button("🚀 Generar Activo Corporativo"):
            if not user_idea:
                st.warning("Por favor, introduce una idea para el diseño visual.")
            else:
                # Limpiamos el contenedor de datos asíncronos compartidos
                st.session_state.shared_container = {"done": False, "error": None, "result": None, "latency": 0.0}
                
                # 🛠️ Hilo aislado para la API (Calcula el tiempo de forma Thread-Safe)
                def async_worker(shared_dict, idea, profile, temp):
                    try:
                        t_start = time.time()  # Empieza el reloj de infraestructura
                        
                        enriched = enrich_prompt_with_gpt4o(idea, profile, temp)
                        raw_image = generate_image_with_dalle3(enriched)
                        
                        t_total = time.time() - t_start  # Detiene el reloj
                        
                        # Decodificación Base64 a bytes binarios puros
                        image_bytes = raw_image
                        if isinstance(raw_image, str) and not raw_image.startswith("http"):
                            if "," in raw_image:
                                raw_image = raw_image.split(",")[1]
                            image_bytes = base64.b64decode(raw_image)
                        
                        # Guardamos los resultados y los segundos calculados en el mapa compartido
                        shared_dict["result"] = {
                            "user_idea": idea, "brand_profile": profile,
                            "enriched_prompt": enriched, "image_bytes": image_bytes, "temperature": temp
                        }
                        shared_dict["latency"] = t_total  # Pasamos el tiempo al hilo principal de forma segura
                        shared_dict["done"] = True
                    except Exception as e:
                        shared_dict["error"] = str(e)
                        shared_dict["done"] = True

                # Disparamos el hilo en paralelo
                bg_thread = threading.Thread(
                    target=async_worker,
                    args=(st.session_state.shared_container, user_idea, brand_profile, user_temperature)
                )
                bg_thread.start()
                
                st.session_state.generating = True
                st.rerun()