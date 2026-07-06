# Cómo generar Jarvis.exe

Este proyecto usa librerías **exclusivas de Windows** (`pycaw`, `comtypes`,
`winshell`, control nativo de volumen/brillo). Por eso el `.exe` final debe
compilarse **en una máquina Windows** (o en un runner de Windows, como GitHub
Actions) — no se puede generar un `.exe` de Windows real desde Linux/macOS,
sin importar la herramienta que se use.

Ya dejé todo listo para que lo compiles en 1-2 pasos. Tienes dos opciones:

## Opción A — Compilar en tu PC con Windows (más simple)

1. Copia la carpeta `Jarvis/` a tu PC con Windows.
2. Ejecuta `install.bat` (crea el entorno virtual e instala dependencias).
3. Activa el entorno virtual e instala PyInstaller:
   ```
   venv\Scripts\activate
   pip install pyinstaller pywin32
   ```
4. Compila:
   ```
   pyinstaller Jarvis.spec --noconfirm --clean
   ```
5. El ejecutable queda en `dist\Jarvis\Jarvis.exe`. Cópiate toda la carpeta
   `dist\Jarvis\` (no solo el .exe) — ahí van las DLLs y datos necesarios.

## Opción B — Compilar automáticamente con GitHub Actions (sin tocar Windows)

Ya incluí el workflow `.github/workflows/build-windows.yml`. Solo tienes que:

1. Subir este proyecto a un repositorio de GitHub.
2. Ir a la pestaña **Actions** → **Build Jarvis.exe (Windows)** → **Run workflow**.
   (También se dispara solo si subes un tag tipo `v1.0.0`.)
3. Cuando termine (unos 3-5 min), descarga el artefacto `Jarvis-Windows` desde
   esa misma ejecución: ahí está `Jarvis-Windows.zip` con el `.exe` listo.

Esto compila en un runner Windows real de GitHub, así que el .exe queda
100% funcional con pycaw/comtypes/winshell incluidos.

## Notas importantes

- **Persistencia de datos arreglada**: antes, si empaquetabas con PyInstaller
  en modo onefile, `config.json`, la base de datos de memoria y los logs se
  guardaban dentro de la carpeta temporal de extracción (que se borra al
  cerrar el programa) — perdías la configuración y el historial en cada
  ejecución. Ya corregí `config.py` y `app.py` para que, al estar empaquetado,
  usen la carpeta donde vive el `.exe` en vez de la carpeta temporal.
- Si quieres un ícono personalizado, coloca un `.ico` en `assets/` y cambia
  la línea `icon=None` en `Jarvis.spec` por `icon="assets/jarvis.ico"`.
- Antes de compilar, no olvides poner tu API key (OpenAI, DeepSeek, etc.) en
  `config.json` o dejar que el usuario la configure desde la ventana de
  Configuración de la app.
