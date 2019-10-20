from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import splitImg
import numpy as np
import cv2

np_data = []
np_label = []

while True:
    cnt = 0
    try:
        chrome = webdriver.Chrome()
        chrome.get('http://111.186.57.85:10202/start')

        while True:
            now = chrome.find_element_by_xpath('/html/body/h1').text
            now = int(now[6:now.find('/')])
            cnt = now
            URL_PATH = chrome.find_element_by_xpath(
                '/html/body/img').get_attribute('src')
            cap = cv2.VideoCapture(URL_PATH)
            ret, img = cap.read()
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            ret, img = cv2.threshold(img, 215, 255, cv2.THRESH_BINARY)
            cur_data = splitImg.Split(img)

            chrome.find_element_by_xpath('/html/body/form/input[2]').submit()
            time.sleep(0.5)
            label_str: str = chrome.find_element_by_xpath('/html/body/p').text
            if label_str.startswith('You maybe smarte'):
                np.save('./Data/np_data.npy', np.array(np_data))
                np.save('./Data/np_label.npy', np.array(np_label))
                print('数据保存成功！')
                chrome.get('http://111.186.57.85:10202/start')
                continue

            label_str = label_str[label_str.find(
                'ASS: ') + 5: label_str.find('!')]
            print(label_str)

            if len(cur_data) != len(label_str):
                print('数据长度校验错误！')
                chrome.get('http://111.186.57.85:10202/start')
                continue

            # Write
            for i in cur_data:
                np_data.append(i)

            for i in label_str:
                np_label.append(int(ord(i) - ord('a')))

            print(f'当前的data长度为{len(np_data)}，label长度为{len(np_label)}。')

    except Exception as err:
        print(err)
        chrome.close()
