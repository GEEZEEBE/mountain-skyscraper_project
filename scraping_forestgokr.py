import requests
from bs4 import BeautifulSoup
from time import strftime
from datetime import datetime
from pymongo import MongoClient
import time


def DBinsert(data):
    db_url = "mongodb://127.0.0.1:27017/"
    db_name = "webscrapDB"
    collection_name = "mountainCollection"

    with MongoClient(db_url) as client:
        db = client[db_name]
        if (collection_name not in db.list_collection_names()):
            db.create_collection(collection_name)

        result = db[collection_name].insert_one(data)
        print(result.inserted_id)


def get_names_urls():
    url = "https://www.forest.go.kr/kfsweb/kfi/kfs/foreston/main/contents/FmmntSrch/selectFmmntSrchList.do?mntIndex=1&searchMnt=&searchCnd=&mn=NKFS_03_01_12&orgId=&mntUnit=100"
    res = requests.get(url=url)

    if res.status_code == 200:
        soup = BeautifulSoup(res.content, 'lxml')

    # print(soup.prettify())

    strong_tags = soup.select('div.list_info > strong')
    names = [s.text for s in strong_tags]
    # print(names)

    a_tags = soup.select('#txt > ul > li > a')
    hrefs = [a.get('href') for a in a_tags]
    urls = ['https://www.forest.go.kr' + h for h in hrefs]
    # print(urls)

    return names, urls


def get_infos(url):
    # url = "https://www.forest.go.kr/kfsweb/kfi/kfs/foreston/main/contents/ClbngManage/selectMntnInfoDetail.do;jsessionid=5rNtRp3tpACPIB1envvV8URSUirTY5Vm1xlnyIUXDaG7rbpaVHMChyM18KYqhoxU.frswas01_servlet_engine5?mntnId=20000004"
    print(url)
    res = requests.get(url=url)

    if res.status_code == 200:
        soup = BeautifulSoup(res.content, 'lxml')

    # print(soup.prettify())

    try:
        title = soup.select('#txt > h4')[0].text.split('-')[1].strip()
    except Exception as e:
        title = ""

    try:
        site = soup.select('#txt > ul:nth-child(3) > li')[0].text
    except Exception as e:
        site = ""

    try:
        height = soup.select('#txt > ul:nth-child(5) > li')[0].text
    except Exception as e:
        height = ""

    try:
        feature = soup.select('#txt > p:nth-child(12)')[0].text
    except Exception as e:
        feature = ""

    try:
        overview = soup.select('#txt > div.right_align.h5_ml > p')[0].text
    except Exception as e:
        overview = ""

    try:
        information = soup.select('#txt > p:nth-child(16)')[0].text
    except Exception as e:
        information = ""

    try:
        leadtime = soup.select('#txt > div.myMountain_content > div:nth-child(1) > table > tbody > tr:nth-child(4) > td:nth-child(2)')[0].text.strip()
    except Exception as e:
        leadtime = ""

    # try:
    #     local = soup.select('#txt > div.myMountain_content > div:nth-child(1) > table > tbody > tr:nth-child(1) > td:nth-child(2)')[0].text.strip()
    # except Exception as e:
    #     local = ""

    try:
        div_tags = soup.select('#txt > div.myMountain_slide')
        a_tags = div_tags[0].find_all('a')
        img_links = ['https://www.forest.go.kr' + a.get('href') for a in a_tags]
    except Exception as e:
        img_links = ""

    infos = {
        'title':title,
        'site':site,
        'height':height,
        'feature':feature,
        'overview':overview,
        'infomation':information,
        'leadtime':leadtime,
        # 'local':local,
        'img_links':img_links
    }

    return infos

def scrapwithmongo():
    names, urls = get_names_urls()

    for name, url in zip(names, urls):
        data = dict()
        info = get_infos(url)
        data['name'] = name
        for k, v in info.items():
            data[k] = v
        print(data)
        DBinsert(data)

# print(datetime.now().strftime('%Y-%m-%d %a %H:%M:%s'))

if __name__ == "__main__":
    scrapwithmongo()

