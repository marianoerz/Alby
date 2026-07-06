"""
app.py — Punto de entrada principal de Jarvis.

Inicializa el sistema de logging, carga la configuración, crea la
aplicación Qt y lanza la ventana principal.

Uso:
    python app.py
"""

import logging
import sys
import os
from pathlib import Path

# ── Asegurar que el directorio del proyecto esté en el path ──────────────────
if getattr(sys, "frozen", False):
    # Empaquetado con PyInstaller: usar la carpeta del ejecutable para
    # datos persistentes (logs, config, memoria), y el bundle interno
    # (_MEIPASS) para localizar los módulos ya incluidos en el exe.
    BASE_DIR = Path(sys.executable).parent.resolve()
    MEIPASS = Path(getattr(sys, "_MEIPASS", BASE_DIR))
    if str(MEIPASS) not in sys.path:
        sys.path.insert(0, str(MEIPASS))
else:
    BASE_DIR = Path(__file__).parent.resolve()
    if str(BASE_DIR) not in sys.path:
        sys.path.insert(0, str(BASE_DIR))


def setup_logging() -> None:
    """Configura el sistema de logging de la aplicación."""
    from config import config

    log_level_str = config.get("log_level", "INFO")
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)

    # Crear directorio de logs
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "jarvis.log"

    # Formato de log
    fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    date_fmt = "%Y-%m-%d %H:%M:%S"

    # Handlers: consola + archivo rotativo
    handlers: list[logging.Handler] = [
        logging.StreamHandler(sys.stdout),
    ]

    try:
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=3,
            encoding="utf-8",
        )
        handlers.append(file_handler)
    except Exception:
        pass

    logging.basicConfig(
        level=log_level,
        format=fmt,
        datefmt=date_fmt,
        handlers=handlers,
    )

    # Silenciar loggers muy verbosos de librerías externas
    for noisy in ("urllib3", "httpx", "httpcore", "openai", "edge_tts"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    logging.info("=" * 60)
    logging.info("Jarvis iniciando...")
    logging.info("Directorio base: %s", BASE_DIR)
    logging.info("Python: %s", sys.version)
    logging.info("=" * 60)


def check_dependencies() -> bool:
    """
    Verifica que las dependencias críticas estén instaladas.
    Devuelve True si todo está bien, False si falta algo crítico.
    """
    critical = ["PySide6"]
    missing = []

    for pkg in critical:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)

    if missing:
        print(f"ERROR: Faltan dependencias críticas: {', '.join(missing)}")
        print("Ejecuta: pip install -r requirements.txt")
        return False

    # Advertencias por dependencias opcionales
    optional_warnings = {
        "edge_tts": "Edge TTS no disponible. Se usará pyttsx3 como motor de voz.",
        "speech_recognition": "SpeechRecognition no disponible. El micrófono no funcionará.",
        "pygame": "pygame no disponible. El audio puede no reproducirse correctamente.",
    }

    for pkg, warning in optional_warnings.items():
        try:
            __import__(pkg)
        except ImportError:
            logging.warning("⚠ %s", warning)

    return True


def main() -> None:
    """Función principal de la aplicación."""
    # Cargar configuración primero (necesaria para logging)
    from config import config
    config.load()

    # Configurar logging
    setup_logging()

    # Verificar dependencias
    if not check_dependencies():
        sys.exit(1)

    # Importar Qt después de verificar dependencias
    try:
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt
        from PySide6.QtGui import QFont
    except ImportError as exc:
        print(f"ERROR: No se pudo importar PySide6: {exc}")
        print("Instala con: pip install PySide6")
        sys.exit(1)

    # Crear aplicación Qt
    app = QApplication(sys.argv)
    app.setApplicationName("Jarvis")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Jarvis AI")

    # Habilitar escalado de alta resolución (DPI)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Fuente predeterminada
    font_size = config.get("font_size", 13)
    font = QFont("Segoe UI", font_size)
    app.setFont(font)

    # Crear y mostrar la ventana principal
    try:
        from gui.main_window import MainWindow
        window = MainWindow()
        window.show()
        logging.info("Ventana principal mostrada.")
    except Exception as exc:
        logging.critical("Error al crear la ventana principal: %s", exc, exc_info=True)
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.critical(
            None,
            "Error al iniciar Jarvis",
            f"No se pudo iniciar la interfaz gráfica:\n\n{exc}\n\n"
            "Revisa el archivo logs/jarvis.log para más detalles.",
        )
        sys.exit(1)

    # Ejecutar el bucle de eventos
    exit_code = app.exec()
    logging.info("Jarvis cerrado con código: %d", exit_code)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
