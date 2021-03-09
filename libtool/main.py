from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, sys
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
def click_by_css(driver, cssstr):
    while 1:
    # for i in range(10):
        try:
            element = get_by_css(driver, cssstr)
            driver.execute_script("$('" + cssstr + "').click()")
            time.sleep(0.2)
        except:
            time.sleep(0.1)
            pass
        else:
            # print('0')
            return
# delay time: depends on network
d = 0.5
# username ans password
username = sys.argv[2]
passwd = sys.argv[3]
# 伯川=1, 令希=2
lib = sys.argv[1]

if __name__ == '__main__':
    if (sys.platform == 'win32'):
        driver = webdriver.Chrome('chromedriver.exe')
    else:
        driver = webdriver.Chrome()
        # driver = webdriver.Firefox()
    driver.get("https://sso.dlut.edu.cn/cas/login?service=http://seat.lib.dlut.edu.cn/yanxiujian/client/login.php?redirect=index.php")
    login_username = driver.find_element_by_class_name('person')
    login_passwd = driver.find_element_by_class_name('lock')
    login_username.send_keys(username)
    login_passwd.send_keys(passwd)
    login_passwd.send_keys(Keys.RETURN)

    clicker = driver.find_element_by_partial_link_text('座位预约')
    ActionChains(driver).click(clicker).perform()

    time.sleep(1)
    click_by_css(driver, 'tr:nth-child(' + lib + ') > td')
    def if_free(rooms):
        for i in rooms:
            if (int(i.text.split('剩余:')[1]) > 0):
            # if (1):
                return i
        return 0
    
    def get_a_free_room():
        cnt = 0
        while 1:
            cnt += 1
            while 1:
                try:
                    rooms = get_by_css(driver, 'td', 1)
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
            if (cnt % 30) == 0:
                print("retry" + str(cnt))
    
    def book_a_seat():
        click_by_css(driver, 'button.btn-primary:nth-child(1)')
        orderModal = get_by_css(driver, '#orderModal')
        # ---- begin check if went to next step ----
        while 1:
            try:
                time.sleep(0.1)
                notification = driver.find_element_by_css_selector('div.bootbox-body')
            except:
                # if orderModal.value_of_css_property('display') != 'none':
                code = 1
                break
            else:
                code = 0
                break
        # ---- end check if went to next step ----
        if code == 1:
            click_by_css(driver, '#btn_submit_addorder')
            result = get_by_css(driver, 'div.bootbox-body')
            if (result == 0):
                code = 1
            else:
                code = 0
        return code
    
    while 1:
        get_a_free_room().click()
        code = book_a_seat()
        if code == 0:
            driver.refresh()
            print('false!')
        else:
            driver.close()
            print('success!')
            break