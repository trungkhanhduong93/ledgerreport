import os
import sys
import subprocess

# Config
if 'ledgerreport' in os.getcwd().lower():
    APP_NAME = 'iPOS_Accounting_Report'
else:
    APP_NAME = 'iPOS_Ledger_Studio'

ICON_NAME = 'icon.ico'
ADD_DATA = [
    'index.html;.',
    'install_driver.ps1;.'
]
if os.path.exists('manifest.json'):
    ADD_DATA.append('manifest.json;.')
if os.path.exists('icon.svg'):
    ADD_DATA.append('icon.svg;.')

VERSION_FILE = 'version.txt'
# version.txt phải nhúng vào EXE: server.py đọc file này rồi tiêm vào APP_VERSION của index.html
# (thêm SAU khi ghi version mới ở dưới, để bundle chứa đúng version vừa tăng).

def get_next_version(v_str):
    try:
        parts = list(map(int, v_str.strip().split('.')))
        if len(parts) != 3:
            parts = [1, 2, 0]
    except:
        parts = [1, 2, 0]
        
    major, minor, patch = parts
    
    if patch < 9:
        patch += 1
    else:
        patch = 0
        minor += 1
        
    return f'{major}.{minor}.{patch}'

# Read current version
if os.path.exists(VERSION_FILE):
    with open(VERSION_FILE, 'r') as f:
        current_version = f.read().strip()
else:
    current_version = '1.1.9' # So it becomes 1.2.0 on first run
    with open(VERSION_FILE, 'w') as f:
        f.write(current_version)

new_version = get_next_version(current_version)

print(f'\n====================================')
print(f' Building {APP_NAME} v{new_version} ')
print(f'====================================\n')

# Save new version
with open(VERSION_FILE, 'w') as f:
    f.write(new_version)

ADD_DATA.append(f'{VERSION_FILE};.')

# Generate version_info.txt
v_parts = list(map(int, new_version.split('.')))
v_tuple = f'{v_parts[0]}, {v_parts[1]}, {v_parts[2]}, 0'

version_info = f"""VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({v_tuple}),
    prodvers=({v_tuple}),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        '040904B0',
        [StringStruct('CompanyName', 'iPOS.vn'),
        StringStruct('FileDescription', '{APP_NAME}'),
        StringStruct('FileVersion', '{new_version}'),
        StringStruct('InternalName', '{APP_NAME}'),
        StringStruct('OriginalFilename', '{APP_NAME}.exe'),
        StringStruct('ProductName', '{APP_NAME}'),
        StringStruct('ProductVersion', '{new_version}')])
      ]), 
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)"""

with open('version_info.txt', 'w') as f:
    f.write(version_info)

# Build command
cmd = [
    sys.executable, '-m', 'PyInstaller',
    '--noconsole', '--onefile', '--clean', '--noconfirm',
    '--name', APP_NAME,
    '--icon', ICON_NAME,
    '--version-file', 'version_info.txt',
    '--collect-submodules', 'pyodbc'
]
for data in ADD_DATA:
    cmd.extend(['--add-data', data])
cmd.append('server.py')

print('Running PyInstaller...')
subprocess.run(cmd)
print(f'\n[SUCCESS] Built {APP_NAME}.exe v{new_version} in dist folder.')
