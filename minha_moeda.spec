# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import sys
import os
from os.path import join

# Adiciona o diretório atual ao path para encontrar os módulos
sys.path.append(join(os.getcwd(), 'controllers'))
sys.path.append(join(os.getcwd(), 'views'))
sys.path.append(join(os.getcwd(), 'models'))
sys.path.append(join(os.getcwd(), 'utils'))

a = Analysis(
    ['main.py'],
    pathex=[os.getcwd()],
    binaries=[],
    datas=[
        # Inclui todos os módulos Python como dados
        ('controllers/*.py', 'controllers'),
        ('views/*.py', 'views'),
        ('models/*.py', 'models'),
        ('utils/*.py', 'utils'),
    ],
    hiddenimports=[
        # Módulos essenciais do Python que foram excluídos por engano
        'urllib',
        'urllib.request',
        'urllib.parse',
        'urllib.error',
        'email',
        'email.mime',
        'email.mime.text',
        'email.mime.multipart',
        'http',
        'http.client',
        'ssl',
        'xml',
        'xml.etree',
        'xml.etree.ElementTree',
        
        # Pandas hidden imports
        'pandas._libs.tslibs.timedeltas',
        'pandas._libs.tslibs.nattype', 
        'pandas._libs.tslibs.timestamps',
        'pandas._libs.tslibs.base',
        'pandas._libs.tslibs.period',
        'pandas._libs.tslibs.dtypes',
        'pandas._libs.tslibs.offsets',
        'pandas._libs.properties',
        'pandas._libs.ops',
        'pandas._libs.ops_dispatch',
        'pandas._libs.parsers',
        'pandas._libs.writers',
        'pandas._libs.json',
        
        # Dateutil e dependências
        'dateutil',
        'dateutil.parser',
        'dateutil.relativedelta',
        'dateutil.tz',
        'python_dateutil',
        
        # Tkinter e tkcalendar
        'tkinter',
        'tkinter.ttk',
        'tkcalendar',
        'tkcalendar.calendar_',
        'tkcalendar.dateentry',
        
        # Nossos módulos
        'controllers.financeiro_controller',
        'controllers.dividas_controller', 
        'controllers.dividas_pessoais_controller',
        'views.main_view',
        'views.dividas_view',
        'views.dividas_pessoais_view',
        'models.transacao',
        'models.divida',
        'models.divida_pessoal',
        'utils.file_manager',
        
        # Outras dependências
        'pytz',
        'pytz.tzfile',
        'pytz.exceptions',
        'numpy',
        'numpy.core',
        'numpy.lib',
        'numpy.random',
        'six',
        'zoneinfo',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Apenas exclua bibliotecas realmente pesadas que não usamos
        'matplotlib',
        'scipy', 
        'pytest',
        'unittest',
        'IPython',
        'jupyter',
        'notebook',
        'qtpy',
        'PyQt5',
        'PySide2',
        'wx',
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MinhaMoeda',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Mude para True se quiser ver o console para debug
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)