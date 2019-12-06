# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/Users/bahrami-a/Desktop/seotool/production_source'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['_tkinter', 'Tkinter', 'enchant', 'twisted'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='seotool',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,Tree('/Users/bahrami-a/Desktop/seotool/production_source/res/'),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='seotool')
app = BUNDLE(coll,
             name='seotool.app',
             icon=None,
             bundle_identifier=None)
