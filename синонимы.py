import requests
import json
'''

url = "https://api.dictionaryapi.dev/api/v2/entries/en/"


entered_word = input("Введите слово: ")
word = url + entered_word
response = requests.get(word).json()
synonyms = ((response[1]).values())

print(synonyms)
'''
#dict.1.1.20230129T170011Z.0479082dea24b7eb.005d61f14c68bc120b7afda9ce5358063056ae91
KEY = 'dict.1.1.20230129T170011Z.0479082dea24b7eb.005d61f14c68bc120b7afda9ce5358063056ae91'
LANG = 'en-ru'
TEXT = input()
URL_AUTH = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key=' + KEY +'&lang=' + LANG + '&text=' + TEXT


auth = requests.post(URL_AUTH)
if auth.status_code == 200:
    token = auth.text
    res_dict = json.loads(token)
    try:
        res_dict = ((res_dict['def'])[0])['tr']
    except IndexError:
        print("Слово не получилось найти. Проверь правильность написания и отправь ещё раз. ")
        
    for i in range(0, len(res_dict)):
        search = res_dict[i]
        count = 0
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
                    print(s)
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
                            print(syn_dict['mean'], '-', syn_dict['syn'])
        else:
            if 'mean' in search.keys():
                for i in range(0, len(search['mean'])):
                    syn = search['text']
                    mean = ((search['mean'])[i])['text']
                    syn_dict = {'mean' : mean, 'syn' : syn}
                    print(syn_dict['mean'], '-', syn_dict['syn']) 
            else:
                pass 
