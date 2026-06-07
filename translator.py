#ZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmxlSEFpT2pFMk56VXhNRFUwTlRFc0lrMXZaR1ZzSWpwN0lrTm9ZWEpoWTNSbGNuTlFaWEpFWVhraU9qVXdNREF3TENKVmMyVnlTV1FpT2pjME5UZ3NJbFZ1YVhGMVpVbGtJam9pWkdJNE1HVmlaRFl0T1RnNE1DMDBZekV5TFdJMVlqa3RNV0ptWmpVNE1qZzNPVEF6SW4xOS5ENmpJNUpuYUllVmM2UVpxbFl5OWkzRS14S0RKWi1xd0x3VnZFcTRBT3Vn

import requests

URL_AUTH = 'https://developers.lingvolive.com/api/v1.1/authenticate'
URL_TRANSLATE = 'https://developers.lingvolive.com/api/v1/Minicard'
KEY = 'ZGI4MGViZDYtOTg4MC00YzEyLWI1YjktMWJmZjU4Mjg3OTAzOjkyMWE1YzEzNTE4YjRhZjk4NWIzMmI5NmNiOWFmZThl'

headers_auth = {'Authorization':'Basic ' + KEY}
auth = requests.post(URL_AUTH, headers=headers_auth)

if auth.status_code == 200:
    token = auth.text

    while True:
        word = input('Введите слово для перевода: ')
        if word:
            headers_translate = {'Authorization':'Bearer ' + token}
            params = {'text': word,'srcLang': 1033,'dstLang': 1049}
            r = requests.get(URL_TRANSLATE, headers=headers_translate, params=params)
            res = r.json()
            try:
                print(res['Translation']['Translation'])
            except:
                print('Не найдено варианта для перевода')
else:
    print("Error!")
#2 способ
from translatepy import Translator
message = input()
translator = Translator()
t = translator.translate(message, "Russian")
print(t)