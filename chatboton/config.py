API_KEY = '983139267:AAGJnunRvpBWopGw95Owa_XIaejxy2OUNHQ'
SEND_MESSAGE = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)
BOT_UPDATE_URL = 'https://api.telegram.org/bot{API_KEY}/getUpdates'.format(API_KEY=API_KEY)
BOT_INFO_URL = 'https://api.telegram.org/bot{API_KEY}/getMe'.format(API_KEY=API_KEY)
BOT_GET_INFO_URL = 'https://api.telegram.org/bot{API_KEY}/getWebhookInfo'.format(API_KEY=API_KEY)
ANSWER_CALLBACK_QUERY_URL = 'https://api.telegram.org/bot{API_KEY}/answerCallbackQuery'.format(API_KEY=API_KEY)
EDIT_MESSAGE_TEXT_URL = 'https://api.telegram.org/bot{API_KEY}/editMessageText'.format(API_KEY=API_KEY)
EDIT_MESSAGE_REPLY_MARKUP_URL = 'https://api.telegram.org/bot{API_KEY}/editMessageReplyMarkup'.format(API_KEY=API_KEY)
DELETE_MESSAGE_URL = 'https://api.telegram.org/bot{API_KEY}/deleteMessage'.format(API_KEY=API_KEY)
SEND_PHOTO = 'https://api.telegram.org/bot{token}/sendPhoto'.format(token=API_KEY)

color_set = [
    ["흰색", "하얀", "하양", "흰", "밝은", "백색", "화이트", "white", "희멀건", "창백한", "아보리", "아이보리", "베이지","하얀색"],
    ["검은색", "검정", "검은", "까만", "흑색", "어두운", "블랙", "dark", "black", "까망"],
    ["회색", "은색", "실버", "그레이", "gray", "크롬"],
    ["빨간색", "빨간", "빨강", "붉은", "적색", "레드", "red", "시뻘건", "진빨강"],
    ["주황색", "주황", "오렌지", "orange", "코랄",'코럴','산호',"피치", "peach", "chorale"],
    ["핑크색", "핑크", "pink","분홍"],
    ["파란색", "파란", "파랑", "푸른", "청색", "남색", "곤색", "하늘", "네이비", "블루", "blue", "시퍼런", "밝은남"],
    ["보라색", "보라", "퍼플", "purple", "자주색","자홍색"],
    ["노란색", "노란", "노랑", "누런", "황색", "옐로", "yellow", "엘로우", "금색"],
    ["초록색", "초록", "그린", "녹색", "연두", "민트", "green", "청록", "녹차색", "카키"],
    ["갈색", "고동색", "브라운", "brown", "똥색", "동색","밤색"],
]

tag_set = [
    ["핸드폰", "휴대폰", "스마트폰", "전화", "아이폰", "갤럭시폰", "폴더폰", "키즈폰","갤s","갤럭시s","v10","g6","g7","v50","갤럭시a","갤럭시 a","갤럭시 j","갤럭시j","갤럭시 s"],
    ["지갑", "머니클립"],
    ["현금·카드", "현금", "유가증권", "상품권", "카드", "식권", "수표"],
    ["신분증", "여권", "면허증", "등록증", "학생증"],
    ["가방", "백", "파우치", "배낭", "베낭", "봉투", "클러치","주머니","봉지"],
    ["전자기기", 'usb',"노트북", "블릿", "충전","스피커", "외장하드", "맥북", "갤탭", "갤럭시탭", "아이패드", "헤드셋", "배터리","밧데리","비게이션","이어폰", "mp3", "카메라", "랩탑", "삼각대", "보청기", "워치", "키보드", "유선", "무선", "블루투스","기어"],
    ["의류", "옷", "모자", "코트", "자켓", "쟈켓", "점퍼", "잠바", "신발", "스카프", "벨트", "밸트", "스웨터", "니트", "티셔츠", "와이셔츠","남방", "원피스","바지","정장", "타이","가디건","양말","속옷"],
    ["악세사리", "안경", "선글", "귀걸이", "목걸이", "반지", "링", "팔찌", "발찌", "귀찌", "시계", "보석", "큐빅"],
    ["화장품", "립스틱", "아이", "쉐도우","볼터치", "블러셔", "립밤", "틴트", "보습제", "로션", "기초", "챱스틱", "바세린", "에센스"],
    ["우산", "양산", "우비"]
]
