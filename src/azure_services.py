import logging
from openai import AzureOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from src.config import Config
from src.styles import BRAND_STYLES

# Configuración de Logging Empresarial para auditoría
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Validar secretos al arrancar
Config.validate()

# 🧠 Cliente 1: Orquestación de Texto (Polonia Central) - ¡ACTUALIZADO!
client_text = AzureOpenAI(
    azure_endpoint=Config.AZURE_OPENAI_ENDPOINT_TEXT,
    api_key=Config.AZURE_OPENAI_KEY_TEXT,
    api_version="2024-12-01-preview"  # <-- Versión de API moderna para soportar el entorno actual
)

# 🎨 Cliente 2: Motor Visual Único (Polonia Central) - ¡ACTUALIZADO!
client_image = AzureOpenAI(
    azure_endpoint=Config.AZURE_OPENAI_ENDPOINT_IMAGE,
    api_key=Config.AZURE_OPENAI_KEY_IMAGE,
    api_version="2024-12-01-preview"  # <-- Versión de API moderna para soportar el entorno actual
)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def enrich_prompt_with_gpt4o(user_idea: str, brand_profile: str, temperature: float) -> str: # <-- ¡Acepta la variable aquí!
    """Toma la idea simple, la fusiona con las guías de estilo, restricciones e inyecta la temperatura dinámica."""
    logging.info(f"Iniciando enriquecimiento de prompt en Polonia Central con temperatura: {temperature}")
    
    style_info = BRAND_STYLES.get(brand_profile, {}).get("description", "")
    negative_info = BRAND_STYLES.get(brand_profile, {}).get("negative_prompt", "")
    
    system_prompt = (
        "Eres un director de arte experto en consistencia de marca corporativa B2B. "
        "Tu tarea es transformar una idea de imagen simple en un prompt fotográfico profesional y detallado en inglés.\n\n"
        "REGLAS VISUALES OBLIGATORIAS A INYECTAR:\n"
        f"- DIRECTRICES DE ESTILO: {style_info}\n"
        f"- RESTRICCIONES ABSOLUTAS (No permitas esto en la composición): {negative_info}\n\n"
        "Devuelve ÚNICAMENTE el prompt final optimizado en inglés listo para el generador de imágenes. "
        "No incluyas introducciones, explicaciones, advertencias ni comillas."
    )

    try:
        response = client_text.chat.completions.create(
            model=Config.AZURE_DEPLOYMENT_GPT4O,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Idea del usuario: {user_idea}"}
            ],
            temperature=temperature # <-- ¡Mapeado dinámicamente con el slider de la pantalla!
        )
        enriched_prompt = response.choices[0].message.content.strip()
        logging.info("Prompt corporativo estructurado con éxito incluyendo exclusiones de marca.")
        return enriched_prompt
    except Exception as e:
        logging.error(f"Error crítico en la capa de texto (GPT-4o): {str(e)}")
        raise e

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def generate_image_with_dalle3(enriched_prompt: str) -> str:
    """Envía el prompt pulido al servidor de Polonia usando gpt-image-2 con extracción segura de URL."""
    logging.info("Enviando petición de renderizado a Polonia Central...")
    try:
        result = client_image.images.generate(
            model=Config.AZURE_DEPLOYMENT_IMAGE_MODEL,
            prompt=enriched_prompt,
            n=1,
            size="1024x1024"
        )
        
        # 🛡️ ALTA DISPONIBILIDAD: Extractor defensivo anti-AttributeError
        logging.info(f"Tipo de objeto devuelto por gpt-image-2: {type(result)}")
        image_url = None

        # Caso A: Estructura estándar del SDK con atributos de objeto (.data)
        if hasattr(result, 'data') and len(result.data) > 0:
            primer_nodo = result.data[0]
            # Si el elemento interno vino formateado como diccionario
            if isinstance(primer_nodo, dict):
                image_url = primer_nodo.get('url') or primer_nodo.get('b64_json')
            # Si vino como un objeto nativo del SDK
            else:
                image_url = getattr(primer_nodo, 'url', None) or getattr(primer_nodo, 'b64_json', None)
        
        # Caso B: La respuesta vino como un diccionario crudo JSON (común en APIs preview de 2026)
        elif isinstance(result, dict) and 'data' in result and len(result['data']) > 0:
            primer_nodo = result['data'][0]
            image_url = primer_nodo.get('url') if isinstance(primer_nodo, dict) else getattr(primer_nodo, 'url', None)

        # Si tras los análisis el pipeline no encontró ningún enlace válido
        if not image_url:
            raise AttributeError(f"La API respondió con éxito pero la estructura no contiene una URL válida: {result}")

        logging.info("Activo visual corporativo generado exitosamente por gpt-image-2.")
        return image_url
        
    except Exception as e:
        logging.error(f"Error crítico en el mapeo o generación visual: {str(e)}")
        raise e