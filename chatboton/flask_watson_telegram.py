from flask import Flask,render_template,request
from datetime import datetime
import requests
import json



############################ telegram config ########################################


# telegram 봇 정보
API_KEY = '983139267:AAGJnunRvpBWopGw95Owa_XIaejxy2OUNHQ'
URL = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)

# telegram 봇 사용자로부터 받은 메세지 파싱
def parse_message(data):
    '''응답data 로부터 chat_id 와 text, user_name을 추출.'''

    chat_id = data['message']['chat']['id']
    msg = data['message']['text']
    user_name = data['message']['chat']['first_name'] + data['message']['chat']['last_name']

    return chat_id, msg, user_name



############################## watson config ########################################

# service = ibm_watson.AssistantV2(
#     iam_apikey='{왓슨 API_KEY를 적어주세요}',  # replace with API key
#     version='2019-02-28'
# )
#
# assistant_id = '{assistant_id를 적어주세요}'
#
# session_id = service.create_session(
#     assistant_id=assistant_id
#
# ).get_result()['session_id']
#
# # 왓슨으로 보내기 위한 딕셔너리?json객체? 생성
# message_input = {
#     'text': ''
# }




app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():

    # telegram으로 입력이 온 경우는 아래의 if문으로 들어온다
    if request.method == 'POST':
        message = request.get_json()
        print(message)
        chat_id, msg, chat_name = parse_message(message)
        print(chat_id,msg,chat_name)

        #text = send_mesage(msg)
        text = "안녕 난 챗봇이얌!"
        params = {'chat_id': chat_id, 'text': text}  # , 'reply_markup' : keyboard}
        requests.post(URL, json=params)
    # telegram으로 입력이 들어오지 않으면 web으로 띄우기
    # return값은 존재해야함
    """Renders the home page."""
    return render_template(
        'chat.html',
        title='Home Page',
        year=datetime.now().year,
    )



# @app.route('/send_message/<message>')
# def send_mesage(message):
#     '''
#     왓슨으로 message를 보내줍니다
#     :param message: telegram으로부터 받은 사용자의 input
#     :return:
#     '''
#     message_input['text'] = message
#
#     #왓슨으로 message를 보내고 결과까지 받기
#     response = service.message(
#         assistant_id = assistant_id,
#         session_id = session_id,
#         input = message_input
#     ).get_result()
#
#
#     # intent 가져오기
#     if response['output']['intents']:
#         print(response['output']['intents'][0]['intent'])
#
#     # 왓슨에서 return한 response가져오기
#     if response['output']['generic']:
#         if response['output']['generic'][0]['response_type'] == 'text':
#             return(response['output']['generic'][0]['text'])

# service.delete_session(
#     assistant_id=assistant_id,
#     session_id=session_id
# )




if __name__ == '__main__':
    app.run(host='localhost', port=80, debug=True)

























