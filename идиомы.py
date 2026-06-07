import random
from translatepy import Translator

f_idiom = open('idioms1.txt', encoding='utf-8')
f_idiom_transl = open('idioms2.txt', encoding='utf-8')

lines = f_idiom.readlines()
lines_tr = f_idiom_transl.readlines()
translator = Translator()

list_khown_idiom = []
list_unknown_idiom = []
list_transl_idiom = []

while len(list_unknown_idiom) != 4:
    r = random.randint(0, len(lines))
    lines_translate = translator.translate(lines_tr[r], "Russian")
    your_answer = input(f"Ты знаешь эту фразу? \n {lines[r]}")
    if your_answer == 'да':
        list_khown_idiom.append(lines[r]+'\n'+str(lines_translate))
    elif your_answer == 'нет':
        print(lines_translate)
        list_unknown_idiom.append(lines[r])
        list_transl_idiom.append(str(lines_translate))
    else:
        print('Отвечай только "да" или "нет"')
list_transl_idioms = []
if len(list_unknown_idiom) == 4:
    print('Теперь потренируем память')
    for i in range(4):
        list_transl_idioms.append(list_transl_idiom[random.randint(0, 3)])
    list_transl_id = random.sample(list_transl_idioms, 4)
    for j in range(0, 4):
        remember_answer = input(f"Как переводится эта фраза? \n {list_unknown_idiom[j]} \n \
        Варианты ответов: \n \
        1. {list_transl_id[0]} \n \
        2. {list_transl_id[1]} \n \
        3. {list_transl_id[2]} \n \
        4. {list_transl_id[3]} \n \
        Ваш ответ: ")
        
        if remember_answer == list_transl_idiom[j]:
            print('Молодец!')
        else:
            print(f'Неверно \n Верный ответ: {list_transl_idiom[j]}')
            
f_idiom.close()
f_idiom_transl.close()