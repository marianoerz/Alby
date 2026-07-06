"""
config.py — Gestor de configuración central de Jarvis.

Lee y escribe el archivo config.json, exponiendo todos los parámetros
del sistema como un objeto accesible desde cualquier módulo.
"""

import json
import os
import sys
import logging
from pathlib import Path
from typing import Any

# Ruta base del proyecto.
# Si la app está empaquetada (PyInstaller), __file__ apunta a una carpeta
# temporal de extracción que se borra al cerrar el programa. En ese caso
# usamos la carpeta donde está el .exe real, para que config.json, la
# memoria y los logs persistan entre ejecuciones.
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent.resolve()
else:
    BASE_DIR = Path(__file__).parent.resolve()

CONFIG_PATH = BASE_DIR / "config.json"

# Configuración predeterminada completa
DEFAULT_CONFIG: dict[str, Any] = {
    # ── Proveedor de Inteligencia Artificial ──────────────────────────────────
    "ai_provider": "openai",          # openai | deepseek | ollama | lmstudio
    "ai_model": "gpt-4o-mini",        # Modelo a utilizar
    "ai_temperature": 0.7,            # Creatividad de las respuestas (0.0–2.0)
    "ai_max_tokens": 1024,            # Tokens máximos por respuesta

    # ── Claves de API ─────────────────────────────────────────────────────────
    "openai_api_key": "",
    "deepseek_api_key": "",
    "ollama_base_url": "http://localhost:11434",
    "lmstudio_base_url": "http://localhost:1234",

    # ── Reconocimiento de voz ─────────────────────────────────────────────────
    "wake_word": "jarvis",            # Palabra de activación (minúsculas)
    "stt_engine": "whisper",          # whisper | google | vosk
    "stt_language": "es-ES",          # Idioma de reconocimiento
    "stt_energy_threshold": 300,      # Umbral de energía del micrófono
    "stt_pause_threshold": 0.8,       # Segundos de silencio para fin de frase

    # ── Síntesis de voz ───────────────────────────────────────────────────────
    "tts_engine": "edge",             # edge | pyttsx3 | azure
    "tts_voice": "es-MX-JorgeNeural", # Voz predeterminada (Edge TTS)
    "tts_rate": "+0%",                # Velocidad: -50% a +100%
    "tts_volume": "+0%",              # Volumen: -50% a +50%
    "tts_pitch": "+0Hz",              # Tono: -50Hz a +50Hz

    # ── Interfaz ──────────────────────────────────────────────────────────────
    "theme": "dark_jarvis",           # Tema visual
    "language": "es",                 # Idioma de la interfaz
    "window_width": 1100,
    "window_height": 720,
    "font_size": 13,

    # ── Memoria ───────────────────────────────────────────────────────────────
    "user_name": "Usuario",
    "memory_max_messages": 20,        # Mensajes del historial enviados a la IA
    "memory_db_path": "memory/jarvis_memory.db",

    # ── Sistema ───────────────────────────────────────────────────────────────
    "confirm_dangerous_actions": True,  # Pedir confirmación antes de acciones peligrosas
    "log_level": "INFO",

    # ── Internet ─────────────────────────────────────────────────────────────
    "weather_api_key": "",            # OpenWeatherMap API Key
    "weather_city": "Buenos Aires",
    "news_api_key": "",               # NewsAPI.org API Key
    "news_country": "ar",
    "news_language": "es",
}


class Config:
    """
    Clase singleton que gestiona la configuración de Jarvis.

    Carga la configuración desde config.json al inicializarse y
    proporciona métodos para leer, modificar y guardar parámetros.
    """

    _instance: "Config | None" = None

    def __new__(cls) -> "Config":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._data: dict[str, Any] = {}
            cls._instance._loaded = False
        return cls._instance

    # ── Inicialización ────────────────────────────────────────────────────────

    def load(self) -> None:
        """Carga la configuración desde disco, creando el archivo si no existe."""
        if CONFIG_PATH.exists():
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                # Combinar con defaults para garantizar que existan todas las claves
                self._data = {**DEFAULT_CONFIG, **saved}
            except (json.JSONDecodeError, OSError) as exc:
                logging.warning("No se pudo leer config.json (%s). Usando valores predeterminados.", exc)
                self._data = dict(DEFAULT_CONFIG)
        else:
            self._data = dict(DEFAULT_CONFIG)
            self.save()  # Crear el archivo con los valores predeterminados

        self._loaded = True
        logging.info("Configuración cargada desde %s", CONFIG_PATH)

    def save(self) -> None:
        """Persiste la configuración actual en config.json."""
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=4, ensure_ascii=False)
        except OSError as exc:
            logging.error("No se pudo guardar config.json: %s", exc)

    # ── Acceso a valores ──────────────────────────────────────────────────────

    def get(self, key: str, default: Any = None) -> Any:
        """Devuelve el valor de una clave de configuración."""
        if not self._loaded:
            self.load()
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Establece el valor de una clave y persiste el cambio."""
        if not self._loaded:
            self.load()
        self._data[key] = value
        self.save()

    def get_all(self) -> dict[str, Any]:
        """Devuelve una copia del diccionario completo de configuración."""
        if not self._loaded:
            self.load()
        return dict(self._data)

    def update(self, updates: dict[str, Any]) -> None:
        """Actualiza múltiples claves a la vez y persiste los cambios."""
        if not self._loaded:
            self.load()
        self._data.update(updates)
        self.save()

    # ── Propiedades de conveniencia ───────────────────────────────────────────

    @property
    def ai_provider(self) -> str:
        return self.get("ai_provider", "openai")

    @property
    def ai_model(self) -> str:
        return self.get("ai_model", "gpt-4o-mini")

    @property
    def wake_word(self) -> str:
        return self.get("wake_word", "jarvis").lower()

    @property
    def user_name(self) -> str:
        return self.get("user_name", "Usuario")

    @property
    def tts_voice(self) -> str:
        return self.get("tts_voice", "es-MX-JorgeNeural")

    @property
    def tts_rate(self) -> str:
        return self.get("tts_rate", "+0%")

    @property
    def tts_volume(self) -> str:
        return self.get("tts_volume", "+0%")

    @property
    def tts_pitch(self) -> str:
        return self.get("tts_pitch", "+0Hz")

    @property
    def memory_db_path(self) -> Path:
        raw = self.get("memory_db_path", "memory/jarvis_memory.db")
        p = Path(raw)
        if not p.is_absolute():
            p = BASE_DIR / p
        return p

    @property
    def confirm_dangerous(self) -> bool:
        return bool(self.get("confirm_dangerous_actions", True))


# Instancia global accesible desde cualquier módulo
config = Config()
config.load()
