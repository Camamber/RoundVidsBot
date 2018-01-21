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
        if data['message']['chat']['id'] in self.users:
            self.exec_command(self.users[data['message']['chat']['id']], data['message']['text'])
        else:
            self.new_user(data)         

    def send_msg(self, chat, text):
        params = {'chat_id': chat, 'text': text}
        response = requests.post(self.url.format(self.token,'sendMessage'), data=params)
        return response

    def new_user(self, data):
        if data['message']['text'] == '/start':
            self.users[data['message']['chat']['id']] = User(data['message']['chat']['id'])
            self.send_msg(data['message']['chat']['id'], 'Enter token of your posting bot:')      
        else:
            self.send_msg(data['message']['chat']['id'], 'Idk who are you man. Try /start to config me:)')

    def exec_command(self, user, command):
        if user.state == 'token':
            if self.check_token(command):
                user.token=command
            else:
                self.send_msg(user._id, 'Incorrect token. Try again')

    def check_token(self, token):
        print(token)
        response = requests.post(self.url.format(token,'getMe'))
        return response.json()['ok']
                
        
