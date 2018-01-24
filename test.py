import json
import requests
import os.path

TOKEN = '456472998:AAGuE397SZVFgX5JIV022BFe6XQzzdDn_7Q'
URL = 'https://api.telegram.org/bot{0}/{1}'

file={'video_note': open('1.mp4', 'rb')}
#keyboard = '{"inline_keyboard":[[{"text":"xyi","url":"pleshka.com"}]]}'
keyboard = {'inline_keyboard':[{'text':'xyi','url':'pleshka.com'}]}
params = {'text':'xyi','chat_id': '339018008', 'reply_markup':str(keyboard).replace('\'', '"') }
print(params)
response = requests.post(URL.format(TOKEN,'sendVideoNote'), data=params, files=file)
print(response.json())
#https://api.telegram.org/sendMessage?chat_id=339018008&text=Choose&reply_markup={%22inline_keyboard%22:[[{%22text%22:%22Yes%22,%20%22url%22:%22google.com%22}]]}
