# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

exe_name = "Genshin_Impact_Tools"

src_root_dir = "src/genshin/"

file_list = [
    src_root_dir + "__init__.py",
    src_root_dir + "main.py",

    src_root_dir + "config/__init__.py",
    src_root_dir + "config/global_setting.py",
    src_root_dir + "config/user_setting.py",
    
    src_root_dir + "core/__init__.py",
    src_root_dir + "core/function.py",
    src_root_dir + "core/log.py",

    src_root_dir + "module/__init__.py",
    src_root_dir + "module/clipboard.py",
    src_root_dir + "module/menu.py",
    src_root_dir + "module/user.py",
    src_root_dir + "module/update.py",

    src_root_dir + "module/gacha/__init__.py",
    src_root_dir + "module/gacha/data_transform.py",
    src_root_dir + "module/gacha/gacha_log.py",
    src_root_dir + "module/gacha/gacha_url.py",
    src_root_dir + "module/gacha/metadata.py",
    src_root_dir + "module/gacha/report_gengrator.py",
]

icon_path = "resource/ys.ico"

global_config = "src/genshin/config/global_setting.py"

data_list = [
    (icon_path, icon_path),
    (global_config, "genshin/config")
]

a = Analysis(
    file_list,
    pathex=[],
    binaries=[],
    datas=data_list,
    hiddenimports=[],
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
    name=exe_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)
