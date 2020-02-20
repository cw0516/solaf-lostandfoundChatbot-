from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def create_callback_data(button_type,category):
    """ Create the callback data associated to each button"""
    return ";".join([button_type,category])

def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")

def create_result_button(losts):

    keyboard = []
    row = []
    length = len(list(losts.index))
    for i in range(0,length):
        print(losts.ix[i])
        name = losts.ix[i]['name']
        place = losts.ix[i]['found_place']
        center = losts.ix[i]['center']
        id = losts.ix[i]['id']
        keyboard.append( [ InlineKeyboardButton("습득물 : " + name + " / " + "습득장소 : " +place + " / " + "보관장소 : " +center ,callback_data = create_callback_data('result',id))])
    return InlineKeyboardMarkup(keyboard).to_json()

def create_yn():
    keyboard = []
    keyboard.append([InlineKeyboardButton('맞아!!!!!! 고마워 솔라프ㅜㅜ', callback_data=create_callback_data('result', 'y'))])
    keyboard.append([InlineKeyboardButton('아니야ㅜㅜ 너 탐정 맞아??', callback_data=create_callback_data('result', 'n'))])
    return InlineKeyboardMarkup(keyboard).to_json()
