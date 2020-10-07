import pandas as pd
import re

def register(info):
    info.name = 'Какое-то описание скрипта'
    info.args = ["links", "output_file"]

def run(a):
    pass

# сам твой скрипт
list_of_links = args["links"]

a_itog = pd.DataFrame(columns = ['№', 'Штрихкод', 'Название', 'Вн. код покуп.','Кол-во', 'Единица', 'Кол-во в упаковке', 'Цена без НДС', 'Цена с НДС', 'Ставка НДС в %','Сумма без НДС', 'Сумма НДС', 'Сумма c НДС'])
for j in list_of_links:
    pass
    # ... твоя обработка

numbers = [4, 6, 7, 8, 9, 10, 11, 12]
for x in range(len(list(a_itog))):
    pass
    # ... еще какой-то твой цикл

a_itog.to_excel(args["ouput_file"], index = False)
