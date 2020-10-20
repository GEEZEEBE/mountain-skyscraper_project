# 모듈 불러오기
import os
import re

def get_coord(building_name):
    """
    설명 : 빌딩의 좌표를 읽어와 리턴함
    building_name : 빌딩 이름
    """
    # 파일 읽기
    strfile = os.path.realpath(__file__)
    strfile = os.path.join(os.path.dirname(strfile), "list.txt")
    f = open(strfile, encoding='utf8')
    lines = f.readlines()
    f.close()

    # 검색하기
    for line in lines:
        line = line.strip()
        line = line.replace('&', ' ')
        building_name = building_name.replace('&', ' ')

        match = re.search("^([a-zA-Z\,\.\-\s\w]*)@([a-zA-Z\,\.\-\s\w]*)@([a-zA-Z\,\.\-\s\w]*)", line)
        if match:
            if building_name ==  match.group(1):
                return match.group(2), match.group(3)

    return 0, 0

if __name__ == "__main__":
    print(get_coord("Makkah Royal Clock Tower"))