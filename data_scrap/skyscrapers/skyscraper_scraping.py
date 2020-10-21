import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
import time

from mongoDB import DBinsert


def getURLs():
    res = requests.get("http://www.skyscrapercenter.com/buildings")
    soup = BeautifulSoup(res.content, 'lxml')
    # URLs 가져오기
    alllinks = soup.find_all("td", "building-hover")
    links = [l.find("a")["href"] for l in alllinks]
    urls = ["http://www.skyscrapercenter.com" + l for l in links]
    
    return urls

def getName(urls):
    for l in urls:
        res = requests.get(l)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'lxml')
        
        try:
            bldg_names= soup.select('a:nth-child(1)')
            bldg_name = [n.text.strip() for n in bldg_names[9:209:2]]
        except Exception as e:
            bldg_name =""
    return bldg_name

# image 정보수집
def getImages(urls):
    image_list=[]
    thumb_list=[]
    for l in urls:
        res = requests.get(l)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'lxml')
            
        try:
            #images
            allimages = soup.select("a.building-image")
            image_href = [i.get("href")[2:] for i in allimages]
            image_list.append(image_href[1:6]) # << 사진개수 수정
            
            # thumbnail
            thumb = [i.get("href")[2:] for i in allimages]
            thumb_list.append(thumb[0])
            
        except Exception as e:
            image = ""
            thumb = ""
        
    return thumb_list, image_list
    
# information
def getInfo(urls, thumbs, images):
    url = "http://www.skyscrapercenter.com/buildings"
    res = requests.get(url)
    
    if res.status_code == 200:
        soup = BeautifulSoup(res.content, "lxml")

        # Rank
    try:
        ranking = [str(ranking) for ranking in range(1, len(urls)+1)]
    except Exception as e:
        ranking = ""
    
    # building names
    try:
        bldg_names= soup.select('a:nth-child(1)')
        bldg_name = [n.text.strip() for n in bldg_names[9:209:2]]
        # print(bldg_name)
    except Exception as e:
        bldg_name =""
            
    # city_name
    try:
        city_names= soup.select('a[href^="/city/"]')
        city_name = [n.text.strip() for n in city_names]
    except Exception as e:
        city_name = ""

    # coutnry
    try:
        countries =soup.select('a[href^="/country/"]')
        country= [n.text.strip() for n in countries]
    except Exception as e:
        country = ""

    # height(m)
    try:
        heights_m = soup.select("td:nth-child(6)")
        height_m = [n.text.strip() for n in heights_m[1:]]
    except Exception as e:
        height_m = ""

    # height(ft)
    try:
        heights_ft = soup.select("td:nth-child(7)")
        height_ft = [n.text.strip() for n in heights_ft[1:]]
    except Exception as e:
        height_ft = ""

    # floor
    try:
        floors = soup.select("td:nth-child(8)")
        floor = [n.text.strip() for n in floors[1:]]
    except Exception as e:
        floor = ""

    # completion
    try:
        completions = soup.select("td:nth-child(9)")
        completion = [n.text.strip() for n in completions[1:]]
    except Exception as e:
        completion= ""

    # material
    try:
        materials = soup.select("td:nth-child(10)")
        material = [n.text.strip() for n in materials[1:]]
    except Exception as e:
        material = ""

    # use
    try:
        categories = soup.select("td:nth-child(11)")
        category = [n.text.strip() for n in categories[1:]]
    except Exception as e:
        category = ""
        
    try:
        r_date = datetime.now()
    except Exception as e:
        r_date =""

    keys = ['ranking', 'building_name', 'city_name', 'country', 'height_m', 'height_ft', 'floor', 'completion_year', 'material', 'category', 'thumbnail', 'image']
    information = []
    for values in zip(ranking, bldg_name, city_name, country, height_m, height_ft, floor, completion, material, category, thumbs, images):
        data = {}
        for k, v in zip(keys, values):
            data[k] = v
        print(data)
        information.append(data)
    return information
    

def skyscraperScrap():
    db = {'db_name':"webscrapDB", 'collection_name':"skyscraperCollection"}
    urls = getURLs()
    thumbs, images = getImages(urls)
    infos = getInfo(urls, thumbs, images)
    for info in infos:
        print(info)
        DBinsert(db, info)

if __name__ == "__main__":
   skyscraperScrap()