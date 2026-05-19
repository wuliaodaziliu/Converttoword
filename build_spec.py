import os

block_cipher = None

_src_dir = os.path.dirname(os.path.abspath(__file__))
_poppler_src = os.path.join(_src_dir, "poppler", "Library")
_poppler_data = [(_poppler_src, "poppler/Library")] if os.path.exists(_poppler_src) else []

a = Analysis(
    ['src/gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src', 'src'),
        ('requirements.txt', '.'),
    ] + _poppler_data,
    hiddenimports=['pdf2image', 'PIL', 'Pillow', 'docx'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='PDFToWordConverter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # DEBUG: 临时开启控制台查看错误
    one_file=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)