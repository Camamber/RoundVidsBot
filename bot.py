from user import User
import json
import requests

class Bot:
    TOKEN = '543482719:AAGSzOTxA8AEoYIU8h8IAVfAlTHWbLLkRb0'
    URL = 'https://api.telegram.org/bot{0}/{1}'

    state= False
    users = {};

    def __init__(self):
        print('Hi. I`m ready')

    def update(self, json_string):
        data = json.loads(json_string)
        print(data['message']['chat']['username'],':',data['message'])
        if data['message']['chat']['id'] in self.users:
            self.exec_command(self.users[data['message']['chat']['id']], data['message'])
        else:
            self.new_user(data)         

    def send_msg(self, chat, text):
        params = {'chat_id': chat, 'text': text}
        response = requests.post(self.URL.format(self.TOKEN,'sendMessage'), data=params)
        return response



    def exec_command(self, user, command):
        if 'text' not in command:
            if user.state == 'token_adding':
                self.add_token(user, command['text'])
            elif user.state == 'channel_adding':
                self.add_channel(user, command['text'])
            elif user.state == 'sleep':
                self.sleep(user, command['text'])
        elif 'document' in command or 'video' in command:
            if user.state == 'video_adding':
                self.add_video(command['document'])
            
            
    def new_user(self, data):
        if 'text' in data['message'] and data['message']['text'] == '/start':
            self.users[data['message']['chat']['id']] = User(data['message']['chat']['id'])
            self.send_msg(data['message']['chat']['id'], 'Enter token of your posting bot:')      
        else:
            self.send_msg(data['message']['chat']['id'], 'Idk who are you man. Try /start to config me:)')

    def add_token(self, user, token):
        response = requests.post(self.URL.format(token, 'getMe'))
        if response.json()['ok']:
            user.token=token
            user.state='channel_adding'
            self.send_msg(user._id, 'Token successfully installed.')
        else:
            self.send_msg(user._id, 'Incorrect token. Try again.')

    def add_channel(self, user, channel):
        params = {'chat_id': channel}
        response = requests.post(self.URL.format(user.token, 'getChat'), params)
        if response.json()['ok']:
            user.add_channel(channel)
            user.state='working'
            self.send_msg(user._id, 'Chat successfully added.')
        else:
            self.send_msg(user._id, 'There is no such chat or your bot are not in it.')

    def sleep(self, user, command):
        if command == '/token':
            user.state='token_adding'
        elif command == '/channels':
            user.state='channel_adding'


    def add_video(self, user, document):
        if document['type'] == 'video/mp4':
            self.send_msg(user._id, 'Nice Shoot')
        else:
            self.send_msg(user._id, 'Hey whait a minute it isnt video')
                               
            
            
                
