# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=['.'],  # Ensure pathex points to the current directory
    binaries=[],
    datas=[
        ('qa_model/*', 'qa_model'),  # Include all files from qa_model folder
        ('pdf_to_text.py', '.'),  # Include the custom pdf_to_text.py script
        ('qa_icon.ico', '.'),  # Include the icon file
    ],
    hiddenimports=['pdf_to_text', 'fitz', 'transformers'],  # Add any hidden imports
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=True,
    strip=False,
    upx=True,  # Set to True if you want UPX compression
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['qa_icon.ico'],  # Ensure the icon file path is correct
)
