import urllib.request
import os
from bs4 import BeautifulSoup
def getpage(url):
    res = urllib.request.urlopen(url)
    return(res.read().decode('gbk'))
# initialization
base_url = input('input base_url:')
page = BeautifulSoup(getpage(base_url), 'lxml')
name = page.title.string.replace('\n', '').replace(' ', '').split('小说在线阅读')[0]
# name = '妹妹'
osbase = 'output/' + name
try:
    os.mkdir(osbase)
except:
    pass
osbase = osbase + '/'
result = []
# get menu
for row in page.select('tr'):
    if (row.select('td')[0]['class'][0] == 'vcss'):
        result.append({'title': row.select('td')[0]\
            .string.replace(' ', '').replace('\n', ''), \
            'contents': []})
    else:
        for article in row.select('td'):
            try:
                al = article.select('a')[0]
            except:
                pass
            else:
                try:
                    result[-1]['contents'].append({'url': al['href'],\
                    'title': al.string.replace(' ', '').replace('\n', ''), \
                    'content': ''})
                except:
                    pass
# get contents
for juan in result:
    for zhang in juan['contents']:
        subpage = BeautifulSoup(getpage(base_url + zhang['url']), 'lxml')
        art = ''
        for i in subpage.select('#content')[0].contents:
            if (str(type(i)) == "<class 'bs4.element.NavigableString'>"):
                art = art + str(i)
        zhang['content'] = art
    # write
    f = open(osbase + juan['title'] + '.txt', 'w')
    fw = juan['title'] + '\n\n'
    for zhang in juan['contents']:
        fw = fw + zhang['title'] + '\n\n' + zhang['content'] + '\n\n'
    f.write(fw)
    print('finish ' + juan['title'])
print('finish!')
