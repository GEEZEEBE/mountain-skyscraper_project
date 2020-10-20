import requests
import json
from datetime import datetime
import datetime

import mongoDB
import mysqlDB 

def readData():
    cursor = mysqlDB.connection.cursor()

    sql = "SELECT id, city_name FROM skyscrapers"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def getWeatherInfo():
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    apikey = '15a69c44009dea19b327ba81ecb4d2b7'
    path = "/home/rapa01/Documents/Develop/learn_webscraping/API_weather/skyscraper_scraping_data.json"
    with open(path, 'rt', encoding='UTF8') as citylist:
        bldgcity_lists = json.load(citylist)
        
    result = readData() 
    bldg_id = []
    cityList = []
    mainList = []
    tempList =[]
    feelsList =[]
    humList = []
    # reg_time = datetime.now()
    for i in range(len(bldgcity_lists)):
        
        # time.sleep(5)
        # cityname
        cities = bldgcity_lists[i]['city_name']
        cityList.append(cities)
        # print(citylist, cities)
        res = requests.get(url.format(cities,apikey))
        if res.status_code == 200:
            rt_dict = json.loads(res.content)

        # wheather
        main = rt_dict['weather'][0]['main']
        temp_F= rt_dict['main']['temp']
        temp_C= round(temp_F-273.15, 1)
        feels_F = rt_dict['main']['feels_like']
        feels_C= round(feels_F-273.15, 1)
        hum = rt_dict['main']['humidity']
        
        # making list
        bldg_id.append(result[0]['id'])
        mainList.append(main)
        tempList.append(temp_C)
        feelsList.append(feels_C)
        humList.append(hum)
        # reg_time.append(datetime.now())
    
    
    information = []   
    for values in zip(cityList, mainList, tempList, feelsList, humList):
        keys = ['city_name', 'main_weather', 'temperature', 'feels_like', 'humidity']
        info = {}
        for k, v in zip(keys, values): # key 하나당 value값 하나씩 묶기 ex) 도시:서울/ 온도:30/ ...
            info[k] = v
        information.append(info)
    print(information)
    return information

def weather_to_SQL():
    bldg_weather_table = 'bldg_weather'                            # mariaDB/ information table
    field_names = ['city_name', 'main_weather', 'temperature', 'feels_like', 'humidity']
    
    result = readData()
    information = getWeatherInfo()
    for data in information:
        # mysqlDB.DBinsert(bldg_weather_table, field_names, data) # (table name, field name, values)
        print(data)
        

if __name__ == "__main__":
    weather_to_SQL()