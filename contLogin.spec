# -*- mode: python -*-

block_cipher = None


a = Analysis(['contLogin.py'],
             pathex=['C:\\Python36\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'c:\\python36\\p', 'C:\\python36\\lib\\site-packages\\PyQt5\\Qt\\plugins\\platforms\\', 'C:\\python36\\lib\\site-packages\\PyQt5\\Qt\\plugins\\imageformats', 'C:\\PythonWorkspace\\BackedUp\\SolutionsDB'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
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
          [],
          exclude_binaries=True,
          name='contLogin',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='contLogin')
