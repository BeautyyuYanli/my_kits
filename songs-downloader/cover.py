import requests, os
from bs4 import BeautifulSoup as bs
def get_cover(url):
    page = bs(requests.get(url).content, 'html.parser')
    img = page.find('meta', {'itemprop': 'thumbnailUrl'})
    img_url = img['content']
    with requests.get(img_url) as getimage:
        return getimage.content
if __name__ == '__main__':
    url = 'https://www.bilibili.com/video/BV1FV411i7ok'
    print(get_cover(url))