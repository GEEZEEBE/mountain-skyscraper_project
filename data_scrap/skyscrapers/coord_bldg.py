from pymongo import MongoClient
from datetime import datetime

from kakaoapi import by_keyword
import mongoDB
import mysqlDB


db = {                                      # mongoDB
        'db_name':"webscrapDB",
        'collection_name':"skyscraperCollection"
        }
bldg_table = 'skyscrapers'                            # mariaDB
bldg_img_table = 'bldg_images'                        # mariaDB


def get_coord(bldg):

    keyword = mt['bldg_name'] + ' ' + mt['site'].replace(',', ' ').split()[0]
    print(keyword)
    # print(get_mountain_info2(keyword))
    # print(apiByKeyword(keyword))

    data = by_keyword(keyword)
    print(data['documents'][0]['x'], data['documents'][0]['y'])

    return data['documents'][0]['x'], data['documents'][0]['y']


def to_mysqlDB():

    keys_img = ['bldg_id', 'bldg_link', 'reg_date']
    keys_bldg = ['rank', 'building_name', 'city_name', 'country', 'height_m', 'height_ft', 'floor', 'completion_year', 'structure', 'use', 'thumbnail', 'image']

    results = mongoDB.DBfindAll(db)

    i = 0
    for result in results:
        x_coord, y_coord = get_coord(result)

        img_links = result['image']

        values = [r for r in result.values()]
        values.pop()
        values.append(x_coord)
        values.append(y_coord)
        values.append(datetime.now())
        print(values)
        mysqlDB.DBinsert(bldg_table, keys_bldg, values)

        i += 1
        for img_link in img_links:
            values = []
            values.append(i)
            values.append(img_link)
            values.append(datetime.now())
            print(values)
            mysqlDB.DBinsert(bldg_img_table, keys_img, values)



if __name__ == "__main__":
    to_mysqlDB()
