from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardRemove
import requests
from config import SEND_MESSAGE
from config import DELETE_MESSAGE_URL
from openpyxl import load_workbook


EXCEL_FILE_NAME = "USER.xlsx"
db = load_workbook(filename=EXCEL_FILE_NAME)
user_db = db['user_info']


def create_callback_data(button_type,category):
    """ Create the callback data associated to each button"""
    return ";".join([button_type,category])

def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")


def create_category_button():

    categories = ['가방','귀금속','도서용품','서류','산업용품','쇼핑백','스포츠용품'\
                  ,'악기','유가증권','의류','자동차','전자기기','지갑','증명서'\
                  ,'컴퓨터','카드','현금','휴대폰','기타물품']
    keyboard = []
    row = []
    for i,category in enumerate(categories):


        if i%4 == 0 and i>0:
            keyboard.append(row)
            row = []

        if i == 18:
            keyboard.append(row)

        row.append(InlineKeyboardButton(category, callback_data=create_callback_data('category',category) ))

    return InlineKeyboardMarkup(keyboard).to_json()


def create_detail_button(category):
    keyboard = []
    category_hash = {

        '가방': ['여성용가방','남성용가방','기타가방'],
        '귀금속': ['반지','목걸이','귀걸이','시계','기타'],
        '도서용품': ['학습서적','소설','컴퓨터서적','만화책','기타서적'],
        '서류': [],
        '산업용품': [],
        '쇼핑백': [],
        '스포츠용품': [],
        '악기': ['건반악기','관악기','타악기','현악기','기타악기'],
        '유가증권': ['어음','상품권','채권','기타'],
        '의류': ['여성의류','남성의류','아기의류','기타의류'],
        '자동차': ['자동차열쇠','네비게이션','자동차번호판','임시번호판','기타용품'],
        '전자기기': ['PMP','MP3','PDA','카메라','전자수첩','기타용품'],
        '지갑': ['여성용지갑','남성용지갑','기타지갑'],
        '증명서': ['신분증','면허증','여권','기타'],
        '컴퓨터': ['삼성노트북','LG노트북','삼보노트북','HP노트북','기타'],
        '카드': ['신용(체크)카드','일반카드','기타카드'],
        '현금': ['현금','수표','외화','기타'],
        '휴대폰': ['모토로라휴대폰','삼성휴대폰','LG휴대폰','스카이휴대폰','아이폰','기타통신기기'],
        '기타물품': []
    }

    button_list = category_hash[category]
    print(button_list)
    if button_list:
        for button in button_list:
            keyboard.append([InlineKeyboardButton(button,callback_data=create_callback_data('category_detail',button))])

        return InlineKeyboardMarkup(keyboard).to_json()

    else:
        return False


def process_category_selection(query,user_row,db,user_db):

    category = separate_callback_data(query['data'])[1]

    params = {'chat_id': query['message']['chat']['id'],
              'message_id': query['message']['message_id']}
    requests.post(DELETE_MESSAGE_URL, json=params)

    params = {'chat_id': query['message']['chat']['id'],
              'reply_markup': ReplyKeyboardRemove(remove_keyboard=True).to_json()}

    requests.post(SEND_MESSAGE, json=params)

    detail_button = create_detail_button(category)
    if detail_button:
        params = {'chat_id': query['message']['chat']['id'], 'text': '더 자세한 분류를 선택해주세요',
                  'reply_markup': detail_button}
        requests.post(SEND_MESSAGE, json=params)
    else:

        params = {'chat_id': query['message']['chat']['id'],
                  'text': '분류명 {}를 고르셨습니다!'.format(category)}
        requests.post(SEND_MESSAGE, json=params)

        params = {'chat_id': query['message']['chat']['id'], 'text': '잃어버린 물건의 설명을 최대한 자세히 적어주시겠어요?\n\n ex) 신용카드와 주민등록증이 들어있는 지갑'}
        requests.post(SEND_MESSAGE, json=params)
        user_db[user_row][6].value = 'DESCRIPTION' #다음 대답에 대한 STATE 등록
        db.save(EXCEL_FILE_NAME)

    return category


def process_category_detail_selection(query):

    category_detail = separate_callback_data(query['data'])[1]

    params = {'chat_id': query['message']['chat']['id'],
              'message_id': query['message']['message_id']}
    requests.post(DELETE_MESSAGE_URL, json=params)

    params = {'chat_id': query['message']['chat']['id'],
              'reply_markup': ReplyKeyboardRemove(remove_keyboard=True).to_json()}

    requests.post(SEND_MESSAGE, json=params)

    return category_detail


if __name__ == '__main__':
    create_category_button()