# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

_src_dir = os.path.abspath(globals().get("SPECPATH", os.getcwd()))
_poppler_src = os.path.join(_src_dir, "poppler", "Library")
_required_poppler_tools = [
    os.path.join(_poppler_src, "bin", "pdfinfo.exe"),
    os.path.join(_poppler_src, "bin", "pdftoppm.exe"),
]
_missing_poppler_tools = [path for path in _required_poppler_tools if not os.path.exists(path)]
if _missing_poppler_tools:
    raise FileNotFoundError(
        "Missing Poppler files required for packaging: " + ", ".join(_missing_poppler_tools)
    )
_poppler_data = [(_poppler_src, "poppler/Library")]

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[
        ("src", "src"),
        ("requirements.txt", "."),
    ] + _poppler_data,
    hiddenimports=["pdf2image", "PIL", "Pillow", "docx"],
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
    name="PDFToWordConverter",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="icon.ico" if os.path.exists("icon.ico") else None,
)
