# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(sys.getrecursionlimit() * 5)

# Path to the Vosk model directory (update with the actual path on your local disk)
model_path = 'C:/vosk-model-small-en-us-0.15'  # Adjust as necessary

a = Analysis(
    ['gideon.py'],
    pathex=[],  # Optional path(s) to add if needed for locating dependencies
    binaries=[('C:\\Users\\HIRRO_TWO\\anaconda3\\Lib\\site-packages\\vosk', 'vosk')],  # Vosk binary path
    datas=[(model_path, 'vosk-model')],  # Path to Vosk model folder
    hiddenimports=['vosk', 'pyaudio', 'pyttsx3', 'speech_recognition'],  # Required modules
    hookspath=[],  # Paths to PyInstaller hooks if any custom ones are used
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],  # List of modules to exclude if needed
    noarchive=False,
    optimize=1,  # You can set optimize=1 for basic optimization
)

# Bundle the analyzed files into a single package
pyz = PYZ(a.pure)

# Define executable settings
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='gideon',            # Name of the output executable
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False to hide console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
