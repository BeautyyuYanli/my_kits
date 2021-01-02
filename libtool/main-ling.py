from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, sys

# delay time: depends on network
d = 0.5
# username ans password
username = '20201081369'
passwd = 'YYHYYH123'
# 伯川=0, 令希=1
lib = 1

if (sys.platform == 'win32'):
    driver = webdriver.Chrome('chromedriver.exe')
else:
    driver = webdriver.Chrome()
driver.get("http://seat.lib.dlut.edu.cn/yanxiujian/client/index.php")

clicker = driver.find_element_by_partial_link_text('登录系统')
ActionChains(driver).click(clicker).perform()

login_username = driver.find_element_by_class_name('person')
login_passwd = driver.find_element_by_class_name('lock')
login_username.send_keys(username)
login_passwd.send_keys(passwd)
login_passwd.send_keys(Keys.RETURN)

clicker = driver.find_element_by_partial_link_text('座位预约')
ActionChains(driver).click(clicker).perform()


# time.sleep(d)
# clicker = wait.until(
#     EC.presence_of_element_located((By.CSS_SELECTOR, 'td'))
# )
while 1:
    try:
        clicker = driver.find_elements_by_css_selector('td')
        ActionChains(driver).click(clicker[lib]).perform()
    except:
        continue
    else:
        break

def if_free(rooms):
    for i in rooms:
        if (int(i.text.split('剩余:')[1]) > 0):
            return i
    return 0

def get_a_free_room():
    while 1:
        # time.sleep(d)
        while 1:
            try:
                rooms = driver.find_elements_by_css_selector('td')
                rooms.pop(0)
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
        time.sleep(d)
        driver.refresh()

def get_a_seat():
    while 1:
        seats = driver.find_elements_by_css_selector('div.seat-normal')
        if not seats:
            continue
        else:
            break
    for i in seats:
        if (i.value_of_css_property('background-color') == 'rgba(185, 222, 160, 1)'):
            return i
    return 0

def book_a_seat():
    seat = get_a_seat()
    if (seat == 0):
        driver.back()
        return 0
    ActionChains(driver).click(seat).perform()
    time.sleep(0.5)
    submit = driver.find_element_by_css_selector('#btn_submit_addorder')
    ActionChains(driver).click(submit).perform()
    while 1:
        try:
            result = driver.find_element_by_css_selector('div.bootbox-body')
        except:
            continue
        else:
            # print(result.text)
            if not result.text:
                continue
            else:
                break
    if (result.text == '预约成功！'):
        code = 1
    else:
        code = 0
        driver.back()
    return code

while 1:
    ActionChains(driver).click(get_a_free_room()).perform()
    # time.sleep(d)
    code = book_a_seat()
    if code:
		drive.close()
        print('success!')
        break
    print('false!')
