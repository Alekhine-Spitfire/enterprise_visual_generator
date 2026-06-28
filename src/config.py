import os
from dotenv import load_dotenv

# Cargar las variables de entorno locales
load_dotenv()

class Config:
    # 🧠 Procesamiento de Texto (Polonia Central)
    AZURE_OPENAI_ENDPOINT_TEXT = os.getenv("AZURE_OPENAI_ENDPOINT_TEXT")
    AZURE_OPENAI_KEY_TEXT = os.getenv("AZURE_OPENAI_KEY_TEXT")
    AZURE_DEPLOYMENT_GPT4O = os.getenv("AZURE_DEPLOYMENT_GPT4O", "gpt-4o")

    # 🎨 Generación Visual (Polonia Central - gpt-image-2)
    AZURE_OPENAI_ENDPOINT_IMAGE = os.getenv("AZURE_OPENAI_ENDPOINT_IMAGE")
    AZURE_OPENAI_KEY_IMAGE = os.getenv("AZURE_OPENAI_KEY_IMAGE")
    AZURE_DEPLOYMENT_IMAGE_MODEL = os.getenv("AZURE_DEPLOYMENT_IMAGE_MODEL", "gpt-image-2")

    @classmethod
    def validate(cls):
        """Valida que no falte ningún secreto crítico antes de encender los motores."""
        required = [
            "AZURE_OPENAI_ENDPOINT_TEXT", "AZURE_OPENAI_KEY_TEXT",
            "AZURE_OPENAI_ENDPOINT_IMAGE", "AZURE_OPENAI_KEY_IMAGE"
        ]
        missing = [var for var in required if not getattr(cls, var)]
        if missing:
            raise ValueError(f"Faltan variables de entorno críticas en tu .env: {', '.join(missing)}")