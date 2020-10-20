# 모듈 불러오기
import requests
from bs4 import BeautifulSoup
from datetime import datetime

import json
import mysqlDB



"""
use mydb;

CREATE TABLE weather_mountain
(
  id         INT(10)     NOT NULL AUTO_INCREMENT,
  name       VARCHAR(30) NULL    ,
  temp       VARCHAR(30) NULL     DEFAULT NULL,
  pressure   VARCHAR(30) NULL     DEFAULT NULL,
  humidity   VARCHAR(30) NULL     DEFAULT NULL,
  wind_speed VARCHAR(30) NULL     DEFAULT NULL,
  wind_deg   VARCHAR(30) NULL     DEFAULT NULL,
  clouds     VARCHAR(30) NULL     DEFAULT NULL,
  reg_date   DATE        NULL     DEFAULT NULL,
  PRIMARY KEY (id)
);
"""


# mariadb table
table_name = 'weather_mountain'



def get_weather(strname, lat, long):
    """
    설명 : 날씨 정보 얻기
    lat : 위도
    long : 경도
    """
    # GET 메서드 호출하기
    strurl = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid=4f02fe76179c9da0b039bc7da2227410&units=metric"
    print(strurl)

    # 요청하기
    res = requests.get(strurl)
    if res.status_code != 200:
        print("error", res.status_code)
        return 0

    # json 데이터 불러오기
    weather = json.loads(res.content)
    # print(weather)
    # print("-"*40)

    data = dict()
    data['name'] = strname
    data['temp'] = weather['main']['temp']
    data['pressure'] = weather['main']['pressure']
    data['humidity'] = weather['main']['humidity']
    data['wind_speed'] = weather['wind']['speed']
    data['wind_deg'] = weather['wind']['deg']
    data['clouds'] = weather['clouds']['all']
    data['reg_date'] = datetime.now()

    print(data)
    mysqlDB.DBinsert(table_name, list(data.keys()), list(data.values()))
    return 1

def getmountains():
    cursor = mysqlDB.connection.cursor()

    sql = "SELECT name, x_coord, y_coord FROM mountains"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

# main
def main():
    results = getmountains()

    for result in results:
        print(result['name'], result['y_coord'], result['x_coord'])
        get_weather(result['name'], result['y_coord'], result['x_coord'])

if __name__ == "__main__":
    main()
