#-*-coding:utf-8-*-

import os
import random
import time
import datetime
import methodpackage
from time import sleep, gmtime, strftime
from appium import webdriver
import sys
import re
import colorsys
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.mobileby import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import unittest

reload(sys)
sys.setdefaultencoding( "utf-8" )

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

selectedColor = (253, 130, 0)
background = (253, 253, 253)
playedColor = (0, 0, 0)


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
            '../../../apps/ApiDemos/bin/com.sumavision.sanping.gudou_4521.apk')

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
        # 选择定位到广州，判断按钮是否存在，存在则直接点，不存在则报异常
        try:
            WebDriverWait(driver, 5).until(lambda x: x.find_element_by_xpath(
                "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout"))
            # 点击确定按钮定位到广州
            el = driver.find_element_by_id("com.sumavision.sanping.gudou:id/btnOk")
            el.click()
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'地位到广州'
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

    # 获取点播小屏时的播放时间
    def getplay_time_vod(self, driver):
        # 获取当前播放进度
        el = methodpackage.find_elementId_conditionXpath(
            driver,
            "com.sumavision.sanping.gudou:id/tv_progress_small",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View"
        )
        currentTime = el.text.split('/')[0]
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'当前播放时间是', currentTime
        totalsecoud_currentTime = int(currentTime.split(':')[0]) * 3600 + int(currentTime.split(':')[1]) * 60 + int(
            currentTime.split(':')[2])
        return totalsecoud_currentTime

    # 获取回看小屏时的播放时间
    def getplay_time_review(self, driver):
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
        temp = el.text.split('/')
        starttime = temp[0]
        temp1 = temp[1].split('(')
        endtime = temp1[0]
        curtime = temp1[1].split(')')[0]

        return [starttime, endtime, curtime]

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

    # 首页观看历史入口
    def test_0002_home_history(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   首页观看历史入口：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“首页”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_home")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'

        # 点击观看历史入口
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/history')
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入观看历史'

        # 检测观看历史页面
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
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/history')
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'返回到首页'

    # 首页我的缓存入口
    def test_0003_home_cache(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   首页我的缓存入口：开始'
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

        # 进入“首页”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_home")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'

        # 点击我的缓存入口
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/download')
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的缓存'

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
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/download")
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'返回到直播首页'

    # 首页遥控器入口
    def test_0004_home_remote_control(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   首页遥控器入口：开始'
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

        # 进入“首页”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_home")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'

        # 点击遥控器入口
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remote_control')
        el.click()
        self.assertEqual(True, self.find_toast(self.driver, u'匹配成功'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入遥控器'

        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteTabButton')
        self.assertIsNotNone(el1)
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteTabChannel')
        self.assertIsNotNone(el2)
        el3 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteTabGesture')
        self.assertIsNotNone(el3)
        el4 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/btnRemoteBack')
        self.assertIsNotNone(el4)
        el5 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteTitle')
        self.assertIsNotNone(el5)
        el6 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteTitleIcon')
        self.assertIsNotNone(el6)
        el7 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/pull')
        self.assertIsNotNone(el7)

        el8 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/btnRemoteMute')
        self.assertIsNotNone(el8)
        el9 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/btnRemoteVolDown')
        self.assertIsNotNone(el9)
        el10 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/btnRemoteVolUp')
        self.assertIsNotNone(el10)

        el11 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteBtnLeft')
        self.assertIsNotNone(el11)
        el12 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteBtnUp')
        self.assertIsNotNone(el12)
        el13 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteBtnOK')
        self.assertIsNotNone(el13)
        el14 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteBtnDown')
        self.assertIsNotNone(el14)
        el15 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteBtnRight')
        self.assertIsNotNone(el15)
        el16 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteBtnMenu')
        self.assertIsNotNone(el16)
        el17 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteBtnExit')
        self.assertIsNotNone(el17)
        el18 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteBtnHome')
        self.assertIsNotNone(el18)
        el19 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteBtnBack')
        self.assertIsNotNone(el19)
        el20 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/directBackGround')
        self.assertIsNotNone(el20)

        el21 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteBtnRed')
        self.assertIsNotNone(el21)
        el22 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteBtnGreen')
        self.assertIsNotNone(el22)
        el23 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteBtnYellow')
        self.assertIsNotNone(el23)
        el24 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteBtnBlue')
        self.assertIsNotNone(el24)

        methodpackage.swipeLeft(self.driver, 500)
        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteTabButton')
        self.assertIsNotNone(el1)
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteTabChannel')
        self.assertIsNotNone(el2)
        el3 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteTabGesture')
        self.assertIsNotNone(el3)
        el4 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/btnRemoteBack')
        self.assertIsNotNone(el4)
        el5 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteTitle')
        self.assertIsNotNone(el5)
        el6 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteTitleIcon')
        self.assertIsNotNone(el6)
        el7 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/pull')
        self.assertIsNotNone(el7)

        el8 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/btnRemoteMute')
        self.assertIsNotNone(el8)
        el9 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/btnRemoteVolDown')
        self.assertIsNotNone(el9)
        el10 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/btnRemoteVolUp')
        self.assertIsNotNone(el10)

        el11 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteBtn_1')
        self.assertIsNotNone(el11)
        el12 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteBtn_2')
        self.assertIsNotNone(el12)
        el13 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteBtn_3')
        self.assertIsNotNone(el13)
        el14 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteBtn_4')
        self.assertIsNotNone(el14)
        el15 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteBtn_5')
        self.assertIsNotNone(el15)
        el16 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteBtn_6')
        self.assertIsNotNone(el16)
        el17 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteBtn_7')
        self.assertIsNotNone(el17)
        el18 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteBtn_8')
        self.assertIsNotNone(el18)
        el19 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteBtn_9')
        self.assertIsNotNone(el19)
        el20 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteBtn_star')
        self.assertIsNotNone(el20)
        el21 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteBtn_0')
        self.assertIsNotNone(el21)
        el22 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteBtn_hash')
        self.assertIsNotNone(el22)

        el2.click()
        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteTabButton')
        self.assertIsNotNone(el1)
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteTabChannel')
        self.assertIsNotNone(el2)
        el3 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteTabGesture')
        self.assertIsNotNone(el3)
        el4 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/btnRemoteBack')
        self.assertIsNotNone(el4)
        el5 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteTitle')
        self.assertIsNotNone(el5)
        el6 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteTitleIcon')
        self.assertIsNotNone(el6)
        el7 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/pull')
        self.assertIsNotNone(el7)
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/re1')
        count = len(els)
        if count > 0:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'至少有%s个频道' % count
        else:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有频道，有异常'
            self.assertTrue(False)

        el3.click()
        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteTabButton')
        self.assertIsNotNone(el1)
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteTabChannel')
        self.assertIsNotNone(el2)
        el3 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteTabGesture')
        self.assertIsNotNone(el3)
        el4 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/btnRemoteBack')
        self.assertIsNotNone(el4)
        el5 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteTitle')
        self.assertIsNotNone(el5)
        el6 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remoteTitleIcon')
        self.assertIsNotNone(el6)
        el7 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/pull')
        self.assertIsNotNone(el7)

        el8 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remote_button_home')
        self.assertIsNotNone(el8)
        el9 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remote_button_menu')
        self.assertIsNotNone(el9)
        el10 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remote_button_volume_subtract')
        self.assertIsNotNone(el10)
        el11 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remote_button_volume_add')
        self.assertIsNotNone(el11)
        el12 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/textviewline')
        self.assertIsNotNone(el12)
        el13 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/remote_gesture_btn')
        self.assertIsNotNone(el13)
        el14 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/gesture_msg_3')
        self.assertIsNotNone(el14)

    # 首页直播页面
    def test_0005_home_livepage(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   首页直播页面：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“首页”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_home")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'

        tempfile = os.path.join(methodpackage.currentDir, 'temp.png')  # 截图使用图片

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_tab_title')
        methodpackage.get_screenshot_by_element(self.driver, els[0], tempfile)
        count = methodpackage.getimage_color_original(methodpackage.load_image(tempfile), selectedColor)
        self.assertGreater(count, 0)
        self.assertEqual(els[0].text, u'直播')

        el1 = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/bannerViewPager")
        self.assertIsNotNone(el1)
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/bannerTitle')
        self.assertIsNotNone(el2)

        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/sub_column_name')
        self.assertEqual(len(els2), 8)
        for i in range(8):
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'直播推荐分类有：', els2[i].text

        methodpackage.moveTo(self.driver, 540, 1600, 540, 550)
        sleep(3)

        els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/title')
        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/subtitle')
        els3 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/count')
        els4 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/status')
        for j in range(len(els1) - 1):
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'频道 %s 的节目 %s 有%s' % (els1[j].text, els2[j].text, els3[j].text)

    # 首页直播横版推荐
    def test_0006_home_live_rec(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   首页直播横版推荐：开始'
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

        # 进入“首页”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_home")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'

        els = self.driver.find_elements_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]'
            '/android.widget.FrameLayout/android.widget.LinearLayout/android.support.v4.view.ViewPager'
            '/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup'
            '/android.support.v7.widget.RecyclerView/android.widget.FrameLayout/android.widget.FrameLayout'
            '/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.LinearLayout'
            '/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ImageView')
        count = len(els)

        for i in range(count):
            el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/bannerTitle')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"横版推荐节目：", el2.text
            methodpackage.swipeLeft_high(self.driver, 500)
            sleep(0.5)

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/bannerTitle')
        name = el.text
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"播放推荐节目：", name

        # 等待播放加载完成
        try:
            WebDriverWait(
                self.driver, 10).until_not(lambda x: x.find_element_by_id(
                "com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        sleep(3)

        # 点击播放器的返回按钮，判断按钮是否存在，存在则直接点，不存在则点播放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_back_header",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View")
        el.click()
        el1 = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/bannerViewPager")
        self.assertIsNotNone(el1)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'返回到直播首页'

    # 首页直播分类
    def test_0007_home_live_column(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   首页直播分类：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“首页”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_home")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/sub_column_name')
        self.assertEqual(len(els), 8)
        for i in range(8):
            els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/sub_column_name')
            name = els[i].text
            els[i].click()
            sleep(2)
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入直播推荐分类：', name
            els4 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/status')
            els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/title')
            els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/subtitle')
            els3 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/count')
            for j in range(len(els1) - 1):
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'频道 %s 的节目 %s 有%s' % (els1[j].text, els2[j].text, els3[j].text)

            el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/toolbar_title')
            el2 = self.driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
                '/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout'
                '/android.widget.LinearLayout/android.view.ViewGroup/android.widget.ImageButton')
            self.assertEqual(name, el1.text)
            el2.click()
            els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/sub_column_name')
            self.assertEqual(len(els), 8)
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'返回到直播首页'

    # 首页直播频道推荐
    def test_0008_home_live_channel(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   首页直播频道推荐：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(10)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        self.relogin(self.driver)

        # 进入“首页”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_home")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        sleep(1)

        methodpackage.moveTo(self.driver, 540, 1600, 540, 550)
        sleep(2)

        els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/title')
        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/subtitle')
        els3 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/count')
        els4 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/status')
        for j in range(len(els4)):
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'频道 %s 的节目 %s 有%s' % (els1[j].text, els2[j].text, els3[j].text)
            if els4[j].text == u'预定':
                els4[j].click()
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'预定频道 %s 的节目 %s' % \
                                                                                       (els1[j].text, els2[j].text)
                self.assertTrue(True, self.find_toast(self.driver, u'预定成功'))
            elif els4[j].text == u'已预定':
                els4[j].click()
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'取消预定频道 %s 的节目 %s' % \
                                                                                       (els1[j].text, els2[j].text)
                self.assertTrue(True, self.find_toast(self.driver, u'已取消预定'))

        els4 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/status')
        for j in range(len(els4)):
            if els4[j].text == u'直播中':
                channel = els1[j].text
                name = els2[j].text
                els4[j].click()
                # 等待播放加载完成
                try:
                    WebDriverWait(
                        self.driver, 10).until_not(lambda x: x.find_element_by_id(
                        "com.sumavision.sanping.gudou:id/LoadingView"))
                    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
                except TimeoutException:
                    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放频道:%s' % channel
                # 获取当前播放进度
                firsttime = self.getplay_time_live(self.driver)[2]
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'当前播放进度：', firsttime
                self.assertEqual(firsttime, u'直播')
                self.driver.back()
                break

        methodpackage.swipeUp(self.driver, 500)
        sleep(1)
        els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/title')
        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/subtitle')
        els4 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/status')
        for j in range(len(els4)):
            if els4[j].text == u'回看':
                channel = els1[j].text
                name = els2[j].text
                els4[j].click()
                # 等待播放加载完成
                try:
                    WebDriverWait(
                        self.driver, 10).until_not(lambda x: x.find_element_by_id(
                        "com.sumavision.sanping.gudou:id/LoadingView"))
                    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
                except TimeoutException:
                    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放频道 %s 的节目 %s' % (
                    channel, name)
                firsttime = self.getplay_time_review(self.driver)
                # print firsttime
                self.assertLess(firsttime, 60)
                self.driver.back()
                break

    # 首页直播推荐节目播放
    def test_0009_home_live_play(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   首页直播推荐节目播放：开始'
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

        # 进入“首页”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_home")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        sleep(1)

        els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/title')
        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/subtitle')
        els3 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/count')
        els4 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/status')

        channel = els1[0].text
        els1[0].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放频道：', channel
        # 等待播放加载完成
        try:
            WebDriverWait(
                self.driver, 10).until_not(lambda x: x.find_element_by_id(
                "com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/img_fav')
        self.assertIsNotNone(el)

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/img_share')
        self.assertIsNotNone(el)

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/chat_heat')
        self.assertIsNotNone(el)

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/view_num')
        self.assertIsNotNone(el)

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/com_num_w')
        self.assertIsNotNone(el)

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/chat_text')
        self.assertIsNotNone(el)

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/left_cur')
        self.assertIsNotNone(el)

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/chat_num')
        self.assertIsNotNone(el)

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/right_cur')
        self.assertIsNotNone(el)

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/enter_chat')
        self.assertIsNotNone(el)

        # tempFile = os.path.join(methodpackage.currentDir, "temp.png")  # 截图使用图片
        # count = 0
        # today = 0
        #
        # # 判断“今天”焦点置亮
        # els = self.driver.find_elements_by_xpath(
        #     "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
        #     "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[3]"
        #     "/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout"
        #     "/android.widget.TextView")
        # # print len(els)
        # for i in range(len(els)):
        #     date_week = els[i].text.split("\n")[0]
        #     # print date_week
        #     if date_week == u'今天':
        #         # print i
        #         today = i
        #         methodpackage.get_screenshot_by_element(self.driver, els[i], tempFile)
        #         count = int(methodpackage.getimage_color_epg(methodpackage.load_image(tempFile), selectedColor))
        #         # print count
        #         break
        # self.assertGreater(count, 0)
        # self.assertEqual(els[today].text.split("\n")[0], u'今天')
        # self.assertEqual(els[today].text.split("\n")[1], strftime("%m.%d", gmtime()))
        # # 判断正在播放按钮置亮
        # els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/live_tvEpg_flag')
        # tempFile1 = os.path.join(methodpackage.currentDir, "temp1.png")  # 截图使用图片
        # for j in range(len(els) - 2):
        #     methodpackage.get_screenshot_by_element(self.driver, els[j + 1], tempFile1)
        #     count = int(methodpackage.getimage_color(methodpackage.load_image(tempFile1), background))
        #     # print count
        #     if 1910 < count < 1970:
        #         # print u'回看图标白色像素：', count
        #         continue
        #     elif 1670 < count < 1730:
        #         # print u'播放图标白色像素：', count
        #         if j == len(els) - 3:
        #             break
        #     else:
        #         # print u'预约图标白色像素：', count
        #         self.assertLess(count, 1585)
        #         self.assertGreater(count, 1525)

        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放页正常'

        # 点击播放器的返回按钮，判断按钮是否存在，存在则直接点，不存在则点播放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_back_header",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'回到首页'

    # 首页点播页面
    def test_0010_home_vodpage(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   首页点播页面：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“首页”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_home")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'

        tempfile = os.path.join(methodpackage.currentDir, 'temp.png')  # 截图使用图片

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_tab_title')
        els[1].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页点播栏'

        methodpackage.get_screenshot_by_element(self.driver, els[1], tempfile)
        count = methodpackage.getimage_color_original(methodpackage.load_image(tempfile), selectedColor)
        self.assertGreater(count, 0)
        self.assertEqual(els[1].text, u'点播')

        el1 = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/bannerViewPager")
        self.assertIsNotNone(el1)
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/bannerTitle')
        self.assertIsNotNone(el2)

        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/sub_column_name')
        self.assertEqual(len(els2), 8)
        for i in range(8):
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点播推荐栏目有：', els2[i].text

        methodpackage.moveTo(self.driver, 540, 1600, 540, 550)
        sleep(3)

        els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/title')
        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_more')
        # els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/arrow')

        for j in range(len(els1)):
            if (j + 5) % 5 != 0:
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'推荐的节目有 %s' % els1[j].text

    # 首页点播横版推荐
    def test_0011_home_vod_rec(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   首页点播横版推荐：开始'
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

        # 进入“首页”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_home")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_tab_title')
        els[1].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页点播栏'

        els = self.driver.find_elements_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]'
            '/android.widget.FrameLayout/android.widget.LinearLayout/android.support.v4.view.ViewPager'
            '/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup'
            '/android.support.v7.widget.RecyclerView/android.widget.FrameLayout/android.widget.FrameLayout'
            '/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.LinearLayout'
            '/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ImageView')
        count = len(els)

        for i in range(count):
            el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/bannerTitle')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"横版推荐节目：", el2.text
            methodpackage.swipeLeft_high(self.driver, 500)
            sleep(0.5)

        el1 = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/bannerViewPager")
        el1.click()

        # 等待播放加载完成
        try:
            WebDriverWait(
                self.driver, 10).until_not(lambda x: x.find_element_by_id(
                "com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 点击播放器的返回按钮，判断按钮是否存在，存在则直接点，不存在则点播放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_back_header",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        el.click()
        el1 = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/bannerViewPager")
        self.assertIsNotNone(el1)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'返回到点播首页'

    # 首页点播分类
    def test_0012_home_vod_column(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   首页点播分类：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“首页”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_home")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_tab_title')
        els[1].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页点播栏'

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/sub_column_name')
        self.assertEqual(len(els), 8)
        for i in range(8):
            els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/sub_column_name')
            name = els[i].text
            els[i].click()
            sleep(2)
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入点播推荐栏目：', name
            els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/title')
            els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_more')
            # els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/arrow')
            for j in range(len(els1) - 1):
                if (j + 5) % 5 != 0:
                    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'推荐的节目有 %s' % els1[j].text

            el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/toolbar_title')
            el2 = self.driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
                '/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout'
                '/android.view.ViewGroup/android.widget.ImageButton')
            els3 = self.driver.find_elements_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
                '/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout'
                '/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout'
                '/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.support.v7.app.ActionBar.b'
                '/android.widget.TextView')
            for k in range(len(els3)):
                if els3[k].get_attribute('selected') == 'true':
                    self.assertEqual(els3[k].text, name)
            columname = els1[0].text
            els2[0].click()
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'查看更多 %s 节目' % columname
            sleep(1)
            el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/toolbar_title')
            self.assertEqual(columname, el1.text)
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/title')
            els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/title')
            self.assertGreater(len(els1), 0)
            el2 = self.driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
                '/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout'
                '/android.view.ViewGroup/android.widget.ImageButton')
            el2.click()
            sleep(0.5)
            el2 = self.driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
                '/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout'
                '/android.view.ViewGroup/android.widget.ImageButton')
            el2.click()
            els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/sub_column_name')
            self.assertEqual(len(els), 8)
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'返回到点播首页'

    # 首页点播节目推荐
    def test_0013_home_vod_program(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   首页点播节目推荐：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(10)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        self.relogin(self.driver)

        # 进入“首页”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_home")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        sleep(1)

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_tab_title')
        els[1].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页点播栏'
        sleep(1)

        methodpackage.moveTo(self.driver, 540, 1600, 540, 550)
        sleep(1)

        els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/title')
        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_more')
        # els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/arrow')

        for j in range(len(els1)):
            if (j + 5) % 5 != 0:
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'推荐的节目有 %s' % els1[j].text

        column = els1[0].text
        name = els1[1].text
        els1[1].click()
        # 等待播放加载完成
        try:
            WebDriverWait(
                self.driver, 10).until_not(lambda x: x.find_element_by_id(
                "com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放栏目 %s 的节目 %s' % (
            column, name)
        firsttime = self.getplay_time_vod(self.driver)
        # print firsttime
        self.assertLess(firsttime, 60)
        self.driver.back()

        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_more')
        # els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/arrow')
        els2[0].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'查看更多 %s 节目' % column
        sleep(1)
        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/toolbar_title')
        self.assertEqual(column, el1.text)
        els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/title')
        self.assertGreater(len(els1), 0)
        el2 = self.driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout'
            '/android.view.ViewGroup/android.widget.ImageButton')
        el2.click()

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_tab_title')
        self.assertEqual(len(els), 4)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'返回到点播首页'

    # 首页点播推荐节目播放
    def test_0014_home_vod_play(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   首页点播推荐节目播放：开始'
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

        # 进入“首页”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_home")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        sleep(1)

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_tab_title')
        els[1].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页点播栏'
        sleep(1)

        methodpackage.moveTo(self.driver, 540, 1600, 540, 550)
        sleep(1)

        els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/title')
        name = els1[1].text
        els1[1].click()

        # 等待播放加载完成
        try:
            WebDriverWait(
                self.driver, 10).until_not(lambda x: x.find_element_by_id(
                "com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放节目：', name

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/img_fav')
        self.assertIsNotNone(el)

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/img_share')
        self.assertIsNotNone(el)

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/img_enter_vod_cache')
        self.assertIsNotNone(el)

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tv_report')
        self.assertIsNotNone(el)

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tv_info')
        self.assertEqual(name, el.text)

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/img_info_more')
        self.assertIsNotNone(el)

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tv_director')
        self.assertIsNotNone(el)

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tv_actor_title')
        self.assertIsNotNone(el)

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tv_actors')
        self.assertIsNotNone(el)

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/image_comment')
        self.assertIsNotNone(el)

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/edit_comment')
        self.assertIsNotNone(el)

        # 点击播放器的返回按钮，判断按钮是否存在，存在则直接点，不存在则点播放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_back_header",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        el.click()
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_tab_title')
        self.assertEqual(len(els), 4)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'返回到点播首页'

    # 首页广东页面
    def test_0015_home_gdpage(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   首页广东页面：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(10)

        # 进入“首页”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_home")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'

        tempfile = os.path.join(methodpackage.currentDir, 'temp.png')  # 截图使用图片

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_tab_title')
        els[2].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页广东栏'

        methodpackage.get_screenshot_by_element(self.driver, els[2], tempfile)
        count = methodpackage.getimage_color_original(methodpackage.load_image(tempfile), selectedColor)
        self.assertGreater(count, 0)
        self.assertEqual(els[2].text, u'广东')

        el1 = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/bannerViewPager")
        self.assertIsNotNone(el1)
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/bannerTitle')
        self.assertIsNotNone(el2)

        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/sub_column_name')
        self.assertEqual(len(els2), 4)
        for i in range(4):
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'推荐业务有：', els2[i].text

        methodpackage.moveTo(self.driver, 540, 1350, 540, 500)
        sleep(3)

        els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/title')
        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/time')
        # els3 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_duration')

        for j in range(len(els1)):
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'推荐的节目有 %s' % els1[j].text

    # 首页广东横版推荐
    def test_0016_home_gd_rec(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   首页广东横版推荐：开始'
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

        # 进入“首页”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_home")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_tab_title')
        els[2].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页广东栏'

        els = self.driver.find_elements_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]'
            '/android.widget.FrameLayout/android.widget.LinearLayout/android.support.v4.view.ViewPager'
            '/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup'
            '/android.support.v7.widget.RecyclerView/android.widget.FrameLayout/android.widget.FrameLayout'
            '/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.LinearLayout'
            '/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ImageView')
        count = len(els)

        for i in range(count):
            el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/bannerTitle')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"横版推荐节目：", el2.text
            methodpackage.swipeLeft_high(self.driver, 500)
            sleep(0.5)

        el1 = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/bannerViewPager")
        name = el1.text
        el1.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(
                self.driver, 10).until_not(lambda x: x.find_element_by_id(
                "com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 点击播放器的返回按钮，判断按钮是否存在，存在则直接点，不存在则点播放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_back_header",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        el.click()
        el1 = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/bannerViewPager")
        self.assertIsNotNone(el1)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'返回到广东首页'

    # 首页广东业务分类
    def test_0017_home_gd_column(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   首页广东业务分类：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“首页”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_home")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_tab_title')
        els[2].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页广东栏'

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/sub_column_name')
        self.assertEqual(len(els), 4)

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/sub_column_name')
        name = els[0].text
        els[0].click()
        sleep(5)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入广东推荐业务：', name
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/toolbar_title')
        self.assertEqual(u'广东省广播电视网络股份有限公司2', el.text)
        el2 = self.driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout'
            '/android.view.ViewGroup/android.widget.ImageButton')
        el2.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'返回到广东首页'

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/sub_column_name')
        name = els[1].text
        els[1].click()
        sleep(5)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入广东推荐业务：', name
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/toolbar_title')
        self.assertEqual(u'广东广电网络', el.text)
        el2 = self.driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout'
            '/android.view.ViewGroup/android.widget.ImageButton')
        el2.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'返回到广东首页'

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/sub_column_name')
        name = els[2].text
        els[2].click()
        sleep(5)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入广东推荐业务：', name
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/toolbar_title')
        self.assertEqual(u'携程旅行-酒店预订,机票预订查询,旅游度假,商旅管理-携程无线官网', el.text)
        el2 = self.driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout'
            '/android.view.ViewGroup/android.widget.ImageButton')
        el2.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'返回到广东首页'

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/sub_column_name')
        name = els[3].text
        els[3].click()
        sleep(5)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入广东推荐业务：', name
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/toolbar_title')
        self.assertEqual(u'南方网络', el.text)
        el2 = self.driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout'
            '/android.view.ViewGroup/android.widget.ImageButton')
        el2.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'返回到广东首页'

    # 首页广东视频推荐
    def test_0018_home_gd_channel(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   首页广东视频推荐：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(10)

        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入我的'
        sleep(1)

        self.relogin(self.driver)

        # 进入“首页”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_home")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        sleep(1)

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_tab_title')
        els[2].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页广东栏'
        sleep(1)

        methodpackage.moveTo(self.driver, 540, 1350, 540, 500)
        sleep(2)

        els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/title')
        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/time')
        # els3 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_duration')

        for j in range(len(els1)):
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'推荐的节目有 %s' % els1[j].text

        name = els1[0].text
        els1[0].click()
        # 等待播放加载完成
        try:
            WebDriverWait(
                self.driver, 10).until_not(lambda x: x.find_element_by_id(
                "com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放节目 %s' % name
        firsttime = self.getplay_time_vod(self.driver)
        # print firsttime
        self.assertLess(firsttime, 60)
        self.driver.back()

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_tab_title')
        self.assertEqual(len(els), 4)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'返回到广东首页'

    # 首页专区页面
    def test_0019_home_special(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   首页专区页面：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“首页”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_home")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'

        tempfile = os.path.join(methodpackage.currentDir, 'temp.png')  # 截图使用图片

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_tab_title')
        els[3].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页专区栏'

        methodpackage.get_screenshot_by_element(self.driver, els[3], tempfile)
        count = methodpackage.getimage_color_original(methodpackage.load_image(tempfile), selectedColor)
        self.assertGreater(count, 0)
        self.assertEqual(els[3].text, u'专区')

        els1 = self.driver.find_elements_by_id("com.sumavision.sanping.gudou:id/im_img")
        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/im_title')
        self.assertEqual(els2[0].text, u'4K专区')
        self.assertEqual(els2[1].text, u'天华专区')

        els1[0].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入4K专区'
        sleep(2)

        # 下划刷新，判断页面元素
        methodpackage.swipeDown(self.driver, 500)

        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/toolbar_title')
        self.assertEqual(el1.text, u'4K专区')

        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/filter_year')
        el2.click()
        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/name')
        self.assertGreater(len(els2), 0)
        el2.click()

        el3 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/filter_locale')
        el3.click()
        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/name')
        self.assertGreater(len(els2), 0)
        el3.click()

        el4 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/filter_category')
        el4.click()
        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/name')
        self.assertGreater(len(els2), 0)
        el4.click()

        el5 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/filter_sorting')
        el5.click()
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/vod_new_txt')
        self.assertIsNotNone(el)
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/vod_hot_txt')
        self.assertIsNotNone(el)
        el5.click()

        els3 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/textView1')
        self.assertGreater(len(els3), 0)

        el = self.driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
            '/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout'
            '/android.view.ViewGroup/android.widget.ImageButton')
        el.click()
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_tab_title')
        self.assertEqual(len(els), 4)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'返回到点播首页'

        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/im_title')
        name = els2[1].text
        els2[1].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击', name
        self.assertEqual(True, self.find_toast(self.driver, u'此分类为网关内容，请连接网关环境后重试'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'弹出提示：此分类为网关内容，请连接网关环境后重试'

        methodpackage.swipeUp(self.driver, 500)
        sleep(1)

        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/im_title')
        for i in range(len(els2)):
            name = els2[i].text
            els2[i].click()
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击', name
            self.assertEqual(True, self.find_toast(self.driver, u'此分类为网关内容，请连接网关环境后重试'))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'弹出提示：此分类为网关内容，请连接网关环境后重试'
            sleep(1)

    # 发现页面
    def test_0020_discover(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   发现页面：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“首页”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_discover")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'

        els1 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/image')
        self.assertGreater(len(els1), 0)
        for i in range(10):
            els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/title')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'推荐内容 ', els2[0].text
            methodpackage.moveTo(self.driver, 540, 1100, 540, 500)
            sleep(1)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
