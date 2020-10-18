# 모듈 불러오기
import get_mountain_info as mountain
import mongodb



def readfile(strname):
    """
    설명 : file을 라인 단위로 읽어 리턴한다
    """
    with open(strname) as f:
        lines = f.readlines()
    return lines

def savedb(client, strname):
    """
    설명 : 산 이름을 입력하면 MongoDB에 저장한다
    - 인덱스 0 : 성공여부
    - 인덱스 1 : 장소이름
    - 인덱스 2 : 주소
    - 인덱스 3 : 전화번호
    - 인덱스 4 : 홈페이지주소
    """
    mountaininfo = mountain.get_mountain_info1(strname)
    if mountaininfo[0]:
        lat_long = mountain.get_mountain_info2(mountaininfo[2])
        if lat_long[0]:
            objlist = [ mountaininfo[1], mountaininfo[2], mountaininfo[3], mountaininfo[4], lat_long[1], lat_long[2] ]
            mongodb.InsertDB(client, objlist)

def get_mountain(strname):
    """
    설명 : 산 이름을 입력하면 산 정보를 반환한다
    - 인덱스 0 : 성공여부
    - 인덱스 1 : 장소이름
    - 인덱스 2 : 주소
    - 인덱스 3 : 전화번호
    - 인덱스 4 : 홈페이지주소
    """
    objlist = list()

    mountaininfo = mountain.get_mountain_info1(strname)
    if mountaininfo[0]:
        lat_long = mountain.get_mountain_info2(mountaininfo[2])
        if lat_long[0]:
            objlist = [ mountaininfo[1], mountaininfo[2], mountaininfo[3], mountaininfo[4], lat_long[1], lat_long[2] ]

    return objlist

def main1():
    # DB 연결하기
    client = mongodb.ConnectDB()

    # 파일 산 이름 한 줄씩 읽기
    lines = readfile('mountain.txt')
    for line in lines:
        strname = line.strip()
        savedb(client, strname)
        print(strname, "OK")

    # 출력하기
    mongodb.ShowDB(client)

    # 닫기
    client.close()

def main2():
    lines = readfile('mountain.txt')
    for line in lines:
        print(get_mountain(line))

if __name__ == "__main__":
    main1()
