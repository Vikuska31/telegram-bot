import requests, telebot, random, json
from translatepy import Translator
import prasal

token = '5800013389:AAGqdugll5tTBYIqZls0j0q--OReXp6o2R0'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = "Скорее нажимай на кнопки и получай новые знания!"
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    button1 = telebot.types.KeyboardButton("переводчик")
    button2 = telebot.types.KeyboardButton("синонимы")
    button3 = telebot.types.KeyboardButton("фраз. глаголы")
    button4 = telebot.types.KeyboardButton("тренажёр")
    button5 = telebot.types.KeyboardButton("идиомы")
    keyboard.add(button1, button2, button3, button4, button5)
    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard)


@bot.message_handler(commands=['translate']) 
def send_translate(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    button1 = telebot.types.KeyboardButton("С русского \n на английский")
    button2 = telebot.types.KeyboardButton("С английского \n на русский")
    button3 = telebot.types.KeyboardButton("Вернуться к основному меню")
    keyboard.add(button1, button2, button3)
    text = bot.send_message(message.chat.id, 'Выбери язык ', reply_markup=keyboard)
    bot.register_next_step_handler(text, translat_choice)


def translat_choice(message):
    if message.text == 'С русского \n на английский':
        text = bot.send_message(message.chat.id, 'Введи слово для перевода')
        bot.register_next_step_handler(text, translat_en)
    elif message.text == 'С английского \n на русский':
        text = bot.send_message(message.chat.id, 'Введи слово для перевода')
        bot.register_next_step_handler(text, translat_ru)
    else:
        bot.send_message(message.chat.id, 'Ошибка! Попробуй снова')


def translat_en(message):
    translator = Translator()
    lang = translator.translate(message.text, "English")
    bot.send_message(message.chat.id, lang)


def translat_ru(message):
    translator = Translator()
    lang = translator.translate(message.text, "Russian")
    bot.send_message(message.chat.id, lang)
    
#яндекс api
#dict.1.1.20230129T170011Z.0479082dea24b7eb.005d61f14c68bc120b7afda9ce5358063056ae91
KEY = 'dict.1.1.20230129T170011Z.0479082dea24b7eb.005d61f14c68bc120b7afda9ce5358063056ae91'
LANG = 'en-ru'

@bot.message_handler(commands=['synonyms'])
def send_synonyms(message):
    text = bot.send_message(message.chat.id, "Введите слово или небольшую фразу(в начальной форме)") 
    bot.register_next_step_handler(text, synn)
def synn(message):
    URL_AUTH = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key=' + KEY +'&lang=' + LANG + '&text=' + str(message.text)
    auth = requests.post(URL_AUTH)
    if auth.status_code == 200:
        Token = auth.text
        res_dict = json.loads(Token)
        try:
            res_dict = ((res_dict['def'])[0])['tr']
        except IndexError:
            bot.reply_to(message,"Слово не получилось найти. Проверь правильность написания и отправь ещё раз. ")

    for i in range(0, len(res_dict)):
        try:
            search = res_dict[i]
        except KeyError:
            pass
            #bot.reply_to(message,"Слово не получилось найти. Проверь правильность написания и отправь ещё раз. ")
        try:
            if ('syn' in search) == True:
                if 'mean' in search.keys():
                    len_mean = len(search['mean'])
                    len_syn = len(search['syn'])
                    if len_mean >= len_syn:
                        for n in range(0, len(search['mean'])):
                            mean = ((search['mean'])[n])['text']
                            s = str(mean)
                            for m in range(0, len(search['syn'])):
                                syn = ((search['syn'])[m])['text']
                                syn_dict = {'mean' : mean, 'syn' : syn}
                                s = s + '-' + syn_dict['syn']
                        bot.send_message(message.chat.id, s)
                    else:
                        s = []
                        if 'mean' in search.keys():
                            for n in range(0, len(search['syn'])):
                                syn = ((search['syn'])[n])['text']
                                s.append(syn)
                                syn_all = ', '.join(s)
                            for m in range(0, len(search['mean'])):
                                mean = ((search['mean'])[m])['text']
                                syn_dict = {'mean' : mean, 'syn' : syn_all}
                                d = syn_dict['mean']+'-'+ syn_dict['syn']
                                bot.send_message(message.chat.id, d)
            else:
                if 'mean' in search.keys():
                    for i in range(0, len(search['mean'])):
                        syn = search['text']
                        mean = ((search['mean'])[i])['text']
                        syn_dict = {'mean' : mean, 'syn' : syn}
                        k = (syn_dict['mean'], '-', syn_dict['syn'])
                        bot.send_message(message.chat.id, k) 
                else:
                    pass
        except UnboundLocalError:
            pass


@bot.message_handler(commands=['phrasal_verb'])
def send_phrasal_verb(message):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    button_1 = telebot.types.InlineKeyboardButton("Среди всех фразовых \n глаголов", callback_data='all_phras')
    button_2 = telebot.types.InlineKeyboardButton("Среди фр. глаголов  \n необходимых для ЕГЭ", callback_data='ege_phras')
    keyboard.add(button_1, button_2)
    bot.send_message(message.chat.id, 'Выбери необходимый формат для поиска', reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call:True)
def callback_phrasal(call):
    if call.message:
        if call.data == 'all_phras':
            text = bot.send_message(call.message.chat.id, 'Введи одно слово (например: carry)')
            bot.register_next_step_handler(text, prasal.all_verbs)
        elif call.data == 'ege_phras':
            text = bot.send_message(call.message.chat.id, 'Введи одно слово (например: carry)')
            bot.register_next_step_handler(text, prasal.ege_verbs)


@bot.message_handler(commands=['trainer'])
def send_trainer(message):
    global a
    a = random.randint(1,5)
    text, all_right_answers, all_s, f = prasal.trainer_m('', a)
    bot.send_message(message.chat.id, 'Прочитай внимательно текст и выполни задания')
    #bot.send_message(message.chat.id, text)
    bot.send_message(message.chat.id, text)
    trainer_text1 = bot.send_message(message.chat.id, 'Если ты ознакомился с текстом и заданием, то отравь мне любой симвоол или слово.')
    bot.register_next_step_handler(trainer_text1, trainer)


def trainer(message):
    count = 0
    text, all_right_answers, all_s, f = prasal.trainer_m('', a)
    if f == 1:
        count += 1
    trainer_text_1 = bot.send_message(message.chat.id, 'Выбери один вариант ответа. Напиши только ЦИФРУ'+'\n'+all_s[0])
    bot.register_next_step_handler(trainer_text_1, answers_m)

def answers_m(message): 
    text, all_right_answers, all_s, f = prasal.trainer_m('', a)
    right_answer = all_right_answers[0]
    if message.text == right_answer:
        r_txt = bot.reply_to(message, "Молодец! Всё верно! \n Чтобы перейти к следующему номеру отправь любой символ")
        bot.register_next_step_handler(r_txt, t2)
    else:
        txt = bot.reply_to(message, ("Неверно"+'\n'+'Верный ответ:  '+ right_answer +'\nЧтобы перейти к следующему номеру отправь любой символ'))
        bot.register_next_step_handler(txt, t2)


def t2(message):
    count = 0
    text, all_right_answers, all_s, f = prasal.trainer_m('', a)
    if f == 1:
        count += 1
    trainer_text_1 = bot.send_message(message.chat.id, 'Выбери один вариант ответа. Напиши только ЦИФРУ'+'\n'+all_s[1])
    bot.register_next_step_handler(trainer_text_1, a2)

def a2(message): 
    text, all_right_answers, all_s, f = prasal.trainer_m('', a)
    right_answer = all_right_answers[1]
    if message.text == right_answer:
        r_txt = bot.reply_to(message, "Молодец! Всё верно! \nЧтобы перейти к следующему номеру отправь любой символ")
        bot.register_next_step_handler(r_txt, t3)
    else:
        txt = bot.reply_to(message, ("Неверно"+'\n'+'Верный ответ: '+ right_answer +' \nЧтобы перейти к следующему номеру отправь любой символ'))
        bot.register_next_step_handler(txt, t3)


def t3(message):
    count = 0
    text, all_right_answers, all_s, f = prasal.trainer_m('', a)
    if f == 1:
        count += 1
    trainer_text_1 = bot.send_message(message.chat.id, 'Выбери один вариант ответа. Напиши только ЦИФРУ'+'\n'+all_s[2])
    bot.register_next_step_handler(trainer_text_1, a3)

def a3(message): 
    text, all_right_answers, all_s, f = prasal.trainer_m('', a)
    right_answer = all_right_answers[2]
    if message.text == right_answer:
        r_txt = bot.reply_to(message, "Молодец! Всё верно!\nЧтобы перейти к следующему номеру отправь любой символ")
        bot.register_next_step_handler(r_txt, t4)
    else:
        txt = bot.reply_to(message, ("Неверно"+'\n'+'Верный ответ: '+ right_answer + '\nЧтобы перейти к следующему номеру отправь любой символ'))
        bot.register_next_step_handler(txt, t4)


def t4(message):
    count = 0
    text, all_right_answers, all_s, f = prasal.trainer_m('', a)
    if f == 1:
        count += 1
    trainer_text_1 = bot.send_message(message.chat.id, 'Выбери один вариант ответа. Напиши только ЦИФРУ'+'\n'+all_s[3])
    bot.register_next_step_handler(trainer_text_1, a4)

def a4(message): 
    text, all_right_answers, all_s, f = prasal.trainer_m('', a)
    right_answer = all_right_answers[3]
    if message.text == right_answer:
        r_txt = bot.reply_to(message, "Молодец! Всё верно!\nЧтобы перейти к следующему номеру отправь любой символ")
        bot.register_next_step_handler(r_txt, t5)
    else:
        txt = bot.reply_to(message, ("Неверно"+'\n'+'Верный ответ: '+ right_answer + '\nЧтобы перейти к следующему номеру отправь любой символ'))
        bot.register_next_step_handler(txt, t5)


def t5(message):
    count = 0
    text, all_right_answers, all_s, f = prasal.trainer_m('', a)
    if f == 1:
        count += 1
    trainer_text_1 = bot.send_message(message.chat.id, 'Выбери один вариант ответа. Напиши только ЦИФРУ'+'\n'+all_s[4])
    bot.register_next_step_handler(trainer_text_1, a5)

def a5(message): 
    text, all_right_answers, all_s, f = prasal.trainer_m('', a)
    right_answer = all_right_answers[4]
    if message.text == right_answer:
        bot.reply_to(message, "Молодец! Всё верно!")
    else:
        bot.reply_to(message, ("Неверно"+'\n'+'Верный ответ: '+ right_answer))
        bot.send_message(message.chat.id, 'Умница, ты справился с заданием!')



@bot.message_handler(commands=['idioms'])
def send_idiom(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    button1 = telebot.types.KeyboardButton("Да, я знаю эту фразу")
    button2 = telebot.types.KeyboardButton("Нет, нужно изучить")
    button3 = telebot.types.KeyboardButton("Вернуться к основному меню")
    keyboard.add(button1, button2, button3)
    #while len(list_unknow_idiom) != 4: 
    r = random.randint(0, 377)
    line, line_tr = prasal.idioms(r)  
    text = bot.send_message(message.chat.id, ("Ты знаешь эту фразу?"+'\n'+line+'\n'+line_tr), reply_markup=keyboard)#+'\n'+line
    bot.register_next_step_handler(text, choice_idioms)
    return r, line_tr


def choice_idioms(message):
    list_khow_idiom = []
    list_unknow_idiom = []
    if message.text == 'Да, я знаю эту фразу':
        r, line, line_tr = send_idiom(message)
        #line, line_tr = prasal.idioms(r)
        list_khow_idiom.append((str(line)+' '+str(line_tr)))
        #answer(message)
    elif message.text == 'Нет, нужно изучить':
        r, line, line_tr = send_idiom(message)
        #r = send_idiom(message)
        #line, line_tr = prasal.idioms(r)
        list_unknow_idiom.append((str(line)+' '+str(line_tr)))
        #answer(message)
    print(list_khow_idiom)
    print(list_unknow_idiom)
"""
@bot.callback_query_handler(func=choice_idioms)
def idiom(message):
    if message.text == 'да':
        list_khow_idiom.append((lines[r]+lines_tr[r]))
    elif message.text == 'нет':
        list_unknow_idiom.append((lines[r]+lines_tr[r]))
    if len(list_unknow_idiom) == 4:
        for i in range(4):
            bot.send_message(message.chat.id, list_unknow_idiom[i])
    else:
        pass
"""


@bot.message_handler(content_types=["text"])
def answer(message):
    if message.text == "переводчик":
        send_translate(message)
    elif message.text == "синонимы":
        send_synonyms(message)
    elif message.text == "фраз. глаголы":
        send_phrasal_verb(message)
    elif message.text == "тренажёр":
        send_trainer(message)
    elif message.text == "идиомы":
        send_idiom(message)
    elif message.text == 'Вернуться к основному меню':
        send_welcome(message)
bot.infinity_polling()