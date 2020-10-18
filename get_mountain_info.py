# 모듈 불러오기
import requests
from bs4 import BeautifulSoup

import urllib.parse
import json



def get_mountain_info1(strname):
    """
    설명 : 주소, 전화번호, 홈페이지주소
    리턴값 :
    - 인덱스 0 : 성공여부
    - 인덱스 1 : 장소이름
    - 인덱스 2 : 주소
    - 인덱스 3 : 전화번호
    - 인덱스 4 : 홈페이지주소
    """
    # 변수 설정하기
    nRet = 1
    objList = [0]

    # URL 설정하기
    strname = urllib.parse.quote_plus( strname )
    strurl = "https://dapi.kakao.com/v2/local/search/keyword.json?query=" + strname

    # 헤더 설정하기
    dictHeader = dict()
    dictHeader['Authorization'] = 'KakaoAK 8bca89540b17aa5ea6811b24f889fba3'

    # GET 메서드 요청하기
    response = requests.get( strurl, headers = dictHeader )
    if response.status_code != 200:
        nRet = 0

    # 문자열 디코딩하기
    if nRet:
        strData = response.content.decode( response.encoding )
        dictRegion = json.loads( strData )

        if dictRegion['meta']['total_count']:
            for dictobj in dictRegion['documents']:
                objList = [ nRet, dictobj['place_name'], dictobj['address_name'], dictobj['phone'], dictobj['place_url'] ]
                break
        else:
            nRet = 0
    
    objList[0] = nRet
    return objList



def get_mountain_info2(straddr):
    """
    설명 : 위도, 경도를 얻는다.
    리턴값 :
    - 인덱스 0 : 성공여부
    - 인덱스 1 : 위도
    - 인덱스 2 : 경도
    """

    # 변수 선언하기
    nRet = 1
    objList = [0]

    # URL 설정하기
    strSearch = urllib.parse.quote_plus( straddr )

    strUrl = "https://dapi.kakao.com/v2/local/search/address.json?page=1&size=10&query=" + strSearch

    # 헤더 설정하기
    dictHeader = dict()
    dictHeader['Authorization'] = 'KakaoAK 8bca89540b17aa5ea6811b24f889fba3'

    # GET 메서드 요청하기
    response = requests.get( strUrl, headers = dictHeader )
    if response.status_code != 200:
        nRet = 0

    # 출력하기
    if nRet:
        strData = response.content.decode( response.encoding )
        dictCoord = json.loads( strData )

        # 데이터 얻기
        if dictCoord['meta']['total_count']:
            objList = [1, dictCoord['documents'][0]['y'], dictCoord['documents'][0]['x']]
        else:
            nRet = 0

    objList[0] = nRet
    return objList

if __name__ == "__main__":
    mountain_name = input("산 이름 : ")
    print(mountain_name)
    data = get_mountain_info1(mountain_name)
    if data[0]:
        print(data)

    if data[0]:
        data = get_mountain_info2(data[2])
    print(data)
