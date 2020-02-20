import requests
from config import SEND_MESSAGE,SEND_PHOTO

class TelegramBot:

    def __init__(self):

        self.chat_id = None
        self.text = None
        self.name = None


    def save_userinfo(self, data):

        if not 'callback_query' in data.keys():
            chat_id = data['message']['chat']['id']
            msg = data['message']['text']
            user_name = data['message']['chat']['first_name'] + data['message']['chat']['last_name']
            self.chat_id = chat_id
            self.text =msg
            self.name = user_name
        else:
            chat_id = data['callback_query']['from']['id']
            msg = data['callback_query']['data']
            user_name = data['callback_query']['from']['first_name'] + data['callback_query']['from']['last_name']
            self.chat_id = chat_id
            self.text =msg
            self.name = user_name


    def send_message(self,text,keyboard=None):

        if not keyboard:
            params = {'chat_id': self.chat_id, 'text': text}
            requests.post(SEND_MESSAGE, json=params)
        else:
            params = {'chat_id': self.chat_id, 'text': text,'reply_markup':keyboard}
            requests.post(SEND_MESSAGE, json=params)



    def send_img(self, url):

        params = {'chat_id': self.chat_id, 'photo': url}
        requests.post(SEND_PHOTO, json=params)
