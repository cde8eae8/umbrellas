from time import *
from gui import *
from PyQt5.QtWidgets import *
import subprocess
import shlex
import os
import json

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(SCRIPT_DIR)

import sys
sys.path.insert(0,os.path.join(SCRIPT_DIR, '..'))
import update

app = QApplication([])
if update.has_new_version():
    print('new version!')
    ans = QMessageBox.question(None, 'Update', 'Доступна новая версия. Скачать?')
    if (ans == QMessageBox.Yes):
        #args = shlex.split(f'{sys.executable} {os.path.join(SCRIPT_DIR, "../update.py")}')
        args = [sys.executable, os.path.join(SCRIPT_DIR, "..", "update.py")]
        subprocess.Popen(args, start_new_session=True, close_fds=True)
        sys.exit(0)

with open('modules.json', 'r') as f:
    config = json.load(f)
gui = MainWindow(config["modules"])
gui.start()

#startGui(lambda x: sleep(3), [
#        ('path-art', InPathWidget, "Артикулы"),
#        ('path-out', OutPathWidget, "Таблица для вывода")
#    ])

app.exec_()
