# JARVIS — Asistente Virtual para Windows

> **J**ust **A** **R**ather **V**ery **I**ntelligent **S**ystem

Asistente virtual de escritorio inspirado en el JARVIS de Iron Man, con interfaz gráfica futurista, reconocimiento de voz continuo, síntesis de voz natural en español e integración con múltiples proveedores de inteligencia artificial.

---

## Características principales

| Módulo | Descripción |
|---|---|
| **Interfaz gráfica** | PySide6 con tema oscuro futurista, animaciones y efectos de brillo |
| **Reconocimiento de voz** | Escucha continua con wake word configurable ("Jarvis") |
| **Síntesis de voz** | Edge TTS con voces neurales de alta calidad en español |
| **Inteligencia Artificial** | OpenAI, DeepSeek, Ollama y LM Studio intercambiables |
| **Memoria** | Historial de conversaciones y preferencias en SQLite |
| **Control del sistema** | Volumen, brillo, capturas, apagado, procesos y más |
| **Sistema de archivos** | Abrir, crear, copiar, mover y eliminar archivos/carpetas |
| **Internet** | Clima (OpenWeatherMap), noticias (NewsAPI) y búsqueda web |

---

## Requisitos del sistema

- **Sistema operativo:** Windows 10 o Windows 11 (64 bits)
- **Python:** 3.12 o superior
- **RAM:** 4 GB mínimo (8 GB recomendado)
- **Espacio en disco:** 500 MB para el entorno virtual y dependencias
- **Micrófono:** Requerido para el reconocimiento de voz
- **Altavoces/auriculares:** Requeridos para la síntesis de voz
- **Conexión a internet:** Requerida para Edge TTS, IA en la nube y consultas web

---

## Instalación

### Paso 1 — Instalar Python

Descarga e instala Python 3.12 o superior desde [python.org](https://www.python.org/downloads/).

**Importante:** Durante la instalación, marca la opción **"Add Python to PATH"**.

### Paso 2 — Descargar Jarvis

Descarga el proyecto y extrae el contenido en una carpeta de tu elección, por ejemplo `C:\Jarvis`.

### Paso 3 — Instalar dependencias

Haz doble clic en `install.bat` o ejecuta en una terminal:

```bat
cd C:\Jarvis
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

> **Nota sobre PyAudio:** Si la instalación de PyAudio falla, descarga el archivo `.whl` correspondiente a tu versión de Python desde [este repositorio](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) e instálalo manualmente:
> ```bat
> pip install PyAudio-0.2.14-cp312-cp312-win_amd64.whl
> ```

### Paso 4 — Configurar la API Key

Abre `config.json` con cualquier editor de texto y agrega tu clave de API:

```json
{
    "ai_provider": "openai",
    "ai_model": "gpt-4o-mini",
    "openai_api_key": "sk-TU_CLAVE_AQUI"
}
```

### Paso 5 — Ejecutar Jarvis

Haz doble clic en `jarvis.bat` o ejecuta:

```bat
venv\Scripts\activate
python app.py
```

---

## Configuración

Toda la configuración se gestiona desde el archivo `config.json` o desde la interfaz gráfica (botón ⚙ en la ventana principal).

### Parámetros principales

| Parámetro | Descripción | Valor predeterminado |
|---|---|---|
| `ai_provider` | Proveedor de IA activo | `openai` |
| `ai_model` | Modelo de IA a utilizar | `gpt-4o-mini` |
| `ai_temperature` | Creatividad de las respuestas (0.0–2.0) | `0.7` |
| `ai_max_tokens` | Tokens máximos por respuesta | `1024` |
| `wake_word` | Palabra de activación | `jarvis` |
| `tts_voice` | Voz de Edge TTS | `es-MX-JorgeNeural` |
| `tts_rate` | Velocidad de la voz | `+0%` |
| `tts_volume` | Volumen de la voz | `+0%` |
| `tts_pitch` | Tono de la voz | `+0Hz` |
| `user_name` | Nombre del usuario | `Usuario` |
| `weather_city` | Ciudad para el clima | `Buenos Aires` |

### Cambiar proveedor de IA

Para cambiar de OpenAI a DeepSeek, edita `config.json`:

```json
{
    "ai_provider": "deepseek",
    "ai_model": "deepseek-chat",
    "deepseek_api_key": "sk-TU_CLAVE_DEEPSEEK"
}
```

Para usar Ollama (local, sin internet):

```json
{
    "ai_provider": "ollama",
    "ai_model": "llama3",
    "ollama_base_url": "http://localhost:11434"
}
```

Para usar LM Studio (local, sin internet):

```json
{
    "ai_provider": "lmstudio",
    "ai_model": "local-model",
    "lmstudio_base_url": "http://localhost:1234"
}
```

---

## Uso

### Interfaz gráfica

La ventana principal contiene:

- **Panel de estado** (izquierda): Indicador animado del estado del asistente y visualizador de onda de audio.
- **Panel de chat** (centro): Historial completo de conversaciones con soporte de streaming.
- **Campo de texto** (inferior): Escribe mensajes directamente.
- **Botón de micrófono** 🎤: Activa/desactiva el reconocimiento de voz continuo.
- **Botón de configuración** ⚙: Abre el panel de configuración completo.

### Reconocimiento de voz

1. Haz clic en el botón 🎤 para activar el micrófono.
2. Di **"Jarvis"** o **"Hey Jarvis"** para activar el asistente.
3. Habla tu comando o pregunta.
4. Jarvis responderá por voz y mostrará el texto en el chat.

### Comandos de voz disponibles

#### Control del sistema

| Comando | Acción |
|---|---|
| "Abre Chrome" | Abre Google Chrome |
| "Cierra Notepad" | Cierra el Bloc de notas |
| "Sube el volumen" | Aumenta el volumen del sistema |
| "Baja el volumen" | Reduce el volumen del sistema |
| "Silencia" | Silencia el audio |
| "Toma una captura" | Captura de pantalla en el escritorio |
| "Apaga el PC" | Apaga el equipo (con confirmación) |
| "Reinicia el PC" | Reinicia el equipo (con confirmación) |
| "Suspende el PC" | Suspende el equipo |
| "Bloquea la pantalla" | Bloquea Windows |
| "Abre el administrador de tareas" | Abre el Task Manager |
| "Abre CMD" | Abre el símbolo del sistema |
| "Abre PowerShell" | Abre PowerShell |

#### Sistema de archivos

| Comando | Acción |
|---|---|
| "Abre la carpeta Descargas" | Abre la carpeta de Descargas |
| "Abre la carpeta Documentos" | Abre la carpeta de Documentos |
| "Vacía la papelera" | Vacía la papelera de reciclaje |

#### Internet

| Comando | Acción |
|---|---|
| "¿Cómo está el clima?" | Muestra el clima de la ciudad configurada |
| "Últimas noticias" | Muestra los titulares más recientes |
| "Busca en internet Python" | Busca en Google |
| "Wikipedia inteligencia artificial" | Busca en Wikipedia |

---

## Voces disponibles

Jarvis utiliza Edge TTS con voces neurales de Microsoft. Las voces en español disponibles son:

| Nombre en la UI | ID de voz | Región |
|---|---|---|
| Jorge (México, Masculino) | `es-MX-JorgeNeural` | México |
| Dalia (México, Femenino) | `es-MX-DaliaNeural` | México |
| Álvaro (España, Masculino) | `es-ES-AlvaroNeural` | España |
| Elvira (España, Femenino) | `es-ES-ElviraNeural` | España |
| Andrés (Colombia, Masculino) | `es-CO-GonzaloNeural` | Colombia |
| Salome (Colombia, Femenino) | `es-CO-SalomeNeural` | Colombia |
| Lupe (Argentina, Femenino) | `es-AR-ElenaNeural` | Argentina |
| Tomás (Argentina, Masculino) | `es-AR-TomasNeural` | Argentina |

Para cambiar la voz, usa el panel de configuración (⚙) o edita `config.json`.

---

## Estructura del proyecto

```
Jarvis/
├── app.py                    # Punto de entrada principal
├── brain.py                  # Cerebro central: coordina todos los módulos
├── config.py                 # Gestor de configuración (singleton)
├── config.json               # Archivo de configuración del usuario
├── requirements.txt          # Dependencias Python
├── install.bat               # Script de instalación para Windows
├── jarvis.bat                # Script de inicio para Windows
├── LICENSE                   # Licencia MIT
├── README.md                 # Esta documentación
│
├── ai/                       # Módulos de inteligencia artificial
│   ├── __init__.py           # Fábrica de proveedores (get_provider)
│   ├── base_provider.py      # Clase base abstracta
│   ├── openai_provider.py    # Proveedor OpenAI
│   ├── deepseek_provider.py  # Proveedor DeepSeek
│   ├── ollama_provider.py    # Proveedor Ollama (local)
│   └── lmstudio_provider.py  # Proveedor LM Studio (local)
│
├── voice/                    # Módulos de voz
│   ├── __init__.py
│   ├── text_to_speech.py     # Síntesis de voz (Edge TTS + pyttsx3)
│   ├── speech_to_text.py     # Reconocimiento de voz continuo
│   └── wakeword.py           # Detector de wake word y gestor de estados
│
├── memory/                   # Módulos de memoria y persistencia
│   ├── __init__.py
│   ├── database.py           # Capa SQLite
│   └── memory.py             # Gestor de memoria de alto nivel
│
├── system/                   # Control del sistema operativo
│   ├── __init__.py
│   ├── actions.py            # Acciones del sistema (volumen, energía, etc.)
│   ├── filesystem.py         # Operaciones de archivos y carpetas
│   └── processes.py          # Gestión de procesos
│
├── internet/                 # Módulos de internet
│   ├── __init__.py
│   ├── weather.py            # Consultas de clima (OpenWeatherMap)
│   ├── news.py               # Noticias (NewsAPI)
│   └── search.py             # Búsqueda web y Wikipedia
│
├── gui/                      # Interfaz gráfica
│   ├── __init__.py
│   ├── main_window.py        # Ventana principal
│   ├── settings_window.py    # Ventana de configuración
│   └── widgets.py            # Widgets personalizados animados
│
├── themes/                   # Temas visuales
│   ├── __init__.py
│   └── dark_jarvis.py        # Tema oscuro futurista (QSS)
│
├── assets/                   # Recursos estáticos (iconos, imágenes)
├── memory/                   # Base de datos SQLite (generada automáticamente)
└── logs/                     # Archivos de log (generados automáticamente)
```

---

## Personalización

### Agregar nuevos comandos

Para agregar un comando personalizado, edita `brain.py` en la sección `_COMMAND_PATTERNS` y registra un manejador en `gui/main_window.py`:

```python
# En brain.py, agregar en _COMMAND_PATTERNS:
("mi_comando", [r"mi patrón de voz (.+)"]),

# En gui/main_window.py, en _register_command_handlers():
"mi_comando": lambda i, p: mi_funcion(p),
```

### Agregar un nuevo proveedor de IA

1. Crea un archivo `ai/mi_proveedor.py` que herede de `BaseAIProvider`.
2. Implementa los métodos `chat()`, `list_models()` y la propiedad `name`.
3. Registra el proveedor en `ai/__init__.py`:

```python
from ai.mi_proveedor import MiProveedor
PROVIDERS["mi_proveedor"] = MiProveedor
```

### Crear un nuevo tema visual

1. Crea `themes/mi_tema.py` con una función `get_stylesheet()` que devuelva una cadena QSS.
2. Importa y aplica el tema en `gui/main_window.py`.

---

## APIs externas (opcionales)

Jarvis puede funcionar sin estas APIs, pero las siguientes funciones las requieren:

| API | Función | Registro gratuito |
|---|---|---|
| **OpenWeatherMap** | Consultas de clima | [openweathermap.org](https://openweathermap.org/api) |
| **NewsAPI** | Titulares de noticias | [newsapi.org](https://newsapi.org/register) |
| **OpenAI** | IA en la nube | [platform.openai.com](https://platform.openai.com) |
| **DeepSeek** | IA en la nube | [platform.deepseek.com](https://platform.deepseek.com) |

---

## Resolución de problemas

### Jarvis no responde por voz

1. Verifica que el micrófono esté conectado y configurado como dispositivo predeterminado en Windows.
2. Asegúrate de que PyAudio esté instalado correctamente.
3. Ajusta el **umbral de energía** en la configuración (valor más bajo = más sensible).
4. Verifica que el idioma del reconocimiento coincida con tu acento.

### Error "No module named 'PyAudio'"

PyAudio requiere compilación en Windows. Instala la versión precompilada:

```bat
pip install pipwin
pipwin install pyaudio
```

O descarga el `.whl` desde [Gohlke's Unofficial Binaries](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio).

### Error de API Key

Verifica que la clave de API esté correctamente copiada en `config.json` sin espacios adicionales.

### La voz suena robótica

Asegúrate de que `tts_engine` esté configurado como `edge` y que tengas conexión a internet. Edge TTS requiere internet para generar las voces neurales.

### Jarvis no puede controlar el volumen

Instala pycaw y sus dependencias:

```bat
pip install pycaw comtypes
```

### Error al abrir la ventana principal

Revisa el archivo `logs/jarvis.log` para obtener detalles del error. Los problemas más comunes son:
- PySide6 no instalado correctamente.
- Conflicto con otras versiones de Qt.

---

## Actualización

Para actualizar las dependencias a las versiones más recientes:

```bat
venv\Scripts\activate
pip install -r requirements.txt --upgrade
```

---

## Licencia

Este proyecto está licenciado bajo la **Licencia MIT**. Consulta el archivo `LICENSE` para más detalles.

---

*Jarvis — Desarrollado con Python, PySide6 y pasión por la IA.*
