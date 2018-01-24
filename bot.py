from user import User
import json
import requests
import os.path

class Bot:

    TOKEN = ''
    URL = 'https://api.telegram.org/bot{0}/{1}'
    users = {};

    def __init__(self, TOKEN):
        self.TOKEN=TOKEN
        self.deserialize('users.json')
        print('Hi. I`m ready')

      
    def update(self, json_string):
        data = json.loads(json_string)
        print('------------------------------\n',data,'\n------------------------------')
        if 'message' in data:
            if 'text' in data['message'] or 'document' in data['message'] or 'video' in data['message']:
                print(data['message']['chat']['username'],':',data['message'])
                if data['message']['chat']['id'] in self.users:
                    self.exec_command(self.users[data['message']['chat']['id']], data['message'])
                else:
                    self.new_user(data)
        elif 'callback_query' in data and 'video_note' in data['callback_query']['message']:
            print(self.post_video(data['callback_query']).json())
            

    def send_msg(self, chat, text):
        params = {'chat_id': chat, 'text': text, 'parse_mode':'HTML'}
        response = requests.post(self.URL.format(self.TOKEN,'sendMessage'), data=params)
        return response



### SERIALIZING-DESERIALIZING SECTION ###

    def deserialize(self, path):
        data = requests.get('http://strilets.com.ua/tools/{0}'.format(path)).json()
        for user in data['users']:
            self.users[user['id']]=User(user['id'],user['state'],user['token'],user['channels'])
    

    def serialize(self, path):
        info = []
        for user in self.users:
            info.append(self.users[user].to_json())
        info =str({'users':info})
        print(info.replace('\'', '"'))
        params = {'action': 'add', 'data': info.replace('\'', '"')}
        response = requests.post('http://strilets.com.ua/tools/saver.php', data=params)
        print(response)



### LOGIC SECTION ###

    def exec_command(self, user, command):
        if 'text' in command:
            if user.state == 'token_adding':
                self.add_token(user, command['text'])
            elif user.state == 'channel_adding':
                self.add_channel(user, command['text'])
            elif user.state == 'sleep':
                self.sleep(user, command['text'])
        elif 'document' in command:
            if user.state == 'video_adding':
                self.add_video(user, command['document'])
        elif 'video' in command:
            if user.state == 'video_adding':
                self.add_video(user, command['video'])


    
### ADDING USER SECTION ###
            
    def new_user(self, data):
        if 'text' in data['message'] and data['message']['text'] == '/start':
            self.users[data['message']['chat']['id']] = User(data['message']['chat']['id'])
            self.send_msg(data['message']['chat']['id'], 'Enter token of your posting bot:')      
        else:
            self.send_msg(data['message']['chat']['id'], 'Idk who are you man. Try /start to config me:)')



### ADDING TOKEN SECTION ###

    def add_token(self, user, token):
        response = requests.post(self.URL.format(token, 'getMe'))
        if response.json()['ok']:
            user.token=token
            user.state='channel_adding'
            self.send_msg(user._id, 'Token successfully installed. Now add channel. Simply type <b>valid</b> @channelname')
        else:
            self.send_msg(user._id, 'Incorrect token. Try again.')



### ADDING CHANNEL SECTION ###
            
    def add_channel(self, user, channel):
        params = {'chat_id': channel, 'user_id': user.token.split(':')[0]}
        response = requests.post(self.URL.format(user.token, 'getChatMember'), params)
        if response.json()['ok'] and response.json()['result']['status']=='administrator':
            user.add_channel(channel)
            user.state='video_adding'
            self.send_msg(user._id, 'Chat successfully added. Now you can send me a video')
            self.serialize('users.json')
        else:
            self.send_msg(user._id, 'There is no such chat or your bot are not admin in it.')



### SLEEPING SECTION ###        

    def sleep(self, user, command):
        if command == '/token':
            user.state='token_adding'
        elif command == '/channels':
            user.state='channel_adding'



### ADDING VIDEO SECTION ###

    def add_video(self, user, document):
        if document['mime_type'] == 'video/mp4':
            if document['width'] == document['width'] and document['duration']<=60:
                params = {'file_id': document['file_id']}
                response = requests.post(self.URL.format(self.TOKEN, 'getFile'), params)
                if response.json()['ok']:
                    print(self.round_it(user, response.json()['result']['file_path']))
            elif document['width']!= document['width']:
                self.send_msg(user._id, 'Video shoud be scaled 1:1')
            elif document['duration']>60:
                self.send_msg(user._id, 'Video shoud be up to one minute')
        else:
            self.send_msg(user._id, 'Hey wait a minute it isnt video')

    def download_file(self, file_path):
        filename = file_path.split('/')[-1]
        url = 'https://api.telegram.org/file/bot{0}/{1}'
        r = requests.get(url.format(self.TOKEN,file_path))       
        return r.content
    
    def round_it(self,user, file_path):
        file={'video_note': self.download_file(file_path)}
        params = {'chat_id': user._id, 'reply_markup':self.inline_keyboard(user)}
        response = requests.post(self.URL.format(self.TOKEN,'sendVideoNote'),files=file, data=params)
        return response

    def inline_keyboard(self, user):
        keyboard={'inline_keyboard':[]}
        for channel in user.channels:
            keyboard['inline_keyboard'].append([{'text':channel, 'callback_data':channel}])
        print(str(keyboard).replace('\'', '"'))
        return str(keyboard).replace('\'', '"')



### POST VIDEO SECTION ###
    
    def post_video(self, query):
        user = self.users[query['from']['id']]
        params = {'file_id': query['message']['video_note']['file_id']}
        response = requests.post(self.URL.format(self.TOKEN, 'getFile'), params)
        if response.json()['ok']:
            file={'video_note': self.download_file(response.json()['result']['file_path'])}
            params = {'chat_id': query['data']}
            response = requests.post(self.URL.format(user.token,'sendVideoNote'),files=file, data=params)
        return response

        
