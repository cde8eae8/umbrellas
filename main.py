from time import *
from gui import *
from PyQt5.QtWidgets import *
import subprocess
import shlex

import sys
sys.path.insert(0,'..')
import update

app = QApplication([])
if update.has_new_version():
    print('new version!')
    ans = QMessageBox.question(None, 'Update', 'Доступна новая версия. Скачать?')
    if (ans == QMessageBox.Yes):
        args = shlex.split('python3 ../update.py')
        subprocess.Popen(args, start_new_session=True)
        sys.exit(0)

startGui(lambda x: sleep(3), [
        ('path-art', InPathWidget, "Артикулы"),
        ('path-out', OutPathWidget, "Таблица для вывода")
    ])

app.exec_()
