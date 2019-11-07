# 获取验证码
import requests, re
from generate import generate_data_path_enc
from bs4 import BeautifulSoup
import time

headers = {
        'referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }

def getCaptcha(username = None):
    if username is None:
        raise Exception("username can't be none in func_getCaptcha")
    print("in {username} captcha obtaining".format(username=username))
    url_get = 'https://captcha.weibo.com/api/pattern/get?ver=daf139fb2696a4540b298756bd06266a&source=ssologin&usrname={username}&line=160&side=100&radius=30&_rnd=0.11071733718672205&callback=pl_cb'\
        .format(username=username)
    r = requests.get(url_get, headers=headers)
    vids = re.findall('id":"([^"]+)"', r.text)
    vid = vids[0] if len(vids) > 0 else ""
    path_encs = re.findall('path_enc":"([^"]+)"', r.text)
    path_enc = str(path_encs[0]) if len(path_encs) > 0 else ""
    print("in {username}, the captcha data obtained is: ".format(username=username) + path_enc)
    (data_image, captcha_order) = path_enc.split('|')
    result = generate_data_path_enc(data_image, captcha_order, vid)
    if result is not None:
        (path_enc, data_enc, code) = result
        print("path_enc: " + path_enc)
        print("data_enc: " + data_enc)
        print("code: " + code)
        print("vid: " + vid)
        return (vid, path_enc, data_enc)
    return None

def verify(username, vid, path_enc, data_enc):
    # 验证(verify) 验证码
    url_verify = "https://captcha.weibo.com/api/pattern/verify?ver={ver}&id={thisid}&usrname={username}&source=ssologin&path_enc={path_enc}&data_enc={data_enc}&callback=pl_cb".format(
        ver='daf139fb2696a4540b298756bd06266a',
        username=username,
        thisid=vid,
        path_enc=path_enc,
        data_enc=data_enc,
    )
    r = requests.get(url_verify, headers=headers)
    code = re.findall('"code":"([0-9^"]+)"', r.text)
    if len(code) > 0:
        code = code[0]
        if code == '100000':
            return True
        else:
            print("{username} captcha verify failed: {text}".format(username=username, text=r.text))
    else:
        print("{username} captcha verify failed: {text}".format(username=username, text="cant find code in results"))
    return False

def getCookie(username, password, vid = ""):
    # 验证之后进行登陆
    data = {
        'username': username,
        'password': password,
        'savestate': '0',
        'r': 'https://weibo.cn/',
        'ec': '0',
        'pagerefer': 'https://weibo.cn/pub/?vt=',
        'entry': 'mweibo',
        'mainpageflag': '1',
        'vid': vid,
        # 'vid': '334cc10c3c9b7ea6da0dbd76c9f843ef896c9f843ef8',
    }
    url_login = 'https://passport.weibo.cn/sso/login'
    r = requests.post(url_login, data=data, headers=headers)
    r.encoding='utf-8'
    retcode = re.findall('"retcode":([0-9]+)', r.text)
    if len(retcode) > 0:
        retcode = retcode[0]
        if retcode=="20000000":
            try:
                result = (sub, type) = (r.cookies['SUB'], 0)
                return result
            except Exception as e:
                return ("cookie sub not found", -1)
        elif retcode=="50011005":
            return ("need captcha", 1)
        else:
            # return ("unknown problem " + retcode, -1)
            return ("need captcha", 1)
    else:
        return ("retcode not found in get cookie", -1)

def login(sub):
    url_entry = 'https://weibo.cn'
    # login in with cookie
    r = requests.get(url_entry, cookies={"SUB": sub})
    r.encoding = 'utf-8'
    return r

def getAccounts(filename):
    result = []
    with open(filename, 'r') as f:
        accounts = f.readlines()
        if len(accounts) % 2 != 0:
            raise Exception("accounts file content format is wrong")
        print("account count: " + str(len(accounts)))
        for i in range(0, len(accounts), 2):
            result.append({'username': accounts[i], 'password': accounts[i+1]})
    return result

def getUser(text=None):
    try:
        bs = BeautifulSoup(text, 'lxml')
        user_div = bs.find_all(name='div', class_='u')[0]
        userinfo = user_div.find_all(name='div', class_='ut')[0]
        username = userinfo.text.split(u'\xa0')[0]
        return username
    except Exception as e:
        return None

if __name__ == '__main__':
    filename = "accounts/accounts.txt"
    accounts = getAccounts(filename)
    for account in accounts:
        time.sleep(1)
        username, password = account['username'].strip("\n"), account['password'].strip("\n")
        result = getCookie(username=username, password=password)
        cookie = None
        if result[1] == -1:
            print("in {username}: ".format(username=username) + result[0])
        elif result[1] == 0:
            cookie = result[0]
        else:
            result = getCaptcha(username)
            if result is not None:
                vid, path_enc, data_enc = result
                if verify(username, vid, path_enc, data_enc):
                    result = getCookie(username=username, password=password, vid=vid)
                    if result[1] == -1:
                        print("in {username} get cookie again failed: ".format(username=username) + result[0])
                    elif result[1] == 0:
                        cookie = result[0]
            else:
                print("in {username} get captcha parameters failed: ".format(username=username))
        if cookie is not None:
            r = login(cookie)
            nickname = getUser(r.text)
            print("{username} obtain cookie succeed, its username is: ".format(username=username) + nickname)
            with open('cookie/cookies.txt', 'a') as f:
                f.write(cookie + "\n")
                f.close()
        else:
            print("in {username} i didnot obtain the cookie, so sorry ".format(username=username))

