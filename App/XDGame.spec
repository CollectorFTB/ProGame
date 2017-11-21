# -*- mode: python -*-
from kivy.deps import sdl2, glew
import cv2
import numpy
block_cipher = None


a = Analysis(['D:\\Desktop shortcuts\\Collection\\Python Projects\\ProGame\\main.py'],
             pathex=['D:\\Desktop shortcuts\\Collection\\Python Projects\\ProGame\\App'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='XDGame',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe, Tree('D:\\Desktop shortcuts\\Collection\\Python Projects\\ProGame'),
               a.binaries,
               a.zipfiles,
               a.datas,
			   *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='XDGame')
