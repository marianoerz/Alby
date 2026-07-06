"""
brain.py — Cerebro central de Jarvis.

Coordina la inteligencia artificial, la memoria, el procesamiento de
comandos del sistema y las consultas a internet. Es el núcleo que
recibe texto del usuario y produce una respuesta apropiada.
"""

import logging
import re
from typing import Callable, Optional

from config import config
from memory.memory import Memory
from ai import get_provider

logger = logging.getLogger(__name__)

# ── Prompt del sistema ────────────────────────────────────────────────────────

SYSTEM_PROMPT_TEMPLATE = """Eres Jarvis, un asistente virtual inteligente, sofisticado y amigable, inspirado en el asistente de Iron Man.

Tu personalidad:
- Eres profesional, eficiente y ligeramente ingenioso.
- Hablas siempre en español, con naturalidad y fluidez.
- Eres proactivo: si puedes ayudar más allá de lo pedido, lo haces.
- Tratas al usuario con respeto y calidez.
- Cuando no sabes algo, lo admites con honestidad.
- Eres conciso en tus respuestas de voz (máximo 3-4 oraciones), pero puedes ser más detallado por escrito.

Información del usuario:
- Nombre: {user_name}

{memory_summary}

Instrucciones:
- Responde siempre en español.
- Para comandos del sistema (abrir programas, controlar volumen, etc.), responde con JSON estructurado cuando sea necesario.
- Mantén el contexto de la conversación.
- Si el usuario menciona información personal importante, recuérdala.
- Fecha y hora actual: {datetime}
"""


class Brain:
    """
    Cerebro de Jarvis: procesa entradas del usuario y genera respuestas.

    Gestiona el contexto de conversación, detecta intenciones de comandos
    del sistema y coordina todos los módulos del asistente.
    """

    def __init__(self) -> None:
        self.memory = Memory()
        self._provider = None
        self._command_handlers: dict[str, Callable] = {}
        logger.info("Cerebro de Jarvis inicializado.")

    # ── Proveedor de IA ───────────────────────────────────────────────────────

    @property
    def provider(self):
        """Devuelve el proveedor de IA activo, recargándolo si cambió."""
        current_name = config.ai_provider
        if self._provider is None or self._provider.name != current_name:
            logger.info("Cargando proveedor de IA: %s", current_name)
            self._provider = get_provider(current_name)
        return self._provider

    def reload_provider(self) -> None:
        """Fuerza la recarga del proveedor de IA."""
        self._provider = None

    # ── Registro de manejadores de comandos ──────────────────────────────────

    def register_command_handler(self, intent: str, handler: Callable) -> None:
        """
        Registra una función que maneja un tipo específico de comando.

        Args:
            intent:  Nombre de la intención (ej: 'open_app', 'weather').
            handler: Función que recibe (intent, params) y ejecuta la acción.
        """
        self._command_handlers[intent] = handler
        logger.debug("Manejador registrado para intención: %s", intent)

    # ── Procesamiento de mensajes ─────────────────────────────────────────────

    def process(
        self,
        user_input: str,
        on_token: Optional[Callable[[str], None]] = None,
    ) -> str:
        """
        Procesa la entrada del usuario y devuelve la respuesta de Jarvis.

        Args:
            user_input: Texto del usuario.
            on_token:   Callback opcional llamado con cada fragmento de texto
                        generado (para streaming en la UI).

        Returns:
            Respuesta completa como cadena de texto.
        """
        if not user_input.strip():
            return ""

        logger.info("Procesando entrada: %s", user_input[:80])

        # 1. Guardar mensaje del usuario en memoria
        self.memory.add_user_message(user_input)

        # 2. Intentar detectar y ejecutar un comando del sistema
        command_response = self._try_execute_command(user_input)
        if command_response is not None:
            self.memory.add_assistant_message(command_response)
            return command_response

        # 3. Construir mensajes para la IA
        messages = self._build_messages()

        # 4. Obtener respuesta de la IA
        try:
            if on_token is not None:
                # Modo streaming: emitir tokens en tiempo real
                full_response = ""
                gen = self.provider.chat(messages, stream=True)
                for token in gen:
                    full_response += token
                    on_token(token)
                response = full_response
            else:
                response = self.provider.chat(messages, stream=False)
                if not isinstance(response, str):
                    # Si por alguna razón devuelve un generador, consumirlo
                    response = "".join(response)
        except Exception as exc:
            logger.error("Error al obtener respuesta de la IA: %s", exc)
            response = (
                f"Lo siento, {self.memory.user_name}, tuve un problema al procesar "
                f"tu solicitud: {exc}. Por favor, verifica la configuración del proveedor de IA."
            )

        # 5. Guardar respuesta en memoria
        self.memory.add_assistant_message(response)

        # 6. Detectar y guardar información personal mencionada
        self._extract_and_remember(user_input, response)

        return response

    # ── Construcción del contexto ─────────────────────────────────────────────

    def _build_messages(self) -> list[dict]:
        """Construye la lista de mensajes para enviar a la IA."""
        from datetime import datetime

        # Prompt del sistema con contexto personalizado
        system_content = SYSTEM_PROMPT_TEMPLATE.format(
            user_name=self.memory.user_name,
            memory_summary=self.memory.get_memory_summary(),
            datetime=datetime.now().strftime("%A, %d de %B de %Y, %H:%M"),
        )

        # Historial de conversación reciente
        history = self.memory.get_context_messages()

        # Construir lista: sistema + historial
        messages: list[dict] = [{"role": "system", "content": system_content}]
        messages.extend(history)

        return messages

    # ── Detección de comandos ─────────────────────────────────────────────────

    # Patrones para detectar comandos del sistema en el texto del usuario
    _COMMAND_PATTERNS: list[tuple[str, list[str]]] = [
        ("open_app", [
            r"abre?\s+(.+)",
            r"ejecuta?\s+(.+)",
            r"inicia?\s+(.+)",
            r"lanza?\s+(.+)",
        ]),
        ("close_app", [
            r"cierra?\s+(.+)",
            r"termina?\s+(.+)",
            r"mata?\s+el proceso\s+(.+)",
        ]),
        ("open_url", [
            r"abre?\s+(https?://\S+)",
            r"navega?\s+a\s+(.+)",
            r"ve\s+a\s+(.+)",
            r"busca?\s+en\s+google\s+(.+)",
        ]),
        ("volume_up", [r"sube?\s+el\s+volumen", r"aumenta?\s+el\s+volumen"]),
        ("volume_down", [r"baja?\s+el\s+volumen", r"reduce?\s+el\s+volumen"]),
        ("volume_mute", [r"silencia?", r"mutea?"]),
        ("screenshot", [r"toma?\s+una?\s+captura", r"screenshot", r"captura\s+de\s+pantalla"]),
        ("shutdown", [r"apaga?\s+(?:el\s+)?(?:pc|computadora|windows|equipo)"]),
        ("restart", [r"reinicia?\s+(?:el\s+)?(?:pc|computadora|windows|equipo)"]),
        ("sleep", [r"suspende?\s+(?:el\s+)?(?:pc|computadora|equipo)", r"modo\s+suspensión"]),
        ("lock", [r"bloquea?\s+(?:la\s+)?(?:pantalla|pc|computadora)"]),
        ("open_folder", [r"abre?\s+(?:la\s+)?carpeta\s+(.+)"]),
        ("weather", [r"(?:qué|como está|cómo está)\s+el\s+clima", r"temperatura\s+(?:en\s+)?(.+)?", r"va\s+a\s+llover"]),
        ("news", [r"(?:últimas?\s+)?noticias", r"qué\s+pasó\s+hoy", r"novedades"]),
        ("search_web", [r"busca?\s+(?:en\s+internet\s+)?(.+)", r"qué\s+es\s+(.+)"]),
        ("wikipedia", [r"(?:busca?\s+en\s+)?wikipedia\s+(.+)", r"según\s+wikipedia\s+(.+)"]),
        ("task_manager", [r"administrador\s+de\s+tareas", r"task\s+manager"]),
        ("cmd", [r"abre?\s+(?:el\s+)?cmd", r"abre?\s+(?:el\s+)?símbolo\s+del\s+sistema"]),
        ("powershell", [r"abre?\s+(?:el\s+)?powershell"]),
        ("empty_trash", [r"vacía?\s+(?:la\s+)?papelera"]),
    ]

    def _try_execute_command(self, text: str) -> Optional[str]:
        """
        Intenta detectar un comando del sistema en el texto del usuario.

        Devuelve la respuesta del comando si se detectó y ejecutó,
        o None si no se detectó ningún comando conocido.
        """
        text_lower = text.lower().strip()

        for intent, patterns in self._COMMAND_PATTERNS:
            for pattern in patterns:
                match = re.search(pattern, text_lower, re.IGNORECASE)
                if match:
                    params = match.group(1) if match.lastindex else ""
                    handler = self._command_handlers.get(intent)
                    if handler:
                        logger.info("Comando detectado: %s (params: %s)", intent, params)
                        try:
                            return handler(intent, params.strip())
                        except Exception as exc:
                            logger.error("Error ejecutando comando %s: %s", intent, exc)
                            return f"Tuve un problema al ejecutar ese comando: {exc}"
                    # Si no hay manejador registrado, dejar que la IA responda
                    break

        return None

    # ── Extracción de información personal ───────────────────────────────────

    def _extract_and_remember(self, user_input: str, response: str) -> None:
        """
        Detecta y guarda información personal mencionada por el usuario.
        """
        text = user_input.lower()

        # Detectar nombre del usuario
        name_match = re.search(
            r"(?:me\s+llamo|mi\s+nombre\s+es|soy)\s+([A-ZÁÉÍÓÚÑa-záéíóúñ]+)",
            user_input,
            re.IGNORECASE,
        )
        if name_match:
            name = name_match.group(1).capitalize()
            self.memory.user_name = name
            config.set("user_name", name)
            logger.info("Nombre del usuario actualizado: %s", name)

        # Detectar preferencias explícitas
        pref_match = re.search(
            r"(?:recuerda\s+que|no\s+olvides\s+que|anota\s+que)\s+(.+)",
            user_input,
            re.IGNORECASE,
        )
        if pref_match:
            fact = pref_match.group(1).strip()
            self.memory.remember(fact, category="preferencia")

    # ── Utilidades ────────────────────────────────────────────────────────────

    def clear_conversation(self) -> None:
        """Borra el historial de conversación actual."""
        self.memory.clear_history()
        logger.info("Conversación borrada.")

    def get_history(self) -> list[dict]:
        """Devuelve el historial completo de la conversación."""
        return self.memory.get_all_history()

    def close(self) -> None:
        """Libera recursos."""
        self.memory.close()
