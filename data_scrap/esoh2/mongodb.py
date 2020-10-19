# 모듈 불러오기
from bs4 import BeautifulSoup
import requests
import re
from pymongo import MongoClient
import sys
import time

def ConnectDB():
    """
    pymongo 연결하기
    리턴값 : MongoCLient 객체
    """
    str_server = "mongodb://127.0.0.1:27017/"
    client = MongoClient(str_server)
    return client

def InsertDB( client, dataList ):
    """
    BUILDING 테이블에 데이터를 추가한다.
    client : MongoClient 객체
    dataList : BUILDING 정보를 담고 있는 리스트 변수 ( NAME, LATITUDE, LONGITUTDE )
    """
    # DB 선택하기
    db = client['esoh']

    # dict 데이터 객체 생성하기
    data = dict()
    data['NAME'] = dataList[0]
    data['LATITUDE'] = dataList[1]
    data['LONGITUTDE'] = dataList[2]    

    db.BUILDING.insert(data)

def ShowDB( client ):
    """
    BUILDING 테이블의 내용을 출력한다.
    client : MongoClient 객체
    """

    # DB 선택하기
    db = client['esoh']

    # cursor 얻기
    cursor = db.BUILDING.find()

    nCount = 1
    for row in cursor:
        print("%d" %nCount)
        print("이름 : %s" %row['NAME'])
        print("위도 : %s" %row['LATITUDE'])
        print("경도 : %s" %row['LONGITUTDE'])
        print("-"*20)
        nCount = nCount + 1

# main 함수 호출하기
if __name__ == "__main__":
    pass
