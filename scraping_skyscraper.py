import requests
from bs4 import BeautifulSoup
import re

def Links():
    url = "http://www.skyscrapercenter.com/buildings"
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'lxml')

    # links 가져오기 
    links = soup.find_all("td", "building-hover")
    link = [link.find("a")["href"] for link in links]
    return link


# 상세페이지 정보수집
def Detail():
    for l in link:
        res = requests.get(f"http://www.skyscrapercenter.com{l}")
        soup = BeautifulSoup(res.content, 'lxml')

res = requests.get("http://www.skyscrapercenter.com/building/burj-khalifa/3")
soup = BeautifulSoup(res.content, 'lxml')     

# index
index_list=[]
indexes = soup.select("td a")
for index in indexes:
    index_list.append(index.text.strip())
index = index_list[9:14]
index.append(index_list[15])
index.extend(index_list[18:23])
# print(type(index), index)

# description


# official website

    
    


        
        


    
# facts 
# td:nth-child(1) >>> 10~27th 
# td:nth-child(2) >>> 1~27th

# #table-buildings > tbody > tr:nth-child(1) > td.building-hover  > a
# #table-buildings > tbody > tr:nth-child(2) > td.building-hover > a