import pymysql.cursors


# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='mydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def DBinsert(table, keys, values):

    # keys = [k for k in data.keys()]
    # values = [v for v in data.values()]

    with connection.cursor() as cursor:
        sql = f"INSERT INTO {table} ({', '.join(list(keys))}) VALUES ({', '.join(['%s']*len(keys))})"
        print(sql)
        cursor.execute(sql, values)

    connection.commit()


def DBselectAll():

    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            cursor.execute(sql, ('webmaster@python.org',))
            result = cursor.fetchone()
            print(result)
    finally:
        connection.close()