# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = []
hiddenimports += collect_submodules('visualizer')
hiddenimports += collect_submodules('bubble_sort')
hiddenimports += collect_submodules('selection_sort')
hiddenimports += collect_submodules('insertion_sort')
hiddenimports += collect_submodules('merge_sort')
hiddenimports += collect_submodules('quick_sort')


a = Analysis(
    ['main.py'],
    pathex=['c:\\Users\\Computec\\Downloads\\algorithem (1)\\algorithem'],
    binaries=[],
    datas=[],
    hiddenimports=hiddenimports,
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
    name='SortingVisualizer',
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
)
