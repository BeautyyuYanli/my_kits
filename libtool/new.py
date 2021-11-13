import json, time
import sys, requests, datetime, math
import py_ver

# delay time: depends on network
d = 0.5
# username ans password
username = sys.argv[3]
passwd = sys.argv[4]
# 伯川=1, 令希=2
lib = sys.argv[1]
# 1: 满馆随机抢座 2: 随机换座 3: 定点抢座 4: 定点换座
mode = sys.argv[2]

s = py_ver.login(username, passwd)
if lib == '1':
    libId = '17'
elif lib == '2':
    libId = '32'
order_date = datetime.date.today().strftime('%Y/%m/%d')

def r_json(r):
    r = r.content.decode('utf-8')
    r = r.replace('\r', '').replace('\n', '').replace('\ufeff', '')
    return json.loads(r)

def get_a_free_room():
    cnt = 0
    while 1:
        delt = math.floor(datetime.datetime.now().timestamp() * 1000)
        r = s.get('http://seat.lib.dlut.edu.cn/yanxiujian/client/orderRoomAction.php?action=roomList&area_id={}&order_date={}&_={}'.format(libId, order_date, delt))
        l = r_json(r)

        for i in l:
            if i['room_name'].find('111') == -1 and i['room_name'].find('临时') == -1:
                if int(i['en_num']) > int(i['use_num']):
                    print(i['room_name'])
                    return i['room_id']
        cnt += 1
        time.sleep(d)
        if (cnt % 30 == 0):
            print('tried {} times'.format(cnt))
    return 0

def book_random_seat(room_id, mode):
    # r = s.post('http://seat.lib.dlut.edu.cn/yanxiujian/client/orderRoomAction.php?action=randomRoomSeatChoose', 
    # "room_id={}&order_date={}".format(room_id, order_date))
    r = s.post('http://seat.lib.dlut.edu.cn/yanxiujian/client/orderRoomAction.php?action=randomRoomSeatChoose', data = {'room_id': room_id, 'order_date': order_date})
    l = r_json(r)
    print(l)
    if l['success']:
        post_data = {'addCode': l['data']['addCode'], 'method': 'addSeat'}
        if mode == '2':
            post_data['method'] = 'changeSeat'
        r = s.post('http://seat.lib.dlut.edu.cn/yanxiujian/client/orderRoomAction.php?action=addSeatOrder', post_data)
        l = r_json(r)
        if l['success']:
            return 1
        return 0
    else:
        return 0

if mode == '1' or mode == '2':
    while 1:
        free_room = get_a_free_room()
        code = book_random_seat(free_room, mode)
        if code == 0:
            print('false!')
        else:
            print('success!')
            break

def book_advanced_seat():
    order_date = datetime.date.today().strftime('%Y/%m/%d')
    delt = math.floor((datetime.datetime.now() + datetime.timedelta(days=1)).timestamp() * 1000)
    r = s.get('http://seat.lib.dlut.edu.cn/yanxiujian/client/orderRoomAction.php?action=querySeatMap&order_date={}&room_id=199&_={}'.format(order_date, delt))
    l = r_json(r)
    advanced_seats = list(range(133,141)) + list(range(157,165)) + list(range(281, 289)) + \
        list(range(256,264)) + list(range(248,256)) + list(range(224, 232)) + \
        list(range(216,224))
    for i in l:
        for j in i:
            if int(j['seat_label']) in advanced_seats and j['seat_type'] == '1':
                postdate = 'seat_id={}&order_date={}'.format(j['seat_id'], order_date)
                r = s.post('http://seat.lib.dlut.edu.cn/yanxiujian/client/orderRoomAction.php?action=seatChoose', postdate)
                ll = r_json(r)
                if ll['success']:
                    post_data = {'addCode': ll['data']['addCode'], 'method': 'addSeat'}
                    r = s.post('http://seat.lib.dlut.edu.cn/yanxiujian/client/orderRoomAction.php?action=addSeatOrder', post_data)
                    lll = r_json(r)
                    if lll['success']:
                        return 1
                    else:
                        print(lll)
                else:
                    print(ll)
                print(j['seat_label'], 'false')
                time.sleep(0.5)
    return 0

if mode == '3':
    for k in range(60):
        if book_advanced_seat():
            break
        print('no avalible')
        time.sleep(1)