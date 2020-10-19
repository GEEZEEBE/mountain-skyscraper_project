from urllib.parse import quote
import json
import requests

def by_keyword(keyword):
    KakaoAK ='KakaoAK 8bca89540b17aa5ea6811b24f889fba3'

    encText = quote(keyword)
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    url = url + "?query=" + encText

    header = {
        "Authorization":KakaoAK
    }
    print(url)

    response = requests.get(url, headers=header)
    print(response.status_code)
    data = json.loads(response.content)
    # print(json.dumps(data, ensure_ascii=False, indent=3))

    return data


def by_keyword_AT4(keyword):
    KakaoAK ='KakaoAK 8bca89540b17aa5ea6811b24f889fba3'

    encText = quote(keyword)
    url = "https://dapi.kakao.com/v2/local/search/keyword.json?page=1&size=15&sort=accuracy&category_group_code=AT4"
    url = url + "&query=" + encText

    header = {
        "Authorization":KakaoAK
    }
    print(url)

    response = requests.get(url, headers=header)
    print(response.status_code)
    data = json.loads(response.content)
    # print(json.dumps(data, ensure_ascii=False, indent=3))

    return data