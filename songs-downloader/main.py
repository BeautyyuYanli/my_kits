import feedparser
import downloader
import ffmpeg
import time
# feed = feedparser.parse('http://127.0.0.1:1200/bilibili/fav/10725385/53706285')
feed = feedparser.parse('file:///home/beautyyu/Downloads/1.xml')
with open('database.pwp', 'r') as f:
    donelist = f.read().split('$')
donelist.pop()
print(donelist)
for i in feed.entries:
    if i.link not in donelist:
        print(i.link)
        try:
            ftitle = downloader.main(i.link + '?p=1')
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
