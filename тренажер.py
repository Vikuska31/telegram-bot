import random

f = open("exr.txt", encoding='utf-8')
lines = f.readlines()
answers = []
ans = []
a = random.randint(1,5)
print(a)
count = 0
for i in range(5):
    line = (''.join(lines)).split('***')
for i in range(0, len(line)):
    if (str(a)+'.\t') in line[i]:
        stroka = (''.join(line[i])).split('*1)')
        print((stroka[0])[:-1])
n_s = ('1)'+stroka[1]).split('*')
for i in range(0,len(n_s)):
    answers.append(n_s[i])
    print("Выберите один вариант ответа. Запиши только ЦИФРУ.")
    for k in range(0,len(answers)):
        ans_str = (''.join(answers[k])).split('\t')
        #for m in range(4):
        ans_str1 = (''.join(ans_str)).split('!')
        h = (''.join(ans_str1[10])).split()
        for m in range(0, len(ans_str1)):
            my_dict = {ans_str1[1]:ans_str1[2],
                    ans_str1[3]:ans_str1[4],
                    ans_str1[5]:ans_str1[6],
                    ans_str1[7]:ans_str1[8],
                    ans_str1[9]:h}
        else:
            pass
    s = (' '.join(ans_str1))[:-7]
    print(s)
    your_answer = input("Ваш ответ: ")
    def answerss(your_answer):
        if your_answer in '0123456789':
            if your_answer == ''.join(my_dict[(ans_str1[9])]):
                return ("Молодец! Всё верно!") 
            else:
                return ('Неверно'+'\n'+'Верный ответ: '+ ''.join(my_dict[(ans_str1[9])]))
    print(answerss(your_answer))
    if answerss(your_answer) == "Молодец! Всё верно!":
        count += 1
print("Всего правильных: ", count)
f.close()

