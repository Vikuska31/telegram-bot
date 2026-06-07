import telebot, random
from translatepy import Translator
token = '5800013389:AAGqdugll5tTBYIqZls0j0q--OReXp6o2R0'
bot = telebot.TeleBot(token)

def all_verbs(message):
    ff = open('phasal.txt', encoding='utf-8')
    line = ff.readlines()
    translator = Translator()
    phras = (message.text)[0].upper() + (message.text)[1:]
    count = 0
    for i in range(0, len(line)):
        mean_line = (''.join(line[i])).split(':')
        if phras in mean_line[0]:
            count = 1
            if len(mean_line) == 2:
                t = translator.translate(mean_line[1], "Russian")
                bot.send_message(message.chat.id, (str(line[i])+'\n'+str(t)))
            else:
                pass
    if count == 0:
        bot.send_message(message.chat.id, 'Слово не найдено. Проверь и отправь ещё раз')
    else:
        pass
    ff.close()



def ege_verbs(message):
    f1 = open('egephr.txt', encoding='utf-8')
    lines_1 = f1.readlines()
    count = 0
    for i in range(0, len(lines_1)):
        if message.text.lower() in lines_1[i]:
            count = 1
            bot.send_message(message.chat.id, lines_1[i])
        else:
            pass
    if count == 0:
        bot.send_message(message.chat.id, 'Слово не найдено. Проверь и отправь ещё раз')
    else:
        pass
    f1.close()


def trainer_m(message, a):
    f = 0
    f_tr = open("exr.txt", encoding='utf-8')
    lines_train = f_tr.readlines()
    try:
        line_train = (''.join(lines_train)).split('***')
        for i in range(0, len(line_train)):
            if (str(a)+'.\t') in line_train[i]:
                stroka = (''.join(line_train[i])).split('*1)')
                f = 1
    except AttributeError:
        pass

    answers = []
    all_s = []
    all_right_answers = []
    for i in range(0, len(line_train)):
        if (str(a)+'.\t') in line_train[i]:
            stroka = (''.join(line_train[i])).split('*1)')
    n_s = ('1)'+stroka[1]).split('*')
    for i in range(0,len(n_s)):
        answers.append(n_s[i])    
        for k in range(0,len(answers)):
            ans_str = (''.join(answers[k])).split('\t')
            ans_str1 = (''.join(ans_str)).split('!')
            h = (''.join(ans_str1[10])).split()
            s = (' '.join(ans_str1))[:-7]
            for m in range(0, len(ans_str1)):
                my_dict = {ans_str1[1]:ans_str1[2],
                                ans_str1[3]:ans_str1[4],
                                ans_str1[5]:ans_str1[6],
                                ans_str1[7]:ans_str1[8],
                                ans_str1[9]:h}
            else:
                pass
        all_s.append(s)
        all_right_answers.append(''.join(my_dict[(ans_str1[9])]))
    f_tr.close()
    return (stroka[0])[:-1], all_right_answers, all_s, f


def idioms(r):
    f_idiom = open('idioms1.txt', encoding='utf-8')
    f_idiom_transl = open('idioms2.txt', encoding='utf-8')
    lines = f_idiom.readlines()
    lines_tr = f_idiom_transl.readlines()
    translator = Translator()
    lines_translate = translator.translate(lines_tr[r], "Russian")
    f_idiom.close()
    f_idiom_transl.close()
    return lines[r], lines_translate
