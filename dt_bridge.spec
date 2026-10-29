# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['dt_bridge.py'],
    pathex=[],
    binaries=[],
    datas=[('index.html', '.'), ('app-design.css', '.')],
    hiddenimports=[],
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
    name='dt_bridge',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['/Users/henry.f.hempeicloud.com/Desktop/Promt_Master/PromptMaster.icns'],
)
app = BUNDLE(
    exe,
    name='dt_bridge.app',
    icon='/Users/henry.f.hempeicloud.com/Desktop/Promt_Master/PromptMaster.icns',
    bundle_identifier='com.promptmaster.bridge',
)
