#-*-coding:utf-8-*-

import os
import subprocess
import random
import time
import datetime
import methodpackage
from time import sleep, gmtime, strftime
from appium import webdriver
import sys
import colorsys
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.mobileby import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import unittest

reload(sys)
sys.setdefaultencoding("utf-8")

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
# apppath = 'F:/autotest/sample-code-master/sample-code-master/sample-code/apps/ApiDemos/bin/'

selectedColor = (253, 130, 0)
background = (253, 253, 253)
playedColor = (0, 0, 0)
background_epg = (215, 215, 215)

class SimpleAndroidTests(unittest.TestCase):
    # 启动app
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        # desired_caps['platformVersion'] = '4.1'
        # desired_caps['deviceName'] = 'YPOV95LJ99999999'
        desired_caps['deviceName'] = 'XPUDU17303004497'
        # desired_caps['deviceName'] = '351BBHGE53V3'
        desired_caps['unicodeKeyboard'] = True
        desired_caps['resetKeyboard'] = True
        desired_caps['noReset'] = True
        desired_caps['automationName'] = 'uiautomator2'
        # desired_caps['automationName'] = 'selendroid'
        # desired_caps['app'] = PATH(
        #    '../../../apps/ApiDemos/bin/com.sumavision.sanping.gudou_4362.apk'
        #)

        # desired_caps['app'] = methodpackage.file_name(apppath)
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

    def sh(self, command):
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), p.stdout.read()

    # 启动应用的弹框处理
    def App_Start(self, driver):
        # 选择定位到成都，判断按钮是否存在，存在则直接点，不存在则报异常
        try:
            WebDriverWait(driver, 5).until(lambda x: x.find_element_by_xpath(
                "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout"))
            # 点击确定按钮定位到成都
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
        except:
            try:
                WebDriverWait(self.driver, 3).until(lambda x: x.find_element_by_xpath(
                    '//android.view.View[@content-desc="谷豆TV隐私条款"]'))
                sleep(6)
                self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/btn_confirm").click()
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'同意条款'
            except:
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'不是第一次进应用'
                return

        sleep(2)
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

    # 查看直播页面显示情况
    def test_0002_livepage(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   查看直播页面显示情况：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")

        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'

        # 判断默认落焦全部
        tab_els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_vod_tab_text')
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'
        self.assertEqual(tab_els[1].text, u'全部')
        self.assertTrue(tab_els[1].get_attribute('selected'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'默认落焦“全部”'

        # 当前页频道列表
        els = self.driver.find_elements_by_id("com.sumavision.sanping.gudou:id/tvName")

        # 当前页频道名称列表
        chanl_els = self.driver.find_elements_by_id("com.sumavision.sanping.gudou:id/tvName")

        # 当前页频道当前EPG列表
        epg1_els = self.driver.find_elements_by_id("com.sumavision.sanping.gudou:id/playNow")

        # 当前页频道下个EPG列表
        epg2_els = self.driver.find_elements_by_id("com.sumavision.sanping.gudou:id/playNext")

        # tempFile = os.path.join(methodpackage.currentDir, "temp.png")  # 截图使用图片
        # methodpackage.get_screenshot_by_element(self.driver, epg1_els[1], tempFile)
        chanl = []
        for i in range(len(els) - 1):
            chanl.append(chanl_els[i].text)
            # methodpackage.get_screenshot_by_element(self.driver, epg1_els[i], tempFile)
            # self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(tempFile)), selectedColor)
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), chanl_els[i].text, u'正在播放：', epg1_els[i].text, u'即将播放：', epg2_els[i].text

        # 上划加载更多频道
        methodpackage.swipeUp(self.driver, 400)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'上划刷新频道'

        chanl_el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")

        # 当前页频道当前EPG列表
        epg1_el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/playNow")

        # 当前页频道下个EPG列表
        epg2_el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/playNext")
        self.assertNotEqual(chanl[0], chanl_el.text)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), chanl_el.text, u'正在播放：', \
            epg1_el.text, u'即将播放：', epg2_el.text

    # 切换直播栏目分类
    def test_0003_liveCategory(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   切换直播栏目分类：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()

        # 判断默认落焦全部
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tv_vod_tab_text")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'
        self.assertTrue(el.get_attribute('selected'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'默认落焦“全部”'

        # 获取当前显示的分类
        els = self.driver.find_elements_by_id("com.sumavision.sanping.gudou:id/tv_vod_tab_text")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播, 获取直播分类' ,\
            str(len(els))

        # 点击每个分类测试
        for i in range(len(els)):
            firstliveName = ''
            if 'false' == els[i].get_attribute('selected'):
                els[i].click()
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击分类' ,els[i].text

            self.assertTrue(els[i].get_attribute('selected'))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击分类', els[i].text, u'成功'

            try:
                el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")
            except Exception:
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'分类', els[i].text, \
                    u'没有频道'
                el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/fragment_gridview_cgcontent")
                tempFile = os.path.join(methodpackage.currentDir, "temp.png")  # 截图使用图片
                methodpackage.get_screenshot_by_element(self.driver, el, tempFile)
                continue
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'分类', els[i].text, \
                u'第一个节目是', el.text
            self.assertNotEqual(firstliveName, el.text)
            firstliveName = el.text[:]

            # 分类直播频道滑动
            methodpackage.swipeUp(self.driver, 500)
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'滑动分类：', els[i].text

            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")

            if firstliveName == el.text[:]:
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'分类', els[i].text, \
                    u'节目不超过一屏'
            else:
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'分类', els[i].text, u'滑动成功'

            # 对直播节目显示框进行截图，然后进行对比
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/fragment_gridview_cgcontent")
            tempFile = os.path.join(methodpackage.currentDir, "temp.png")  # 截图使用图片
            emptyimage = os.path.join(methodpackage.currentDir, "png", "notloadlive.png")
            methodpackage.get_screenshot_by_element(self.driver, el, tempFile)
            self.assertFalse(methodpackage.image_same_as(emptyimage, tempFile, 0.7))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'分类', els[i].text, u'显示海报成功'

    #  直播节目播放
    def test_0004_liveplay(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   切换直播栏目分类：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'

        # 播放一个节目
        try:
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")
            name = el.text
        except Exception:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道'
            return
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

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

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/channel_name')
        self.assertEqual(el.text, name)

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

        tempFile = os.path.join(methodpackage.currentDir, "temp.png")  # 截图使用图片
        count = 0
        today = 0

        # 判断“今天”焦点置亮
        els = self.driver.find_elements_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[3]"
            "/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout"
            "/android.widget.TextView")
        # print len(els)
        for i in range(len(els)):
            date_week = els[i].text.split("\n")[0]
            # print date_week
            if date_week == u'今天':
                # print i
                today = i
                methodpackage.get_screenshot_by_element(self.driver, els[i], tempFile)
                count = int(methodpackage.getimage_color_epg(methodpackage.load_image(tempFile), selectedColor))
                # print count
                break
        self.assertGreater(count, 0)
        self.assertEqual(els[today].text.split("\n")[0], u'今天')
        self.assertEqual(els[today].text.split("\n")[1], strftime("%m.%d", gmtime()))
        # 判断正在播放按钮置亮
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/live_tvEpg_flag')
        tempFile1 = os.path.join(methodpackage.currentDir, "temp1.png")  # 截图使用图片
        for j in range(len(els) - 2):
            methodpackage.get_screenshot_by_element(self.driver, els[j + 1], tempFile1)
            count = int(methodpackage.getimage_color(methodpackage.load_image(tempFile1), background))
            # print count
            if 1910 < count < 1970:
                # print u'回看图标白色像素：', count
                continue
            elif 1670 < count < 1730:
                # print u'播放图标白色像素：', count
                if j == len(els) - 3:
                    break
            else:
                # print u'预约图标白色像素：', count
                self.assertLess(count, 1585)
                self.assertGreater(count, 1525)

        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放页正常'

        # 点击播放器的返回按钮，判断按钮是否存在，存在则直接点，不存在则点播放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_back_header",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'回到首页'

    # 直播节目播放时切换到手机桌面后再次进入应用时播放暂停
    def test_0005_livePlay_home_pause_ster(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), \
            u'  直播节目播放时切换到手机桌面后再次进入应用：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'

        # 播放一个节目
        try:
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")
            name = el.text
        except Exception:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道'
            return
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

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

        tempFile = os.path.join(methodpackage.currentDir, "temp.png")  # 截图使用图片
        tempFile1 = os.path.join(methodpackage.currentDir, "temp1.png")  # 截图使用图片
        el = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        methodpackage.get_screenshot_by_element(self.driver, el, tempFile)

        #  Home 5秒钟再进入应用
        # self.driver.background_app(5)
        self.driver.press_keycode(3)
        sleep(2)
        self.driver.press_keycode(3)
        el = self.driver.find_element_by_xpath('//android.widget.TextView[@text="谷豆TV"]')
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击home5秒，进入应用'
        sleep(10)
        el = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        methodpackage.get_screenshot_by_element(self.driver, el, tempFile1)
        self.assertFalse(methodpackage.image_same_as(tempFile1, tempFile, 0.7))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'继续播放视频'

    # 直播节目播放断网重连续播
    def test_0006_livePlay_network_off_on(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   直播节目播放断网重连续播：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'

        # 播放一个节目
        try:
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")
            name = el.text
        except Exception:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道'
            return
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

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

        # 设置为飞行模式
        self.driver.set_network_connection(1)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'设置为飞行模式'
        sleep(5)

        # 提示“当前为移动网络，播放将产生流量费用，确定继续播放吗？”，点击取消
        methodpackage.wait_xPathMsg_click_xPathButton(
            self.driver,
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.FrameLayout",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.Button",
            5,
            u'当前为移动网络，播放将产生流量费用，确定继续播放吗？',
            False)

        # 设置为wifi+数据
        self.driver.set_network_connection(6)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'设置为wifi+数据'
        sleep(5)
        tempFile = os.path.join(methodpackage.currentDir, "temp.png")  # 截图使用图片
        tempFile1 = os.path.join(methodpackage.currentDir, "temp1.png")
        el = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        methodpackage.get_screenshot_by_element(self.driver, el, tempFile)
        sleep(10)
        el = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        methodpackage.get_screenshot_by_element(self.driver, el, tempFile1)
        self.assertFalse(methodpackage.image_same_as(tempFile1, tempFile, 0.7))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'继续播放视频'

    '''# wifi切换到4G网时节目正常播放
    def test_0007_livePlay_wifi_to_4G(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   wifi切换到4G网时节目正常播放：开始'

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'

        # 播放一个节目
        try:
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")
            name = el.text
        except Exception:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道'
            return
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

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

        if self.driver.network_connection != 2 and self.driver.network_connection != 6:
            self.driver.set_network_connection(2)
            sleep(3)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'网络为Wifi状态'

        self.driver.set_network_connection(4)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'切换网络为4G状态'
        # try:
        #     el = self.driver.find_element_by_xpath('//android.widget.Button[@text="允许"]')
        #     el.click()
        # except NoSuchElementException:
        #     pass
        tempFile = os.path.join(methodpackage.currentDir, "temp.png")  # 截图使用图片
        tempFile1 = os.path.join(methodpackage.currentDir, "temp1.png")

        # 提示“当前为移动网络，播放将产生流量费用，确定继续播放吗？”，点击确定
        methodpackage.wait_xPathMsg_click_xPathButton(
            self.driver,
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.FrameLayout",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.Button",
            5,
            u'当前为移动网络，播放将产生流量费用，确定继续播放吗？',
            True)

        el = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        methodpackage.get_screenshot_by_element(self.driver, el, tempFile)
        sleep(10)
        el = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        methodpackage.get_screenshot_by_element(self.driver, el, tempFile1)
        self.assertFalse(methodpackage.image_same_as(tempFile1, tempFile, 0.7))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'继续播放视频'
        self.driver.set_network_connection(6)
        # try:
        #     el = self.driver.find_element_by_xpath('//android.widget.Button[@text="允许"]')
        #     el.click()
        # except NoSuchElementException:
        #     pass

    # 4G切换到wifi网时节目正常播放
    def test_0008_livePlay_4G_to_wifi(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   wifi切换到4G网时节目正常播放：开始'

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'

        # 播放一个节目
        try:
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")
            name = el.text
        except Exception:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道'
            return
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

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

        if self.driver.network_connection != 4:
            self.driver.set_network_connection(4)
            # try:
            #     el = self.driver.find_element_by_xpath('//android.widget.Button[@text="允许"]')
            #     el.click()
            #     print u'允许'
            # except NoSuchElementException:
            #     pass
            sleep(3)
            # 如果提示更新，放弃更新应用
            methodpackage.wait_xPathMsg_click_idButton(
                self.driver,
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.TextView[1]",
                "com.sumavision.sanping.gudou:id/btnOK",
                3,
                u'应用更新',
                False)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'网络为4G状态'

        self.driver.set_network_connection(2)
        # try:
        #     el = self.driver.find_element_by_xpath('//android.widget.Button[@text="允许"]')
        #     el.click()
        #     print u'允许'
        # except NoSuchElementException:
        #     pass
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'切换网络为wifi状态'

        tempFile = os.path.join(methodpackage.currentDir, "temp.png")  # 截图使用图片
        tempFile1 = os.path.join(methodpackage.currentDir, "temp1.png")

        el = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        methodpackage.get_screenshot_by_element(self.driver, el, tempFile)
        sleep(10)
        el = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        methodpackage.get_screenshot_by_element(self.driver, el, tempFile1)
        self.assertFalse(methodpackage.image_same_as(tempFile1, tempFile, 0.7))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'继续播放视频'
        self.driver.set_network_connection(6)
        # try:
        #     el = self.driver.find_element_by_xpath('//android.widget.Button[@text="允许"]')
        #     el.click()
        # except NoSuchElementException:
        #     pass

    # 节目播放时手机来电后可以恢复播放
    def test_0009_livePlay_inCall(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   节目播放时手机来电后可以恢复播放无法实现'
    '''

    # 直播节目全屏播放功能
    def test_0010_liveplay_fullscreen(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   直播节目全屏播放功能：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'

        # 播放一个节目
        try:
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")
            name = el.text
        except Exception:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道'
            return
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 5).until_not(lambda x: x.find_element_by_id(
                "com.sumavision.sanping.gudou:id/LoadingView"))
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
        sleep(3)

        # 找到返回按钮，判断按钮是否存在，存在则直接点，不存在则直播放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_back_header",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'退出全屏播放'

        # 找到全屏按钮，判断按钮是否存在，存在则直接点，不存在则直播放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_expand",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击全屏'
        sleep(3)

        # 找到缩屏按钮，判断按钮是否存在，存在则直接点，不存在则直播放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_unexpand",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击缩屏'
        sleep(3)

    # 直播节目播放暂停/恢复
    def test_0011_liveplay_pause(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   直播节目播放暂停/恢复：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(10)

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'

        # 播放一个节目
        try:
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")
            name = el.text
        except Exception:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道'
            return
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(
                self.driver, 5).until_not(lambda x: x.find_element_by_id(
                "com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 暂停
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_ctrl_small_play",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'暂停播放'

        sleep(5)

        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_ctrl_small_play",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'恢复播放'
        sleep(5)

        # 找到全屏按钮，判断按钮是否存在，存在则直接点，不存在则直播放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_expand",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击全屏'
        sleep(3)

        # 暂停
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_ctrl_large_play",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'暂停播放'
        sleep(5)

        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_ctrl_large_play",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'恢复播放'
        sleep(5)

    # 屏幕锁定功能
    def test_0012_liveplay_lockscreen(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   屏幕锁定功能：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'

        # 播放一个节目
        try:
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")
            name = el.text
        except Exception:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道'
            return
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

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

        # 点击锁屏按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_lock_live",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'锁定全屏'
        sleep(3)

        el = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        el.click()
        els = self.driver.find_elements_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/*"
        )
        self.assertEqual(2, len(els))
        sleep(3)

        # 退出锁屏
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_lock_live",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'退出锁屏'
        sleep(2)

    # 投放电视功能
    def test_0013_liveplay_push(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   投放电视功能：开始'
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

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'

        # 播放一个节目
        try:
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")
            name = el.text
        except Exception:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道'
            return
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(
                self.driver, 15).until_not(lambda x: x.find_element_by_id(
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

        # 点击投屏按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_push_header",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'投屏'
        sleep(10)

        els = self.driver.find_elements_by_id("com.sumavision.sanping.gudou:id/tv_vod_tab_text")
        self.assertEqual(els[0].text, u'多屏互动')
        self.assertEqual(els[1].text, u'电视播放')

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_login_back")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'退出投屏'
        sleep(2)

    # 直播节目码率切换功能
    def test_0014_liveplay_resolution(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   直播节目码率切换功能：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'

        # 播放一个节目
        try:
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")
            name = el.text
        except Exception:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道'
            return
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

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

        # 找到全屏按钮，判断按钮是否存在，存在则直接点，不存在则点播放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_expand",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击全屏'

        # 找到码率按钮，判断按钮是否存在，存在则直接点，不存在则点播放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/text_setting",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        el.click()
        els = self.driver.find_elements_by_class_name('android.widget.TextView')
        count = len(els)
        for i in range(count):
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'选择播放：', els[i].text
            els[i].click()
            sleep(3)
            if i != count - 1:
                el = methodpackage.find_elementId_conditionXpath(
                    self.driver,
                    "com.sumavision.sanping.gudou:id/text_setting",
                    "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                    "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
                )
                el.click()
                els = self.driver.find_elements_by_class_name('android.widget.TextView')

        self.driver.back()

    # 直播节目收藏、取消收藏
    def test_0015_liveplay_favor(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   直播节目收藏、取消收藏：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)
        # 清空直播收藏记录
        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        # 进入“我的收藏”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_fav")
        el.click()
        # 进入收藏的“直播”页
        el = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout"
            "/android.widget.LinearLayout[1]/android.widget.TextView")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"进入收藏直播页"
        try:
            # 清空直播收藏内容
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mycollection_deleteall")
            el.click()
            el = self.driver.find_element_by_xpath(
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.LinearLayout/android.widget.LinearLayout[2]")
            el.click()
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"清空收藏记录"
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"之前没有收藏记录"
            pass
        # 返回到“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_myfav_back")
        el.click()
        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'
        el.click()
        # 播放一个节目
        try:
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")
            channel_name1 = el.text
        except Exception:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道'
            return
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', channel_name1
        # 收藏
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_fav")
        tempFile = os.path.join(methodpackage.currentDir, "temp.png")  # 截图使用图片
        methodpackage.get_screenshot_by_element(self.driver, el, tempFile)
        self.assertEqual(0, methodpackage.getimage_color(methodpackage.load_image(tempFile), (235, 97, 0)))
        el.click()
        self.assertEqual(True, self.find_toast(self.driver, u'收藏成功'))
        methodpackage.get_screenshot_by_element(self.driver, el, tempFile)
        self.assertGreater(methodpackage.getimage_color(methodpackage.load_image(tempFile), (235, 97, 0)), 150)
        # el.click()
        # 点击物理返回键
        self.driver.press_keycode(4)
        sleep(1)

        # 进入“收藏”分类验证收藏功能
        els = self.driver.find_elements_by_id("com.sumavision.sanping.gudou:id/tv_vod_tab_text")
        els[0].click()
        try:
            WebDriverWait(self.driver, 3).until(lambda x: x.find_element_by_id(
                'com.sumavision.sanping.gudou:id/tvName'))
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tvName')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"收藏成功"
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'收藏有问题'
            self.assertFalse(True)
        channel_name2 = el.text
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"收藏节目：%s" % channel_name2
        self.assertIs(channel_name1 == channel_name2, True)
        # 进入“我的收藏”验证收藏功能
        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        # 进入“我的收藏”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_fav")
        el.click()
        # 进入收藏的“直播”页
        el = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout"
            "/android.widget.LinearLayout[1]/android.widget.TextView")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"进入收藏直播页"
        try:
            # 选中收藏的第一条记录的节目名
            WebDriverWait(self.driver, 2).until(lambda x: x.find_element_by_xpath(
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout/android.support.v4.view.ViewPager/android.widget.FrameLayout"
                "/android.widget.LinearLayout/android.widget.ScrollView/android.widget.ListView"
                "/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.RelativeLayout"
                "/android.widget.LinearLayout/android.widget.TextView[1]"))
            el = self.driver.find_element_by_xpath(
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout/android.support.v4.view.ViewPager/android.widget.FrameLayout"
                "/android.widget.LinearLayout/android.widget.ScrollView/android.widget.ListView"
                "/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.RelativeLayout"
                "/android.widget.LinearLayout/android.widget.TextView[1]")
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'收藏存在异常'
            self.assertFalse(True)
        # 保存收藏节目的节目名
        channel_name3 = el.text
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"收藏节目：%s" % channel_name3
        self.assertIs(channel_name1 == channel_name3, True)
        # 返回到“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_myfav_back")
        el.click()
        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        el.click()

        methodpackage.swipeDown(self.driver, 500)
        sleep(5)

        # 播放一个节目
        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tvName')
            name = el.text
        except Exception:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道，有异常'
            self.assertFalse(True)
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name
        # 再点击收藏按钮
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_fav")
        methodpackage.get_screenshot_by_element(self.driver, el, tempFile)
        self.assertGreater(methodpackage.getimage_color(methodpackage.load_image(tempFile), (235, 97, 0)), 150)
        el.click()
        self.assertEqual(True, self.find_toast(self.driver, u'已取消收藏'))
        methodpackage.get_screenshot_by_element(self.driver, el, tempFile)
        self.assertEqual(0, methodpackage.getimage_color(methodpackage.load_image(tempFile), (235, 97, 0)))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"已取消收藏，验证提示信息正确"
        self.driver.back()

        # 进入“收藏”分类验证收藏功能
        els = self.driver.find_elements_by_id("com.sumavision.sanping.gudou:id/tv_vod_tab_text")
        els[0].click()

        methodpackage.swipeDown(self.driver, 500)
        sleep(5)

        try:
            el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tvName')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"取消收藏有问题"
            self.assertIs(False, True)
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"取消收藏成功"

        # 再次进入“我的收藏”验证收藏功能
        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()
        # 进入“我的收藏”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_fav")
        el.click()
        # 进入收藏的“直播”页
        el = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout"
            "/android.widget.LinearLayout[1]/android.widget.TextView")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"进入收藏直播页"
        # 判断收藏直播页收藏节目是否存在
        try:
            WebDriverWait(self.driver, 3).until_not(lambda x: x.find_element_by_id(
                'com.sumavision.sanping.gudou:id/tvName'))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"取消收藏成功"
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"取消收藏有问题"
            self.assertIs(False, True)

    # 直播节目取消分享、直播分享功能
    def test_0016_liveplay_share(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   直播节目取消分享、直播分享功能：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(10)
        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'

        # 等待播放加载完成
        while True:
            # 播放一个节目
            try:
                el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")
                name = el.text
            except Exception:
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道'
                return
            el.click()
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

            try:
                WebDriverWait(
                    self.driver, 10).until_not(lambda x: x.find_element_by_id(
                    "com.sumavision.sanping.gudou:id/LoadingView"))
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
                # 点击分享按钮
                el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_share")
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"进入分享"
                el.click()
                break
            except TimeoutException:
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'
                # 按物理返回键，回到直播列表
                self.driver.press_keycode(4)
                continue

        # 点击取消按钮，取消分享
        el = self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'取消分享')]")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"取消分享"

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

        # 点击分享按钮
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_share")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"进入分享"
        # 点击QQ按钮，分享到QQ
        el = self.driver.find_element_by_xpath("//android.widget.TextView[@text='QQ']")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"分享到QQ"
        # 点击右上角取消按钮，取消分享
        el = self.driver.find_element_by_id("com.tencent.mobileqq:id/ivTitleBtnRightText")
        el.click()
        self.assertEqual(True, self.find_toast(self.driver, u'分享取消'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"分享取消，验证提示信息正确"
        # 点击分享按钮
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_share")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"点击分享"

        # 点击QQ按钮，分享到QQ
        el = self.driver.find_element_by_xpath("//android.widget.TextView[@text='QQ']")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"分享到QQ"
        # 点击“我的电脑”按钮，分享到我的电脑
        el = self.driver.find_element_by_xpath(
            "//android.widget.AbsListView[@content-desc=\" \"]/android.widget.RelativeLayout[2]")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"分享到“我的电脑”"
        # 点击取消按钮，取消分享到我的电脑
        el = self.driver.find_element_by_id("com.tencent.mobileqq:id/dialogLeftBtn")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"取消分享到“我的电脑”"
        # 点击“我的电脑”按钮，分享到我的电脑
        el = self.driver.find_element_by_xpath(
            "//android.widget.AbsListView[@content-desc=\" \"]/android.widget.RelativeLayout[2]")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"分享到“我的电脑”"
        # 点击发送按钮，分享到我的电脑
        el = self.driver.find_element_by_id("com.tencent.mobileqq:id/dialogRightBtn")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"选择发送"
        # 点击“返回谷豆TV”按钮，回到谷豆TV
        el = self.driver.find_element_by_id("com.tencent.mobileqq:id/dialogLeftBtn")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"选择回到“谷豆TV”"

        self.assertEqual(True, self.find_toast(self.driver, u'分享成功'))

        # 点击分享按钮
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_share")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"点击分享"
        # 点击微信按钮，分享到微信
        el = self.driver.find_element_by_xpath("//android.widget.TextView[@text='微信']")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"分享到微信"
        # 点击返回按钮，取消分享微信（此时在登录微信界面）
        el = self.driver.find_element_by_xpath("//android.widget.ImageView[@content-desc=\"返回\"]")
        el.click()
        # self.driver.back()
        self.assertEqual(True, self.find_toast(self.driver, u'分享取消'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"分享取消，验证提示信息正确"
        # 点击分享按钮
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_share")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"点击分享"
        # 点击微信朋友圈按钮，分享到朋友圈
        el = self.driver.find_element_by_xpath("//android.widget.TextView[@text='微信朋友圈']")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"分享到朋友圈"
        # 点击返回按钮，取消分享微信
        el = self.driver.find_element_by_xpath("//android.widget.ImageView[@content-desc=\"返回\"]")
        el.click()

        # 如果提示是否退出，选择确定
        methodpackage.wait_xPathMsg_click_idButton(
            self.driver,
            "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
            "/android.widget.LinearLayout/android.widget.LinearLayout",
            "com.tencent.mm:id/akt",
            2,
            u'退出这次编辑',
            True)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'确定退出'

        self.assertEqual(True, self.find_toast(self.driver, u'分享取消'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"分享取消，验证提示信息正确"
        # 点击分享按钮
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_share")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"点击分享"
        # 点击QQ空间按钮，分享到QQ空间
        el = self.driver.find_element_by_xpath("//android.widget.TextView[@text='QQ空间']")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"分享到QQ空间"
        # 点击输入框
        el = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]"
            "/android.widget.ScrollView/android.widget.LinearLayout/android.widget.EditText")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"点击输入框"
        # 输入内容
        x = "iPhone8"
        el.send_keys(x)
        el.send_keys(u"真心贵")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"输入iPhone8真心贵"
        el.clear()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"清除输入内容"
        # 点击取消按钮，取消分享到QQ空间
        el = self.driver.find_element_by_id("com.tencent.mobileqq:id/ivTitleBtnLeftButton")
        el.click()
        self.assertEqual(True, self.find_toast(self.driver, u'分享取消'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"分享取消，验证提示信息正确"

    # 直播频道节目单查看
    def test_0017_liveplay_epg(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   直播频道节目单查看：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'

        # 播放一个节目
        try:
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")
            name = el.text
        except Exception:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道'
            return
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

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

        # 找到全屏按钮，判断按钮是否存在，存在则直接点，不存在则点播放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_expand",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击全屏'

        # 找到节目按钮，判断按钮是否存在，存在则直接点，不存在则点播放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/text_epg",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        el.click()

        # epg列表
        els = self.driver.find_elements_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
            "/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout"
            "/android.widget.TextView")
        tempFile = os.path.join(methodpackage.currentDir, "temp1.png")  # 截图使用图片
        today = 0
        count = 0

        # 判断“今天”焦点置亮
        for i in range(len(els)):
            date_week = els[i].text.split("\n")[0]
            if date_week == u'今天':
                today = i
                methodpackage.get_screenshot_by_element(self.driver, els[i], tempFile)
                count = int(methodpackage.getimage_color_epg(methodpackage.load_image(tempFile), selectedColor))
                break
        self.assertGreater(count, 0)
        self.assertEqual(els[today].text.split("\n")[0], u'今天')
        self.assertEqual(els[today].text.split("\n")[1], strftime("%m.%d", gmtime()))

        # 遍历epg按钮
        els = self.driver.find_elements_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
            "/android.widget.LinearLayout/android.support.v4.view.ViewPager/android.widget.ListView"
            "/android.widget.LinearLayout/android.widget.ImageView")
        tempFile1 = os.path.join(methodpackage.currentDir, "temp.png")  # 截图使用图片
        # print len(els)
        for j in range(len(els) - 2):
            # print j
            methodpackage.get_screenshot_by_element(self.driver, els[j + 1], tempFile1)
            count = int(methodpackage.getimage_greater(methodpackage.load_image(tempFile1), 200))
            # print u'白色像素点：', count
            if 200 < count < 260:
                print u'回看图标白色像素：', count
                continue
            elif count == 0:
                print u'播放图标白色像素：', count
                if j == len(els) - 3:
                    break
            else:
                print u'预约图标白色像素：', count
                self.assertLess(count, 440)
                self.assertGreater(count, 380)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'当天时移、播放、预约按钮都存在'
        methodpackage.swipeRight_fullright(self.driver, 500)
        # 遍历epg按钮
        els = self.driver.find_elements_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
            "/android.widget.LinearLayout/android.support.v4.view.ViewPager/android.widget.ListView"
            "/android.widget.LinearLayout/android.widget.ImageView")
        for j in range(len(els) - 2):
            methodpackage.get_screenshot_by_element(self.driver, els[j + 1], tempFile1)
            count = int(methodpackage.getimage_greater(methodpackage.load_image(tempFile1), 200))
            self.assertLess(count, 260)
            self.assertGreater(count, 200)
            print u'回看图标白色像素：', count
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'昨天回看按钮都存在'
        methodpackage.swipeLeft_fullright(self.driver, 500)
        sleep(1)
        methodpackage.swipeLeft_fullright(self.driver, 500)
        # 遍历epg按钮
        els = self.driver.find_elements_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout"
            "/android.widget.LinearLayout/android.support.v4.view.ViewPager/android.widget.ListView"
            "/android.widget.LinearLayout/android.widget.ImageView")
        for j in range(len(els) - 2):
            methodpackage.get_screenshot_by_element(self.driver, els[j + 1], tempFile1)
            count = int(methodpackage.getimage_greater(methodpackage.load_image(tempFile1), 200))
            self.assertLess(count, 440)
            self.assertGreater(count, 380)
            print u'预约图标白色像素：', count
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'明天预约按钮都存在'

    # 直播录制功能
    def test_0018_liveplay_record(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   直播录制功能：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'

        # 播放一个节目
        try:
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")
            name = el.text
        except Exception:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道'
            return
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(
                self.driver, 5).until_not(lambda x: x.find_element_by_id(
                "com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 找到全屏按钮，判断按钮是否存在，存在则直接点，不存在则点播放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_expand",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击全屏'

        action = TouchAction(self.driver)
        # 找到录屏按钮，判断按钮是否存在，存在则直接点，不存在则点播放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/ald_record_gif",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View")
        action.long_press(el, duration=2000).perform()

        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/lgs_share_qq')
        self.assertIsNotNone(el1)
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/lgs_share_wechat')
        self.assertIsNotNone(el2)

        el1.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"分享到QQ"
        # 点击“我的电脑”按钮，分享到我的电脑
        el = self.driver.find_element_by_xpath(
            "//android.widget.AbsListView[@content-desc=\" \"]/android.widget.RelativeLayout[2]")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"分享到“我的电脑”"
        # 点击取消按钮，取消分享到我的电脑
        el = self.driver.find_element_by_id("com.tencent.mobileqq:id/dialogLeftBtn")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"取消分享到“我的电脑”"
        # 点击“我的电脑”按钮，分享到我的电脑
        el = self.driver.find_element_by_xpath(
            "//android.widget.AbsListView[@content-desc=\" \"]/android.widget.RelativeLayout[2]")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"分享到“我的电脑”"
        # 点击发送按钮，分享到我的电脑
        el = self.driver.find_element_by_id("com.tencent.mobileqq:id/dialogRightBtn")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"选择发送"
        # 点击“返回好看宽屏”按钮，回到谷豆TV
        el = self.driver.find_element_by_id("com.tencent.mobileqq:id/dialogLeftBtn")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"选择回到“谷豆TV”"

    # 音量调节功能
    def test_0019_liveplay_voice(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   音量调节功能：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'

        # 播放一个节目
        try:
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")
            name = el.text
        except Exception:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道'
            return
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

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

        for i in range(5):
            sleep(1)
            self.driver.press_keycode(24)

        for i in range(5):
            sleep(1)
            self.driver.press_keycode(25)

        # 找到全屏按钮，判断按钮是否存在，存在则直接点，不存在则点播放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_expand",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击全屏'

        methodpackage.swipeUp_right(self.driver, 500)
        sleep(1)
        methodpackage.swipeDown_right(self.driver, 500)
        sleep(1)
        # methodpackage.swipeMid_right(self.driver, 500)

    # 时移进度调整，时移回直播功能
    def test_0020_liveplay_setstime(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   时移进度调整，时移回直播：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'

        # 播放一个节目
        try:
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")
            name = el.text
        except Exception:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道'
            return
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 10).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 初始化播放进度条
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/progress",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        size = el.size
        height = size["height"]
        width = size["width"]
        local = el.location
        x = local["x"]
        y = local["y"]

        self.driver.swipe(x + height / 2, y + height / 2, x + width, y + height / 2, 800)
        self.assertEqual(True, self.find_toast(self.driver, u'节目尚未播放'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'向右拖动进度条'
        sleep(2)

        # 获取当前播放进度
        firsttime = self.getplay_time_live(self.driver)[2]
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'当前播放进度：', firsttime
        self.assertEqual(firsttime, u'直播')

        sleep(10)

        # 拖动播放进度条
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/progress",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        self.driver.swipe(x + width - height / 2, y + height / 2, x + height / 2, y + height / 2, 800)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'向左拖动进度条'

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 10).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 获取当前播放时间
        temp = self.getplay_time_live(self.driver)
        secondtime = temp[2]
        starttime = temp[0]
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'当前播放进度：', secondtime
        self.assertEqual(secondtime, starttime)
        sleep(10)

        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/progress",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )

        self.driver.swipe(x + height / 2, y + height / 2, x + width, y + height / 2, 800)
        self.assertEqual(True, self.find_toast(self.driver, u'进入直播'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'向右拖动进度条'

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 5).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 获取当前播放时间
        thirdtime = self.getplay_time_live(self.driver)[2]
        self.assertEqual(thirdtime, u'直播')
        sleep(3)

    # 频道回看功能，回看进度调整
    def test_0021_liveplay_review(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   频道回看功能，回看进度调整：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'

        # 播放一个节目
        try:
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")
            name = el.text
        except Exception:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道'
            return
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 5).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 划动epg列表
        methodpackage.swipeRight_low(self.driver, 500)
        
        # 获取回看按钮
        try:
            self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/live_tvEpg_flag")
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有回看epg'
            self.assertTrue(False)
        els = self.driver.find_elements_by_id("com.sumavision.sanping.gudou:id/live_tvEpg_flag")
        els[3].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放回看'

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 5).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 获取当前播放进度
        firsttime = self.getplay_time_vod(self.driver)

        # 初始化播放进度条
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/progress",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        size = el.size
        height = size["height"]
        width = size["width"]
        local = el.location
        x = local["x"]
        y = local["y"]
        self.driver.swipe(x + height / 2, y + height / 2, x + width / 2, y + height / 2, 800)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'向右拖动进度条'

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 5).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 获取当前播放时间
        secondtime = self.getplay_time_vod(self.driver)
        self.assertGreater(secondtime, firsttime)

        # 拖动播放进度条
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/progress",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        self.driver.swipe(x + width / 2, y + height / 2, x + width * 2 / 3, y + height / 2, 800)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'向右拖动进度条'

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 5).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 获取当前播放时间
        thirdtime = self.getplay_time_vod(self.driver)
        self.assertGreater(thirdtime, secondtime)

        self.driver.swipe(x + width * 2 / 3, y + height / 2, x + width / 4, y + height / 2, 800)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'向左拖动进度条'

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 5).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 获取当前播放时间
        fourthtime = self.getplay_time_vod(self.driver)
        self.assertGreater(thirdtime, fourthtime)
        sleep(3)

    # 直播聊天室功能
    def test_0022_liveplay_chatroom(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   直播聊天室功能：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'

        # 播放一个节目
        try:
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")
            name = el.text
        except Exception:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道'
            return
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

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

        el1 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/chat_num')
        prenums = int(el1.text.split(u'人')[0])
        # print prenums
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/enter_chat')
        el2.click()
        sleep(2)
        postnums = int(el1.text.split(u'人')[0])
        # print postnums
        self.assertLess(prenums, postnums)

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/edit_com')
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"点击输入框"
        # 输入内容
        x = u"你好"

        # print self.sh('adb shell ime list -s')
        self.sh('adb shell ime set com.baidu.input_huawei/.ImeService')
        sleep(1)
        el.send_keys(x)
        sleep(1)
        action = TouchAction(self.driver)
        action.tap(x=987, y=1692).perform()
        # self.sh('adb shell ime set io.appium.android.ime/.UnicodeIME')
        sleep(2)

    # 直播频道播放退出
    def test_0023_liveplay_quit(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   直播频道播放退出：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'

        # 播放一个节目
        try:
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")
            name = el.text
        except Exception:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道'
            return
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

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

        # 点击播放器的返回按钮，判断按钮是否存在，存在则直接点，不存在则点播放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_back_header",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'回到直播列表'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")
        self.assertIsNotNone(el)

    # 屏幕自动旋转功能
    def test_0024_liveplay_autoturn(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   屏幕自动旋转功能：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'

        # 播放一个节目
        try:
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tvName")
            name = el.text
        except Exception:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'该分类没有频道'
            return
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

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

        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), self.driver.orientation

        try:
            self.driver.orientation ='LANDSCAPE'
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'切换横屏成功'
        except:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'切换横屏失败'
            # 找到全屏按钮，判断按钮是否存在，存在则直接点，不存在则直播放器显示出按钮
            el = methodpackage.find_elementId_conditionXpath(
                self.driver,
                "com.sumavision.sanping.gudou:id/img_expand",
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View")
            el.click()
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击全屏'

        # 切换手机旋转
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), self.driver.orientation
        try:
            self.driver.orientation ='PORTRAIT'
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'切换竖屏成功'
        except:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'切换竖屏失败'

    # 直播节目搜索
    def test_0025_liveplay_search(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   直播节目搜索：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“直播”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_live")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入直播'

        # 进入搜索页面
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_search")
        el.click()

        # 搜索存在的
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/edt_keyword")
        el.click()
        el.clear()
        el.send_keys('CCTV')
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'搜索"CCTV"'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_search")
        el.click()

        # 显示直播搜索结果，并且计算搜索结果的个数
        searchs = 0
        try:
            el = self.driver.find_element_by_id(
                "com.sumavision.sanping.gudou:id/search_channel_more_iv"
            )
            el.click()
        except:
            pass
        els = self.driver.find_elements_by_xpath("//android.widget.GridView//android.widget.TextView")
        searchs = searchs + len(els)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'搜索到节目数量至少为：', searchs
        self.assertTrue(searchs)

        # 搜索不存在的
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/edt_keyword")
        el.click()
        el.send_keys("not exitst")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'搜索不存在直播节目'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_search")
        el.click()
        sleep(2)

        # 显示直播搜索结果，并且计算搜索结果的个数
        searchs = 0
        try:
            els = self.driver.find_elements_by_xpath("//android.widget.GridView//android.widget.TextView")
            searchs = searchs + len(els)
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'搜索到节目数量：', str(len(els))
        except:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'搜索到节目数量：', str(searchs)
        self.assertFalse(searchs)

        # 搜索超长字符串
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/edt_keyword")
        el.click()
        el.clear()
        myChars = 'adbefghigk' * 100
        el.send_keys(myChars)

        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'搜索不存在直播节目'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_search")
        el.click()
        sleep(2)

        # 显示直播搜索结果，并且计算搜索结果的个数
        searchs = 0
        try:
            els = self.driver.find_elements_by_xpath("//android.widget.GridView//android.widget.TextView")
            searchs = searchs + len(els)
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'搜索到节目数量：', str(len(els))
        except:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'搜索到节目数量：', str(searchs)
        self.assertFalse(searchs)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
