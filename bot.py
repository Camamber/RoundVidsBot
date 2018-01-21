from user import User
import json
import requests

class Bot:
    token = '543482719:AAGSzOTxA8AEoYIU8h8IAVfAlTHWbLLkRb0'
    url = 'https://api.telegram.org/bot{0}/{1}'
    state= False
    users = [];

    def __init__(self):
        print(User().lol())

    def update(self, json_string):
        data = json.loads(json_string)
        if data['message']['text'] == '/start':
            print(data['message']['chat']['username'],':',data['message']['text'])
            send_msg(data['message']['chat']['id'], 'Welcome:)')
        

    def send_msg(self, chat, text):
        params = {'chat_id': chat, 'text': text}
        response = requests.post(url.format(token,'sendMessage'), data=params)
        return response
