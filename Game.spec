# -*- mode: python ; coding: utf-8 -*-
import os

# Get the directory of this spec file
block_cipher = None
spec_root = os.path.abspath(SPECPATH)

a = Analysis(
    ['main.py'],
    pathex=[spec_root],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('scenes', 'scenes'),
    ],
    hiddenimports=[
        'pygame',
        'pygame.mixer',
        'pygame.font',
        'pygame.image',
        'pygame.transform',
        'pygame.display',
        'pygame.event',
        'pygame.key',
        'pygame.time',
        'pygame.surface',
        'pygame.rect',
        'pygame.sprite',
        'pygame.mask',
        'scenes.main_game',
        'scenes.dino',
        'scenes.obstacles',
        'scenes.tokens',
        'scenes.background',
        'scenes.hud',
        'scenes.game_over',
        'scenes.game_object',
        'scenes.path_utils',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'PIL',
        'cv2',
        'tensorflow',
        'torch',
        'sklearn',
        'IPython',
        'jupyter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DinoRun',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # You can add an icon file path here if you have one
)
