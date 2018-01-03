#-*-coding:utf-8-*-

from appium.webdriver.webdriver import WebDriver
import time
from time import sleep
import os
from PIL import Image
from selenium.webdriver.support.ui import WebDriverWait
import tempfile
import shutil
import colorsys
from appium.webdriver.common.touch_action import TouchAction
import subprocess
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.mobileby import By
from selenium.common.exceptions import NoSuchElementException
import unittest

PATH = lambda p: os.path.abspath(p)
TEMP_FILE = PATH(os.path.join(tempfile.gettempdir(), "temp_screen.png"))
currentDir = os.path.dirname(os.path.abspath(__file__))


def find_elementXpath_conditionXpath(driver, elementxPath, conditionXpath):

    if not isinstance(driver,WebDriver):
        raise Exception("driver is not legal boject")
    try:
        el = driver.find_element_by_xpath(elementxPath)
        return el
    except:
        el = driver.find_element_by_xpath(conditionXpath)
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击屏幕显示出按钮'
        el = driver.find_element_by_xpath(elementxPath)
        return el


def find_elementId_conditionXpath(driver, elementId, conditionXpath):

    if not isinstance(driver, WebDriver):
        raise Exception("driver is not legal boject")
    try:
        el = driver.find_element_by_id(elementId)
        return el
    except:
        el = driver.find_element_by_xpath(conditionXpath)
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击屏幕显示出按钮'
        el = driver.find_element_by_id(elementId)
        return el


# 根据Xpath判断消息
def wait_xPathMsg_click_xPathButton(driver, xPathMsg, xPathButton, timeout=20, info='', isOk=True):
    # 如果弹出对话框
    try:
        WebDriverWait(driver, timeout).until(lambda x: x.find_element_by_xpath(xPathMsg))
    except:
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), info,u'未提示'
        return

    el = driver.find_element_by_xpath(xPathButton)
    el.click()
    if isOk:
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), info, u'确定'
        return
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), info, u'取消'


def wait_xPathMsg_click_idButton(driver, xPathMsg, idButton, timeout=20, info='', isOk=True):
    # 如果弹出对话框
    try:
        WebDriverWait(driver, timeout).until(lambda x: x.find_element_by_xpath(xPathMsg))
    except:
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), info, u'未提示'
        return

    el = driver.find_element_by_id(idButton)
    el.click()
    if isOk:
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), info, u'确定'
        return
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), info, u'取消'


# 加载图片
def load_image(image_path):
    if os.path.isfile(image_path):
        load = Image.open(image_path)
        return load
    else:
        return Exception("%s is not exist"%image_path)


# 判断图片相似度
def image_same_as(image_path1,image_path2, percent):
    import math
    import operator

    image1 = load_image(image_path1)
    image2 = load_image(image_path2)

    histogram1 = image1.histogram()
    histogram2 = image2.histogram()

    differ = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a-b)**2 , histogram1, histogram2)))/len(histogram1))

    if differ <= percent:
        return True
    else:
        return False


def write_to_file(dirPath, imageName):
    if not os.path.isdir(dirPath):
        os.makedirs(dirPath)
    zyj = PATH(os.path.join(dirPath, imageName))
    shutil.copy(TEMP_FILE, zyj)


# 控件截图
def get_screenshot_by_box(driver, box, file=TEMP_FILE):

    driver.get_screenshot_as_file(TEMP_FILE)
    image = Image.open(TEMP_FILE)
    newImage = image.crop(box)
    newImage.save(TEMP_FILE)

    if file != TEMP_FILE:
        write_to_file(os.path.split(file)[0], os.path.split(file)[1])


# 控件截图
def get_screenshot_by_element(driver, element, file=TEMP_FILE):

    location = element.location
    size = element.size
    driver.get_screenshot_as_file(TEMP_FILE)

    box = (location["x"], location["y"], location["x"]+size["width"], location["y"]+size["height"])

    image = Image.open(TEMP_FILE)
    newImage = image.crop(box)
    newImage.save(TEMP_FILE)

    if file != TEMP_FILE:
        write_to_file(os.path.split(file)[0], os.path.split(file)[1])


# 获取图片的主要颜色
def get_dominant_color(image):

    #颜色模式转换，以便输出rgb颜色值
    image = image.convert('RGBA')
    #生成缩略图，减少计算量，减小cpu压力
    # image.thumbnail((200, 200))
    max_score = None
    dominant_color = None
    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
        # 跳过纯黑色
        if a == 0:
            continue
        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
        y = (y - 16.0) / (235 - 16)
        # 忽略高亮色
        # if y > 0.9:
        #     continue
        # Calculate the score, preferring highly saturated colors.
        # Add 0.1 to the saturation so we don't completely ignore grayscale
        # colors by multiplying the count by zero, but still give them a low
        # weight.
        score = (saturation + 0.1) * count
        if score > max_score:
            max_score = score
            dominant_color = (r, g, b)
    return dominant_color


def getimage_color(image, color):
    # 颜色模式转换，以便输出rgb颜色值
    image = image.convert('RGBA')
    # 生成缩略图，减少计算量，减小cpu压力
    image.thumbnail((50, 50))
    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
        if (r,g,b) ==color:
            return count

    return 0


def getimage_color_original(image, color):
    # 颜色模式转换，以便输出rgb颜色值
    image = image.convert('RGBA')
    # 生成缩略图，减少计算量，减小cpu压力
    # image.thumbnail((50, 50))
    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
        if (r,g,b) ==color:
            return count

    return 0


def getimage_color_epg(image, color):
    # 颜色模式转换，以便输出rgb颜色值
    image = image.convert('RGBA')
    # 生成缩略图，减少计算量，减小cpu压力
    image.thumbnail((77, 75))
    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
        if (r,g,b) ==color:
            return count

    return 0


def getimage_greater(image, value):
    # 颜色模式转换，以便输出rgb颜色值
    image = image.convert('RGB')
    temp = 0
    # 生成缩略图，减少计算量，减小cpu压力
    #image.thumbnail((50, 50))
    # print image.getcolors(image.size[0] * image.size[1])
    for count, (r, g, b) in image.getcolors(image.size[0] * image.size[1]):
        if r > value and g > value and b > value:
            temp += count
    return temp


def moveTo(driver, x_start, y_start, x_end, y_end):
    action = TouchAction(driver)
    action.long_press(x=x_start, y=y_start).move_to(x=x_end, y=y_end)
    action.release()
    action.perform()


def getSize(driver):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return x, y


# 右划
def swipeRight(driver, t):
    l = getSize(driver)
    x1 = int(l[0] / 5)
    y1 = int(l[1] / 2)
    x2 = int(l[0] * 4 / 5)
    driver.swipe(x1, y1, x2, y1, t)


# 在屏幕上方右划
def swipeRight_high(driver, t):
    l = getSize(driver)
    x1 = int(l[0] / 5)
    y1 = int(l[1] / 5)
    x2 = int(l[0] * 4 / 5)
    driver.swipe(x1, y1, x2, y1, t)


# 在屏幕下方右划
def swipeRight_low(driver, t):
    l = getSize(driver)
    x1 = int(l[0] / 5)
    y1 = int(l[1] * 4 / 5)
    x2 = int(l[0] * 4 / 5)
    driver.swipe(x1, y1, x2, y1, t)


# 左划
def swipeLeft(driver, t):
    l = getSize(driver)
    x1 = int(l[0] * 4 / 5)
    y1 = int(l[1] / 2)
    x2 = int(l[0] / 5)
    driver.swipe(x1, y1, x2, y1, t)


# 在屏幕上方左划
def swipeLeft_high(driver, t):
    l = getSize(driver)
    x1 = int(l[0] * 4 / 5)
    y1 = int(l[1] / 5)
    x2 = int(l[0] / 5)
    driver.swipe(x1, y1, x2, y1, t)


# 在屏幕下方左划
def swipeLeft_low(driver, t):
    l = getSize(driver)
    x1 = int(l[0] * 4 / 5)
    y1 = int(l[1] * 4 / 5)
    x2 = int(l[0] / 5)
    driver.swipe(x1, y1, x2, y1, t)


# 下划
def swipeDown(driver, t):
    l = getSize(driver)
    x1 = int(l[0] / 2)
    y1 = int(l[1] / 4)
    y2 = int(l[1] * 4 / 5)
    driver.swipe(x1, y1, x1, y2, t)


# 在屏幕下方下划
def swipeDown_low(driver, t):
    l = getSize(driver)
    x1 = int(l[0] / 2)
    y1 = int(l[1] * 11 / 18)
    y2 = int(l[1] * 16 / 18)
    driver.swipe(x1, y1, x1, y2, t)


# 上划
def swipeUp(driver, t):
    l = getSize(driver)
    x1 = int(l[0] / 2)
    y1 = int(l[1] * 4 / 5)
    y2 = int(l[1] / 5)
    driver.swipe(x1, y1, x1, y2, t)


# 在屏幕下方上划
def swipeUp_low(driver, t):
    l = getSize(driver)
    x1 = int(l[0] / 2)
    y1 = int(l[1] * 15 / 18)
    y2 = int(l[1] * 12 / 18)
    driver.swipe(x1, y1, x1, y2, t)


# 播放器全屏时

# 右划
def swipeRight_full(driver, t):
    l = getSize(driver)
    x1 = int(l[0] / 5)
    y1 = int(l[1] / 2)
    x2 = int(l[0] * 4 / 5)
    driver.swipe(x1, y1, x2, y1, t)


# 在屏幕右侧右划
def swipeRight_fullright(driver, t):
    l = getSize(driver)
    x1 = int(l[0] * 4 / 7)
    y1 = int(l[1] / 2)
    x2 = int(l[0] * 6 / 7)
    driver.swipe(x1, y1, x2, y1, t)


# 左划
def swipeLeft_full(driver, t):
    l = getSize(driver)
    x1 = int(l[0] * 4 / 5)
    y1 = int(l[1] / 2)
    x2 = int(l[0] / 5)
    driver.swipe(x1, y1, x2, y1, t)


# 在屏幕右侧左划
def swipeLeft_fullright(driver, t):
    l = getSize(driver)
    x1 = int(l[0] * 6 / 7)
    y1 = int(l[1] / 2)
    x2 = int(l[0] * 4 / 7)
    driver.swipe(x1, y1, x2, y1, t)


# 在屏幕左侧 上划
def swipeUp_left(driver, t):
    l = getSize(driver)
    x1 = int(l[0] / 4)
    y1 = int(l[1] * 3 / 4)
    y2 = int(l[1] / 4)
    driver.swipe(x1, y1, x1, y2, t)


# 在屏幕左侧下划
def swipeDown_left(driver, t):
    l = getSize(driver)
    x1 = int(l[0] / 4)
    y1 = int(l[1] / 4)
    y2 = int(l[1] * 3 / 4)
    driver.swipe(x1, y1, x1, y2, t)


# 在屏幕左侧 上划置中间
def swipeMid_left(driver, t):
    l = getSize(driver)
    x1 = int(l[0] / 4)
    y1 = int(l[1] * 5 / 8)
    y2 = int(l[1] * 3 / 8)
    driver.swipe(x1, y1, x1, y2, t)


# 在屏幕右侧上划
def swipeUp_right(driver, t):
    l = getSize(driver)
    x1 = int(l[0] * 3 / 4)
    y1 = int(l[1] * 3 / 4)
    y2 = int(l[1] / 4)
    driver.swipe(x1, y1, x1, y2, t)


# 在屏幕右侧下划
def swipeDown_right(driver, t):
    l = getSize(driver)
    x1 = int(l[0] * 3 / 4)
    y1 = int(l[1] / 4)
    y2 = int(l[1] * 3 / 4)
    driver.swipe(x1, y1, x1, y2, t)


# 在屏幕右侧上划置中间
def swipeMid_right(driver, t):
    l = getSize(driver)
    x1 = int(l[0] * 3 / 4)
    y1 = int(l[1] * 5 / 8)
    y2 = int(l[1] * 3 / 8)
    driver.swipe(x1, y1, x1, y2, t)


def compare(x, y):
    stat_x = os.stat(x)
    stat_y = os.stat(y)
    if stat_x.st_ctime > stat_y.st_ctime:
        return -1
    elif stat_x.st_ctime < stat_y.st_ctime:
        return 1
    else:
        return 0


def file_name(path):
    iterms = os.listdir(path)

    iterm_1 = [path+iterm for iterm in iterms]

    iterm_1.sort(compare)

    # for temp in iterm_1:
    #     print temp
    return iterm_1[0]
