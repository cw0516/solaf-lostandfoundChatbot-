# -*- coding: utf-8 -*-
import os, time, urllib, requests
import webbrowser, selenium, ast
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import smtplib
from email.mime.text import MIMEText
# from sqlalchemy import create_engine
# import pymysql
from konlpy.tag import Okt

# pymysql.install_as_MySQLdb()

# url = 'http://www.seoul.go.kr/v2012/find.html'
url = 'http://115.84.165.106/admin/find_list.jsp'
url_img = 'http://115.84.165.106/upload/'
url_page = 'http://115.84.165.106/admin/find_list.jsp?like_where=get_name&targetCode=&searchKey=&sort_1=&code1=&code2=&code3=&code4=&code5=&code6=&code7=&code8=&cate1=&cate2=&cate3=&cate4=&cate5=&cate6=&cate7=&cate8=&cate9=&cate10=&cate11=&date_start=&date_end=&yy=&mm=&id=1371392&curPage='
# 크롬 드라이버에 옵션 주기
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 인터페이스 없는 , 창 꼭 안띄워도 되는
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920x1080')

# path = "C://class//"   # 파일 저장 위치


######### 내부 DB  ######## (색, 사이즈, 재질 등 특징)
color_set = [
    ["회색", "은색", "실버", "그레이", "gray", "크롬"],
    ["빨간색", "빨간", "빨강", "붉은", "적색", "레드", "red", "시뻘건"],
    ["주황색", "주황", "오렌지", "orange", "코랄", "피치", "peach", "chorale"],
    ["핑크색", "핑크", "분홍", "pink"],
    ["파란색", "파란", "파랑", "푸른", "청색", "남색", "곤색", "하늘", "네이비", "블루", "blue", "시퍼런", "밝은남"],
    ["보라색", "보라", "퍼플", "purple", "자주색"],
    ["노란색", "노란", "노랑", "누런", "황색", "옐로", "yellow", "엘로우", "금색"],
    ["초록색", "초록", "그린", "녹색", "연두", "민트", "green", "청록", "녹차색", "카키", "옥색"],
    ["갈색", "고동색", "브라운", "brown", "똥색", "동색", "밤색"],
    ["흰색", "하얀", "하양", "흰", "밝은", "백색", "화이트", "white", "희멀건", "창백한", "아보리", "아이보리", "베이지"],
    ["검은색", "검정", "검은", "까만", "흑색", "어두운", "블랙", "dark", "black", "까망"]
]

tag_set = [
    ["핸드폰", "휴대폰", "스마트폰", "전화", "아이폰", "갤럭시폰", "폴더폰", "키즈폰", "갤s", "갤럭시s", "갤럭시a", "갤럭시j", "갤럭시 s", "갤럭시 a", "갤럭시 j",
     "v10", "g6", "g7", "v50"],
    ["지갑", "머니클립"],
    ["현금·카드", "현금", "유가증권", "상품권", "카드", "식권", "수표"],
    ["신분증", "여권", "면허증", "등록증", "학생증"],
    ["가방", "백", "파우치", "배낭", "베낭", "봉투", "클러치", "주머니", "봉지"],
    ["전자기기", "노트북", "블릿", "충전", "스피커", "외장하드", "맥북", "갤탭", "갤럭시탭", "아이패드", "헤드셋", "배터리", "밧데리", "비게이션", "이어폰", "mp3",
     "카메라", "랩탑", "삼각대", "보청기", "워치", "키보드", "유선", "무선", "블루투스", "기어", "usb"],
    ["의류", "옷", "모자", "코트", "자켓", "쟈켓", "점퍼", "잠바", "신발", "스카프", "벨트", "밸트", "스웨터", "니트", "티셔츠", "와이셔츠", "남방", "원피스",
     "바지", "정장", "타이", "가디건", "양말", "속옷"],
    ["악세사리", "안경", "썬글", "선글", "귀걸이", "목걸이", "반지", "링", "팔찌", "발찌", "귀찌", "시계", "보석", "큐빅"],
    ["화장품", "립스틱", "아이", "쉐도우", "볼터치", "블러셔", "립밤", "틴트", "보습제", "로션", "기초", "챱스틱", "바세린", "에센스"],
    ["우산", "양산", "우비"],
    ["기타", "전자담배", "아이코스", "식품", "식료품", "애완", "반려", "동물", "텀블러"]
]


def find_text(a):  # 태그 안에 텍스트만 추출 !!
    text = []
    i = 0
    while i < len(a) - 2:
        if a[i] == '>' and a[i + 1] != '<' and a[i + 2] != '<':

            for k in range(1, len(a) - i - 1):
                if a[i + k] == '<' and a[i + k + 1] == '/' and 2 < k:
                    text.append(a[i + 1:i + k])
                    i += k
                    break
        i += 1

    content = []
    for t in text:
        t = t.replace('\t', '')
        t = t.replace('\n', '')
        t = t.strip()
        if t != '' and '<' not in t and '>' not in t and '{' not in t: content.append(t)

    return content


def write(a, filename):
    # f = open(path+'lost.txt','w')
    f = open(filename, 'w', encoding='utf-8')
    f.write(str(a))
    f.close()


def crawler(url, number):
    ### 다운받은 크롬드라이브를    ,, driver를 이용해서, 가상으로 해당 홈페이지를 방문한 사용자처럼 행위를 함
    driver = webdriver.Chrome('C:/Users/tachy/py_class/python/chromedriver.exe', options=options)  # 각자 주소 바꾸기
    # os.system('cls')   # 화면 지우기
    ### 창을 띄우는 3초간의 시간 주기
    driver.implicitly_wait(3)
    ### url에 들어가기

    page = 1
    max_page = number  ######
    lost_set = []
    while page <= max_page:
        # time.sleep(1)

        driver.get(url_page + str(page))  # url에  중간에 '?' 들어간위치 바로 앞까지 잘라도 되는듯?
        time.sleep(1.5)

        """
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        s1 = soup.find_all('span',{'class':'font_gray8'})
        for s in s1:
            print(s.text,"ooooooo")"""

        for i in range(1, 11):  # 페이지당 게시글 10개이므로 10번 반복
            driver.find_element_by_xpath(
                '/html/body/form/table/tbody/tr[4]/td/table[2]/tbody/tr[' + str(i) + ']/td[4]/span/a').click()

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            lost = find_text(str(soup).replace('\\xa0', ''))  # 유실물 정보들 텍스트 값들 추출해서 배열로 저장하기

            # 이미지 있으면 이미지 주소 얻어오기
            img_link = ""
            index = str(soup).find('/upload/')
            if index != -1 and 'file' not in str(soup)[index + 8:index + 26]:
                img_link = url_img + str(soup)[index + 8:index + 26]
            else:
                img_link = ""

            # 게시글 내용부분 따로 얻어오기
            content = soup.find_all('td', {'colspan': '2'})[-1].text
            content = content.replace('\n', "")
            content = content.replace('\t', "")
            print(content)
            lost.append(img_link)
            content = content.split('을(를)')[0]
            content = content.split('일 ')[1]
            lost.append(content)

            print('\n', lost)
            print(img_link)
            lost_set.append(lost)  # 데이터 축적

            driver.back()
            if i == 10:  # 페이지 게시글 다 훑었으면 다음 페이지로
                page += 1
                if page % 2 == 0: write(lost_set, "raw_data.txt")  # 기록

    write(lost_set, "raw_data.txt")  # 기록

    """
        except selenium.common.exceptions.NoSuchElementException:

        """


def load_txt():
    f = open('raw_data.txt', 'r', encoding='utf-8')
    text_str = f.read()
    text_str = text_str.replace('\\xa0', '')
    lost_array = ast.literal_eval(text_str)
    # columns = ['date', 'category', 'center', 'center_number', 'center_email', 'state', 'name', 'image', 'id','center_address', 'found_place','description','tag']
    """['0소속기관', '1고려운수(택시번호: 서울33아6707)', '2습득물 이미지', '3습득경위', '4습득물', 
    '5핸드폰', '6습득일', '7 2019-09-27', '담당자', '고려운수(주)', '연락처', '02-2244-7054', 
    'E-mail', 'krtaxi80@naver.com', '처리상태', '수령', '보관장소', '수령', '습득 내용물', 
    '갤럭시J7', '내용', 'http://115.84.165.106/upload/20190927154622.jpg', 
    '저희 고려운수(택시번호: 서울33아6707)에서는 2019년 09월 27일  갤럭시J7을(를) 습득/보관 하(였"""
    result_set = []
    cnt_color = 0
    for i in lost_array:
        result = []
        for k in range(0, len(i)):  # date
            if i[k] == '습득일' and i[k + 1] != '담당자':
                result.append(i[k + 1])

        for k in range(0, len(i)):  # category
            if i[k] == '습득물' and i[k + 1] != '습득일':
                result.append(i[k + 1])

        for k in range(0, len(i)):  # center
            if i[k] == '소속기관' and i[k + 1] != '습득물 이미지':
                result.append(i[k + 1])

        for k in range(0, len(i)):  # center num
            if i[k] == '연락처' and i[k + 1] != 'E-mail':
                result.append(i[k + 1])

        for k in range(0, len(i)):  # center email
            if i[k] == 'E-mail' and i[k + 1] != '처리상태':
                result.append(i[k + 1])

        """if len(result) < 5 :  # 누락 보충 
            result.append('')"""

        for k in range(0, len(i)):  # state
            if i[k] == '처리상태' and i[k + 1] != '보관장소':
                result.append(i[k + 1])

        for k in range(0, len(i)):  # name
            if i[k] == '습득 내용물' and i[k + 1] != '내용':
                result.append(i[k + 1])

        for k in range(0, len(i)):  # image  (내용물은 공백으로 크롤링하는것을 가정), append 안되는것도 잇음
            if i[k] == '내용' and i[k + 1] != '':
                result.append(i[k + 1])
                if result[-1].endswith('jpe'):
                    result[-1] = result[-1].replace('.jpe', '.jpeg')
                elif result[-1].endswith('jpg') or result[-1].endswith('JPG'):
                    pass
                else:
                    result[-1] = ""  # 이외 포맷은 공백처리
        if len(result) == 7: result.append('')

        result.append("")  # id
        result.append("")  # center addr
        result.append("")  # found_place

        # result.append(result[1]+" "+result[6])  # description

        for db in color_set:  # description
            break_on = 0
            for d in db:

                if len(result) > 6 and d in result[6].lower():
                    result.append(db[0])
                    cnt_color += 1
                    # print(result[6]," / ",db[0])
                    break_on = 1
                    break
            if break_on == 1: break

        if len(result) < 12:  # 색정보 없으면 공백 넣기
            result.append("")

        for tag in tag_set:  # tag
            break_on = 0
            for t in tag:
                if len(result) > 6 and t in result[6].lower():
                    result.append(tag[0])
                    break_on = 1
                    break
            if break_on == 1: break

        if len(result) < 13:  # 물품 매치 없으면 기타 분류로 넣기
            result.append("기타")

        for k in range(0, len(i)):  # 치환하기
            if i[k] == '담당자' and i[k + 1] != '연락처':
                result[2] = result[2] + ' ' + i[k + 1]

        # print(len(result),result)

        if len(result) == 13:  # 정상 데이터만
            if '과락' in result[6] or '락됨' in result[6] or '통화' in result[6] or '본인' in result[6] or '지인' in result[
                6] or '연락' in result[6]:
                # print(result[6], '주인 찾아서 제외')
                pass
            else:
                print(result)
                result_set.append(result)

    # print(cnt_color/len(result_set))
    return result_set


def analysis(array):
    analy_cnt = [['폰', 0], ['지갑', 0], ['우산', 0], ['이어폰', 0], ['가방', 0], ['열쇠', 0], ['전자기기', 0], ['현금', 0]]
    for obj in array:
        for item in ['핸드폰', '휴대폰', '스마트폰', '전화']:
            if item in obj[6] or item in obj[1]:
                print(obj[6]);
                analy_cnt[0][1] += 1;
                break
        for item in ['지갑']:
            if item in obj[6] or item in obj[1]:
                print(obj[6]);
                analy_cnt[1][1] += 1;
                break
        for item in ['우산', '양산']:
            if item in obj[6] or item in obj[1]:
                print(obj[6]);
                analy_cnt[2][1] += 1;
                break
        for item in ['이어폰', '에어팟']:
            if item in obj[6] or item in obj[1]:
                print(obj[6]);
                analy_cnt[3][1] += 1;
                break
        for item in ['가방', '봉투', '백']:
            if item in obj[6] or item in obj[1]:
                print(obj[6]);
                analy_cnt[4][1] += 1;
                break
        for item in ['키', '열쇠']:
            if item in obj[6] or item in obj[1]:
                print(obj[6]);
                analy_cnt[5][1] += 1;
                break
        for item in ['전자기기', '노트북', '태블릿', '테블릿', '랩탑']:
            if item in obj[6] or item in obj[1]:
                print(obj[6]);
                analy_cnt[6][1] += 1;
                break
        for item in ['현금', '유가증권', '수표', '상품권']:
            if item in obj[6] or item in obj[1]:
                print(obj[6]);
                analy_cnt[6][1] += 1;
                break

    analy_cnt = sorted(analy_cnt, key=lambda analy_cnt: analy_cnt[1], reverse=True)
    print(analy_cnt, len(array))
    ratio = analy_cnt
    for r in ratio:
        r[1] = round(r[1] * 100 / len(array), 2)
    print('%비율', ratio)


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
    return 'https://map.naver.com/index.nhn?query=' + s1.text


def draw_spots(p_x, p_y):  # 점찍기
    fig = plt.figure(figsize=(18, 12))
    ax1 = fig.add_subplot(1, 1, 1)  # 그래프 1개중 1번째
    # plt.axvline(x=0, color='black', linestyle='-', linewidth=2)
    title = 'words similarity'
    plt.grid()
    plt.title(title)

    plt.axhline(y=0, color='black', linewidth=2)  # 가로 0선 그리기
    # plt.axhline(y=avg, color='green', linewidth=2)  # 가로 평균선 그리기
    plt.scatter(p_x, p_y, s=20, color='red', alpha=0.5)
    plt.legend()
    plt.show()


def insertDB(array):  # data frame 에 넣기
    # for a in array: print(a,'\n')
    columns = ['date', 'category', 'center', 'center_number', 'center_email', 'state', 'name', 'image', 'id',
               'center_address', 'found_place', 'description', 'tag']  # 13개 , 0 ~12
    # engine = create_engine("mysql+pymysql://root:"+"root"+"@localhost:3306/lostandfound?charset=utf8", encoding='utf-8')
    df = pd.DataFrame(array, columns=columns)
    print(df)
    # df.to_sql(name='lostinfo', con=engine, if_exists='append',index=False)
    # df.to_excel('raw_data.xlsx', sheet_name='Sheet1')  # excel 파일로 저장   #####
    return (df)


def date_inc(date, inc):
    import datetime
    date = datetime.datetime.strptime(str(date), '%Y-%m-%d')
    new_date = date + datetime.timedelta(days=int(inc))
    return new_date.strftime('%Y-%m-%d')


def search_DB(text):  # text = 사용자 인풋 문자열
    for words in color_set:
        for word in words:
            if word in text:
                text_add = text.replace(word, word + " " + words[0])
                text = text.replace(word, words[0])
                return [word, words[0], text_add, text]  # 찾은 단어, 인덱스 키워드, 추가한 문자열, 대체한 문자열

    return -1


def get_DB_index():  # 인덱스 정보 출력
    for words in color_set:
        print(words[0])


def send_email(title, text, email):
    if email == "": email = 'lshyun0119@naver.com'  # default 받는 메일 주소
    # 세션 생성
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # TLS 보안 시작
        s.starttls()
        # 로그인 인증  (bunssiri 계정비번은 12345abcde!)
        s.login('bunssiri@gmail.com', 'imufvatjiecjkhwt')  # 지멜주소와 구글 앱비밀번호 (계정비번아님..)
        # 보낼 메시지 설정
        msg = MIMEText(text)
        msg['Subject'] = title
        # 메일 보내기
        s.sendmail("bunssiri@gmail.com", email, msg.as_string())  # 보내는주소, 받는주소
        # 세션 종료
        s.quit()
    except TimeoutError:
        print("email 전송 재시도")
        send_email(title, text, email)


def split(text):  # 형태소 쪼개기
    results = []
    sentence = Okt()
    malist = sentence.pos(text, norm=True, stem=True)

    for word in malist:
        break_on = 0
        if word[1] in ["Noun"]:
            for color in color_set:
                for c in color:
                    if c in word[0]:
                        break_on = 1
                        break
                if break_on == 1: break
            if break_on == 0:
                results.append(word[0])

    return results


def word_freq_check(array):  # 키워드간 유사도 측정
    word_set = []  # 모든 단어 집합
    freq = []
    for a in array:
        words = split(a[6])
        if len(words) > 0:
            for word in words:
                if word not in word_set:  # 단어 목록에 없을땐 추가
                    word_set.append(word)
                    freq.append(1)
                else:  # 단어에 이미 존재시 빈도수 증가
                    for w in range(0, len(word_set)):
                        if word_set[w] == word:
                            freq[w] += 1
    word_freq = []
    for i in range(0, len(word_set)):
        word_freq.append([word_set[i], freq[i]])

    word_freq = sorted(word_freq, key=lambda word_freq: word_freq[1], reverse=True)

    # print(word_freq[:200])
    result_set = []
    word_freq = word_freq  ####
    for n in range(0, len(word_freq)):
        # print(word_freq[n])
        for k in range(n + 1, len(word_freq)):
            if len(word_freq[n][0]) == 1 and word_freq[n][0] != '백' and word_freq[n][0] != '책' and word_freq[n][
                0] != '폰':
                continue
            if n + 1 < len(word_freq) and len(word_freq[k][0]) == 1 and word_freq[k][0] != '백' and word_freq[n + 1][
                0] != '책' and word_freq[n + 1][0] != '폰':
                continue
            if word_freq[n][0].isdigit() == True: continue
            if n + 1 < len(word_freq) and word_freq[k][0].isdigit() == True: continue

            if n + 1 < len(word_freq):
                result = naver_search(word_freq[n][0], word_freq[k][0])
                print(result)
                result_set.append(result)

    write(result_set, 'similar.txt')
    print('==============================\n')
    result_set = sorted(result_set, key=lambda result_set: result_set[2], reverse=True)
    for i in result_set[:200]:
        print(i)


def naver_search(word1, word2):  # array는 2차원 배열
    page = 1
    blog_url = 'https://search.naver.com/search.naver?date_from=&date_option=0&date_to=&dup_remove=1&nso=&post_blogurl=&post_blogurl_without=&query=' + word1 + '&sm=tab_pge&srchby=all&st=sim&where=post&start=1'
    shop_url = 'https://search.shopping.naver.com/search/all.nhn?origQuery=' + word1 + '&pagingIndex=' + str(
        page) + '&pagingSize=40&viewType=list&sort=rel&frm=NVSHPAG&query=' + word1
    # response = requests.get("https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query="+word1)
    response = requests.get(shop_url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    s1 = soup.text

    cnt = s1.count(word2)
    # 최고 빈도수 찾기
    return [word1, word2, cnt]


def load_draw_freq():
    f = open('similar.txt', 'r', encoding='utf-8')
    text_str = f.read()
    f.close()
    text = ast.literal_eval(text_str)
    x, y = [], []
    for i in range(0, len(text)):
        x.append(i)
        y.append(text[i][2])
    draw_spots(x, y)


# get_DB_index()
# print(search_DB("검정 우산"))


##### 본문, main, 실행 제어부분  #####
# crawler(url,200)
# print(get_addr("백제운수"))
# print(len(load_txt()))
# insertDB(load_txt())
# print(date_inc("2019-09-30",2))
# send_email('test 입니다','아하하핳',"")
# analysis(load_txt())
# word_freq_check(load_txt())
# load_draw_freq()
print(get_addr('마포경찰서'))

# print(naver_search("지갑","머니클립"))
# print(naver_search("언더웨어","속옷"))
# print(naver_search("카드","속옷"))
# print(naver_search("카드","현금"))
# print(naver_search("밧데리","배터리"))
# print(naver_search("유가증권","선글라스"))
# print(naver_search("식권","수표"))
# print(naver_search("신발","발찌"))
# print(naver_search("큐빅","귀걸이"))
# print(naver_search("양산","우산"))
# print(naver_search("외장하드","맥북"))
## 자연어처리
## 외부 DB 그대로 이용? : 개인 대 개인 > 분실자 등록 시스템 >