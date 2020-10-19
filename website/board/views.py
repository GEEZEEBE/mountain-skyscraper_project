from django.shortcuts import render
from django.core.paginator import Paginator
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='mydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


# Create your views here.
def mt_list(request):
    page = request.GET.get('page', '1')

    with connection.cursor() as cursor:
        sql = "SELECT id, name, title, height FROM mountains"
        cursor.execute(sql)
        result = cursor.fetchall()
        paginator = Paginator(result, 10)
        page_obj = paginator.get_page(page)
        # print(result)

        context = {'data':page_obj}

    return render(request, 'board/mt_list.html', context)

def mt_detail(request, id):
    with connection.cursor() as cursor:
        sql = f"""SELECT * FROM mountains, mt_images
                  WHERE mountains.id={id} AND mountains.id = mt_images.mt_id"""
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)

        context = {'data':result}

    return render(request, 'board/mt_detail.html', context)