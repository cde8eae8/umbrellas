from time import *
from gui import *

startGui(lambda x: sleep(3), [
        ('path-art', InPathWidget, "Артикулы"),
        ('path-out', OutPathWidget, "Таблица для вывода")
    ])

