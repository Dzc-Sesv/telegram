import sys
import os
if sys.version_info.major != 3:
    print('python major version must be 3')
    sys.exit(1)
if sys.version_info.minor < 6:
    print('python minor version must greater than 6')
os.system('apt install python3-pip')
os.system('pip3 install sanic')
os.system('pip3 install jinja2')
os.system('pip3 install telethon')
print('all requirement is installed')