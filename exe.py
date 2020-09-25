import pandas as pd
import re
import numpy as np

from gui import *

def p(config):
    upak = pd.read_excel(config["table1-xlsl"])
    zakaz = pd.read_excel(config["umbrellas-xlsl"])

    empty = {0 : [0], 1 : [0]}
    empty1 = pd.DataFrame(empty)
    empty1 = empty1.append(upak, ignore_index = True)
    empty = {0 : [0], 1 : [0]}
    empty = pd.DataFrame(empty)
    itog = pd.DataFrame({0:[], 1: []})
    upak1 = pd.DataFrame(upak)
    upak1.loc[1, 1] = '30.09.2020'
    for x in range(1, len(zakaz) - 1):
        upak1.loc[5, 1] = zakaz.loc[x, 'заказ АЛИЭКСПРЕСС 22.09.20']
        upak1.loc[4, 1] = str(zakaz.loc[x, 'Unnamed: 2'])
        upak1.loc[3, 1] = zakaz.loc[x, 'Unnamed: 4']
        itog = itog.append(upak1, ignore_index = True)
        itog = itog.append(empty, ignore_index = True)

    itog.to_excel(config["out"])

startGui(p, [
    ('table1-xlsl', InPathWidget, "Первая таблица"),
    ('umbrellas-xlsl', InPathWidget, "Зонтики"),
    ('out', OutPathWidget, "Файл для сохранения"),
])
