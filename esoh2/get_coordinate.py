# 모듈 불러오기
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib
import os
import time
import re
import mongodb

def readfile(strname):
    """
    설명 : file을 라인 단위로 읽어 리턴한다
    """
    with open(strname) as f:
        lines = f.readlines()
    return lines

def main():
    # 드라이버 불러오기
    driver = webdriver.Chrome("./chromedriver.exe")

    # GET 메서드 호출하기
    strurl = "https://www.google.co.kr/maps/place/"
    driver.get(strurl)
    driver.implicitly_wait(5)

    # mongodb 연결하기
    client = mongodb.ConnectDB()
    # 파일 읽기
    lines = readfile("city.txt")

    for line in lines:
        # 입력어 
        line = line.strip()
        data = line.replace('&', ' ')

        # 검색어 입력하기
        elem = driver.find_element_by_css_selector("#searchboxinput")
        elem.click()
        elem.clear()
        elem.send_keys(data)
        elem.send_keys(Keys.ENTER)

        time.sleep(3)

        # 데이터 존재 유무 파악하기
        try:
            elem = driver.find_element_by_css_selector("#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-bad-query > div:nth-child(1) > div.section-bad-query-title")
            if elem.text:
                objlist = [line, '0', '0']
            else:
                match = re.search("@([0-9\.\-]+),([0-9\.\-]+)", driver.current_url)

                 # 이름, 위도, 경도
                objlist = [line, match.group(1), match.group(2)]
        except Exception as e:
            match = re.search("@([0-9\.\-]+),([0-9\.\-]+)", driver.current_url)

            # 이름, 위도, 경도
            objlist = [line, match.group(1), match.group(2)]

        print(objlist)

        # DB 넣기
        mongodb.InsertDB(client, objlist)

    # mongodb 닫기
    client.close()

if __name__ == "__main__":
    main()
