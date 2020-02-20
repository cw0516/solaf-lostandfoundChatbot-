from config import tag_set,color_set
from konlpy.tag import Okt
#from eunjeon import Mecab
#mecab = Mecab()
twitter = Okt()

def get_tokens(text):

    #tokens_mecab = mecab.pos(text)
    #print(tokens_mecab)

    tokens_twitter = twitter.pos(text)
    print(tokens_twitter)

    #tokens = [token[0] for token in tokens_mecab if token[1] == "NNG" or token[1] == "NNP" or token[1] == "VA+ETM"]
    tokens = []
    for token in tokens_twitter:
        if token[1] == "Adjective" or token[1] == "Alpha":
            tokens.append(token[0])

    return tokens

def get_color_token(tokens):


    for colors in color_set:
        for color in colors:
            if color in tokens:

                index = tokens.index(color)
                tokens[index] = colors[0]
                color_token = tokens.pop(index)
                return color_token, tokens
    #색깔 토큰이 없을 때
    return False


def get_tag_token(tokens):

    tag_exist = False
    for tags in tag_set:
        for tag in tags:

            if tag in tokens:
                tag_exist = True
                tag_query = tags[0]
                break
    if tag_exist == False:
        tag_query = "기타"
    return tag_query


if __name__ =='__main__':

    print(get_tag_token(['손톱깍이','검은색']))










