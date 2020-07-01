import feedparser
import requests
import downloader
import ffmpeg
import time
import re
import codecs
def bv2av(bvid):
    site = "https://api.bilibili.com/x/web-interface/view?bvid=" + bvid
    lst = codecs.decode(requests.get(site).content, "utf-8").split("\"")
    if int(lst[2][1:-1]) != 0:
        return "视频不存在"
    return 'https://www.bilibili.com/video/av' + lst[16][1:-1]
proxies = { 'http': 'http://127.0.0.1:8888', 'https': 'http://127.0.0.1:8888'}
rss = requests.get('https://rsshub.app/bilibili/fav/10725385/53706285', proxies=proxies).text
feed = feedparser.parse(rss)
# feed = feedparser.parse('file:///home/beautyyu/Downloads/1.xml')
with open('database.pwp', 'r') as f:
    donelist = f.read().split('$')
donelist.pop()
print(donelist)
for i in feed.entries:
    if i.link not in donelist:
        print(i.link)
        print(bv2av(i.link.split('/')[-1]))
        try:
            ftitle = downloader.main(bv2av(i.link.split('/')[-1]) + '?p=1')
            {ffmpeg
                .input('bilibili_video/' + ftitle + '/' + ftitle + '.flv')
                .output('output/' + re.sub(r'[\/\\:*?"<>|]', '', i.title) + '.mp3', ab = '1080k')
                .run()
            }
            donelist.append(i.link)
            with open('database.pwp', 'w') as f:
                f.write('$'.join(donelist) + '$')
                f.close()
        except:
            print('wrong!!')
        time.sleep(900)
