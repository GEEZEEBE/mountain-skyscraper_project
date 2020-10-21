import requests
import json
from datetime import datetime

import mysqlDB 

def readData():
    cursor = mysqlDB.connection.cursor()

    sql = "SELECT id, city_name FROM skyscrapers"
    cursor.execute(sql)
    result = cursor.fetchall()
    # print(result)
    return result

def getWeatherInfo():
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    apikey = '73901a8ae28e9d6f98f3e1ecbe3903fa'
    
    result = readData()
    bldg_id = [result[i]['id'] for i in range(len(result))]
    cities = [result[i]['city_name'] for i in range(len(result))]
    mainList=[]
    tempList=[]
    feelsList=[]
    humList=[]
    regList=[]
    
    for city in cities:
        # time.sleep(5)
        
        # cityname
        strurl = url.format(city,apikey)
        # print(strurl)
        res = requests.get(strurl)
        if res.status_code == 200:
            rt_dict = json.loads(res.content)
            
        # wheather
        main = rt_dict['weather'][0]['main']
        # print(main)
        temp_F= rt_dict['main']['temp']
        temp_C= str(round(temp_F-273.15, 1))
        feels_F = rt_dict['main']['feels_like']
        feels_C= str(round(feels_F-273.15, 1))
        hum = str(rt_dict['main']['humidity'])
        
        reg_date = datetime.now()

        mainList.append(main)
        tempList.append(temp_C)
        feelsList.append(feels_C)
        humList.append(hum)
        regList.append(reg_date)
        
    all_i = {
    'bldg_id':bldg_id,
    'city_name':cities,
    'main':mainList,
    'temp_C':tempList,
    'feels_C':feelsList,
    'hum':humList,
    'reg_date':regList
    }
    
    info = []       
    for value in zip (bldg_id, cities, mainList, tempList, feelsList, humList, regList):
        keys = ['bldg_id', 'city_name', 'main_weather', 'temperature_C', 'feels_like_C', 'humidity', 'reg_date']
        infodata = {}
        for k, v in zip(keys, value): # key 하나당 value값 하나씩 묶기 ex) 도시:서울/ 온도:30/ ...
            infodata[k] = v
        info.append(infodata)
    # print(info)
    return info

def weather_to_SQL():
    bldg_weather_table = 'bldg_weather'                            # mariaDB/ information table
    field_names = ['bldg_id', 'city_name', 'main_weather', 'temperature_C', 'feels_like_C', 'humidity', 'reg_date']
    
    infodata= getWeatherInfo()
    for data in infodata:
        mysqlDB.DBinsert(bldg_weather_table, field_names, list(data.values())) # (table name, field name, values)
        print(data)
        

if __name__ == "__main__":
    weather_to_SQL()