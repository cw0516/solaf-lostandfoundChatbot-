# 분실물 찾아주는 챗봇
##### 서울시 인공지능 챗봇톤 우수상 
![z](https://user-images.githubusercontent.com/48001039/74924939-b58aaf00-5416-11ea-85c5-d60c7f118c6e.png)
<br><br><br>

## 기획/문제인식

서울시에서 주최하는 인공지능 챗봇톤에 참여하기 위해 준비한 프로젝트이다.  

어떤 챗봇을 만들면 서울시가 마주한 문제를 조금이라도 해결할 수 있을까 고민을 하면서 여러 민원 사례를  찾아보다가  

분실물을 찾는 과정에서 몇몇 불편한 점들이 있다는 것을 알아냈다  

__1. 분실물들의 정보가 [경찰청] 과 [대중교통통합분실물센터] 로 분리되어 있어 한번에 찾기 어렵다__

__2. 분실물을 검색할때 사용자 UI/UX 가 불편하다.__
![search](https://user-images.githubusercontent.com/48001039/74925963-7f4e2f00-5418-11ea-87f3-79501d39921b.PNG)

<br><br>

챗봇의 페르소나는 명탐정 코난 캐릭터를 차용해서 분실물과 분실장소/날짜를 사용자와 대화를 통해 찾아주는 탐정의 페르소나를 채택했다.

<br><br>
## 해결방안
```
분실물들의 정보가 여러 사이트에 흩어져 있는 문제
```
경찰청과 대중교통통합분실물센터에 제공되는 3개월 내 분실물들에 대한 정보를 크롤링해서 통합한 DB를 구축해서 해결
<br>
<br>
<br>

```
분실물 검색할때 사용자 UI/UX 문제
```
현재 위의 두 사이트에서 제공하는 검색보다는 챗봇을 통해 대화형으로 분실물과 분실장소/날짜에 대한 정보를 입력받으면 훨씬 좋은 사용자 경험을
만들 수 있을 것이며 UI는 텔레그램 API 를 이용해서 챗봇의 형태를 갖출 것이다.

<br><br>

## 구현 

> 사용자가 접속하면 간단한 챗봇 소개를 하고 물건을 잃어버린 날짜부터 물어본다.
<img width="543" alt="1" src="https://user-images.githubusercontent.com/48001039/74929544-13bb9000-541f-11ea-8ca4-79851eef994a.PNG">
<br><br>

> 사용자가 입력한 날짜로부터 오늘까지 잃어버린 분실물의 개수를 알려준다 없다면 대화를 마무리 해야한다
> 분실물들이 존재 한다면 사용자가 입력한 날짜는 잠시 저장하고 있고 분실물에 대한 설명을 사용자로부터 입력받고 자연어처리를 통해 키워드를 뽑아낸뒤 입력받은 날짜와 설명을 토대로 DB 검색을한다

<img width="551" alt="2" src="https://user-images.githubusercontent.com/48001039/74930027-1965a580-5420-11ea-96ec-933e1f5925b4.PNG">

> DB 검색 결과를 버튼 형식으로 제공해서 사용자가 버튼을 눌러서 분실물의 상세정보를 확인할 수 있도록 한다.
<img width="529" alt="3" src="https://user-images.githubusercontent.com/48001039/74930581-541c0d80-5421-11ea-9aa0-c233b09a13f6.PNG">

> 분실물이 맞다면 분실물을 보관하고 있는 보관소의 전화번호 위치 정보까지 제공해준다.
<img width="518" alt="4" src="https://user-images.githubusercontent.com/48001039/74930600-5b431b80-5421-11ea-8bb4-e83e2b01b75b.PNG">

<br><br>

## DB 명세

<img width="201" alt="DB" src="https://user-images.githubusercontent.com/48001039/74931052-3c915480-5422-11ea-8923-32b475628a63.PNG">
<img width="735" alt="DB1" src="https://user-images.githubusercontent.com/48001039/74931057-3ef3ae80-5422-11ea-8457-86908b5be24a.PNG">


## 배운 것들
* telegram API document를 정독하고 실제로 사용하면서 Rest API를 사용하는 방법과 document 읽는 것에 익숙해진 것 같다.
* flask로 파이썬 서버를 구축해보았다
* 웹사이트와 다르게 로그인이 없을뿐이지 사용자별로 대화 세션을 다르게 유지해야하므로 엑셀/db에 사용자 정보를 저장하면서 대화를 진행해나가야한다는 것을 
* 자연어처리를 통해 사용자의 입력으로부터 필요한 키워드를 추출하고 그 키워드와 관련된 유의어들을 처리해보았다.
* python과 mysql 


## 사용된 것들

* python _Flask_ for server
* _konlpy_ for natural language processing
* _telegram API_ for client
* _mysql_ for DB  


