from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt


def VSplit(img):
    x = 0
    while x < img.height:
        flg = 0
        for y in range(img.width):
            if img.getpixel((y, x)) == 0:
                flg = 1
                break
        if flg:
            m = img.height - 1
            while m > x:
                flg = 1
                for n in range(img.width):
                    if img.getpixel((n, m)) == 0:
                        flg = 0
                        break
                if flg:
                    croped = img.crop((0, x, 15, m))
                    newimg = Image.new('1', (15, 20), 1)
                    newimg.paste(croped, (0, 0))
                    return newimg
                m -= 1
            break
        x += 1


def HSplit(img):
    ret = []
    y = 0
    while y < img.width:
        flg = 0
        for x in range(img.height):
            if img.getpixel((y, x)) == 0:
                flg = 1
                break
        if flg:
            n = y + 1
            while n < img.width:
                flg = 1
                for m in range(img.height):
                    if img.getpixel((n, m)) == 0:
                        flg = 0
                        break
                if flg:
                    croped = img.crop((y, 0, n, 40))
                    newimg = Image.new('1', (15, 40), 1)
                    newimg.paste(croped, (0, 0))
                    ret.append(newimg)
                    break
                n += 1
            y = n
        y += 1
    return ret


def Split(img):
    img = Image.fromarray(img)
    ret = []
    tmp = HSplit(img)
    for i in tmp:
        ret.append(np.asarray(VSplit(i)))

    return ret
