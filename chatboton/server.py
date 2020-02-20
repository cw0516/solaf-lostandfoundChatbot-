from flask import Flask,request
from telegram_bot import TelegramBot
from controller import text_controller, button_controller
from user_manager import get_user

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':

        bot = TelegramBot() # 봇 생성

        message = request.get_json() #telegram 서버로부터 받은 json객체 받기
        print(message) #사용자 응답 로깅

        bot.save_userinfo(message) #봇에 사용자 id,이름,텍스트 등록

        user_row = get_user(bot.chat_id, bot.name) # user_info 액셀에서 사용자 행 찾아오기

        #사용자의 text 입력 처리
        if not 'callback_query' in message.keys():

            text_controller(bot, user_row)

        #사용자의 keyboard 입력 처리
        else:

            button_controller(bot,message,user_row)

    return ''

if __name__ == '__main__':
    app.run(host='localhost', port=80, debug=True)
