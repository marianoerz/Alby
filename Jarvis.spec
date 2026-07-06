# -*- mode: python ; coding: utf-8 -*-
# ══════════════════════════════════════════════════════════════════
# Jarvis.spec — Configuración de PyInstaller para generar Jarvis.exe
#
# Uso (en Windows, con el entorno virtual activado):
#     pyinstaller Jarvis.spec --noconfirm --clean
#
# El .exe resultante queda en dist\Jarvis\Jarvis.exe
# ══════════════════════════════════════════════════════════════════

import sys
from PyInstaller.utils.hooks import collect_all, collect_submodules

block_cipher = None

datas = []
binaries = []
hiddenimports = []

# Algunas librerías (edge_tts, pyttsx3, pycaw, comtypes, speech_recognition)
# usan importación dinámica o datos internos que PyInstaller no detecta solo.
for pkg in ("edge_tts", "pyttsx3", "speech_recognition", "pycaw", "comtypes", "certifi"):
    try:
        d, b, h = collect_all(pkg)
        datas += d
        binaries += b
        hiddenimports += h
    except Exception:
        pass

hiddenimports += collect_submodules("comtypes.stream")
hiddenimports += [
    "engineio.async_drivers",
    "pygame",
    "screen_brightness_control",
    "winshell",
    "win32com",
    "win32com.client",
    "win32timezone",
]

# Incluir el config.json inicial y assets del proyecto
datas += [
    ("config.json", "."),
    ("assets", "assets"),
]

a = Analysis(
    ["app.py"],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Jarvis",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,          # Ventana sin consola (app de escritorio)
    icon=None,              # Agrega aquí la ruta a un .ico si tienes uno
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="Jarvis",
)
