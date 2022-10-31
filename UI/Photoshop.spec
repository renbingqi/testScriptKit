# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['project/study/PyQt5/dataDownload/Pictures/Photoshop.ico'],
             pathex=['/Users/rexren/python project/study/PyQt5/dataDownload/UI'],
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
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='Photoshop',
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
          entitlements_file=None , icon='/Users/rexren/python')
app = BUNDLE(exe,
             name='Photoshop.app',
             icon='/Users/rexren/python',
             bundle_identifier=None)
