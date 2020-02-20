from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardRemove
import calendar
import datetime
import requests
from config import SEND_MESSAGE,ANSWER_CALLBACK_QUERY_URL,EDIT_MESSAGE_TEXT_URL



def create_callback_data(action,year,month,day):
    """ Create the callback data associated to each button"""
    return ";".join(['calendar',action,str(year),str(month),str(day)])

def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")


def create_calendar(year=None,month=None):

    '''
    :param year,month : 사용자에게 보여질 달력에 필요한 날짜 정보
    :return: telegram 서버에 전달만 하면 되는 완성된 inline keyboard button
    '''

    keyboard = []

    # next / prev 버튼 안 누른 경우
    now = datetime.datetime.now()
    if year == None: year = now.year
    if month == None: month = now.month

    # 날짜, next/prev 버튼과 상관없는 버튼들의 callback_data 설정
    data_ignore = create_callback_data("IGNORE", year, month, 0)

    #첫번째 줄 생성
    row=[]
    row.append(InlineKeyboardButton(calendar.month_name[month]+" "+str(year),callback_data=data_ignore))
    keyboard.append(row)

    #두번째 줄 생성
    row=[]
    for day in ["Mo","Tu","We","Th","Fr","Sa","Su"]:
        row.append(InlineKeyboardButton(day,callback_data=data_ignore))
    keyboard.append(row)

    #달력 날짜 생성
    my_calendar = calendar.monthcalendar(year, month)
    print(my_calendar)
    for week in my_calendar:
        row=[]
        for day in week:
            if(day==0):
                row.append(InlineKeyboardButton(" ",callback_data=data_ignore))

            else:
                row.append(InlineKeyboardButton(str(day),callback_data=create_callback_data("DAY",year,month,day)))

        keyboard.append(row)

    # prev/next 버튼 생성
    row=[]
    row.append(InlineKeyboardButton("<",callback_data=create_callback_data("PREV-MONTH",year,month,day)))
    row.append(InlineKeyboardButton(" ",callback_data=data_ignore))
    row.append(InlineKeyboardButton(">",callback_data=create_callback_data("NEXT-MONTH",year,month,day)))

    keyboard.append(row)

    return InlineKeyboardMarkup(keyboard).to_json()


def process_calendar_selection(query):

    '''
    :param query:사용자로부터 돌아온 json객체의 'callback_data' 의 value
    :return:
    '''


    # 사용자가 실제로 달력의 버튼을 누른다면 위의 create_calendar를 만들때 설정한 callback_data가 돌아오게 된다
    # 그 callback_data는 ';'으로 구분했고 아래에서 ';' 을 구분자로 쪼개서 사용자의 버튼 입력 정보를 저장한다
    action = separate_callback_data(query['data'])[1] #IGNORE인지/DAY인지/PREV-MONTH인지/NEXT-MONTH인지
    year = separate_callback_data(query['data'])[2]
    month = separate_callback_data(query['data'])[3]
    day = separate_callback_data(query['data'])[4]

    curr = datetime.datetime(int(year), int(month), 1)

    if action == "IGNORE":
        params = {'callback_query_id': query['id']}
        requests.post(ANSWER_CALLBACK_QUERY_URL, json=params)

    elif action == "DAY":

        # params = {'chat_id': query['message']['chat']['id'], 'message_id': query['message']['message_id']}
        # requests.post(DELETE_MESSAGE_URL, json=params)
        date = datetime.datetime(int(year), int(month), int(day))

        params = {'chat_id': query['message']['chat']['id'], 'text': "%s에 잃어버렸군." % (date.strftime("%Y-%m-%d")),
                  'reply_markup': ReplyKeyboardRemove(remove_keyboard=True).to_json()}
        requests.post(SEND_MESSAGE, json=params)

        return str(date.strftime("%Y-%m-%d"))

    elif action == "PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)

        params = {'chat_id': query['message']['chat']['id'], 'text': query['message']['text'],
                  'message_id': query['message']['message_id'],
                  'reply_markup': create_calendar(int(pre.year), int(pre.month))}

        requests.post(EDIT_MESSAGE_TEXT_URL, json=params)



    elif action == "NEXT-MONTH":
        ne = curr + datetime.timedelta(days=31)
        print(ne)
        params = {'chat_id': query['message']['chat']['id'], 'text': query['message']['text'],
                  'message_id': query['message']['message_id'],
                  'reply_markup': create_calendar(int(ne.year), int(ne.month))}

        requests.post(EDIT_MESSAGE_TEXT_URL, json=params)

    return None

if __name__ == '__main__':
    print(create_calendar())