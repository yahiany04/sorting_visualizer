# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=['c:\\Users\\Computec\\Downloads\\algos\\algorithem'],
    binaries=[],
    datas=[
        ('visualizer.py', '.'),
        ('bubble_sort.py', '.'),
        ('selection_sort.py', '.'),
        ('insertion_sort.py', '.'),
        ('merge_sort.py', '.'),
        ('quick_sort.py', '.'),
    ],
    hiddenimports=['visualizer', 'bubble_sort', 'selection_sort', 'insertion_sort', 'merge_sort', 'quick_sort'],
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
