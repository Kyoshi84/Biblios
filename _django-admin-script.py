#!C:\Python27\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'Django==1.9.8','console_scripts','django-admin'
__requires__ = 'Django==1.9.8'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('Django==1.9.8', 'console_scripts', 'django-admin')()
    )
