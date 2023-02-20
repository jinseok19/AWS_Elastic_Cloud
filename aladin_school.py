# 알라딘 & 학술정보관 열처럼 ㄱㄱ
# 학교

# 문학 : 고전, 소설/시/희곡
# 에세이/산문 : 에세이, 자기계발
# 인문 : 인문학
# 경제/비즈니스 : 경제/경영
# 자연/과학 : 과학, 사회과학
# 컴퓨터/인터넷 : 컴퓨터/모바일
# 외국어 : 외국어
# 문화/예술 : 예술/대중문화
# 가정/생활 : 요리/살림, 건강/취미
# 강의지원도서 : 대학교재/전문서적
# 국외 eBook


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen
import time
from selenium.webdriver.common.by import By
import requests
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import xlwt

driver = webdriver.Chrome("C:/Users/김근영/chromedriver_win32.zip/chromedriver.exe")

# 칼럼 리스트 준비
book_list = []

genre_dict = { 
    3 : "가정/생활", #요리/살림
    4 : "가정/생활", #건강/취미
    5 : "경제/비즈니스", #경제/경영
#    6 : "문학", #고전
    7 : "자연/과학", #과학, 사회과
    8 : "강의지원도서", #대학교재/전문서적
#    9 : "라이트 노벨",
    10 : "문학", #소설/시/희곡
#    11 : "사전/기타",
    12 : "인문", #사회과학
#    13 : "수험서/자격증",
#    14 : "어린이",
    15 : "에세이/산문", # 에세이, 자기계발
#    16 : "여행",
#    17 : "역사",
    18 : "문화/예술", # 예술/대중문화
    19 : "외국어", #외국어
#    20 : "유아",
    21 : "인문", #인문학
#    22 : "인물/평전",
    23 : "에세이/산문",
#    24 : "잡지",
#    25 : "전집/중고전집",
#    26 : "종교/역학",
    27 : "가정/생활", #좋은부모
#    28 : "참고서/학습서",
#    29 : "청소년",
    30 : "컴퓨터/인터넷", # 컴퓨터/모바일
}

df = pd.DataFrame(book_list, columns = ["제목", "저자", "출판사", "출간일", "별점", "장르"])

driver.get("https://www.aladin.co.kr/shop/common/wbest.aspx?BestType=EBookBestseller&BranchType=9&CID=38409")
for genre_num in range(3, 30):
    
    if(genre_num == 3):
        genre_id = 38409
        
    if(genre_num == 6 or genre_num == 9 or genre_num == 11 or genre_num == 13 or genre_num == 14 or genre_num == 16 or genre_num == 17
       or genre_num == 20 or genre_num == 22 or genre_num == 24 or genre_num == 25 or genre_num == 26 or genre_num == 28
       or genre_num == 29):
        genre_num += 1
        continue

    elif(genre_num == 4):
        genre_id = 56388
    elif(genre_num == 5):
        genre_id = 38398
    elif(genre_num == 6):
        genre_id = 38414
    elif(genre_num == 7):
        genre_id = 38405
    elif(genre_num == 8):
        genre_id = 38422
    # elif(genre_num == 9):
    #     genre_id = 56548
    elif(genre_num == 10):
        genre_id = 38396
    # elif(genre_num == 11):
    #     genre_id = 38419
    elif(genre_num == 12):
        genre_id = 38404
    # elif(genre_num == 13):
    #     genre_id = 38412
    # elif(genre_num == 14):
    #     genre_id = 38406
    elif(genre_num == 15):
        genre_id = 56387
    # elif(genre_num == 16):
    #     genre_id = 38408
    # elif(genre_num == 17):
    #     genre_id = 38397
    elif(genre_num == 18):
        genre_id = 38402
    elif(genre_num == 19):
        genre_id = 38411
    # elif(genre_num == 20):
    #     genre_id = 38424
    elif(genre_num == 21):
        genre_id = 38403
    # elif(genre_num == 22):
    #     genre_id = 38399
    elif(genre_num == 23):
        genre_id = 38400
    # elif(genre_num == 24):
    #     genre_id = 38417
    # elif(genre_num == 25):
    #     genre_id = 38426
    # elif(genre_num == 26):
    #     genre_id = 38410
    elif(genre_num == 27):
        genre_id = 38413
    # elif(genre_num == 28):
    #     genre_id = 38420
    # elif(genre_num == 29):
    #     genre_id = 38407
        
        
    genre_num += 1
    time.sleep(1)


    for i in range(1, 3):
        driver.get("https://www.aladin.co.kr/shop/common/wbest.aspx?BestType=EBookBestseller&BranchType=9&CID="+str(genre_id)+"&page="+str(i)+"&cnt=300&SortOrder=1")
        time.sleep(0.5)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 1위 책 클릭(대여 횟수 긁어오기 위함)

        books = soup.select('div.ss_book_box')
        def get_star(book):
            stars = book.select_one("div.ss_book_list img")
            if stars is None:
                return 0
            elif stars['src'] == "//image.aladin.co.kr/img/common/star_s10.gif":
                return 5
            elif stars['src'] == "//image.aladin.co.kr/img/common/star_s9.gif":
                return 4.5
            elif stars['src'] == "//image.aladin.co.kr/img/common/star_s8.gif":
                return 4
            elif stars['src'] == "//image.aladin.co.kr/img/common/star_s7.gif":
                return 3.5
            elif stars['src'] == "//image.aladin.co.kr/img/common/star_s6.gif":
                return 3
            elif stars['src'] == "//image.aladin.co.kr/img/common/star_s5.gif":
                return 2.5
            elif stars['src'] == "//image.aladin.co.kr/img/common/star_s4.gif":
                return 2
            else:
                return 0
        
        for book in books:
            try: #일반적인 경우
                title = book.select('a.bo3')[0].text

                
                li_tags = book.find_all('li')
                second_li_tag = li_tags[2] # 2. 두 번째 li 태그 선택
                info = second_li_tag.get_text() # 3. 두 번째 li 태그 내부의 첫 번째 내용 가져오기

                author=info.split('|')[0]
                publisher=info.split('|')[1]
                date=info.split('|')[2] 
                
                genre = genre_dict[genre_num - 1]
                
                star = get_star(book)
                
                i += 1
                

            except IndexError: #행사 상품
                title = book.select('a.bo3')[0].text

                
                star = get_star(book)
                try: #only 행사 상품
                    li_tags = book.find_all('li')
                    third_li_tag = li_tags[3] # 2. 두 번째 li 태그 선택
                    info = third_li_tag.get_text() # 3. 두 번째 li 태그 내부의 첫 번째 내용 가져오기

                    author=info.split('|')[0]
                    publisher=info.split('|')[1]
                    date=info.split('|')[2]
                    genre = genre_dict[genre_num - 1]
                

                except IndexError: #행사 상품은 아닌데, 출판사가 없음.
                    second_li_tag = li_tags[2]
                    info = second_li_tag.get_text()
                    author=info.split('|')[0]
                    publisher=None
                    date=info.split('|')[1] 
                    genre = genre_dict[genre_num - 1]

            book_list.append([title, author, publisher, date, star, genre])
            i += 1

for i in range(1, 3):
    driver.get("https://www.aladin.co.kr/shop/common/wbest.aspx?BestType=EBookBestseller&BranchType=9&CID=38401&page="+str(i)+"&cnt=300&SortOrder=1")
    time.sleep(0.5)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 1위 책 클릭(대여 횟수 긁어오기 위함)
    books = soup.select('div.ss_book_box')
    def get_star(book):
        stars = book.select_one("div.ss_book_list img")
        if stars is None:
            return 0
        elif stars['src'] == "//image.aladin.co.kr/img/common/star_s10.gif":
            return 5
        elif stars['src'] == "//image.aladin.co.kr/img/common/star_s9.gif":
            return 4.5
        elif stars['src'] == "//image.aladin.co.kr/img/common/star_s8.gif":
            return 4
        elif stars['src'] == "//image.aladin.co.kr/img/common/star_s7.gif":
            return 3.5
        elif stars['src'] == "//image.aladin.co.kr/img/common/star_s6.gif":
            return 3
        elif stars['src'] == "//image.aladin.co.kr/img/common/star_s5.gif":
            return 2.5
        elif stars['src'] == "//image.aladin.co.kr/img/common/star_s4.gif":
            return 2
        else:
            return 0
    for book in books:
        try: #일반적인 경우
            title = book.select('a.bo3')[0].text

            li_tags = book.find_all('li')
            second_li_tag = li_tags[2] # 2. 두 번째 li 태그 선택
            info = second_li_tag.get_text() # 3. 두 번째 li 태그 내부의 첫 번째 내용 가져오기

            author=info.split('|')[0]
            publisher=info.split('|')[1]
            date=info.split('|')[2] 
            
            genre = genre_dict[genre_num]            
            star = get_star(book)
            
            i += 1
            

        except IndexError: #행사 상품
            title = book.select('a.bo3')[0].text

            star = get_star(book)
            try: #only 행사 상품
                li_tags = book.find_all('li')
                third_li_tag = li_tags[3] # 2. 두 번째 li 태그 선택
                info = third_li_tag.get_text() # 3. 두 번째 li 태그 내부의 첫 번째 내용 가져오기

                author=info.split('|')[0]
                publisher=info.split('|')[1]
                date=info.split('|')[2]
                genre = genre_dict[genre_num]
            
            except IndexError: #행사 상품은 아닌데, 출판사가 없음.
                second_li_tag = li_tags[2]
                info = second_li_tag.get_text()
                author=info.split('|')[0]
                publisher=None
                date=info.split('|')[1] 
                genre = genre_dict[genre_num]

        book_list.append([title, author, publisher, date, star, genre])
        i += 1


                
df = pd.DataFrame(book_list, columns = ["제목", "저자", "출판사", "출간일", "별점", "장르"])


df.to_csv("알라딘_장르top100_11개" + '.csv', index = False, encoding = 'utf-8-sig')
print(df)
