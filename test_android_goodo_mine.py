#-*-coding:utf-8-*-

import os
import random
import string
import time
import datetime
import methodpackage
from time import sleep,gmtime,strftime
from appium import webdriver
import re
import sys
import win32con
import win32clipboard as w
import colorsys
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.mobileby import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import unittest
import pytesseract
reload(sys)
sys.setdefaultencoding( "utf-8" )

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

selectedColor = (253, 130, 0)
playedColor = (0, 0, 0)

# 定义字符集
alphas = string.letters
nums = string.digits
smybol = "'`~!@#$%^&*()_-+=[]{};:\|,<.>/?\""
alphasnums = alphas + nums
characterset = alphas + nums + smybol


class SimpleAndroidTests(unittest.TestCase):
    # 启动app
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        #desired_caps['platformVersion'] = '4.2'
        # desired_caps['deviceName'] = 'YPOV95LJ99999999'
        desired_caps['deviceName'] = 'XPUDU17303004497'
        # desired_caps['deviceName'] = '351BBHGE53V3'
        desired_caps['unicodeKeyboard'] = True
        desired_caps['resetKeyboard'] = True
        desired_caps['noReset'] = True
        desired_caps['automationName'] = 'uiautomator2'
        desired_caps['app'] = PATH(
            '../../../apps/ApiDemos/bin/com.sumavision.sanping.gudou_4521.apk'
        )

        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

    def tearDown(self):
        # end the session
        self.driver.quit()

    # 等待消息弹出
    def find_toast(self, driver, message):
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, ".//*[contains(@text,'" + message + "')]")),
                message='not find')
            return True
        except:
            return False

    # 启动应用的弹框处理
    def App_Start(self, driver):
        # 选择定位到广东，判断按钮是否存在，存在则直接点，不存在则报异常
        try:
            WebDriverWait(driver, 5).until(lambda x: x.find_element_by_xpath(
                "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout"))
            # 点击确定按钮定位到广东
            el = driver.find_element_by_id("android:id/button2")
            el.click()
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'地位到广东'
        except:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'定位与地区一致'

        # 如果提示更新，放弃更新应用
        methodpackage.wait_xPathMsg_click_idButton(
            driver,
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.LinearLayout/android.widget.Button[1]",
            "com.sumavision.sanping.gudou:id/btnCancel",
            5,
            u'应用更新',
            False)

    # 重现登录
    def relogin(self, driver):
        for i in range(2):
            methodpackage.swipeUp(driver, 500)
            sleep(0.5)

        try:
            el = driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mylogin_logout')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已登录，先退出再登录'
            el.click()
            # 提示“你确认要退出登录吗？”，点击确定
            methodpackage.wait_xPathMsg_click_idButton(
                driver,
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout",
                "com.sumavision.sanping.gudou:id/btnOK",
                3,
                u'你确认要退出登录吗？',
                True)
            self.assertEqual(self.find_toast(self.driver, u'退出登录成功'), True)
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'未登录'

        el = driver.find_element_by_id("com.sumavision.sanping.gudou:id/tv_mine_username")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入我的圈子'

        el = driver.find_element_by_id("com.sumavision.sanping.gudou:id/edit_user_name")
        el.clear()
        el.send_keys("18500986394")

        el = driver.find_element_by_id("com.sumavision.sanping.gudou:id/text")
        el.send_keys("123456")
        sleep(1)

        el = driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mylogin_login")
        el.click()

        # self.assertEqual(True, self.find_toast(self.driver, u'登录成功'))
        el = driver.find_element_by_id('com.sumavision.sanping.gudou:id/tv_mine_username')
        # self.assertEqual(el.text, u'测试结果')
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'登录成功'

    # 获取回看小屏时的播放时间
    def getplay_time_vod(self, driver):
        # 获取当前播放进度
        el = methodpackage.find_elementId_conditionXpath(
            driver,
            "com.sumavision.sanping.gudou:id/tv_progress_small",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        currentTime = el.text.split('/')[0]
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'当前播放时间是', currentTime
        totalsecoud_currentTime = int(currentTime.split(':')[0]) * 3600 + int(currentTime.split(':')[1]) * 60 + int(
            currentTime.split(':')[2])
        return totalsecoud_currentTime

    # 获取直播小屏时的播放时间
    def getplay_time_live(self, driver):
        # 获取当前播放进度
        el = methodpackage.find_elementId_conditionXpath(
            driver,
            "com.sumavision.sanping.gudou:id/tv_progress_small",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        if el.text != u'正在直播':
            curdate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            offsettime = curdate + ' ' + el.text.split('/')[1]
            offtime = datetime.datetime.strptime(offsettime, '%Y-%m-%d %H:%M:%S')
            currenttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            curtime = datetime.datetime.strptime(currenttime, '%Y-%m-%d %H:%M:%S')
            livetime = curtime - offtime
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'当前播放时间是', livetime
            return livetime
        else:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'当前正在直播'
            return el.text

    # 比较时间
    def compare_time(self, start_time, end_time):
        start = time.strptime(start_time, "%m-%d %H:%M")
        end = time.strptime(end_time, "%m-%d %H:%M")
        for i in range(1, 5):
            if start[i] > end[i]:
                return True
            elif start[i] == end[i]:
                continue
            else:
                return False

    def randstr(self, l, strs):
        temp = ''
        for i in range(l):
            s = random.choice(strs)
            temp = temp + s
        return temp

    # 初次启动应用点击所有帮助页面
    def test_0001_first_start(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   初次启动应用点击所有帮助页面：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 滑动首次进应用时的帮助说明图片，判断图片是否存在，存在则操作，不存在则报异常
        try:
            WebDriverWait(self.driver, 3).until(lambda x: x.find_element_by_xpath(
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout"
                "/android.support.v4.view.ViewPager"))
        except:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'不是第一次进应用'
            return

        # 滑动首次进应用时的帮助说明图片
        for i in range(3):
            methodpackage.swipeLeft(self.driver, 500)
        # 如果提示是否同意条款，选择同意
        methodpackage.wait_xPathMsg_click_idButton(
            self.driver,
            '//android.view.View[@content-desc="谷豆TV隐私条款"]',
            "com.sumavision.sanping.gudou:id/btn_confirm",
            2,
            u'同意条款',
            True)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'划动三张图片，同意条款'

        # 随意点击屏幕任意一处，去掉操作说明图示
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/ll_content")
        el.click()

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        el.click()

        # 播放一个节目
        try:
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")
            name = el.text
        except Exception:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道'
            self.assertTrue(False)
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/vod_detail_container').click()

        # 等待播放加载完成
        try:
            WebDriverWait(
                self.driver, 5).until_not(lambda x: x.find_element_by_id(
                "com.sumavision.sanping.gudou:id/LoadingView"
            )
                                           )
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 找到全屏按钮，判断按钮是否存在，存在则直接点，不存在则直播放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_expand",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击全屏'

        # 随意点击两次屏幕，去掉操作说明图示
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/fl_player_container')
        el.click()
        el.click()

    # 获取地区功能
    def test_0002_mine_getlocation(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   获取地区功能：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)
        methodpackage.swipeUp(self.driver, 500)

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_sysconfig")
        el.click()
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/RelativeLayout_City")
        el.click()
        sleep(1)
        els = self.driver.find_elements_by_xpath('//android.widget.ImageView/../android.widget.TextView')
        locname = els[-1].text
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'当前地区：', locname
        self.assertEqual(locname, u'广东')

    # 地区切换功能
    def test_0003_mine_changelocation(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   地区切换功能：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)
        methodpackage.swipeUp(self.driver, 500)

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_sysconfig")
        el.click()
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/RelativeLayout_City")
        el.click()
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/textView1')
        locname1 = els[1].text
        els[1].click()
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/btnOk")
        el.click()
        # 如果提示更新，放弃更新应用
        methodpackage.wait_xPathMsg_click_idButton(
            self.driver,
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout",
            "com.sumavision.sanping.gudou:id/btnOK",
            2,
            u'修改地区',
            True)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'修改地区为', locname1

        self.driver.launch_app()
        # 选择不定位到广东，判断按钮是否存在，存在则直接点，不存在则报异常
        try:
            WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath(
                "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout"))
            # 点击确定按钮定位到广东
            el = self.driver.find_element_by_id("android:id/button1")
            el.click()
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'不地位到广东'
        except:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'定位与地区一致'
        sleep(5)
        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        methodpackage.swipeUp(self.driver, 500)

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_sysconfig")
        el.click()
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/RelativeLayout_City")
        el.click()
        sleep(1)
        els = self.driver.find_elements_by_xpath('//android.widget.ImageView/../android.widget.TextView')
        locname2 = els[-1].text
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'当前地区：', locname2
        self.assertEqual(locname2, locname1)

    '''        
    # 语音设置功能
    def test_0004_mine_voice(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   语音设置功能：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'

        methodpackage.swipeUp(self.driver, 500)

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_sysconfig")
        el.click()
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/RelativeLayout_City")
        el.click()
        el = self.driver.find_element_by_xpath('//android.widget.ImageView/../android.widget.TextView')
        locname = el.text
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'当前地区：', locname
        self.assertEqual(locname, u'广东')
    '''

    # 查看系统缓存
    def test_0005_mine_cache(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   查看系统缓存：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        methodpackage.swipeUp(self.driver, 500)

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_sysconfig")
        el.click()
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tv_cleancache")
        cache = el.text
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'当前缓存：', cache

    '''
    # 设置允许在3G/4G下缓存视频
    def test_0006_mine_allowcache(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   设置允许在3G/4G下缓存视频：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)
        tempfile1 = os.path.join(methodpackage.currentDir, 'temp.png')
        tempfile2 = os.path.join(methodpackage.currentDir, 'png/allow.png')

        methodpackage.swipeUp(self.driver, 500)

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_sysconfig")
        el.click()
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_allowMobileDl")
        methodpackage.get_screenshot_by_element(self.driver, el, tempfile1)
        if methodpackage.image_same_as(tempfile1, tempfile2):
            methodpackage.swipeDown_low(self.driver, 500)
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mine_cache')
            el.click()

        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'当前缓存：', cache
    '''

    # 清除系统缓存
    def test_0007_mine_cleancache(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   清除系统缓存：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        methodpackage.swipeUp(self.driver, 500)

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_sysconfig")
        el.click()
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tv_cleancache")
        precache = el.text
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'当前缓存：', precache
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/RelativeLayout_Cleancache')
        el.click()

        # 提示“确定要清除缓存吗？”，点击确定
        methodpackage.wait_xPathMsg_click_idButton(
            self.driver,
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout",
            "com.sumavision.sanping.gudou:id/btnOK",
            5,
            u'确定要清除缓存吗？',
            True)

        self.assertEqual(self.find_toast(self.driver, u'清除缓存成功！'), True)

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tv_cleancache")
        postcache = el.text
        self.assertEqual(postcache, '0.0Byte')
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'当前缓存：', postcache

    # 好友圈隐私设置
    def test_0008_mine_setfriend(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   好友圈隐私设置：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        methodpackage.swipeUp(self.driver, 500)

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_sysconfig")
        el.click()
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tv_friend_access')
        flag = el.text
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'当前好友圈隐私设置：', flag
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/rl_friend")
        el.click()
        sleep(1)
        els = self.driver.find_elements_by_xpath('//android.widget.ImageView/../android.widget.TextView')
        flag1 = els[-1].text
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'当前好友圈隐私设置：', flag1
        self.assertEqual(flag, flag1)

    # 检查终端版本
    def test_0009_mine_checkupdate(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   检查终端版本：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        methodpackage.swipeUp(self.driver, 500)

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_sysconfig")
        el.click()
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/rl_update")
        el.click()

        self.assertEqual(self.find_toast(self.driver, u'已是最新版本'), True)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已是最新版本'

    # 用户正确注册功能
    def test_0010_mine_register(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   用户正确注册功能：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mylogin_logout')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已登录，先退出再注册'
            el.click()
            # 提示“你确认要退出登录吗？”，点击确定
            methodpackage.wait_xPathMsg_click_idButton(
                self.driver,
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout",
                "com.sumavision.sanping.gudou:id/btnOK",
                5,
                u'你确认要退出登录吗？',
                True)
            self.assertEqual(self.find_toast(self.driver, u'退出登录成功'), True)
        except NoSuchElementException:
            pass

        # 用户登录页面
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
        el.click()

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/text_my_login_register")
        el.click()
        sleep(1)

        els = self.driver.find_elements_by_class_name('android.widget.EditText')
        self.assertEqual(els[0].text, u'请输入手机号或广电号')
        self.assertEqual(els[1].text, u'请输入手机验证码')
        self.assertEqual(els[2].text, u'请输入密码')
        self.assertEqual(els[3].text, u'请再次输入密码')
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/toggle_password')
        self.assertIsNotNone(el)

        els[0].click()
        els[0].send_keys("13436550661")

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/text_register_verification_code")
        el.click()
        self.assertTrue(self.find_toast(self.driver, u'发送短信验证码成功！'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'输入手机号，获取验证码'
        sleep(10)

        self.driver.press_keycode(3)
        el = self.driver.find_element_by_xpath('//android.widget.TextView[@content-desc="信息"]')
        el.click()
        try:
            el = self.driver.find_element_by_xpath('//android.widget.TextView[@text="通知信息"]')
            el.click()
        except:
            pass

        try:
            el = self.driver.find_element_by_xpath('//android.widget.TextView[@text="‪广东广电网络‬"]')
            el.click()
        except:
            pass

        els = self.driver.find_elements_by_id('com.android.mms:id/text_view')
        mes = els[-1].text
        # print mes
        patt = '\d{6}'
        ma = re.search(patt, mes).group()

        self.driver.press_keycode(3)
        self.driver.press_keycode(3)
        el = self.driver.find_element_by_xpath('//android.widget.TextView[@text="谷豆TV"]')
        el.click()

        els = self.driver.find_elements_by_class_name('android.widget.EditText')
        els[1].send_keys(ma)
        els[2].send_keys("123456")
        els[3].send_keys("123456")

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_myregister_register")
        el.click()
        self.assertTrue(self.find_toast(self.driver, u'该账号已注册！'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该账号已注册！'

    # 注册时手机号异常
    def test_0011_mine_register_phone(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   注册时手机号异常：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mylogin_logout')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已登录，先退出再注册'
            el.click()
            # 提示“你确认要退出登录吗？”，点击确定
            methodpackage.wait_xPathMsg_click_idButton(
                self.driver,
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout",
                "com.sumavision.sanping.gudou:id/btnOK",
                5,
                u'你确认要退出登录吗？',
                True)
            self.assertEqual(self.find_toast(self.driver, u'退出登录成功'), True)
        except NoSuchElementException:
            pass

        # 用户登录页面
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
        el.click()

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/text_my_login_register")
        el.click()
        sleep(1)

        els = self.driver.find_elements_by_class_name('android.widget.EditText')
        self.assertEqual(els[0].text, u'请输入手机号或广电号')
        self.assertEqual(els[1].text, u'请输入手机验证码')
        self.assertEqual(els[2].text, u'请输入密码')
        self.assertEqual(els[3].text, u'请再次输入密码')
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/toggle_password')
        self.assertIsNotNone(el)

        els[0].click()
        els[0].send_keys("13436550661")

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/text_register_verification_code")
        el.click()
        self.assertTrue(self.find_toast(self.driver, u'发送短信验证码成功！'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'输入手机号，获取验证码'
        sleep(10)

        self.driver.press_keycode(3)
        el = self.driver.find_element_by_xpath('//android.widget.TextView[@content-desc="信息"]')
        el.click()
        try:
            el = self.driver.find_element_by_xpath('//android.widget.TextView[@text="通知信息"]')
            el.click()
        except:
            pass

        try:
            el = self.driver.find_element_by_xpath('//android.widget.TextView[@text="‪广东广电网络‬"]')
            el.click()
        except:
            pass

        els = self.driver.find_elements_by_id('com.android.mms:id/text_view')
        mes = els[-1].text
        # print mes
        patt = '\d{6}'
        ma = re.search(patt, mes).group()

        self.driver.press_keycode(3)
        sleep(1)
        self.driver.press_keycode(3)
        el = self.driver.find_element_by_xpath('//android.widget.TextView[@text="谷豆TV"]')
        el.click()

        els = self.driver.find_elements_by_class_name('android.widget.EditText')
        els[1].send_keys(ma)
        els[2].send_keys("123456")
        els[3].send_keys("123456")

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_myregister_register")
        el.click()
        self.assertTrue(self.find_toast(self.driver, u'该账号已注册！'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该账号已注册！'

    # 注册时验证码过期
    def test_0012_mine_register_verification_Expiration(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   注册时验证码过期：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mylogin_logout')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已登录，先退出再注册'
            el.click()
            # 提示“你确认要退出登录吗？”，点击确定
            methodpackage.wait_xPathMsg_click_idButton(
                self.driver,
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout",
                "com.sumavision.sanping.gudou:id/btnOK",
                5,
                u'你确认要退出登录吗？',
                True)
            self.assertEqual(self.find_toast(self.driver, u'退出登录成功'), True)
        except NoSuchElementException:
            pass

        # 用户登录页面
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
        el.click()

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/text_my_login_register")
        el.click()
        sleep(1)

        els = self.driver.find_elements_by_class_name('android.widget.EditText')
        self.assertEqual(els[0].text, u'请输入手机号或广电号')
        self.assertEqual(els[1].text, u'请输入手机验证码')
        self.assertEqual(els[2].text, u'请输入密码')
        self.assertEqual(els[3].text, u'请再次输入密码')
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/toggle_password')
        self.assertIsNotNone(el)

        els[0].click()
        els[0].send_keys("13436550662")
        els[1].send_keys('111111')
        els[2].send_keys("123456")
        els[3].send_keys("123456")

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_myregister_register")
        el.click()
        self.assertTrue(self.find_toast(self.driver, u'随机码错误'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'随机码错误'

    # 注册时验证码异常
    def test_0013_mine_register_verification_err(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   注册时验证码异常：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mylogin_logout')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已登录，先退出再注册'
            el.click()
            # 提示“你确认要退出登录吗？”，点击确定
            methodpackage.wait_xPathMsg_click_idButton(
                self.driver,
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout",
                "com.sumavision.sanping.gudou:id/btnOK",
                5,
                u'你确认要退出登录吗？',
                True)
            self.assertEqual(self.find_toast(self.driver, u'退出登录成功'), True)
        except NoSuchElementException:
            pass

        # 用户登录页面
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
        el.click()

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/text_my_login_register")
        el.click()
        sleep(1)

        els = self.driver.find_elements_by_class_name('android.widget.EditText')
        self.assertEqual(els[0].text, u'请输入手机号或广电号')
        self.assertEqual(els[1].text, u'请输入手机验证码')
        self.assertEqual(els[2].text, u'请输入密码')
        self.assertEqual(els[3].text, u'请再次输入密码')
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/toggle_password')
        self.assertIsNotNone(el)

        els[0].click()
        els[0].send_keys("13436550662")
        els[1].send_keys('111111')
        els[2].send_keys("123456")
        els[3].send_keys("123456")

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_myregister_register")
        el.click()
        self.assertTrue(self.find_toast(self.driver, u'随机码错误'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'随机码错误'

    # 注册时密码不一致
    def test_0014_mine_register_password_dif(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   注册时密码不一致：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mylogin_logout')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已登录，先退出再注册'
            el.click()
            # 提示“你确认要退出登录吗？”，点击确定
            methodpackage.wait_xPathMsg_click_idButton(
                self.driver,
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout",
                "com.sumavision.sanping.gudou:id/btnOK",
                5,
                u'你确认要退出登录吗？',
                True)
            self.assertEqual(self.find_toast(self.driver, u'退出登录成功'), True)
        except NoSuchElementException:
            pass

        # 用户登录页面
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
        el.click()

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/text_my_login_register")
        el.click()
        sleep(1)

        els = self.driver.find_elements_by_class_name('android.widget.EditText')
        self.assertEqual(els[0].text, u'请输入手机号或广电号')
        self.assertEqual(els[1].text, u'请输入手机验证码')
        self.assertEqual(els[2].text, u'请输入密码')
        self.assertEqual(els[3].text, u'请再次输入密码')
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/toggle_password')
        self.assertIsNotNone(el)

        els[0].click()
        els[0].send_keys("13436550661")
        els[1].send_keys('111111')
        els[2].send_keys("123456")
        els[3].send_keys("1234567")

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_myregister_register")
        el.click()
        self.assertTrue(self.find_toast(self.driver, u'两次密码不相同!'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'两次密码不相同!'

    # 注册时密码为空
    def test_0015_mine_register_password_emp(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   注册时密码为空：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mylogin_logout')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已登录，先退出再注册'
            el.click()
            # 提示“你确认要退出登录吗？”，点击确定
            methodpackage.wait_xPathMsg_click_idButton(
                self.driver,
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout",
                "com.sumavision.sanping.gudou:id/btnOK",
                5,
                u'你确认要退出登录吗？',
                True)
            self.assertEqual(self.find_toast(self.driver, u'退出登录成功'), True)
        except NoSuchElementException:
            pass

        # 用户登录页面
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
        el.click()

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/text_my_login_register")
        el.click()
        sleep(1)

        els = self.driver.find_elements_by_class_name('android.widget.EditText')
        self.assertEqual(els[0].text, u'请输入手机号或广电号')
        self.assertEqual(els[1].text, u'请输入手机验证码')
        self.assertEqual(els[2].text, u'请输入密码')
        self.assertEqual(els[3].text, u'请再次输入密码')
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/toggle_password')
        self.assertIsNotNone(el)

        els[0].click()
        els[0].send_keys("13436550661")
        els[1].send_keys('111111')
        # els[2].send_keys("123456")
        els[3].send_keys("1234567")

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_myregister_register")
        el.click()
        self.assertTrue(self.find_toast(self.driver, u'信息内容填写不完整'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'信息内容填写不完整'

    # 注册时密码过长或过短
    def test_0016_mine_register_password_longorshort(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   注册时密码过长或过短：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mylogin_logout')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已登录，先退出再注册'
            el.click()
            # 提示“你确认要退出登录吗？”，点击确定
            methodpackage.wait_xPathMsg_click_idButton(
                self.driver,
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout",
                "com.sumavision.sanping.gudou:id/btnOK",
                5,
                u'你确认要退出登录吗？',
                True)
            self.assertEqual(self.find_toast(self.driver, u'退出登录成功'), True)
        except NoSuchElementException:
            pass

        # 用户登录页面
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
        el.click()

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/text_my_login_register")
        el.click()
        sleep(1)

        els = self.driver.find_elements_by_class_name('android.widget.EditText')
        self.assertEqual(els[0].text, u'请输入手机号或广电号')
        self.assertEqual(els[1].text, u'请输入手机验证码')
        self.assertEqual(els[2].text, u'请输入密码')
        self.assertEqual(els[3].text, u'请再次输入密码')
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/toggle_password')
        self.assertIsNotNone(el)

        els[0].click()
        els[0].send_keys("13436550661")
        els[1].send_keys('111111')
        els[2].send_keys("1")
        els[3].send_keys("1234567")

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_myregister_register")
        el.click()
        self.assertTrue(self.find_toast(self.driver, u'密码输入有误'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'密码输入有误，请输入长度为6-32位密码'

    # 成功登录
    def test_0017_mine_login(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功登录'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        self.relogin(self.driver)

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)

        # 退出登录
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mylogin_logout")
        el.click()

        # 提示确定要退出登录，点击确定
        methodpackage.wait_xPathMsg_click_idButton(
            self.driver,
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.TextView[1]",
            "com.sumavision.sanping.gudou:id/btnOK",
            2,
            u'确定退出？',
            True)

        self.assertEqual(True, self.find_toast(self.driver, u'退出登录成功'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'退出登录成功'

        sleep(1)

    # 登录时用户名错误
    def test_0018_mine_login_usr(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'登录时用户名错误'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)
            sleep(0.5)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mylogin_logout')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已登录，先退出再登录'
            el.click()
            # 提示“你确认要退出登录吗？”，点击确定
            methodpackage.wait_xPathMsg_click_idButton(
                self.driver,
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout",
                "com.sumavision.sanping.gudou:id/btnOK",
                5,
                u'你确认要退出登录吗？',
                True)
            self.assertEqual(self.find_toast(self.driver, u'退出登录成功'), True)
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'未登录'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
        el.click()

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/edit_user_name")
        el.clear()
        el.send_keys("18500986395")

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/text")
        el.send_keys("123456")
        sleep(1)

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mylogin_login")
        el.click()

        self.assertEqual(True, self.find_toast(self.driver, u'用户不存在'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'登录失败'

    # 登录时密码错误
    def test_0019_mine_login_password(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'登录时密码错误'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)
            sleep(0.5)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mylogin_logout')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已登录，先退出再登录'
            el.click()
            # 提示“你确认要退出登录吗？”，点击确定
            methodpackage.wait_xPathMsg_click_idButton(
                self.driver,
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout",
                "com.sumavision.sanping.gudou:id/btnOK",
                5,
                u'你确认要退出登录吗？',
                True)
            self.assertEqual(self.find_toast(self.driver, u'退出登录成功'), True)
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'未登录'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
        el.click()

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/edit_user_name")
        el.clear()
        el.send_keys("18500986394")

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/text")
        el.send_keys("1234567")
        sleep(1)

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mylogin_login")
        el.click()

        self.assertEqual(True, self.find_toast(self.driver, u'用户名或者密码错误'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'登录失败'

        sleep(1)

    '''
    # 广电号成功登录
    def test_0020_mine_login_guangdian(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功登录'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)
            sleep(0.5)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mylogin_logout')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已登录，先退出再登录'
            el.click()
            # 提示“你确认要退出登录吗？”，点击确定
            methodpackage.wait_xPathMsg_click_idButton(
                self.driver,
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout",
                "com.sumavision.sanping.gudou:id/btnOK",
                5,
                u'你确认要退出登录吗？',
                True)
            self.assertEqual(self.find_toast(self.driver, u'退出登录成功'), True)
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'未登录'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
        el.click()

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/edit_user_name")
        el.clear()
        el.send_keys("18500986394")

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/text")
        el.send_keys("123456")
        sleep(1)

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mylogin_login")
        el.click()

        # self.assertEqual(True, self.find_toast(self.driver, u'登录成功'))
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tv_mine_username')
        self.assertEqual(el.text, u'测试结果')
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'登录成功'

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)

        # 退出登录
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mylogin_logout")
        el.click()

        # 提示确定要退出登录，点击确定
        methodpackage.wait_xPathMsg_click_idButton(
            self.driver,
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.TextView[1]",
            "com.sumavision.sanping.gudou:id/btnOK",
            2,
            u'确定退出？',
            True)

        self.assertEqual(True, self.find_toast(self.driver, u'退出登录成功'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'退出登录成功'

        sleep(1)

    # 登录时广电号错误
    def test_0021_mine_login_usr_guangdian(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'登录时用户名错误'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)
            sleep(0.5)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mylogin_logout')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已登录，先退出再登录'
            el.click()
            # 提示“你确认要退出登录吗？”，点击确定
            methodpackage.wait_xPathMsg_click_idButton(
                self.driver,
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout",
                "com.sumavision.sanping.gudou:id/btnOK",
                5,
                u'你确认要退出登录吗？',
                True)
            self.assertEqual(self.find_toast(self.driver, u'退出登录成功'), True)
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'未登录'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
        el.click()

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/edit_user_name")
        el.clear()
        el.send_keys("18500986395")

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/text")
        el.send_keys("123456")
        sleep(1)

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mylogin_login")
        el.click()

        self.assertEqual(True, self.find_toast(self.driver, u'账号或密码错误，用户不存在！'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'登录失败'

        sleep(1)
        
    # 卡号绑定CA卡功能
    def test_0022_mine_CA_cardnumber(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'登录时用户名错误'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)
            sleep(0.5)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mylogin_logout')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已登录，先退出再登录'
            el.click()
            # 提示“你确认要退出登录吗？”，点击确定
            methodpackage.wait_xPathMsg_click_idButton(
                self.driver,
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout",
                "com.sumavision.sanping.gudou:id/btnOK",
                5,
                u'你确认要退出登录吗？',
                True)
            self.assertEqual(self.find_toast(self.driver, u'退出登录成功'), True)
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'未登录'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
        el.click()

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/edit_user_name")
        el.clear()
        el.send_keys("18500986395")

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/text")
        el.send_keys("123456")
        sleep(1)

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mylogin_login")
        el.click()

        self.assertEqual(True, self.find_toast(self.driver, u'账号或密码错误，用户不存在！'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'登录失败'

        sleep(1)
        
    # 卡号过期绑定CA卡功能
    def test_0023_mine_CA_cardnumber_Expiration(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'登录时用户名错误'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)
            sleep(0.5)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mylogin_logout')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已登录，先退出再登录'
            el.click()
            # 提示“你确认要退出登录吗？”，点击确定
            methodpackage.wait_xPathMsg_click_idButton(
                self.driver,
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout",
                "com.sumavision.sanping.gudou:id/btnOK",
                5,
                u'你确认要退出登录吗？',
                True)
            self.assertEqual(self.find_toast(self.driver, u'退出登录成功'), True)
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'未登录'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
        el.click()

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/edit_user_name")
        el.clear()
        el.send_keys("18500986395")

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/text")
        el.send_keys("123456")
        sleep(1)

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mylogin_login")
        el.click()

        self.assertEqual(True, self.find_toast(self.driver, u'账号或密码错误，用户不存在！'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'登录失败'

        sleep(1)'''
        
    # 重置密码功能
    def test_0024_mine_resetpassword(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   重置密码功能：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)
            sleep(0.5)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mylogin_logout')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已登录，先退出再登录'
            el.click()
            # 提示“你确认要退出登录吗？”，点击确定
            methodpackage.wait_xPathMsg_click_idButton(
                self.driver,
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout",
                "com.sumavision.sanping.gudou:id/btnOK",
                5,
                u'你确认要退出登录吗？',
                True)
            self.assertEqual(self.find_toast(self.driver, u'退出登录成功'), True)
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'未登录'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
        el.click()

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/text_login_forget')
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击‘忘记密码’，进行密码重置'
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/edit_text')
        lis = [els[i].text for i in range(4)]
        els[0].click()
        els[0].send_keys('13436550661')
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/text_reset_psw_verification_code')
        el.click()
        self.assertTrue(self.find_toast(self.driver, u'发送短信验证码成功！'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'输入手机号，获取验证码'
        sleep(10)

        self.driver.press_keycode(3)
        el = self.driver.find_element_by_xpath('//android.widget.TextView[@content-desc="信息"]')
        el.click()
        try:
            el = self.driver.find_element_by_xpath('//android.widget.TextView[@text="通知信息"]')
            el.click()
        except:
            pass

        try:
            el = self.driver.find_element_by_xpath('//android.widget.TextView[@text="‪广东广电网络‬"]')
            el.click()
        except:
            pass

        els = self.driver.find_elements_by_id('com.android.mms:id/text_view')
        mes = els[-1].text
        # print mes
        patt = '\d{6}'
        ma = re.search(patt, mes).group()

        self.driver.press_keycode(3)
        self.driver.press_keycode(3)
        el = self.driver.find_element_by_xpath('//android.widget.TextView[@text="谷豆TV"]')
        el.click()
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/edit_text')
        els[1].send_keys(ma)
        els[2].send_keys('123456')
        els[3].send_keys('123456')
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_my_reset_psw')
        el.click()

        self.assertTrue(self.find_toast(self.driver, u'重置密码成功'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'重置密码成功'

    # 重置密码时手机号异常
    def test_0025_mine_resetpassword_phone(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'登录时用户名错误'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)
            sleep(0.5)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mylogin_logout')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已登录，先退出再登录'
            el.click()
            # 提示“你确认要退出登录吗？”，点击确定
            methodpackage.wait_xPathMsg_click_idButton(
                self.driver,
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout",
                "com.sumavision.sanping.gudou:id/btnOK",
                5,
                u'你确认要退出登录吗？',
                True)
            self.assertEqual(self.find_toast(self.driver, u'退出登录成功'), True)
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'未登录'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
        el.click()
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/text_login_forget')
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击‘忘记密码’，进行密码重置'
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/edit_text')
        lis = [els[i].text for i in range(4)]
        els[0].click()
        els[0].send_keys('1343655066')
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/text_reset_psw_verification_code')
        el.click()
        self.assertTrue(self.find_toast(self.driver, u'手机号输入有误，请输入11位手机号'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'手机号输入有误，请输入11位手机号'
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'重置密码失败'
        
    # 重置密码时验证码异常
    def test_0026_mine_resetpassword_verification_err(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'登录时用户名错误'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)
            sleep(0.5)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mylogin_logout')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已登录，先退出再登录'
            el.click()
            # 提示“你确认要退出登录吗？”，点击确定
            methodpackage.wait_xPathMsg_click_idButton(
                self.driver,
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout",
                "com.sumavision.sanping.gudou:id/btnOK",
                5,
                u'你确认要退出登录吗？',
                True)
            self.assertEqual(self.find_toast(self.driver, u'退出登录成功'), True)
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'未登录'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
        el.click()
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/text_login_forget')
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击‘忘记密码’，进行密码重置'
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/edit_text')
        lis = [els[i].text for i in range(4)]
        els[0].click()
        els[0].send_keys('13436550661')
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/text_reset_psw_verification_code')
        el.click()
        self.assertTrue(self.find_toast(self.driver, u'发送短信验证码成功！'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'输入手机号，获取验证码'

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/edit_text')
        els[1].send_keys('111111')
        els[2].send_keys('123456')
        els[3].send_keys('123456')
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_my_reset_psw')
        el.click()

        self.assertTrue(self.find_toast(self.driver, u'重置密码失败'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'重置密码失败'
        
    # 重置密码时新密码异常
    def test_0027_mine_resetpassword_password_err(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'登录时用户名错误'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)
            sleep(0.5)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mylogin_logout')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已登录，先退出再登录'
            el.click()
            # 提示“你确认要退出登录吗？”，点击确定
            methodpackage.wait_xPathMsg_click_idButton(
                self.driver,
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout",
                "com.sumavision.sanping.gudou:id/btnOK",
                5,
                u'你确认要退出登录吗？',
                True)
            self.assertEqual(self.find_toast(self.driver, u'退出登录成功'), True)
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'未登录'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
        el.click()
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/text_login_forget')
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击‘忘记密码’，进行密码重置'
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/edit_text')
        lis = [els[i].text for i in range(4)]
        els[0].click()
        els[0].send_keys('13436550661')
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/text_reset_psw_verification_code')
        el.click()
        self.assertTrue(self.find_toast(self.driver, u'发送短信验证码成功！'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'输入手机号，获取验证码'

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/edit_text')
        els[1].send_keys('111111')
        els[2].send_keys('1')
        els[3].send_keys('123456')
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_my_reset_psw')
        el.click()

        self.assertTrue(self.find_toast(self.driver, u'密码输入有误'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'密码输入有误，请输入长度为6-32位密码'

    # 重置密码时密码不一致
    def test_0028_mine_resetpassword_password_dif(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'登录时用户名错误'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)
            sleep(0.5)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mylogin_logout')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已登录，先退出再登录'
            el.click()
            # 提示“你确认要退出登录吗？”，点击确定
            methodpackage.wait_xPathMsg_click_idButton(
                self.driver,
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout",
                "com.sumavision.sanping.gudou:id/btnOK",
                5,
                u'你确认要退出登录吗？',
                True)
            self.assertEqual(self.find_toast(self.driver, u'退出登录成功'), True)
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'未登录'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
        el.click()
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/text_login_forget')
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击‘忘记密码’，进行密码重置'
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/edit_text')
        lis = [els[i].text for i in range(4)]
        els[0].click()
        els[0].send_keys('13436550661')
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/text_reset_psw_verification_code')
        el.click()
        self.assertTrue(self.find_toast(self.driver, u'发送短信验证码成功！'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'输入手机号，获取验证码'

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/edit_text')
        els[1].send_keys('111111')
        els[2].send_keys('1')
        els[3].send_keys('123456')
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_my_reset_psw')
        el.click()

        self.assertTrue(self.find_toast(self.driver, u'两次密码不相同'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'两次密码不相同'

    # 查看个人圈子页面信息
    def test_0029_mine_info(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   查看个人圈子页面信息：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)
            sleep(0.5)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mylogin_logout')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已登录，不用再登录'
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'未登录'
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
            el.click()

            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/edit_user_name")
            el.clear()
            el.send_keys("18500986394")

            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/text")
            el.send_keys("123456")
            sleep(1)

            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mylogin_login")
            el.click()

            # self.assertEqual(True, self.find_toast(self.driver, u'登录成功'))
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tv_mine_username')
            # self.assertEqual(el.text, u'测试结果')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'登录成功'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
        el.click()

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/ev_circle_userName')
        username = el.text
        # self.assertEqual(username, u'测试结果')
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'用户名：', username

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tv_username')
        phone = el.text
        self.assertEqual(phone, '18500986394')
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'手机账号：', phone

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/add_friend')
        addfriend = el.text
        self.assertEqual(addfriend, u'添加好友')

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_vod_tab_text')
        self.assertEqual(els[0].get_attribute('selected'), 'true')
        self.assertEqual(els[0].text, u'动态')
        self.assertEqual(els[1].get_attribute('selected'), 'false')
        self.assertEqual(els[1].text, u'关注')
        self.assertEqual(els[2].get_attribute('selected'), 'false')
        self.assertEqual(els[2].text, u'粉丝')

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/edit_nick_name')
        self.assertIsNotNone(el)

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/iv_mine_circle_back')
        el.click()
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        self.assertEqual(el.get_attribute('selected'), 'true')
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'退出我的圈子，回到我的'

    # 修改昵称
    def test_0030_mine_modify_nickname(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   修改昵称：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        self.relogin(self.driver)

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
        el.click()

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/ev_circle_userName')
        username = el.text
        # self.assertEqual(username, u'测试结果')
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'原昵称：', username

        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/edit_nick_name')
        el1.click()

        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/ev_circle_userName')
        el2.click()
        el2.clear()
        newname = 'test' + str(random.randint(0, 100))
        el2.send_keys(newname)
        el1.click()
        self.assertEqual(self.find_toast(self.driver, u'更改昵称成功！'), True)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'新昵称：', newname

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/iv_mine_circle_back')
        el.click()

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tv_mine_username')
        self.assertEqual(el.text, newname)

    # 修改头像
    def test_0031_mine_modify_picture(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   修改头像：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        self.relogin(self.driver)

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tv_mine_username")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入我的圈子'
        sleep(1)

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/iv_mine_user_logo')
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击头像'
        sleep(3)

        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/textView2')
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/textView3')
        el3 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/textView4')
        self.assertEqual(el1.text, u'拍照')
        self.assertEqual(el2.text, u'从相册中选择')
        self.assertEqual(el3.text, u'取消')
        el1.click()
        sleep(2)
        self.driver.back()
        #self.driver.press_keycode(4)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击拍照并返回'
        el3.click()
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/iv_mine_user_logo')
        el.click()
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/textView3')
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击取消并再次更换头像'

        els = self.driver.find_elements_by_id('com.android.documentsui:id/linnerlayout')
        # action = TouchAction(self.driver)
        # action.tap(els[-2]).perform()
        els[-2].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'选择图库栏'
        els = self.driver.find_elements_by_id('com.android.gallery3d:id/list_item_content')
        els[2].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'选择杂志图片'
        x_axis = random.randint(0, 1080)
        y_axis = random.randint(215, 1780)
        # print x_axis, y_axis
        sleep(1)
        action = TouchAction(self.driver)
        action.tap(x=x_axis, y=y_axis).perform()
        el = self.driver.find_element_by_id('com.android.gallery3d:id/head_select_right')
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'随机选择一张图片'
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/menu_crop')
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'确定裁剪'

        self.assertEqual(self.find_toast(self.driver, u'头像修改成功！'), True)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'头像修改成功！：'

    # 修改昵称异常
    def test_0032_mine_modify_nickname_err(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   修改昵称异常：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        self.relogin(self.driver)

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入我的圈子'

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/ev_circle_userName')
        username = el.text
        # self.assertEqual(username, u'测试结果')
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'原昵称：', username

        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/edit_nick_name')
        el1.click()
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/ev_circle_userName')
        el2.click()

        el2.clear()
        el1.click()
        self.assertEqual(self.find_toast(self.driver, u'信息内容填写不完整'), True)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'修改昵称为空'
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'信息内容填写不完整'

        newname1 = self.randstr(1, alphasnums)
        el2.send_keys(newname1)
        el1.click()
        self.assertEqual(self.find_toast(self.driver, u'昵称输入有误，请输入2-20位字符'), True)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'修改昵称为：', newname1
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'提示：昵称输入有误，请输入2-20位字符'
        newname2 = self.randstr(21, alphasnums)
        el2.clear()
        el2.send_keys(newname2)
        el1.click()
        self.assertEqual(self.find_toast(self.driver, u'更改昵称成功！'), True)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'修改昵称为：', newname2
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'更改昵称成功'
        name = el2.text
        self.assertEqual(name, newname2[:-1])
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'实际昵称为：', name

        self.driver.back()
        self.driver.back()

    # 添加好友
    def test_0033_mine_addfriend(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   添加好友：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)
            sleep(0.5)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mylogin_logout')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已登录，不用再登录'
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'未登录'
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
            el.click()

            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/edit_user_name")
            el.clear()
            el.send_keys("13436550661")

            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/text")
            el.send_keys("123456")
            sleep(1)

            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mylogin_login")
            el.click()

            # self.assertEqual(True, self.find_toast(self.driver, u'登录成功'))
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tv_mine_username')
            # self.assertEqual(el.text, u'测试结果')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'登录成功'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
        el.click()

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/add_friend')
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入手机好友'
        sleep(5)
        tempfile = os.path.join(methodpackage.currentDir, 'temp.png')
        # els = self.driver.find_elements_by_class_name('android.widget.TextView')
        # for i in range(len(els)):
        #     print els[i].text
        els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/itemTv')
        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/itemUname')
        els3 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/btn_invite')
        for i in range(len(els2)):
            itemUname = els2[i].text
            if itemUname == u'尚未注册谷豆TV':
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), els1[i].text, u'尚未注册谷豆TV'
                self.assertEqual(els3[i].text, u'邀请')
                methodpackage.get_screenshot_by_element(self.driver, els3[i], tempfile)
                self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(tempfile)), (123, 199, 41))
                break

        for j in range(len(els3)):
            invite = els3[j].text
            if invite == u'关注':
                methodpackage.get_screenshot_by_element(self.driver, els3[j], tempfile)
                self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(tempfile)), selectedColor)
                itemTv = els1[j].text
                itemUname = els2[j].text
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'尚未关注：', itemTv
                self.assertEqual(itemUname.split(":")[0], u'U互动')
                els3[j].click()
                self.assertEqual(True, self.find_toast(self.driver, u'关注成功'))
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击关注：', itemTv
                els3 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/btn_invite')
                invite2 = els3[j].text
                self.assertEqual(invite2, u'已关注')
                methodpackage.get_screenshot_by_element(self.driver, els3[j], tempfile)
                self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(tempfile)), (197, 197, 197))

                sleep(2)
                els3[j].click()
                self.assertEqual(True, self.find_toast(self.driver, u'已取消关注'))
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击取消关注：', itemTv
                els3 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/btn_invite')
                invite3 = els3[j].text
                self.assertEqual(invite3, u'关注')
                methodpackage.get_screenshot_by_element(self.driver, els3[j], tempfile)
                self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(tempfile)), selectedColor)
                break

    # 动态显示功能
    def test_0034_mine_news(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   动态显示功能：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)
            sleep(0.5)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mylogin_logout')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已登录，不用再登录'
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'未登录'
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
            el.click()

            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/edit_user_name")
            el.clear()
            el.send_keys("13436550661")

            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/text")
            el.send_keys("123456")
            sleep(1)

            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mylogin_login")
            el.click()

            # self.assertEqual(True, self.find_toast(self.driver, u'登录成功'))
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tv_mine_username')
            # self.assertEqual(el.text, u'测试结果')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'登录成功'
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
        el.click()

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_vod_tab_text')
        self.assertEqual(els[0].get_attribute('selected'), 'true')
        self.assertEqual(els[0].text, u'动态')
        self.assertEqual(els[1].get_attribute('selected'), 'false')
        self.assertEqual(els[1].text, u'关注')
        self.assertEqual(els[2].get_attribute('selected'), 'false')
        self.assertEqual(els[2].text, u'粉丝')

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/ll_title')
        self.assertGreater(len(els), 1)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已有不止一条动态'

    # 关注列表功能
    def test_0035_mine_friend(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   关注列表功能：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)
            sleep(0.5)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mylogin_logout')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已登录，不用再登录'
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'未登录'
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
            el.click()

            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/edit_user_name")
            el.clear()
            el.send_keys("13436550661")

            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/text")
            el.send_keys("123456")
            sleep(1)

            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mylogin_login")
            el.click()

            # self.assertEqual(True, self.find_toast(self.driver, u'登录成功'))
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tv_mine_username')
            # self.assertEqual(el.text, u'测试结果')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'登录成功'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
        el.click()
        sleep(2)

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_vod_tab_text')
        els[1].click()
        sleep(1)

        self.assertEqual(els[0].get_attribute('selected'), 'false')
        self.assertEqual(els[0].text, u'动态')
        self.assertEqual(els[1].get_attribute('selected'), 'true')
        self.assertEqual(els[1].text, u'关注')
        self.assertEqual(els[2].get_attribute('selected'), 'false')
        self.assertEqual(els[2].text, u'粉丝')

        els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/itemUName')
        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/btn_concern_or_not')
        if len(els1) > 0:
            for i in range(len(els2)):
                self.assertEqual(els2[i].text, u'已关注')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已有好友'
        else:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'还没有好友'

    # 粉丝列表功能
    def test_0036_mine_fans(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   粉丝列表功能：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)
            sleep(0.5)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mylogin_logout')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已登录，不用再登录'
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'未登录'
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
            el.click()

            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/edit_user_name")
            el.clear()
            el.send_keys("13436550661")

            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/text")
            el.send_keys("123456")
            sleep(1)

            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mylogin_login")
            el.click()

            # self.assertEqual(True, self.find_toast(self.driver, u'登录成功'))
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tv_mine_username')
            # self.assertEqual(el.text, u'测试结果')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'登录成功'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
        el.click()
        sleep(1)

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_vod_tab_text')
        els[2].click()
        sleep(1)

        self.assertEqual(els[0].get_attribute('selected'), 'false')
        self.assertEqual(els[0].text, u'动态')
        self.assertEqual(els[1].get_attribute('selected'), 'false')
        self.assertEqual(els[1].text, u'关注')
        self.assertEqual(els[2].get_attribute('selected'), 'true')
        self.assertEqual(els[2].text, u'粉丝')

        els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/itemUName')
        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/btn_concern_or_not')
        if len(els2) > 0:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已有粉丝'
        else:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'还没有粉丝'

    # 好友圈功能
    def test_0037_mine_circle(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   好友圈功能：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for i in range(2):
            methodpackage.swipeUp(self.driver, 500)
            sleep(0.5)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mylogin_logout')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已登录，不用再登录'
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'未登录'
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_mine_user_logo")
            el.click()

            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/edit_user_name")
            el.clear()
            el.send_keys("18500986394")

            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/text")
            el.send_keys("123456")
            sleep(1)

            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mylogin_login")
            el.click()

            # self.assertEqual(True, self.find_toast(self.driver, u'登录成功'))
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tv_mine_username')
            # self.assertEqual(el.text, u'测试结果')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'登录成功'
        methodpackage.swipeDown(self.driver, 500)
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_friends_circle")
        el.click()
        sleep(2)

        els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/item_nickName')
        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/item_time')
        els3 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/item_tv_type')
        els4 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/item_program_name')
        if len(els1) > 0:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已有好友动态'
            if els3[0].text == u'赞了视频':
                el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/item_nickName')
                el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/item_time')
                el3 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/item_tv_type')
                el4 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/item_program_name')
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'其中最新的一条为：',\
                    el1.text, u'在', el2.text, u'赞了视频', el4.text
            else:
                el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/item_nickName')
                el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/item_time')
                el3 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/item_tv_type')
                el4 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/item_program_name')
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'其中最新的一条为：', \
                    el1.text, u'在', el2.text, u'对视频', el4.text, u'进行了评论'
        else:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'还没有好友动态'

    # 观看历史页面
    def test_0038_mine_history(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   观看历史页面：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'

        # 进入“观看历史”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_his")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入观看历史'

        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_myhistory_edit')
        self.assertIsNotNone(el1)
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_myhistory_deleteall')
        self.assertIsNotNone(el2)
        el3 = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_myhis_back")
        self.assertIsNotNone(el3)

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_name')
        if len(els) > 0:
            name = els[0].text
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'最近观看了：', name
        else:
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_his_empty")
            self.assertIsNotNone(el)
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有观看历史'
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_myhis_back")
        el.click()
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        self.assertEqual(el.get_attribute('selected'), 'true')

    # 观看历史续播
    def test_0039_mine_history_continue(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   观看历史续播：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.——sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'

        # 进入“观看历史”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_his")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入观看历史'

        try:
            el = self.driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
                '/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout'
                '/android.widget.LinearLayout/android.widget.ScrollView/android.widget.ListView'
                '/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.GridView'
                '/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView')
        except:
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_his_empty")
            self.assertIsNotNone(el)
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有观看历史'
            return

        els = self.driver.find_elements_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout'
            '/android.widget.LinearLayout/android.widget.ScrollView/android.widget.ListView'
            '/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.GridView'
            '/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView')
        name = els[0].text
        date = els[1].text.split(' ')[1]
        historyTime = int(date.split(':')[0]) * 3600 + int(date.split(':')[1]) * 60 + int(
            date.split(':')[2])
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'最近观看了\"%s\"到:%s' % (name, historyTime)
        els[0].click()
        # 等待播放加载完成
        try:
            WebDriverWait(
                self.driver, 8).until_not(lambda x: x.find_element_by_id(
                "com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/tv_progress_small",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View")
        date2 = el.text.split('/')[0]
        currentTime = int(date2.split(':')[0]) * 3600 + int(date2.split(':')[1]) * 60 + int(
            date2.split(':')[2])
        self.assertLess(abs(historyTime - currentTime), 10)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'续播正常'

    # 观看历史删除
    def test_0040_mine_history_delete(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   观看历史删除：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'

        # 进入“观看历史”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_his")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入观看历史'

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tv_name')
        except:
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_his_empty")
            self.assertIsNotNone(el)
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有观看历史'
            return

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_name')
        name = els[0].text
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'最近观看了：', name
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_myhistory_edit')
        el.click()
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_poster")
        el.click()
        el3 = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_myhistory_edit")
        el3.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'删除\"%s\"的观看历史' % name
        try:
            els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_name')
            self.assertNotEqual(name, els[0].text)
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'删除成功'
        except:
            # el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_his_empty")
            # self.assertIsNotNone(el)
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有观看历史，删除成功'
            return

    # 观看历史清空
    def test_0041_mine_history_empty(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   观看历史清空：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'

        # 进入“观看历史”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_his")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入观看历史'

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_name')
        if len(els) > 0:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'最近观看了至少%s部影片' % len(els)
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_myhistory_deleteall')
            el.click()

            # 如果提示是否清空记录，选择确定
            methodpackage.wait_xPathMsg_click_idButton(
                self.driver,
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.TextView[1]",
                "com.sumavision.sanping.gudou:id/btnOK",
                2,
                u'清空历史记录',
                True)
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'确定清空历史记录'
            els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_name')
            if len(els) > 0:
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'清空历史记录有问题'
                self.assertTrue(False)
            else:
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'清空历史记录成功'
        else:
            # el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_his_empty")
            # self.assertIsNotNone(el)
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有观看历史'

    # 我的缓存页面
    def test_0042_mine_cache(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   我的缓存页面：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        self.relogin(self.driver)

        methodpackage.swipeDown(self.driver, 500)
        # 进入“我的缓存”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_cache")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入我的缓存'
        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/clean_all')
        self.assertIsNotNone(el1)
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/edit')
        self.assertIsNotNone(el2)
        el3 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remain_textView1')
        el4 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remain_textView2')
        el5 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remain_textView3')
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), el3.text, el4.text, el5.text
        try:
            el6 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/downloading_textShow')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'有未缓存完成的'
            el7 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tv_first_cache_status')
            status = el7.text
            if status == u'正在缓存':
                el6.click()
                el9 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/suspend_all')
                self.assertIsNotNone(el9)
                els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_status')
                els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/medialib_movie_name')
                for j in range(len(els1)):
                    if els1[j].text != u'暂停':
                        patt = '(\d+)K/s'
                        m = re.match(patt, els1[j].text)
                        self.assertIsNotNone(m)
                        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'正在缓存', els2[j].text, \
                            u'当前速度:', els1[j].text
                el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/iv_my_cache_back')
                el.click()
            elif status == u'暂无正在下载的任务':
                el6.click()
                el9 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/suspend_all')
                self.assertIsNotNone(el9)
                els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_status')
                for j in range(len(els1)):
                    self.assertEqual(els1[j].text, u'暂停')
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'有%s部视频正在缓存' % len(els1)
                el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/iv_my_cache_back')
                el.click()
            else:
                pass
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有未缓存完成的'

        try:
            els3 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/medialib_movie_name')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已经缓存了%s部视频' % len(els3)
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有已经缓存完成的'

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/iv_my_cache_back')
        el.click()
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_cache")
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'返回到我的'

    # 删除正在进行的缓存
    def test_0043_mine_caching_del(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   删除正在进行的缓存：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        self.relogin(self.driver)
        methodpackage.swipeDown(self.driver, 500)

        # 进入“我的缓存”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_cache")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入我的缓存'

        try:
            el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/downloading_textShow')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'有未缓存完成的'
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有未缓存完成的'
            return
        el1.click()
        sleep(1)
        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/clean_all')
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/edit')
        el3 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/suspend_all')
        els3 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_status')
        els4 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/medialib_movie_name')
        nums = len(els3)
        name = els4[0].text
        el2.click()
        els5 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/img_delete_checkbox')
        els5[0].click()
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/edit')
        el2.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'删除缓存的视频：', name
        sleep(1)
        try:
            els4 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/medialib_movie_name')
        except:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有缓存了，删除成功'
            return
        self.assertNotEqual(name, els4[0].text)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'删除成功'

    # 清空正在进行的缓存
    def test_0044_mine_caching_emp(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   清空正在进行的缓存：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        self.relogin(self.driver)
        methodpackage.swipeDown(self.driver, 500)

        # 进入“我的缓存”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_cache")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入我的缓存'
        try:
            el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/downloading_textShow')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'有未缓存完成的'
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有未缓存完成的'
            return
        el1.click()
        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/clean_all')
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/edit')
        el3 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/suspend_all')
        els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_status')
        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/medialib_movie_name')
        el1.click()

        # 如果提示是否清空记录，选择确定
        methodpackage.wait_xPathMsg_click_idButton(
            self.driver,
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.TextView[1]",
            "com.sumavision.sanping.gudou:id/btnOK",
            2,
            u'清空正在缓存',
            True)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'确定清空正在缓存'
        sleep(1)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/medialib_movie_name')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'还有未缓存完成的，清空失败'
            self.assertTrue(False)
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有未缓存完成的，清空成功'

    # 删除已完成的缓存
    def test_0045_mine_cached_del(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   删除已完成的缓存：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        self.relogin(self.driver)
        methodpackage.swipeDown(self.driver, 500)

        # 进入“我的缓存”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_cache")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入我的缓存'

        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/clean_all')
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/edit')
        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/medialib_movie_name')
        except:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有已完成的缓存，退出'
            return
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/medialib_movie_name')
        name = els[0].text
        el2.click()
        els5 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/img_delete_checkbox')
        els5[0].click()
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/edit')
        el2.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'删除缓存的视频：', name
        sleep(1)
        try:
            els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/medialib_movie_name')
        except:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有缓存了，删除成功'
            return
        self.assertNotEqual(name, els[0].text)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'删除成功'

    # 清空已完成的缓存
    def test_0046_mine_cached_emp(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   清空已完成的缓存：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        self.relogin(self.driver)
        methodpackage.swipeDown(self.driver, 500)

        # 进入“我的缓存”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_cache")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入我的缓存'
        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/clean_all')
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/edit')
        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/medialib_movie_name')
        except:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有已完成的缓存，退出'
            return
        el1.click()

        # 如果提示是否清空记录，选择确定
        methodpackage.wait_xPathMsg_click_idButton(
            self.driver,
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.TextView[1]",
            "com.sumavision.sanping.gudou:id/btnOK",
            2,
            u'清空正在缓存',
            True)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'清空正在缓存'
        sleep(1)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/medialib_movie_name')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'还有已完成的缓存，清空失败'
            self.assertTrue(False)
        except:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有已完成的缓存，清空成功'

    # 全部暂停正在进行的缓存
    def test_0047_mine_caching_suspend_all(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   全部暂停正在进行的缓存：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        self.relogin(self.driver)
        methodpackage.swipeDown(self.driver, 500)

        # 进入“我的缓存”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_cache")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入我的缓存'
        try:
            el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/downloading_textShow')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'有未缓存完成的'
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有未缓存完成的'
            return
        el1.click()
        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/clean_all')
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/edit')
        el3 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/suspend_all')
        els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_status')
        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/medialib_movie_name')
        el3.click()

        # 如果提示是否清空记录，选择确定
        methodpackage.wait_xPathMsg_click_idButton(
            self.driver,
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.TextView[1]",
            "com.sumavision.sanping.gudou:id/btnOK",
            2,
            u'全部暂停',
            True)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'确定全部暂停'
        sleep(1)

        els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_status')
        for j in range(len(els1)):
            self.assertEqual(els1[j].text, u'暂停')
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'全部暂停成功'

    # 剩余空间
    def test_0048_mine_cached_remain(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   剩余空间：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        self.relogin(self.driver)
        methodpackage.swipeDown(self.driver, 500)

        # 进入“我的缓存”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_cache")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入我的缓存'

        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/clean_all')
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/edit')
        el3 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remain_textView1')
        el4 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remain_textView2')
        el5 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remain_textView3')
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), el3.text, el4.text, el5.text
        presize = float(el4.text.split(" ")[0])
        unit = el4.text.split(" ")[1]
        if unit == 'GB':
            presize = presize * 1024
        print presize
        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/medialib_movie_name')
        except:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有已完成的缓存，退出'
            return
        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/medialib_movie_cachedSize')
        patt = '(.+)(K|M|G)'
        print els2[0].text
        movsize = float(re.match(patt, els2[0].text).group(1))
        movunit = re.match(patt, els2[0].text).group(2)
        print movsize, movunit
        name = els[0].text
        el2.click()
        els5 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/img_delete_checkbox')
        els5[0].click()
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/edit')
        el2.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'删除缓存的视频：', name
        sleep(1)
        try:
            els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/medialib_movie_name')
        except:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有缓存了，删除成功'
            return
        self.assertNotEqual(name, els[0].text)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'删除成功'

        el3 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remain_textView1')
        el4 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remain_textView2')
        el5 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remain_textView3')
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), el3.text, el4.text, el5.text
        postsize = float(el4.text.split(" ")[0])
        unit = el4.text.split(" ")[1]
        if unit == 'GB':
            postsize = postsize * 1024
        print postsize

        self.assertTrue(presize + movsize == postsize)

    # 查看直播收藏页面
    def test_0049_mine_liveshare(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'观看收藏页面'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'
        el.click()
        # 播放一个节目
        try:
            els = self.driver.find_elements_by_id("com.sumavision.sanping.gudou:id/tvName")
            i = random.randint(0, len(els))
            name = els[i].text
        except Exception:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道'
            return
        els[i].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(
                self.driver, 5).until_not(lambda x: x.find_element_by_id(
                "com.sumavision.sanping.sichuan415:id/progressBar1"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 收藏
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_fav")
        el.click()
        self.driver.back()

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'

        # 进入“我的收藏”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_fav")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入我的收藏'

        el1 = self.driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout'
            '/android.widget.LinearLayout[1]/android.widget.TextView')
        el2 = self.driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout'
            '/android.widget.LinearLayout[2]/android.widget.TextView')
        self.assertIsNotNone(el1)
        self.assertEqual(u'直播', el1.text)
        self.assertIsNotNone(el2)
        self.assertEqual(u'片库', el2.text)
        self.assertEqual('true', el1.get_attribute('selected'))

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tvName')
        if len(els) > 0:
            el3 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mycollection_deleteall')
            self.assertEqual(u'清空', el3.text)
            el4 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mycollection_edit')
            self.assertEqual(u'删除', el4.text)
            name = els[0].text
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'最近收藏了频道：', name
        else:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有收藏频道'
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'
            el.click()
            # 进入“收藏”分类验证收藏功能
            els = self.driver.find_elements_by_id("com.sumavision.sanping.gudou:id/tv_vod_tab_text")
            els[0].click()
            try:
                WebDriverWait(self.driver, 3).until(lambda x: x.find_element_by_id(
                    'com.sumavision.sanping.gudou:id/tvName'))
                el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tvName')
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"我的收藏频道显示有问题"
                self.assertFalse(True)
            except NoSuchElementException:
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'确实没有收藏频道'

    # 播放直播收藏频道
    def test_0050_mine_liveshare_play(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放直播收藏频道'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'

        # 进入“我的收藏”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_fav")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入我的收藏'

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tvName')
        if len(els) > 0:
            for i in range(len(els)):
                els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tvName')
                name = els[i].text
                els[i].click()
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放收藏频道：', name
                sleep(8)
                self.driver.back()
                continue
        else:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有收藏频道'
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'
            el.click()
            # 进入“收藏”分类验证收藏功能
            els = self.driver.find_elements_by_id("com.sumavision.sanping.gudou:id/tv_vod_tab_text")
            els[0].click()
            try:
                WebDriverWait(self.driver, 3).until(lambda x: x.find_element_by_id(
                    'com.sumavision.sanping.gudou:id/tvName'))
                el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tvName')
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"我的收藏频道显示有问题"
                self.assertFalse(True)
            except NoSuchElementException:
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'确实没有收藏频道'

    # 删除直播收藏频道
    def test_0051_mine_liveshare_delete(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'删除直播收藏频道'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'

        # 进入“我的收藏”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_fav")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入我的收藏'

        el1 = self.driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout'
            '/android.widget.LinearLayout[1]/android.widget.TextView')
        el2 = self.driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout'
            '/android.widget.LinearLayout[2]/android.widget.TextView')
        self.assertIsNotNone(el1)
        self.assertEqual(u'直播', el1.text)
        self.assertIsNotNone(el2)
        self.assertEqual(u'片库', el2.text)
        self.assertEqual('true', el1.get_attribute('selected'))

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tvName')
        if len(els) > 0:
            name = els[0].text
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mycollection_edit')
            el.click()
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/btnEpg")
            el.click()
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'删除收藏频道：', name
        else:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有收藏频道'
            self.driver.back()
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'
            el.click()
            # 进入“收藏”分类验证收藏功能
            els = self.driver.find_elements_by_id("com.sumavision.sanping.gudou:id/tv_vod_tab_text")
            els[0].click()
            try:
                el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tvName')
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"我的收藏频道显示有问题"
                self.assertFalse(True)
            except NoSuchElementException:
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'确实没有收藏频道'

    # 清空直播收藏频道
    def test_0052_mine_liveshare_empty(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'清空直播收藏频道'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'

        # 进入“我的收藏”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_fav")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入我的收藏'

        el1 = self.driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout'
            '/android.widget.LinearLayout[1]/android.widget.TextView')
        el2 = self.driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout'
            '/android.widget.LinearLayout[2]/android.widget.TextView')
        self.assertIsNotNone(el1)
        self.assertEqual(u'直播', el1.text)
        self.assertIsNotNone(el2)
        self.assertEqual(u'片库', el2.text)
        self.assertEqual('true', el1.get_attribute('selected'))

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tvName')
        if len(els) > 0:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mycollection_deleteall')
            el.click()

            # 如果提示是否清空记录，选择确定
            methodpackage.wait_xPathMsg_click_idButton(
                self.driver,
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.TextView[1]",
                "com.sumavision.sanping.gudou:id/btnOK",
                2,
                u'清空直播收藏',
                True)
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'确定清空直播收藏'
            els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tvName')
            if len(els) > 0:
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'清空直播收藏异常'
                self.assertTrue(False)
            else:
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'清空收藏频道成功'
        else:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有收藏频道'
            self.driver.back()
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'
            el.click()
            # 进入“收藏”分类验证收藏功能
            els = self.driver.find_elements_by_id("com.sumavision.sanping.gudou:id/tv_vod_tab_text")
            els[0].click()
            try:
                el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tvName')
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"我的收藏频道显示有问题"
                self.assertFalse(True)
            except NoSuchElementException:
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'确实没有收藏频道'

    # 查看点播收藏页面
    def test_0053_mine_vodshare(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'查看点播收藏页面'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“点播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()

        methodpackage.swipeDown(self.driver, 500)
        sleep(3)

        # 播放一个节目
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/textView1')
        i = random.randint(0, len(els))
        name = els[i].text
        els[i].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(
                self.driver, 5).until_not(lambda x: x.find_element_by_id(
                "com.sumavision.sanping.sichuan415:id/progressBar1"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 收藏
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_fav")
        el.click()
        self.driver.back()

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'

        # 进入“我的收藏”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_fav")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入我的收藏'

        el1 = self.driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout'
            '/android.widget.LinearLayout[1]/android.widget.TextView')
        el2 = self.driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout'
            '/android.widget.LinearLayout[2]/android.widget.TextView')
        self.assertIsNotNone(el1)
        self.assertEqual(u'直播', el1.text)
        self.assertIsNotNone(el2)
        self.assertEqual(u'片库', el2.text)
        self.assertEqual('true', el1.get_attribute('selected'))

        el2.click()
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_name')
        if len(els) > 0:
            el3 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mycollection_deleteall')
            self.assertEqual(u'清空', el3.text)
            el4 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mycollection_edit')
            self.assertEqual(u'删除', el4.text)
            name = els[0].text
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'最近收藏了节目：', name
        else:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有收藏节目'

    # 播放点播收藏节目
    def test_0054_mine_vodshare_play(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放点播收藏节目'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“点播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()

        methodpackage.swipeDown(self.driver, 500)
        sleep(3)

        # 播放一个节目
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/textView1')
        i = random.randint(0, len(els))
        name = els[i].text
        els[i].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(
                self.driver, 5).until_not(lambda x: x.find_element_by_id(
                "com.sumavision.sanping.sichuan415:id/progressBar1"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 收藏
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_fav")
        el.click()
        self.driver.back()

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'

        # 进入“我的收藏”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_fav")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入我的收藏'

        el = self.driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout'
            '/android.widget.LinearLayout[2]/android.widget.TextView')
        el.click()
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_name')
        if len(els) > 0:
            for i in range(len(els)):
                els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_name')
                name = els[i].text
                els[i].click()
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放收藏节目：', name
                sleep(8)
                self.driver.back()
                continue
        else:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有收藏节目'

    # 删除点播收藏节目
    def test_0055_mine_vodshare_delete(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'删除点播收藏节目'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“点播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()

        methodpackage.swipeDown(self.driver, 500)
        sleep(2)

        # 播放一个节目
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/textView1')
        i = random.randint(0, len(els))
        name = els[i].text
        els[i].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(
                self.driver, 5).until_not(lambda x: x.find_element_by_id(
                "com.sumavision.sanping.sichuan415:id/progressBar1"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 收藏
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_fav")
        el.click()
        self.driver.back()

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'

        # 进入“我的收藏”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_fav")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入我的收藏'

        el1 = self.driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout'
            '/android.widget.LinearLayout[1]/android.widget.TextView')
        el2 = self.driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout'
            '/android.widget.LinearLayout[2]/android.widget.TextView')
        self.assertIsNotNone(el1)
        self.assertEqual(u'直播', el1.text)
        self.assertIsNotNone(el2)
        self.assertEqual(u'片库', el2.text)
        self.assertEqual('true', el1.get_attribute('selected'))

        el2.click()
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_name')
        if len(els) > 0:
            name = els[0].text
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mycollection_edit')
            el.click()
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/rl_mycollection_deletemark')
            el.click()
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mycollection_edit')
            el.click()
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'删除收藏节目：', name
        else:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有收藏节目'

    # 清空点播收藏节目
    def test_0056_mine_vodshare_empty(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'清空点播收藏节目'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“点播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()

        methodpackage.swipeDown(self.driver, 500)
        sleep(2)

        # 播放一个节目
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/textView1')
        i = random.randint(0, len(els))
        name = els[i].text
        els[i].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(
                self.driver, 5).until_not(lambda x: x.find_element_by_id(
                "com.sumavision.sanping.sichuan415:id/progressBar1"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 收藏
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_fav")
        el.click()
        self.driver.back()

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'

        # 进入“我的收藏”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_fav")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入我的收藏'

        el1 = self.driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout'
            '/android.widget.LinearLayout[1]/android.widget.TextView')
        el2 = self.driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout'
            '/android.widget.LinearLayout[2]/android.widget.TextView')
        self.assertIsNotNone(el1)
        self.assertEqual(u'直播', el1.text)
        self.assertIsNotNone(el2)
        self.assertEqual(u'片库', el2.text)
        self.assertEqual('true', el1.get_attribute('selected'))
        el2.click()

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_name')
        if len(els) > 0:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_mycollection_deleteall')
            el.click()

            # 如果提示是否清空记录，选择确定
            methodpackage.wait_xPathMsg_click_idButton(
                self.driver,
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.TextView[1]",
                "com.sumavision.sanping.gudou:id/btnOK",
                2,
                u'清空点播收藏',
                True)
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'确定清空点播收藏'
            els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_name')
            if len(els) > 0:
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'清空点播收藏异常'
                self.assertTrue(False)
            else:
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'清空收藏节目成功'
        else:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有收藏节目'

    # 查看我的预定页面
    def test_0057_mine_remind(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'查看我的预定页面'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'
        el.click()
        # 播放一个节目
        try:
            els = self.driver.find_elements_by_id("com.sumavision.sanping.gudou:id/tvName")
            i = random.randint(0, len(els))
            name = els[i].text
        except Exception:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道'
            return
        els[i].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(
                self.driver, 5).until_not(lambda x: x.find_element_by_id(
                "com.sumavision.sanping.gudou:id/progressBar1"
            )
                                           )
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 预约
        methodpackage.swipeLeft_low(self.driver, 500)
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/live_tvEpg_flag')
        els[random.randint(0, len(els))].click()
        self.driver.back()

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'

        # 进入“我的预约”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_remind")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入我的预订'

        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_myremind_clearall')
        self.assertEqual(u'清空', el1.text)
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_myremind_edit')
        self.assertEqual(u'编辑', el2.text)
        el3 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_myremind_totalnum')
        totalnum = int(el3.text)
        els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_remind_epgname')
        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_remind_channelname')
        els3 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_remind_time')
        els4 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_remind_date')
        remnum = len(els1)
        # print remnum
        if remnum <= 0:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有预订节目'
            return

        if totalnum > remnum:
            c = totalnum//remnum
            for j in range(c+1):
                els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_remind_epgname')
                els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_remind_channelname')
                els3 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_remind_time')
                els4 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_remind_date')
                for i in range(remnum):
                    epgname = els1[i].text
                    chaname = els2[i].text
                    remtime = els3[i].text
                    remdate = els4[i].text
                    datetime = remdate + ' ' + remtime
                    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'在%s预订了%s的节目：%s' \
                                                                                       % (datetime, chaname, epgname)
                    if i != 0:
                        pre_remtime = els3[i-1].text
                        pre_remdate = els4[i-1].text
                        predatetime = pre_remdate + ' ' + pre_remtime
                        self.assertTrue(self.compare_time(datetime, predatetime))
                # methodpackage.swipeUp(self.driver, 500)
                action = TouchAction(self.driver)
                action.long_press(x=540, y=1600).move_to(x=540, y=250)
                action.release()
                action.perform()
                sleep(5)
        else:
            for i in range(remnum):
                epgname = els1[i].text
                chaname = els2[i].text
                remtime = els3[i].text
                remdate = els4[i].text
                datetime = remdate + ' ' + remtime
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'在%s预订了%s的节目：%s' \
                                                                                       % (datetime, chaname, epgname)
                if i != 0:
                    pre_remtime = els3[i - 1].text
                    pre_remdate = els4[i - 1].text
                    predatetime = pre_remdate + ' ' + pre_remtime
                    self.assertTrue(self.compare_time(datetime, predatetime))

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/iv_myremind_back')
        el.click()
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_remind")
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'返回到我的'

    # 删除预订节目
    def test_0058_mine_remind_delete(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'删除预订节目'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'
        el.click()
        # 播放一个节目
        try:
            els = self.driver.find_elements_by_id("com.sumavision.sanping.gudou:id/tvName")
            i = random.randint(0, len(els))
            name = els[i].text
        except Exception:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道'
            return
        els[i].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(
                self.driver, 5).until_not(lambda x: x.find_element_by_id(
                "com.sumavision.sanping.gudou:id/progressBar1"
            )
                                           )
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 预约
        methodpackage.swipeLeft_low(self.driver, 500)
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/live_tvEpg_flag')
        els[3].click()
        self.driver.back()

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'

        # 进入“我的预订”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_remind")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入我的预订'

        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_myremind_clearall')
        self.assertEqual(u'清空', el1.text)
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_myremind_edit')
        self.assertEqual(u'编辑', el2.text)

        els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_remind_epgname')
        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_remind_channelname')
        if len(els1) > 0:
            epgname = els1[0].text
            chaname = els2[0].text
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_myremind_edit')
            el.click()
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/iv_remind_delete')
            el.click()
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_myremind_edit')
            el.click()
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'删除预订频道%s的节目：%s' % (chaname, epgname)
        else:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有预订节目'

    # 清空预订节目
    def test_0059_mine_remind_empty(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'清空预订节目'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'
        el.click()
        # 播放一个节目
        try:
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")
        except Exception:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道'
            return
        els = self.driver.find_elements_by_id("com.sumavision.sanping.gudou:id/tvName")
        i = random.randint(0, len(els))
        name = els[i].text
        els[i].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(
                self.driver, 5).until_not(lambda x: x.find_element_by_id(
                "com.sumavision.sanping.gudou:id/progressBar1"
            )
                                           )
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 预约
        methodpackage.swipeLeft_low(self.driver, 500)
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/live_tvEpg_flag')
        els[3].click()
        self.driver.back()

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'

        # 进入“我的收藏”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_remind")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入我的预订'

        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_myremind_clearall')
        self.assertEqual(u'清空', el1.text)
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_myremind_edit')
        self.assertEqual(u'编辑', el2.text)

        els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_remind_epgname')
        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_remind_channelname')
        if len(els1) > 0:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/frg_myremind_clearall')
            el.click()

            # 如果提示是否清空记录，选择确定
            methodpackage.wait_xPathMsg_click_idButton(
                self.driver,
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.TextView[1]",
                "com.sumavision.sanping.gudou:id/btnOK",
                2,
                u'清空我的预定',
                True)
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'确定清空我的预定'
            els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_remind_epgname')
            if len(els1) > 0:
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'清空我的预定异常'
                self.assertTrue(False)
            else:
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'清空我的预定成功'
        else:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有预定节目'

    # 查看本地图片页面
    def test_0060_mine_location_photo(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'查看本地图片页面'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        methodpackage.swipeUp(self.driver, 500)

        # 进入“本地资源”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_localmedia")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入本地资源'

        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/ivMediaPhoto')
        self.assertEqual(u'图片', el1.text)
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/ivMediaVideo')
        self.assertEqual(u'视频', el2.text)
        el3 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/iv_mymedia_back')
        self.assertIsNotNone(el3)

        els = self.driver.find_elements_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.LinearLayout/android.widget.RelativeLayout[2]/android.widget.GridView'
            '/android.widget.ImageView')
        picnum = len(els)
        if picnum > 0:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'本地至少有%s图片' % picnum
        else:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'本地没有图片'

        el3.click()
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_localmedia")
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'回到我的'

    # 查看本地图片
    def test_0061_mine_location_photoplay(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'查看本地图片'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        methodpackage.swipeUp(self.driver, 500)

        # 进入“本地资源”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_localmedia")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入本地资源'

        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/ivMediaPhoto')
        self.assertEqual(u'图片', el1.text)
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/ivMediaVideo')
        self.assertEqual(u'视频', el2.text)
        el3 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/iv_mymedia_back')
        self.assertIsNotNone(el3)

        els = self.driver.find_elements_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.LinearLayout/android.widget.RelativeLayout[2]/android.widget.GridView'
            '/android.widget.ImageView')
        count = len(els)
        if count > 0:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'本地至少有%s图片' % count
            els[0].click()
            el = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/btnViewPic')
            self.assertIsNotNone(el)
            for i in range(min([5, count])):
                methodpackage.swipeLeft(self.driver, 500)
                sleep(1)
        else:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'本地没有照片'

    # 查看本地视频页面
    def test_0062_mine_location_video(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'查看本地视频页面'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        methodpackage.swipeUp(self.driver, 500)

        # 进入“本地资源”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_localmedia")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入本地资源'

        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/ivMediaPhoto')
        self.assertEqual(u'图片', el1.text)
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/ivMediaVideo')
        self.assertEqual(u'视频', el2.text)
        el3 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/iv_mymedia_back')
        self.assertIsNotNone(el3)

        el2.click()
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/ivVideo')
        count = len(els)
        if count > 0:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'本地至少有%s视频' % count
        else:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'本地没有视频'

    # 播放本地视频
    def test_0063_mine_location_videoplay(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放本地视频'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        methodpackage.swipeUp(self.driver, 500)

        # 进入“本地资源”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_localmedia")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入本地资源'

        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/ivMediaPhoto')
        self.assertEqual(u'图片', el1.text)
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/ivMediaVideo')
        self.assertEqual(u'视频', el2.text)
        el3 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/iv_mymedia_back')
        self.assertIsNotNone(el3)

        el2.click()
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/ivVideo')
        count = len(els)
        if count > 0:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'本地至少有%s视频' % count
            els[0].click()
            sleep(5)
        else:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'本地没有视频'

    # 查看帮助说明页面
    def test_0064_mine_userguide(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'查看帮助说明页面'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        methodpackage.swipeUp(self.driver, 500)

        # 进入“帮助说明”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_userguide")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入帮助说明'

        els = self.driver.find_elements_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.LinearLayout')
        if len(els) > 0:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'有帮助说明'
            for i in range(3):
                methodpackage.swipeLeft(self.driver, 500)
        else:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有帮助说明'

        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/iv_myuserguide_back')
        el2.click()
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_localmedia")
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'回到我的'

    # 反馈功能
    def test_0065_mine_freeback(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'反馈功能'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for j in range(2):
            methodpackage.swipeUp(self.driver, 500)

        # 进入“我要反馈”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_fedback")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入我要反馈'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/edtFedBack")
        el.send_keys(u"测试")
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/checkBox6")
        el.click()
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/ivFedBack")
        el.click()
        self.assertEqual(True, self.find_toast(self.driver, u'反馈成功'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'反馈"测试"成功'

    # 反馈功能异常
    def test_0066_mine_freeback_excep(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'反馈功能异常'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for j in range(2):
            methodpackage.swipeUp(self.driver, 500)

        # 进入“我要反馈”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_fedback")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入我要反馈'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/ivFedBack")
        el.click()
        self.assertEqual(True, self.find_toast(self.driver, u'请选择问题分类'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'提示请选择问题分类'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/checkBox6")
        el.click()
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/ivFedBack")
        el.click()
        self.assertEqual(True, self.find_toast(self.driver, u'请填写详细内容'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'提示请填写详细内容'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/edtFedBack")
        el.send_keys(u"测试")
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/ivFedBack")
        el.click()
        self.assertEqual(True, self.find_toast(self.driver, u'反馈成功'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'提示反馈成功'

    # 关于我们
    def test_0067_mine_aboutus(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'关于我们'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        for j in range(2):
            methodpackage.swipeUp(self.driver, 500)

        # 进入“关于我们”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_aboutus")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入关于我们'

        el1 = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/ivAboutUsLogo")
        self.assertIsNotNone(el1)
        el2 = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvAboutUsMsg")
        self.assertIsNotNone(el2)
        el3 = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_myaboutus_back")
        self.assertIsNotNone(el3)
        el4 = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/my_icon_qr")
        self.assertIsNotNone(el4)
        el5 = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tv_about_us")
        self.assertIsNotNone(el5)
        el6 = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvAboutUsMsg2")
        self.assertIsNotNone(el6)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
