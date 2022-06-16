from kivy_deps import sdl2, glew
import os
from os.path import join

# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['snmpXL.py'],
    pathex=[os.getcwd()],
    binaries=[],
    datas=[],
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

a.datas += [('Code\v3_tools.py', 'C:\\Users\\S356430\\Documents\\VSCode\\snmpXL\v3_tools.py', 'DATA')]
a.datas += [('Code\excel_integration.py', 'C:\\Users\\S356430\\Documents\\VSCode\\snmpXL\excel_integration.py', 'DATA')]
a.datas += [('Code\isnmpXL.ico', 'C:\\Users\\S356430\\Documents\\VSCode\\snmpXL\\images\snmpXL.ico', 'DATA')]

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='snmpXL',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
	icon = 'C:\\Users\\S356430\\Documents\\VSCode\\snmpXL\\images\snmpXL.ico',
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
	Tree('C:\\Users\\S356430\\Documents\\VSCode\\snmpXL\\'),
    a.binaries,
    a.zipfiles,
    a.datas,
	*[Tree(p) for p in
	(sdl2.dep_bins + 
	glew.dep_bins)],
    strip=False,
    upx=True,
    upx_exclude=[],
    name='snmpXL',
)
