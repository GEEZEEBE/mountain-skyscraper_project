from django.shortcuts import render
from django.core.paginator import Paginator
import pymysql.cursors
import folium


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

        lat_long = [result[0]['y_coord'], result[0]['x_coord']]
        m = folium.Map(lat_long, zoom_start=14)
        # m = folium.Map(lat_long, zoom_start=12, tiles='Stamen Terrain')

        # folium 한글깨짐 해결 방법 : 아래 명령어 실행 후 서버 재실행
        # sudo pip3 install git+https://github.com/python-visualization/branca.git@master
        text = "<b>"+result[0]['name']+"</b></br><i>"+result[0]['title']+"</i></br>"

        popText = folium.Html(text+str(lat_long), script=True)
        popup = folium.Popup(popText, max_width=2650)
        folium.Marker(location=lat_long, popup=popup).add_to(m)
        m=m._repr_html_() #updated

        context = {'data':result, 'mountain_map': m}

    return render(request, 'board/mt_detail.html', context)