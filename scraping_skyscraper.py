import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# mongoDB
def insertDB(data):
    db_url = "mongodb://127.0.0.1:27017"
    db_name = "skyscraperDB"
    collection_name = "skyscraperCollection2"

    with MongoClient(db_url) as client:
        db = client[db_name]
        result = db[collection_name].insert_one(data)

# urls
def getLinks():
    url = "http://www.skyscrapercenter.com/buildings"
    res = requests.get(url)

    if res.status_code == 200:
        soup = BeautifulSoup(res.content, 'lxml')

    # links 가져오기
    alllinks = soup.find_all("td", "building-hover")
    link = [l.find("a")["href"] for l in alllinks]
    return link

 # official website
def getWebsite(link):
    web_list=[]
    for l in link:
        res = requests.get(f"http://www.skyscrapercenter.com{l}")
# res = requests.get("http://www.skyscrapercenter.com/building/burj-khalifa/3")
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'lxml')

        try:
            websites = soup.select("")
            website = [w.get("href") for w in websites]
            web_list.append(website)
        except Exception as e:
            website = "" # append 일경우??? 
    return web_list

# image 정보수집
def getImages(link):
    image_list=[]
    thumb_list=[]
    for l in link:
        res = requests.get(f"http://www.skyscrapercenter.com{l}")
    # res = requests.get("http://www.skyscrapercenter.com/building/burj-khalifa/3")

        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'lxml')
        try:
            #images
            images = soup.select("a.building-image")
            image = [i.get("href") for i in images]
            image_list.append(image[1:3]) # << 사진개수 수정
            
            # thumbnail
            thumbs = soup.select("a.building-image")
            thumb = [i.get("href") for i in thumbs]
            thumb_list.append(thumb[0])
            # image = image[1:]
        except Exception as e:
            image = ""
            thumb = ""
    # print(image_list)
    return thumb_list, image_list

# information
def getInfo(link, image_list, thumb_list):
    res = requests.get("http://www.skyscrapercenter.com/buildings")

    if res.status_code == 200:
        soup = BeautifulSoup(res.content, 'lxml')

    # column_titles
    # column_titles = [soup.select(f"th:nth-child({n})")[0].text for n in range(4, 12)]

    # building names
    try:
        bldg_names= soup.select('a:nth-child(1)')
        bldg_name = [n.text.strip() for n in bldg_names[9:209:2]]
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

    # height(m) >>> Q. selector (5)(6)  ?????
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
        uses = soup.select("td:nth-child(11)")
        use = [n.text.strip() for n in uses[1:]]
    except Exception as e:
        use = ""


    info = {
        "bldg_name":bldg_name,
        "city_name":city_name,
        "country":country,
        "height_m":height_m,
        "height_ft":height_ft,
        "floor":floor,
        "completion":completion,
        "material":material,
        "use":use,
        # "web":web_list,
    }

    info2 = [info for info in zip(bldg_name, city_name, country, height_m, height_ft, floor, completion, material, use, thumb_list, image_list)]
    # print(info2)
    return info2

def skyscraperScrap():
    link = getLinks()
    thumb_list, image_list = getImages(link)
    info = getInfo(link, image_list, thumb_list)
    numbers = [str(number) for number in range(1, len(link)+1)]
    for n, i in zip(numbers, info):
        data = dict()
        data[n] = i
        print(data)
        insertDB(data)

if __name__ == "__main__":
   skyscraperScrap()