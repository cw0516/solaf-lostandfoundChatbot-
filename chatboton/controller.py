from calendar_button_maker import *
from category_button_maker import *
import result_button_maker
import filter
from bs4 import BeautifulSoup
import datetime
import user_manager as user
import db_manager


def get_addr(query):
    import requests
    common = ' 우편번호'
    # query = '백제운수'
    url = 'https://search.naver.com/search.naver?where=nexearch&ie=utf8&X_CSA=address_search&query='
    res = requests.get(url + query + common)

    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    s1 = soup.find('span', {'class': 'r_addr'})
    # return s1.text
    return 'https://map.naver.com/index.nhn?query=' + s1.text.replace(" ","")

def date_inc(date,inc):

    date = datetime.datetime.strptime(str(date),'%Y-%m-%d')
    new_date = date+datetime.timedelta(days=int(inc))
    return new_date.strftime('%Y-%m-%d')

def separate_callback_data(data):
    return data.split(";")

def get_search_dates(user_input):

    #strptime의 첫번째 인자는 문자열!!
    today = datetime.datetime.now().strftime(("%Y-%m-%d"))
    today_obj = datetime.datetime.strptime(today, "%Y-%m-%d")

    #리턴할 리스트 생성
    search_dates = []


    date_param = user_input

    #datetime객체로 만들어주기(날짜 비교를 위해서)
    date_obj = datetime.datetime.strptime(date_param, "%Y-%m-%d")

    if date_obj.date() <= today_obj.date():
        search_dates.append(date_param)

    while (True):

        date_param = date_inc(date_param, 1) # 달력기반으로 하루 증가한 문자열
        date_obj = datetime.datetime.strptime(date_param, "%Y-%m-%d")
        if date_obj.date() > today_obj.date():
            break
        search_dates.append(date_param)

    return search_dates



def make_detail_message(df):
    detail_message = ""
    if df.ix[0]['date']:
        detail_message += "습득일자 : " + df.ix[0]['date'] + '\n'
    if df.ix[0]['category']:
        detail_message += "분류 : " + df.ix[0]['category'] + '\n'
    if df.ix[0]['name']:
        detail_message += "이름 : " + df.ix[0]['name'] + '\n'
    if df.ix[0]['found_place']:
        detail_message += "습득장소 : " + df.ix[0]['found_place'] + '\n'
    if df.ix[0]['state']:
        detail_message += "보관상태 : " + df.ix[0]['state'] + '\n'
    return detail_message




# 사용자의 텍스트 입력 컨트롤러
def text_controller(bot,user_row):


    if bot.text == '/start':
        user.reset_with_start(user_row)
        hello_text = '''
        내이름 솔라프,탐정이죠.\n
지금부터 {}에게 보여주겠어. \n탐정이 무엇인지를....\n 이 세상에 찾지 못하는 것은 단 하나도 없어.'''

        date_text = '''
        홈즈도 이렇게 말했어. \n"감정적인 성질은 때론 추리를 방해해 진실과 멀어지게 만든다"라고.
\n\n물건을 잃어버려 속상하겠지만
진정하고, 먼저 물건 잃어버린 날짜를 생각해봐.'''

        bot.send_message(hello_text.format(bot.name))

        bot.send_message(date_text,create_calendar())


    # DESCRIPTION 입력받기
    elif user.get_step(user_row) == 'DESCRIPTION':


        user.save_description(user_row,bot.text)

        remaining_tokens = filter.get_tokens(user.get_description(user_row))

        date_query = str(user.get_date(user_row)).split()

        tag_query = filter.get_tag_token(user.get_description(user_row))

        color_search = filter.get_color_token(remaining_tokens)

        if color_search:
            color_query = color_search[0]
            remaining_tokens = color_search[1]
            print(remaining_tokens)

            df = db_manager.select_by_dates_and_description(date_query,tag_query,color_query)

            result_text = "그래!! 너가 찾고 있는 분실물이 이제 뭔지 알겠어!!" +'\n\n'+ str(len(list(df.index))) + "건이 발견되었어!!"
            keyboard = result_button_maker.create_result_button(df)
            bot.send_message(result_text,keyboard)

        else:

            df = db_manager.select_by_dates_and_description(date_query,tag_query,None)
            result_text = "그래!! {}가 찾고 있는 분실물이 이제 뭔지 알겠어!!".format(bot.name) + '\n\n' + str(len(list(df.index))) + "건이 발견되었군.."
            keyboard = result_button_maker.create_result_button(df)
            bot.send_message(result_text, keyboard)

        return

# 사용자의 버튼 입력 컨트롤러
def button_controller(bot,message,user_row):


    query = message['callback_query']

    # 어떤 keyboard 입력인지 구분
    button_type = separate_callback_data(query['data'])[0]

    if button_type == 'calendar':

        user_input = process_calendar_selection(query)

        #날짜 버튼을 눌렀을 때만
        if user_input:

            search_dates = get_search_dates(user_input)

            #오늘 이전 날짜를 입력했다면
            if search_dates:

                result = ""
                for date in search_dates:
                    result += date + " "

                user.save_date(user_row, result)

                df = db_manager.select_by_dates(search_dates)

                if (len(list(df.index))):
                    bot.send_message('너가 잃어버린 날부터 오늘까지의 습득물을 검색한 결과 ' + str(len(list(df.index))) + '건이 발견되었어.')

                    user.save_step(user_row,'DESCRIPTION')
                    bot.send_message('이제 잃어버린 물건을 나에게 최대한 자세히 설명해봐..\n\nex) 신용카드와 주민등록증이 들어있는 지갑')

                else:
                    bot.send_message('미안해 이 날은 내가 아는 습득물이 하나도 없어 ㅠㅠ')


            else:
                bot.send_message('아직 벌어지지도 않은 일은 걱정하지 말라구..')

    # 분실물 상세보기 또는 예/아니오 버튼
    elif button_type == 'result':

        id = separate_callback_data(query['data'])[1]

        if id == 'y':
            bot.send_message("다행이군 찾게되어서.\n습득물 보관소 연락처와 위치를 알려줄께")
            bot.send_message("보관소 연락처 : {}".format(user.get_center_num(user_row)))

            bot.send_message("보관소 위치 : {}".format(get_addr(user.get_center(user_row))))
        elif id == 'n':
            bot.send_message("아직 분실물 습득 추리중이야 빠른 시일내에 사건을 해결하겠어!")

        #분실물 상세보기
        else:

            df = db_manager.select_by_id(id)

            # 사용자가 이 다음 질문에서 맞다고 할때 보내줄 정보들 미리 excel에 저장해야한다
            user.save_center(user_row,df.ix[0]['center'])
            user.save_center_num(user_row,df.ix[0]['center_number'])
            user.save_code(user_row,df.ix[0]['id'])

            detail_message = make_detail_message(df)

            bot.send_message(detail_message)
            if df.ix[0]['image']:
                bot.send_img(df.ix[0]['image'])

            bot.send_message("너가 찾고 있던거 이거 맞지???", result_button_maker.create_yn())

