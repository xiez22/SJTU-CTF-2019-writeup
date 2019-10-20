import PytorchCaptcha
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome = webdriver.Chrome()
chrome.get('http://111.186.57.85:10202/start')
while True:
    cnt = 0
    try:
        flag = False
        while True:
            now = chrome.find_element_by_xpath('/html/body/h1').text
            now = int(now[6:now.find('/')])
            '''
            if cnt > 0 and cnt == now:
                time.sleep(2)
            '''
            cnt = now
            url = chrome.find_element_by_xpath(
                '/html/body/img').get_attribute('src')
            ans = PytorchCaptcha.captchaDecode(url)

            chrome.find_element_by_xpath(
                '/html/body/form/input[1]').send_keys(ans)

            if cnt >= 85:
                input_ans = input('请您确认：')
                if len(input_ans) != 0:
                    chrome.find_element_by_xpath(
                        '/html/body/form/input[1]').clear()
                    chrome.find_element_by_xpath(
                        '/html/body/form/input[1]').send_keys(input_ans)

            chrome.find_element_by_xpath('/html/body/form/input[2]').submit()

            if cnt >= 99:
                print('请您手动完成提交！')
                flag = True
                break
        if flag:
            break

    except Exception as err:
        print(err)
        print(f'完成了{cnt}次识别。')
        time.sleep(1)
        if cnt > 90:
            break
        chrome.get('http://111.186.57.85:10202/start')
