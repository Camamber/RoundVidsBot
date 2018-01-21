from user import User
import json
import requests

class Bot:
    token = '543482719:AAGSzOTxA8AEoYIU8h8IAVfAlTHWbLLkRb0'
    url = 'https://api.telegram.org/bot{0}/{1}'
    state= False
    users = {};

    def __init__(self):
        print('Hi. I`m ready')

    def update(self, json_string):
        data = json.loads(json_string)
        print(data['message']['chat']['username'],':',data['message']['text'])
        if data['message']['chat']['id'] in users and data['message']['chat']['message_id'] != users[data['message']['chat']['id']].get_last():
            users[data['message']['chat']['id']].set_last(data['message']['chat']['message_id'])
            if data['message']['text'] == '/start':
                self.send_msg(data['message']['chat']['id'], 'Welcome:)')
        

    def send_msg(self, chat, text):
        params = {'chat_id': chat, 'text': text}
        response = requests.post(self.url.format(self.token,'sendMessage'), data=params)
        return response
