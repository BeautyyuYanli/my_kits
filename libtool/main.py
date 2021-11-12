from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Firefox as CustomDriver
from seleniumrequests.request import RequestMixin
from datetime import date
from xvfbwrapper import Xvfb
import time, sys, json, codecs
def get_by_css(driver, cssstr, multi=0):
    for i in range(30):
    # while 1:
        try:
            if multi:
                element = driver.find_elements_by_css_selector(cssstr)
            else:
                element = driver.find_element_by_css_selector(cssstr)
        except:
            time.sleep(0.3)
            continue
        else:
            return element
    return 0
# delay time: depends on network
d = 0.5
# username ans password
username = sys.argv[2]
passwd = sys.argv[3]
# 伯川=1, 令希=2
lib = sys.argv[1]
vdis = Xvfb()
vdis.start()
class MyCustomWebDriver(CustomDriver, RequestMixin):
    pass
if (sys.platform == 'win32'):
    driver = MyCustomWebDriver('chromedriver.exe')
else:
    driver = MyCustomWebDriver()

if __name__ == '__main__':

    def if_free(rooms):
        for i in rooms:
            if (int(i.text.split('剩余:')[1]) > 0):
            # if (1):
                return i
        return 0
    
    def get_a_free_room():
        cnt = 0
        while 1:
            time.sleep(d)
            cnt += 1
            while 1:
                try:
                    rooms = get_by_css(driver, 'tbody>tr', 1)
                    rooms.pop(0)
                    rooms.pop(-1)
                except:
                    continue
                else:
                    if not rooms:
                        continue
                    else:
                        break
            room = if_free(rooms)
            if (room != 0):
                return room
            driver.refresh()
            if (cnt % 30) == 0:
                print("retry" + str(cnt))
    
    def book_a_seat(room_id):
        date_str = date.today().strftime('%Y/%m/%d')
        res = driver.request('POST', 'http://seat.lib.dlut.edu.cn/yanxiujian/client/orderRoomAction.php?action=randomRoomSeatChoose', data = {'room_id': str(room_id), 'order_date': date_str})
        if res.status_code == 200:
            res_json = json.loads(codecs.decode(res.text.encode(), 'utf-8-sig')) 
            if res_json['success']:
                code = 1
            else:
                code = 0
        else:
            code = 0

        if code == 1:
            post_data = {'addCode': res_json['data']['addCode'], 'method': 'addSeat'}
            res = driver.request('POST', 'http://seat.lib.dlut.edu.cn/yanxiujian/client/orderRoomAction.php?action=addSeatOrder', data = post_data)
            res_json = json.loads(codecs.decode(res.text.encode(), 'utf-8-sig')) 
            if res.status_code and res_json['success']:
                pass
            else:
                code = 0
        return code
    # login
    driver.get("https://sso.dlut.edu.cn/cas/login?service=http://seat.lib.dlut.edu.cn/yanxiujian/client/login.php?redirect=index.php")
    login_username = driver.find_element_by_class_name('person')
    login_passwd = driver.find_element_by_class_name('lock')
    login_username.send_keys(username)
    login_passwd.send_keys(passwd)
    login_passwd.send_keys(Keys.RETURN)
    time.sleep(d * 2)
    # get list
    if lib == '1':
        driver.get("http://seat.lib.dlut.edu.cn/yanxiujian/client/roomSelectSeat.php?area_id=17")
    elif lib == '2':
        driver.get("http://seat.lib.dlut.edu.cn/yanxiujian/client/roomSelectSeat.php?area_id=32")
    time.sleep(d * 2)
    # check list
    while 1:
        free_room = get_a_free_room()
        room_id = free_room.get_attribute('data-uniqueid')
        code = book_a_seat(room_id)
        if code == 0:
            driver.refresh()
            print('false!')
        else:
            driver.close()
            vdis.stop()
            print('success!')
            break