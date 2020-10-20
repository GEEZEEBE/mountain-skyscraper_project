from pymongo import MongoClient
from datetime import datetime

import mongoDB
import mysqlDB
import get_coord
db = {                                      # mongoDB
        'db_name':"webscrapDB",
        'collection_name':"skyscraperCollection"
        }
bldg_table = 'skyscrapers'                            # mariaDB
bldg_img_table = 'bldg_images'                        # mariaDB

def to_mysqlDB():
    keys_img = ['bldg_id', 'bldg_link', 'reg_date']
    keys_bldg = ['ranking', 'building_name', 'city_name', 'country', 'height_m', 'height_ft', 'floor', 'completion_year', 'structure', 'category', 'thumbnail', 'x_coord', 'y_coord', 'reg_date']
    results = mongoDB.DBfindAll(db)
    i = 0
    for result in results:
        x_coord, y_coord = get_coord.get_coord(result['building_name'])
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
            values = list()
            values.append(i)
            values.append(img_link)
            values.append(datetime.now())
            print(values)
            mysqlDB.DBinsert(bldg_img_table, keys_img, values)

if __name__ == "__main__":
    to_mysqlDB()

