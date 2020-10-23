from pymongo import MongoClient
from datetime import datetime

from kakaoapi import by_keyword, by_keyword_AT4
import mongoDB
import mysqlDB


db = {                                      # mongoDB
        'db_name':"webscrapDB",
        'collection_name':"mountainCollection"
        }
mt_table = 'mountains'                            # mariaDB
mt_img_table = 'mt_images'                        # mariaDB


def get_coord(results):

    keyword = results['name']
    print(keyword)
    data = by_keyword_AT4(keyword)
    if data['meta']['total_count'] == 0:
        keyword = results['name'] + ' ' + results['site'].replace(',', ' ').split()[0]
        print(keyword)
        data = by_keyword(keyword)

    area = ['강원', '충북', '충남', '경북', '경남', '전북', '울산', '전남', '경기']

    for d in data['documents']:
        if d['address_name'][:2] in area and d['phone'] == "":
            print(d['x'], d['y'])
            return d['x'], d['y']

    print(data['documents'][0]['x'], data['documents'][0]['y'])

    return data['documents'][0]['x'], data['documents'][0]['y']


def to_mysqlDB():

    keys_img = ['mt_id', 'link', 'reg_date']
    keys_mt = ['name', 'title', 'site', 'height', 'feature', 'overview', 'information', 'leadtime', 'x_coord', 'y_coord', 'reg_date']

    results = mongoDB.DBfindAll(db)

    i = 0
    for result in results:
        x_coord, y_coord = get_coord(result)

        img_links = result['img_links']

        values = [r for r in result.values()]
        values.pop()
        values.append(x_coord)
        values.append(y_coord)
        values.append(datetime.now())
        print(values)
        mysqlDB.DBinsert(mt_table, keys_mt, values)

        i += 1
        for img_link in img_links:
            values = []
            values.append(i)
            values.append(img_link)
            values.append(datetime.now())
            print(values)
            mysqlDB.DBinsert(mt_img_table, keys_img, values)



if __name__ == "__main__":
    to_mysqlDB()
