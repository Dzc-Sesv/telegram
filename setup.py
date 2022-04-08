import sys
import os
if sys.version_info.major != 3:
    print('python major version must be 3')
    sys.exit(1)
os.system('apt install python3-pip')
os.system('pip3 install telethon')
print('all requirement is installed')
