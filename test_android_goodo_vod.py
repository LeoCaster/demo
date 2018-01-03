#-*-coding:utf-8-*-

import os
import random
import string
import time
import methodpackage
from time import sleep
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.mobileby import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import unittest



# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

selectedColor = (253, 130, 0)
background = (255, 255, 255)
postplay = (238, 237, 241)
defaultpost = (239, 239, 239)
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
        # desired_caps['platformVersion'] = '4.2'
        # desired_caps['deviceName'] = 'YPOV95LJ99999999'
        # desired_caps['deviceName'] = '351BBHGE53V3'
        desired_caps['deviceName'] = 'XPUDU17303004497'
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
            WebDriverWait(driver, 1).until(
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

    def getplay_time(self, driver):
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

    # 查看片库页面显示情况
    def test_0002_vodpage(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   查看片库页面显示情况：开始'
        # 启动弹框处理
        self.App_Start(self.driver)

        # 隐式等待
        self.driver.implicitly_wait(3)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'

        tempfile = os.path.join(methodpackage.currentDir, 'temp.png')  # 截图使用图片

        # 判断默认落焦综艺娱乐
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_vod_tab_text')
        self.assertTrue(els[0].get_attribute('selected'))
        methodpackage.get_screenshot_by_element(self.driver, els[0], tempfile)
        count = methodpackage.getimage_color_original(methodpackage.load_image(tempfile), selectedColor)
        self.assertGreater(count, 0)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'默认落焦“综艺娱乐”'

        # 判断筛选条件元素
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/filter_year')
        el2.click()
        # els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/name')
        # self.assertGreater(len(els2), 0)
        el2.click()

        el3 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/filter_locale')
        el3.click()
        # els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/name')
        # self.assertGreater(len(els2), 0)
        el3.click()

        el4 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/filter_category')
        el4.click()
        # els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/name')
        # self.assertGreater(len(els2), 0)
        el4.click()

        el5 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/filter_sorting')
        el5.click()
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/vod_new_txt')
        methodpackage.get_screenshot_by_element(self.driver, el, tempfile)
        self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(tempfile)), selectedColor)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'控件"最新"置亮'
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/vod_hot_txt')
        self.assertIsNotNone(el)
        el5.click()

        # 判断默认海报的像素点个数，差不多170个为一张默认海报的像素点个数
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/gridview")
        methodpackage.get_screenshot_by_element(self.driver, el, tempfile)
        count = int(methodpackage.getimage_color(methodpackage.load_image(tempfile), defaultpost))

        # print count
        if count > 20:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'有海报缺失'
        else:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'海报显示正常'

        # 滑到底
        while True:
            methodpackage.swipeUp(self.driver, 400)
            if self.find_toast(self.driver, u'没有更多节目了'):
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'滑到底了'
                break

        # 判断默认海报的像素点个数，差不多170个为一张默认海报的像素点个数
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/gridview")
        methodpackage.get_screenshot_by_element(self.driver, el, tempfile)
        count = int(methodpackage.getimage_color(methodpackage.load_image(tempfile), defaultpost))
        # print count
        if count > 20:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'有海报缺失'
        else:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'海报显示正常'

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_vod_tab_text')
        for i in range(1, len(els)):
            methodpackage.swipeLeft(self.driver, 500)
            self.assertTrue(els[i].get_attribute('selected'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'栏目切换正常'

    # 切换片库栏目分类
    def test_0003_vodCategory(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   切换片库栏目分类：开始'

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'

        tempfile = os.path.join(methodpackage.currentDir, 'temp.png')  # 截图使用图片

        # 判断默认落焦资讯
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_vod_tab_text')
        self.assertTrue(els[0].get_attribute('selected'))
        methodpackage.get_screenshot_by_element(self.driver, els[0], tempfile)
        count = methodpackage.getimage_color_original(methodpackage.load_image(tempfile), selectedColor)
        self.assertGreater(count, 0)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'默认落焦“综艺娱乐”'

        # 获取当前显示的栏目
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_vod_tab_text')
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'获取片库栏目' ,\
            str(len(els))

        # 点击每个栏目测试
        firstVodName = ''
        for i in range(len(els)):
            if 'false' == els[i].get_attribute('selected'):
                els[i].click()
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击栏目', els[i].text

            self.assertTrue(els[i].get_attribute('selected'))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击栏目', els[i].text, u'成功'

            els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/textView1')
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'栏目', els[i].text, \
                u'第一个节目是', els2[0].text
            self.assertNotEqual(firstVodName, els2[0].text)
            firstVodName = els2[0].text[:]

            # 栏目片库节目滑动
            methodpackage.swipeUp(self.driver, 500)
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'滑动栏目：', els[i].text

            els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/textView1')
            if firstVodName == els2[0].text[:]:
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'栏目', els[i].text, \
                    u'节目不超过一屏'
            else:
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'栏目', els[i].text, u'滑动成功'

            # 判断默认海报的像素点个数，差不多170个为一张默认海报的像素点个数
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/gridview")
            methodpackage.get_screenshot_by_element(self.driver, el, tempfile)
            count = int(methodpackage.getimage_color(methodpackage.load_image(tempfile), defaultpost))
            # print count
            if count > 20:
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'有海报缺失'
            else:
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'海报显示正常'

    #  片库节目播放
    def test_0004_vodplay(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   片库节目播放：开始'

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'
        sleep(0.5)

        # 播放一个节目
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
        name = el.text
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 5).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tv_info')
        self.assertEqual(name, el.text)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放成功'

    # 片库节目播放时切换到手机桌面后再次进入应用时播放暂停
    def test_0005_vodPlay_home_pause_ster(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), \
            u'  片库节目播放时切换到手机桌面后再次进入应用：开始'

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'
        sleep(0.5)

        # 播放一个节目
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
        name = el.text
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name
        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 10).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        first = self.getplay_time_vod(self.driver)

        #  Home 5秒钟再进入应用
        self.driver.background_app(5)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击home5秒，进入应用'
        sleep(5)
        second = self.getplay_time_vod(self.driver)
        self.assertGreaterEqual(second, first)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'继续播放视频'

    # 片库节目播放断网重连续播
    def test_0006_vodPlay_network_off_on(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u' 片库节目播放断网重连续播：开始'

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'
        sleep(0.5)

        # 播放一个节目
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
        name = el.text
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 10).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        self.driver.set_network_connection(1)
        sleep(5)
        self.driver.set_network_connection(6)
        sleep(15)
        tempFile = os.path.join(methodpackage.currentDir, "temp.png")  # 截图使用图片
        tempFile1 = os.path.join(methodpackage.currentDir, "temp1.png")
        el = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        methodpackage.get_screenshot_by_element(self.driver, el, tempFile)
        sleep(10)
        el = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        methodpackage.get_screenshot_by_element(self.driver, el, tempFile1)
        self.assertFalse(methodpackage.image_same_as(tempFile1, tempFile, 0.7))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'继续播放视频'

    # wifi切换到4G网时节目正常播放
    def test_0007_vodPlay_wifi_to_4G(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u' wifi切换到4G网时节目正常播放：开始'

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'
        sleep(0.5)

        # 播放一个节目
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
        name = el.text
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 10).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        if self.driver.network_connection != 2 and self.driver.network_connection != 6:
            self.driver.set_network_connection(2)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'网络为Wifi状态'

        sleep(10)
        self.driver.set_network_connection(4)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'切换网络为4G状态'
        tempFile = os.path.join(methodpackage.currentDir, "temp.png")  # 截图使用图片
        tempFile1 = os.path.join(methodpackage.currentDir, "temp1.png")

        # 如果提示更新，放弃更新应用
        methodpackage.wait_xPathMsg_click_idButton(
            self.driver,
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.TextView[1]",
            "com.sumavision.sanping.gudou:id/btnOK",
            20,
            u'应用更新',
            False)

        el = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        methodpackage.get_screenshot_by_element(self.driver, el, tempFile)
        sleep(30)
        el = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        methodpackage.get_screenshot_by_element(self.driver, el, tempFile1)
        self.assertFalse(methodpackage.image_same_as(tempFile1, tempFile, 0.7))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'继续播放视频'
        self.driver.set_network_connection(6)

    # 4G切换到wifi网时节目正常播放
    def test_0008_vodPlay_4G_to_wifi(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u' wifi切换到4G网时节目正常播放：开始'

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'
        sleep(0.5)

        # 播放一个节目
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
        name = el.text
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 10).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        if self.driver.network_connection != 4 :
            self.driver.set_network_connection(4)
            sleep(10)
            # 如果提示更新，放弃更新应用
            methodpackage.wait_xPathMsg_click_idButton(
                self.driver,
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout"
                "/android.widget.TextView[1]",
                "com.sumavision.sanping.gudou:id/btnOK",
                20,
                u'应用更新',
                False)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'网络为4G状态'

        sleep(20)
        self.driver.set_network_connection(2)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'切换网络为wifi状态'
        tempFile = os.path.join(methodpackage.currentDir, "temp.png")  # 截图使用图片
        tempFile1 = os.path.join(methodpackage.currentDir, "temp1.png")

        el = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        methodpackage.get_screenshot_by_element(self.driver, el, tempFile)
        sleep(30)
        el = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View"
        )
        methodpackage.get_screenshot_by_element(self.driver, el, tempFile1)
        self.assertFalse(methodpackage.image_same_as(tempFile1, tempFile, 0.7))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'继续播放视频'
        self.driver.set_network_connection(6)

    # 节目播放时手机来电后可以恢复播放
    def test_0009_vodPlay_inCall(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   节目播放时手机来电后可以恢复播放无法实现：开始'

    # 片库节目续播
    def test_0010_vodplay_stop_contimue(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   片库节目续播：开始'

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'
        sleep(0.5)

        # 播放一个节目
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
        name = el.text
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
        el = methodpackage.find_elementXpath_conditionXpath(
            self.driver,
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout[2]/android.widget.LinearLayout"
            "/android.widget.SeekBar",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        size = el.size
        height = size["height"]
        width = size["width"]
        local = el.location
        x = local["x"]
        y = local["y"]
        self.driver.swipe(x+width, y + height / 2, x, y + height / 2, 800)
        sleep(10)

        # 拖动播放进度条
        el = methodpackage.find_elementXpath_conditionXpath(
            self.driver,
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout[2]/android.widget.LinearLayout"
            "/android.widget.SeekBar",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        self.driver.swipe(x, y + height / 2, x + width/2, y + height / 2, 800)
        sleep(10)

        # 获取当前播放进度
        first = self.getplay_time_vod(self.driver)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'当前播放时间（换算成秒为单位）', first

        # 退出播放
        self.driver.back()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'退出播放'

        # 播放一个节目
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/textView1')
        name = els[0].text
        els[0].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 10).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 判断续播时间
        second = self.getplay_time_vod(self.driver)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'当前播放时间（换算成秒为单位）', second
        self.assertTrue(second - first < 20)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'续播成功'

    # 查看电影类节目详情页面显示情况
    def test_0011_vodplay_movieinfo(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   查看电影类节目详情页面显示情况：开始'

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'

        # 进入电影
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_vod_tab_text')
        column = els[2].text
        els[2].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入:', column
        sleep(0.5)

        # 播放一个节目
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
        name = el.text
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 10).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_fav")
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'收藏按钮正常'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_share")
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'分享按钮正常'

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/img_enter_vod_cache')
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'缓存按钮正常'

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tv_report')
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'举报按钮正常'

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/img_info_more')
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'更多节目信息按钮正常'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tv_info")
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), el.text

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tv_director")
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), el.text

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tv_actor_title")
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), el.text

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tv_actors")
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), el.text

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tv_region")
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), el.text

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tv_type")
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), el.text

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tv_des")
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), el.text

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/image_comment')
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'评论按钮正常'

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/edit_comment')
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'评论输入框正常'

        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'节目详情正常'

        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_back_header",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'退出按钮正常'

    # 查看剧集类节目详情页面显示情况
    def test_0012_vodplay_episodeinfo(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   查看剧集类节目详情页面显示情况：开始'

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'

        # 进入电视剧
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_vod_tab_text')
        column = els[1].text
        els[1].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入:', column
        sleep(0.5)

        # 播放一个节目
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
        name = el.text
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 10).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_fav")
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'收藏按钮正常'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_share")
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'分享按钮正常'

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/img_enter_vod_cache')
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'缓存按钮正常'

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/tv_report')
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'举报按钮正常'

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/img_info_more')
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'更多节目信息按钮正常'

        # 查看剧集类节目信息
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tv_info")
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), el.text

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tv_director")
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), el.text

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tv_actor_title")
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), el.text

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tv_actors")
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), el.text

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/img_info_more')
        el.click()

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tv_region")
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), el.text

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tv_type")
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), el.text

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/tv_des")
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), el.text

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/image_comment')
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'评论按钮正常'

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/edit_comment')
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'评论输入框正常'

        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/img_info_more')
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'节目详情正常'

    # 查看剧集类节目详情页面显示情况
    def test_0013_vodplay_playepisode(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   查看剧集类节目详情页面显示情况：开始'

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
        while len(els) > 0:
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
        self.driver.back()
        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'

        # 进入电视剧
        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_vod_tab_text')
        column = els[1].text
        els[1].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入:', column
        sleep(0.5)
        methodpackage.swipeDown(self.driver, 500)

        # 播放一个节目
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
        name = el.text
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 15).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 滑动剧集详情页面，显示全部剧集信息
        x = methodpackage.getSize(self.driver)[0]
        y = methodpackage.getSize(self.driver)[1]
        methodpackage.moveTo(self.driver, x/2, y * 24/32, x/2, y * 19/32)
        lis = []
        lis2 = []
        els = self.driver.find_elements_by_xpath(
            '//android.widget.HorizontalScrollView/android.widget.LinearLayout/android.widget.LinearLayout'
            '/android.widget.TextView')
        long1 = len(els)
        items = 0
        temp1 = os.path.join(methodpackage.currentDir, "temp1.png")  # 截图使用图片
        temp2 = os.path.join(methodpackage.currentDir, "temp2.png")  # 截图使用图片
        temp3 = os.path.join(methodpackage.currentDir, "temp3.png")  # 截图使用图片
        for i in range(long1):
            s = str(els[i].text)
            # print s
            int1 = int(s.split('-')[0])
            int2 = int(s.split('-')[1])
            lis.append(int1)
            lis2.append(int2)
            els = self.driver.find_elements_by_xpath(
                '//android.widget.HorizontalScrollView/android.widget.LinearLayout/android.widget.LinearLayout'
                '/android.widget.TextView')
            els[i].click()
            sleep(1)
            item_els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_episode_name')
            long2 = len(item_els)
            items = items + long2
            if lis2[i] == items:
                for j in range(long2):
                    # print len(item_els)
                    if j == 0:
                        if i == 0:
                            name = item_els[j].text
                            sleep(5)
                            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放', name
                            methodpackage.get_screenshot_by_element(self.driver, item_els[j], temp1)
                            self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(temp1)),
                                             selectedColor)
                            methodpackage.get_screenshot_by_element(self.driver, item_els[j + 1], temp2)
                            self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(temp2)), background)
                        else:
                            item_els[j].click()
                            name = item_els[j].text
                            sleep(5)
                            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放', name
                            methodpackage.get_screenshot_by_element(self.driver, item_els[j], temp1)
                            self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(temp1)),
                                             selectedColor)
                            methodpackage.get_screenshot_by_element(self.driver, item_els[j + 1], temp2)
                            self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(temp2)), background)
                    elif j == len(item_els) - 1:
                        item_els[j].click()
                        name = item_els[j].text
                        sleep(5)
                        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放', name
                        methodpackage.get_screenshot_by_element(self.driver, item_els[j], temp1)
                        self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(temp1)), selectedColor)
                        methodpackage.get_screenshot_by_element(self.driver, item_els[j - 1], temp2)
                        self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(temp2)), postplay)
                    else:
                        item_els[j].click()
                        name = item_els[j].text
                        sleep(5)
                        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放', name
                        methodpackage.get_screenshot_by_element(self.driver, item_els[j - 1], temp1)
                        self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(temp1)), postplay)
                        methodpackage.get_screenshot_by_element(self.driver, item_els[j], temp2)
                        self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(temp2)), selectedColor)
                        methodpackage.get_screenshot_by_element(self.driver, item_els[j + 1], temp3)
                        self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(temp3)), background)
            else:
                for j in range(long2 - 1):
                    # print len(item_els)
                    if j == 0:
                        if i == 0:
                            name = item_els[j].text
                            sleep(5)
                            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放', name
                            methodpackage.get_screenshot_by_element(self.driver, item_els[j], temp1)
                            self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(temp1)),
                                             selectedColor)
                            methodpackage.get_screenshot_by_element(self.driver, item_els[j + 1], temp2)
                            self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(temp2)),
                                             background)
                        else:
                            item_els[j].click()
                            name = item_els[j].text
                            sleep(5)
                            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放', name
                            methodpackage.get_screenshot_by_element(self.driver, item_els[j], temp1)
                            self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(temp1)),
                                             selectedColor)
                            methodpackage.get_screenshot_by_element(self.driver, item_els[j + 1], temp2)
                            self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(temp2)),
                                             background)
                    else:
                        item_els[j].click()
                        name = item_els[j].text
                        sleep(5)
                        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放', name
                        methodpackage.get_screenshot_by_element(self.driver, item_els[j - 1], temp1)
                        self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(temp1)), postplay)
                        methodpackage.get_screenshot_by_element(self.driver, item_els[j], temp2)
                        self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(temp2)),
                                         selectedColor)
                        methodpackage.get_screenshot_by_element(self.driver, item_els[j + 1], temp3)
                        self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(temp3)), background)
                for k in range(lis2[i] - lis[i] - long2 + 1):
                    x = methodpackage.getSize(self.driver)[0]
                    y = methodpackage.getSize(self.driver)[1]
                    methodpackage.moveTo(self.driver, x / 2, y * 24 / 32, x / 2, y * 21 / 32)
                    item_els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_episode_name')
                    item_els[-2].click()
                    name = item_els[-2].text
                    sleep(5)
                    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放', name
                    methodpackage.get_screenshot_by_element(self.driver, item_els[-3], temp1)
                    self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(temp1)), postplay)
                    methodpackage.get_screenshot_by_element(self.driver, item_els[-2], temp2)
                    self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(temp2)), selectedColor)
                    methodpackage.get_screenshot_by_element(self.driver, item_els[-1], temp3)
                    self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(temp3)), background)

                item_els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_episode_name')
                item_els[-1].click()
                name = item_els[-1].text
                sleep(5)
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放', name
                methodpackage.get_screenshot_by_element(self.driver, item_els[-1], temp1)
                self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(temp1)), selectedColor)
                methodpackage.get_screenshot_by_element(self.driver, item_els[-2], temp2)
                self.assertEqual(methodpackage.get_dominant_color(methodpackage.load_image(temp2)), postplay)
                methodpackage.swipeDown_low(self.driver, 500)

        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'剧集数量：', str(items)

        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_back_header",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View"
        )
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'退出按钮正常'

    # 查看片库节目播放进度
    def test_0014_vodplay_process(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   查看片库节目播放进度：开始'

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'
        sleep(0.5)
        methodpackage.swipeDown(self.driver, 500)

        # 播放一个节目
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
        name = el.text
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 10).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 判断续播时间
        first = self.getplay_time_vod(self.driver)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'当前播放时间（换算成秒为单位）', first

        # 退出播放
        self.driver.back()

    # 片库节目播放暂停/片库节目播放恢复
    def test_0015_vodplay_pause(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   片库节目播放暂停/片库节目播放恢复：开始'

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'
        sleep(0.5)
        methodpackage.swipeDown(self.driver, 500)

        # 播放一个节目
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
        name = el.text
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 10).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 暂停
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_ctrl_small_play",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'暂停播放'

        sleep(10)

        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_ctrl_small_play",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'恢复播放'
        sleep(10)

    # 片库节目全屏播放功能
    def test_0016_vodplay_fullscreen(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   片库节目全屏播放功能：开始'

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'
        sleep(0.5)
        methodpackage.swipeDown(self.driver, 500)

        # 播放一个节目
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
        name = el.text
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 10).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 找到全屏按钮，判断按钮是否存在，存在则直接点，不存在则片库放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_expand",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击全屏'
        sleep(10)

        # 找到返回按钮，判断按钮是否存在，存在则直接点，不存在则片库放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_back_header",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'退出全屏播放'

        # 找到全屏按钮，判断按钮是否存在，存在则直接点，不存在则片库放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_expand",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击全屏'
        sleep(10)

        # 找到缩屏按钮，判断按钮是否存在，存在则直接点，不存在则片库放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_unexpand",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击缩屏'
        sleep(10)

    # 屏幕自动旋转功能
    def test_0017_vodplay_autoturn(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   屏幕自动旋转功能：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'
        sleep(0.5)
        methodpackage.swipeDown(self.driver, 500)

        # 播放一个节目
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
        name = el.text
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 10).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 找到全屏按钮，判断按钮是否存在，存在则直接点，不存在则片库放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_expand",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击全屏'

        # 切换手机旋转
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), self.driver.orientation
        try:
            self.driver.orientation ='PORTRAIT'
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'切换竖屏成功'
        except:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'切换竖屏失败'

    # 屏幕锁定功能
    def test_0018_vodplay_lockscreen(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   屏幕锁定功能：开始'

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'
        sleep(0.5)
        methodpackage.swipeDown(self.driver, 500)

        # 播放一个节目
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
        name = el.text
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 10).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 找到全屏按钮，判断按钮是否存在，存在则直接点，不存在则片库放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_expand",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击全屏'

        # 点击锁屏按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_lock_vod",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'锁定全屏'
        sleep(10)

        el = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        el.click()
        els = self.driver.find_elements_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/*")
        self.assertLessEqual(len(els), 3)

        # 退出锁屏
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_lock_vod",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        el.click()
        sleep(10)

    # 片库录制功能
    def test_0019_vodplay_record(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   片库录制功能：开始'

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'
        sleep(0.5)
        methodpackage.swipeDown(self.driver, 500)

        # 播放一个节目
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
        name = el.text
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 10).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 找到全屏按钮，判断按钮是否存在，存在则直接点，不存在则片库放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_expand",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击全屏'

        action = TouchAction(self.driver)
        # 找到录屏按钮，判断按钮是否存在，存在则直接点，不存在则点播放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/vpt_record_gif",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
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

    # 播放速度切换功能
    def test_0020_vodplay_speed(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   播放速度切换功能：开始'

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'
        sleep(0.5)
        methodpackage.swipeDown(self.driver, 500)

        # 播放一个节目
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
        name = el.text
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 10).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 找到全屏按钮，判断按钮是否存在，存在则直接点，不存在则片库放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_expand",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击全屏'

        tempfile = os.path.join(methodpackage.currentDir, 'temp.png')
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/player_speed",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        methodpackage.get_screenshot_by_element(self.driver, el, tempfile)
        el.click()
        count = methodpackage.getimage_color_original(methodpackage.load_image(tempfile), background)
        # print u'正常速度', count
        self.assertEqual(count, 0)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'切换到1.5倍速'

        sleep(5)

        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/player_speed",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        methodpackage.get_screenshot_by_element(self.driver, el, tempfile)
        el.click()
        count = methodpackage.getimage_color_original(methodpackage.load_image(tempfile), background)
        # print u'1.5倍速度', count
        self.assertGreater(count, 95)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'切换到2倍速'
        sleep(5)

        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/player_speed",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        methodpackage.get_screenshot_by_element(self.driver, el, tempfile)
        el.click()
        count = methodpackage.getimage_color_original(methodpackage.load_image(tempfile), background)
        # print u'2倍速度', count
        self.assertGreater(count, 55)
        self.assertLess(count, 70)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'切换到正常速度'
        sleep(2)

    # 音量调节功能
    def test_0021_vodplay_voice(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   音量调节功能：开始'

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'
        sleep(0.5)
        methodpackage.swipeDown(self.driver, 500)

        # 播放一个节目
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
        name = el.text
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 10).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        for i in range(5):
            sleep(1)
            self.driver.press_keycode(24)

        for i in range(5):
            sleep(1)
            self.driver.press_keycode(25)

    # 播放进度调整功能
    def test_0022_vodplay_setstime(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   播放进度调整：开始'

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'
        sleep(0.5)
        methodpackage.swipeDown(self.driver, 500)

        # 播放一个节目
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
        name = el.text
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
        el = methodpackage.find_elementXpath_conditionXpath(
            self.driver,
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout[2]/android.widget.LinearLayout"
            "/android.widget.SeekBar",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        size = el.size
        height = size["height"]
        width = size["width"]
        local = el.location
        x = local["x"]
        y = local["y"]
        self.driver.swipe(x+width, y + height / 2, x, y + height / 2, 800)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'初始化播放进度条'

        # 获取当前播放进度
        firstTime = self.getplay_time_vod(self.driver)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放时间是：',str(firstTime)
        sleep(10)

        # 向右拖动进度条
        el = methodpackage.find_elementXpath_conditionXpath(
            self.driver,
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout[2]/android.widget.LinearLayout"
            "/android.widget.SeekBar",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        self.driver.swipe(x, y + height / 2, x + width / 2, y + height / 2, 800)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'向右拖动进度条'

        # 获取当前播放时间
        secondTime = self.getplay_time_vod(self.driver)
        self.assertGreater(secondTime, firstTime)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放时间是：', str(secondTime)
        sleep(10)

        # 拖动播放进度条
        el = methodpackage.find_elementXpath_conditionXpath(
            self.driver,
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.widget.LinearLayout[2]/android.widget.LinearLayout"
            "/android.widget.SeekBar",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        self.driver.swipe(x + width / 2, y + height / 2, x + height / 2, y + height / 2, 800)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'向左拖动进度条'

        # 获取当前播放时间
        ThirdTime = self.getplay_time_vod(self.driver)
        self.assertGreater(secondTime, ThirdTime)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放时间是：', str(ThirdTime)
        sleep(2)

    # 片库节目码率切换功能
    def test_0023_vodplay_resolution(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   片库节目码率切换功能：开始'

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'
        sleep(0.5)
        methodpackage.swipeDown(self.driver, 500)

        # 播放一个节目
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
        name = el.text
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 10).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 找到全屏按钮，判断按钮是否存在，存在则直接点，不存在则片库放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_expand",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击全屏'
        # 找到码率按钮，判断按钮是否存在，存在则直接点，不存在则点播放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/text_setting",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
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
                    "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
                    "/android.widget.FrameLayout/android.view.View")
                el.click()
                els = self.driver.find_elements_by_class_name('android.widget.TextView')

        self.driver.back()

    # 点赞点踩功能
    def test_0024_vodplay_like(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   点赞点踩功能：开始'

        #self.driver.reset()

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'

        like = 0
        not_like = 0
        tempfile1 = os.path.join(methodpackage.currentDir, "temp1.png")  # 截图使用图片
        tempfile2 = os.path.join(methodpackage.currentDir, "temp2.png")  # 截图使用图片
        category_els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_vod_tab_text')
        for n in range(len(category_els)):
            if like and not_like:
                break

            category_els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/tv_vod_tab_text')
            category_els[n].click()

            # 播放一个节目
            el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
            els = self.driver.find_elements_by_id("com.sumavision.sanping.gudou:id/textView1")
            for i in range(len(els)):
                currentName = els[i].text
                els[i].click()
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：',currentName

                # 等待播放加载完成
                try:
                    WebDriverWait(self.driver, 10).until_not(
                        lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
                    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
                except TimeoutException:
                    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

                # 找到全屏按钮，判断按钮是否存在，存在则直接点，不存在则片库放器显示出按钮
                el = methodpackage.find_elementId_conditionXpath(
                    self.driver,
                    "com.sumavision.sanping.gudou:id/img_expand",
                    "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                    "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
                    "/android.widget.FrameLayout/android.view.View")
                el.click()
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击全屏'

                # 获取点赞状态
                el = methodpackage.find_elementId_conditionXpath(
                    self.driver,
                    "com.sumavision.sanping.gudou:id/img_like",
                    "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                    "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
                    "/android.widget.FrameLayout/android.view.View")

                methodpackage.get_screenshot_by_element(self.driver, el, tempfile1)
                if selectedColor == methodpackage.get_dominant_color(methodpackage.load_image(tempfile1)):
                    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已经点赞过：', currentName
                    self.driver.back()
                    self.driver.back()
                    continue
                sleep(5)

                el = methodpackage.find_elementId_conditionXpath(
                    self.driver,
                    "com.sumavision.sanping.gudou:id/img_like_not",
                    "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                    "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
                    "/android.widget.FrameLayout/android.view.View")
                methodpackage.get_screenshot_by_element(self.driver, el, tempfile2)
                if (235, 97, 0) == methodpackage.get_dominant_color(methodpackage.load_image(tempfile2)) :
                    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已经踩过：', currentName
                    self.driver.back()
                    self.driver.back()
                    continue

                if not like:
                    # 获取点赞总数
                    el = methodpackage.find_elementId_conditionXpath(
                        self.driver,
                        "com.sumavision.sanping.gudou:id/text_like",
                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                        "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
                        "/android.widget.FrameLayout/android.view.View")
                    likes_num = int(el.text)

                    # 点赞
                    el = methodpackage.find_elementId_conditionXpath(
                        self.driver,
                        "com.sumavision.sanping.gudou:id/img_like",
                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                        "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
                        "/android.widget.FrameLayout/android.view.View")
                    el.click()
                    sleep(8)

                    # 获取点赞数目
                    # el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/text_like")
                    # liked_num = int(el.text)
                    # el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_like")
                    # methodpackage.get_screenshot_by_element(self.driver, el, tempfile1)
                    el = methodpackage.find_elementId_conditionXpath(
                        self.driver,
                        "com.sumavision.sanping.gudou:id/text_like",
                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                        "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
                        "/android.widget.FrameLayout/android.view.View")
                    liked_num = int(el.text)

                    el = methodpackage.find_elementId_conditionXpath(
                        self.driver,
                        "com.sumavision.sanping.gudou:id/img_like",
                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                        "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
                        "/android.widget.FrameLayout/android.view.View")
                    methodpackage.get_screenshot_by_element(self.driver, el, tempfile1)
                    self.assertEqual(likes_num+1, liked_num)
                    self.assertEqual(selectedColor, methodpackage.get_dominant_color(methodpackage.load_image(tempfile1)))
                    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'第一次点赞：', currentName

                    # 再次点赞
                    el = methodpackage.find_elementId_conditionXpath(
                        self.driver,
                        "com.sumavision.sanping.gudou:id/img_like",
                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                        "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
                        "/android.widget.FrameLayout/android.view.View")
                    el.click()
                    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'再次点赞：', currentName

                    # 判断弹出消息
                    self.assertEqual(True, self.find_toast(self.driver, u'您已经赞过啦'))

                    # 踩
                    el = methodpackage.find_elementId_conditionXpath(
                        self.driver,
                        "com.sumavision.sanping.gudou:id/img_like_not",
                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                        "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
                        "/android.widget.FrameLayout/android.view.View")
                    el.click()
                    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'踩：', currentName

                    # 判断弹出消息
                    self.assertEqual(True, self.find_toast(self.driver, u'您已经赞过啦'))

                    like = 1
                    self.driver.back()
                    self.driver.back()
                    continue

                if like and not not_like:
                    # 获取踩总数
                    el = methodpackage.find_elementId_conditionXpath(
                        self.driver,
                        "com.sumavision.sanping.gudou:id/text_like_not",
                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                        "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
                        "/android.widget.FrameLayout/android.view.View")
                    not_likes_num = int(el.text)

                    # 踩
                    el = methodpackage.find_elementId_conditionXpath(
                        self.driver,
                        "com.sumavision.sanping.gudou:id/img_like_not",
                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                        "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
                        "/android.widget.FrameLayout/android.view.View")
                    el.click()
                    sleep(8)
                    # 获取踩数目
                    # el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/text_like_not")
                    # not_liked_num = int(el.text)
                    # el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_like_not")
                    # methodpackage.get_screenshot_by_element(self.driver, el, tempfile1)
                    el = methodpackage.find_elementId_conditionXpath(
                        self.driver,
                        "com.sumavision.sanping.gudou:id/text_like_not",
                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                        "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
                        "/android.widget.FrameLayout/android.view.View")
                    not_liked_num = int(el.text)

                    el = methodpackage.find_elementId_conditionXpath(
                        self.driver,
                        "com.sumavision.sanping.gudou:id/img_like_not",
                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                        "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
                        "/android.widget.FrameLayout/android.view.View")
                    methodpackage.get_screenshot_by_element(self.driver, el, tempfile1)
                    self.assertEqual((235, 97, 0), methodpackage.get_dominant_color(methodpackage.load_image(tempfile1)))
                    self.assertEqual(not_likes_num + 1, not_liked_num)
                    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'第一次踩：', currentName

                    # 再次点踩
                    el = methodpackage.find_elementId_conditionXpath(
                        self.driver,
                        "com.sumavision.sanping.gudou:id/img_like_not",
                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                        "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
                        "/android.widget.FrameLayout/android.view.View")
                    el.click()
                    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'第二次踩：', currentName

                    # 判断弹出消息
                    self.assertEqual(True, self.find_toast(self.driver, u'您已经踩过啦'))

                    # 再次点赞
                    el = methodpackage.find_elementId_conditionXpath(
                        self.driver,
                        "com.sumavision.sanping.gudou:id/img_like",
                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                        "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
                        "/android.widget.FrameLayout/android.view.View")
                    el.click()
                    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'赞：', currentName

                    # 判断弹出消息
                    self.assertEqual(True, self.find_toast(self.driver, u'您已经踩过啦'))
                    not_like = 1
                    break

    # 片库节目投屏功能
    def test_0025_vodplay_push(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   片库节目投屏功能：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'
        el.click()

        methodpackage.swipeDown(self.driver, 500)

        # 播放一个节目
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
        name1 = el.text
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name1

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 10).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 找到全屏按钮，判断按钮是否存在，存在则直接点，不存在则片库放器显示出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_expand",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击全屏'

        # 点击投屏按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_push_header",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
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

    # 片库节目收藏、取消收藏
    def test_0026_vodplay_favor(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   片库节目收藏、取消收藏：开始'
        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 清空片库收藏记录
        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()

        # 进入“我的收藏”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_fav")
        el.click()

        # 进入收藏的“片库”页
        el = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout"
            "/android.widget.LinearLayout[2]/android.widget.TextView")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"进入收藏片库页"

        try:
            # 清空片库收藏内容
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

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'
        el.click()

        methodpackage.swipeDown(self.driver, 500)

        # 播放一个节目
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
        name1 = el.text
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name1

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 10).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 收藏
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_fav")
        tempFile = os.path.join(methodpackage.currentDir, "temp.png")  # 截图使用图片
        methodpackage.get_screenshot_by_element(self.driver, el, tempFile)
        self.assertEqual(0, methodpackage.getimage_color(methodpackage.load_image(tempFile), (235, 97, 0)))
        el.click()
        self.assertEqual(True, self.find_toast(self.driver, u'收藏成功'))
        tempFile = os.path.join(methodpackage.currentDir, "temp.png")  # 截图使用图片
        methodpackage.get_screenshot_by_element(self.driver, el, tempFile)
        self.assertGreater(methodpackage.getimage_color(methodpackage.load_image(tempFile), (235, 97, 0)), 150)

        #el.click()

        # 点击物理返回键
        self.driver.press_keycode(4)

        # 进入“我的收藏”验证收藏功能
        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()

        # 进入“我的收藏”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_fav")
        el.click()

        # 进入收藏的“片库”页
        el = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout"
            "/android.widget.LinearLayout[2]/android.widget.TextView")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"进入收藏片库页"

        try:
            # 选中收藏的第一条记录的节目名
            WebDriverWait(self.driver, 2).until(lambda x: x.find_element_by_xpath(
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout/android.support.v4.view.ViewPager/android.widget.FrameLayout"
                "/android.widget.LinearLayout/android.widget.ScrollView/android.widget.GridView"
                "/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout"
                "/android.widget.TextView"))
            el = self.driver.find_element_by_xpath(
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout/android.support.v4.view.ViewPager/android.widget.FrameLayout"
                "/android.widget.LinearLayout/android.widget.ScrollView/android.widget.GridView"
                "/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout"
                "/android.widget.TextView")
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'收藏存在异常'

        # 保存收藏节目的节目名
        name2 = el.text
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"收藏节目：%s" % name2

        self.assertIs(name1 == name2, True)

        # 返回到“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_myfav_back")
        el.click()

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        el.click()

        methodpackage.swipeDown(self.driver, 500)

        # 播放一个节目
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
        name = el.text
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

        # 再次进入“我的收藏”验证收藏功能
        # 进入“我的”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_mine")
        el.click()

        # 进入“我的收藏”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/frg_mine_fav")
        el.click()

        # 进入收藏的“片库”页
        el = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout"
            "/android.widget.LinearLayout[2]/android.widget.TextView")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"进入收藏片库页"

        # 判断收藏片库页“清空”按钮是否存在
        try:
            WebDriverWait(self.driver, 2).until_not(lambda x: x.find_element_by_xpath(
                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                "/android.widget.LinearLayout/android.support.v4.view.ViewPager/android.widget.FrameLayout"
                "/android.widget.LinearLayout/android.widget.ScrollView/android.widget.GridView"
                "/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout"
                "/android.widget.TextView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"取消收藏成功"
        except NoSuchElementException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"取消收藏有问题"
            self.assertIs(False, True)

    # 片库节目取消分享、片库分享功能
    def test_0027_vodplay_share(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   片库节目取消分享、片库分享功能：开始'
        # 启动弹框处理
        self.App_Start(self.driver)

        # 隐式等待
        self.driver.implicitly_wait(15)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'
        sleep(0.5)
        methodpackage.swipeDown(self.driver, 500)

        # 播放一个节目
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
        name = el.text
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 10).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        # 点击分享按钮
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_share")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"进入分享"

        # 点击取消按钮，取消分享
        el = self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'取消分享')]")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"取消分享"

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
        # self.assertEqual(True, self.find_toast(self.driver, u'分享取消'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"分享取消啦，验证提示信息正确"

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
        self.assertEqual(True, self.find_toast(self.driver, u'分享取消'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"分享取消啦，验证提示信息正确"

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
            u'确定退出',
            True)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'确定退出'

        self.assertEqual(True, self.find_toast(self.driver, u'分享取消'))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"分享取消啦，验证提示信息正确"

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
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u"分享取消啦，验证提示信息正确"

    # 片库节目退出功能
    def test_0028_vodplay_exit(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   片库节目退出功能：开始'

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'
        sleep(0.5)
        methodpackage.swipeDown(self.driver, 500)

        # 播放一个节目
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
        name = el.text
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放：', name

        # 等待播放加载完成
        try:
            WebDriverWait(self.driver, 10).until_not(
                lambda x: x.find_element_by_id("com.sumavision.sanping.gudou:id/LoadingView"))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载完成'
        except TimeoutException:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'播放加载超时'

        sleep(2)

        # 点击退出按钮
        el = methodpackage.find_elementId_conditionXpath(
            self.driver,
            "com.sumavision.sanping.gudou:id/img_back_header",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.FrameLayout/android.view.View")
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击退出'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/textView1")
        self.assertIsNotNone(el)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'退出播放成功'

    # 节目筛选
    def test_0029_vodplay_filter(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   片库节目搜索：开始'

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'

        # 判断筛选条件元素
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/filter_year')
        el2.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击"年代"'
        methodpackage.swipeDown_low(self.driver, 500)
        sleep(3)
        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/name')
        # self.assertGreater(len(els2), 0)
        tempfiel = os.path.join(methodpackage.currentDir, 'temp.png')
        tempfiel1 = os.path.join(methodpackage.currentDir, 'temp1.png')
        methodpackage.get_screenshot_by_box(self.driver, (0, 560, 1080, 1630), tempfiel)

        if len(els2):
            els2[1].click()
            methodpackage.swipeDown_low(self.driver, 500)
            sleep(5)
            methodpackage.get_screenshot_by_box(self.driver, (0, 560, 1080, 1630), tempfiel1)
            self.assertFalse(methodpackage.image_same_as(tempfiel, tempfiel1, 0.7))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'年代筛选正常'
            els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/name')
            els2[0].click()
        el2 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/filter_year')
        el2.click()

        el3 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/filter_locale')
        el3.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击"地区"'
        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/name')
        # self.assertGreater(len(els2), 0)
        if len(els2):
            els2[1].click()
            methodpackage.swipeDown_low(self.driver, 500)
            sleep(3)
            methodpackage.get_screenshot_by_box(self.driver, (0, 560, 1080, 1630), tempfiel1)
            self.assertFalse(methodpackage.image_same_as(tempfiel, tempfiel1, 0.7))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'地区筛选正常'
            els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/name')
            els2[0].click()
        el3 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/filter_locale')
        el3.click()

        el4 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/filter_category')
        el4.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'点击"分类"'
        els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/name')
        # self.assertGreater(len(els2), 0)
        if len(els2):
            els2[1].click()
            methodpackage.swipeDown_low(self.driver, 500)
            sleep(3)
            methodpackage.get_screenshot_by_box(self.driver, (0, 560, 1080, 1630), tempfiel1)
            self.assertFalse(methodpackage.image_same_as(tempfiel, tempfiel1, 0.7))
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'分类筛选正常'
            els2 = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/name')
            els2[0].click()
        el4 = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/filter_category')
        el4.click()

    # 片库节目搜索
    def test_0030_vodplay_search(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   片库节目搜索：开始'

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'

        # 进入搜索页面
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_search")
        el.click()

        # 搜索存在的
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/edt_keyword")
        el.click()
        el.clear()
        el.send_keys(u'北京')
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'搜索存在片库节目'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_search")
        el.click()

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/search_top_textview')
        els[1].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入搜索点播页'

        # 显示片库搜索结果，并且计算搜索结果的个数
        searchs = 0
        try:
            el = self.driver.find_elements_by_id("com.sumavision.sanping.gudou:id/search_vod_first_cover")
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'有搜索到节目'
            els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/search_vod_result_iv')
            searchs = len(els)
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'搜索到节目数量至少：', searchs
        except:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有搜索到节目'
        self.assertTrue(searchs)

        # 搜索不存在的
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/edt_keyword")
        el.click()
        el.send_keys("not exitst")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'搜索不存在片库节目'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_search")
        el.click()

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/search_top_textview')
        els[1].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入搜索点播页'

        # 显示片库搜索结果，并且计算搜索结果的个数
        searchs = 0
        try:
            el = self.driver.find_elements_by_id("com.sumavision.sanping.gudou:id/search_vod_first_cover")
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'有搜索到节目'
            els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/search_vod_result_iv')
            searchs = len(els)
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'搜索到节目数量至少：', searchs
        except:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有搜索到节目'
        self.assertFalse(searchs)

        # 搜索超长字符串
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/edt_keyword")
        el.click()
        el.clear()
        myChars = 'adbefghigk' * 100
        el.send_keys(myChars)

        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'搜索不存在片库节目'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_search")
        el.click()

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/search_top_textview')
        els[1].click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'进入搜索点播页'

        # 显示片库搜索结果，并且计算搜索结果的个数
        searchs = 0
        try:
            el = self.driver.find_elements_by_id("com.sumavision.sanping.gudou:id/search_vod_first_cover")
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'有搜索到节目'
            els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/search_vod_result_iv')
            searchs = len(els)
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'搜索到节目数量至少：', searchs
        except:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'没有搜索到节目'
        self.assertFalse(searchs)

    # 片库节目搜索历史
    def test_0031_vodplay_searchhistory(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   片库节目搜索历史：开始'

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'

        # 进入搜索页面
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_search")
        el.click()

        # 搜索随机关键词
        keys = self.randstr(2, alphas)
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/edt_keyword")
        el.click()
        el.clear()
        el.send_keys(keys)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'搜索关键词：', keys

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_search")
        el.click()
        sleep(5)
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/img_back')
        el.click()

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/item_hot_search_programName')
        lis = [els[i].text for i in range(4)]

        # 判断之前搜索的关键词在不在历史记录里
        if keys in lis:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'搜索的关键词在历史记录里'
            self.assertTrue(True)
        else:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'搜索的关键词不在历史记录里'
            self.assertTrue(False)

    # 片库节目搜索历史清空
    def test_0032_vodplay_searchhistory_emp(self):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'   片库节目搜索历史清空：开始'

        # 启动弹框处理
        self.App_Start(self.driver)
        # 隐式等待
        self.driver.implicitly_wait(8)

        # 进入“片库”
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/iv_footer_vod")
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入首页'
        el.click()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'成功进入片库'

        # 进入搜索页面
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_search")
        el.click()

        # 搜索随机关键词
        keys = self.randstr(2, alphas)
        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/edt_keyword")
        el.click()
        el.clear()
        el.send_keys(keys)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'搜索关键词：', keys

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_search")
        el.click()
        sleep(5)
        el = self.driver.find_element_by_id('com.sumavision.sanping.gudou:id/img_back')
        el.click()

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/item_hot_search_programName')
        self.assertGreater(len(els), 10)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'已有搜索历史记录'

        el = self.driver.find_element_by_id("com.sumavision.sanping.gudou:id/img_del")
        el.click()

        # 如果提示是否清空记录，选择确定
        methodpackage.wait_xPathMsg_click_idButton(
            self.driver,
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
            "/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout"
            "/android.widget.TextView[1]",
            "com.sumavision.sanping.gudou:id/btnOK",
            2,
            u'清空搜索历史记录',
            True)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'确定清空搜索历史记录'
        sleep(1)

        els = self.driver.find_elements_by_id('com.sumavision.sanping.gudou:id/item_hot_search_programName')
        self.assertEqual(len(els), 10)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), u'清空成功'


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)











