# -*- coding: utf-8 -*-
# @Time    : 2018/05/08 13:30
# @Author  : AngesZhu
# @File    : UIBase.py
# @desc:selenium简单封装

import configparser
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from config.LoggerText import Logger
# from framework.getconfig import GetConfig
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os.path
import sys
import time
# from selenium.common.exceptions import *   # 导入所有的异常类
import os

logger = Logger(logger="BasePage").getlog()


class BasePage(object):
    """
    定义一个页面基类，让所有页面都继承这个类，封装一些常用的页面操作方法到这个类
    """
    getinfo = configparser.ConfigParser()
    file_path = os.path.dirname(os.path.dirname(os.path.abspath('.'))) + '/config/config.ini'
    getinfo.read(file_path, encoding="utf-8-sig")

    def __init__(self, driver):
        """
        启动浏览器参数化，
        """
        # self.driver = webdriver.Firefox()
        self.driver = driver

    # quit browser and end testing
    def quit_browser(self):
        self.driver.quit()
        logger.info("Quit browser.")

    # 浏览器前进操作
    def forward(self):
        self.driver.forward()
        logger.info("Click forward on current page.")

    # 浏览器后退操作
    def back(self):
        self.driver.back()
        logger.info("Click back on current page.")

    # 隐式等待
    def wait(self, seconds):
        self.driver.implicitly_wait(seconds)
        logger.info("wait for %d seconds." % seconds)

    # 强行等待
    def sleep(self, seconds):
        time.sleep(seconds)
        logger.info("wait for %d seconds." % seconds)

    # 点击关闭当前窗口
    def close(self):
        try:
            self.driver.close()
            logger.info("Closing and quit the browser.")
        except NameError as e:
            logger.error("Failed to quit the browser with %s" % e)

    # 鼠标悬停某元素
    def museover(self, element):
        _element = self.get_element(element)
        try:
            ActionChains(self.driver).move_to_element(_element).perform()
            self.sleep(1)
            logger.info("museover element: %s" % element)
        except:
            logger.error("Failed to museover element:  %s" % element)

    # 保存图片
    def get_windows_img(self):
        """
        在这里我们把file_path这个参数写死，直接保存到我们项目根目录的一个文件夹.\Screenshots下
        """
        file_path = os.path.dirname(os.path.abspath('.')) + '/screenshots/'
        rq = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))  # 获取系统当前时间
        screen_name = file_path + rq + '.png'
        try:
            self.driver.get_screenshot_as_file(screen_name)
            logger.info("Had take screenshot and save to folder : /screenshots")
        except NameError as e:
            logger.error("Failed to take screenshot! %s" % e)
            self.get_windows_img()

    # 聚焦到某元素
    def focus(self, locator):
        u"""聚焦到某元素"""
        """Sets focus to element identified by `locator`."""
        element = self.get_element(locator)  # 先找到这个元素
        self.driver.execute_script("arguments[0].focus();", element)  # 传入这个元素，就直接聚焦了。
        logger.info("Focus element success.")

    # 拉浏览器滚动条
    def scroll_top(self):
        js = "var q=document.documentElement.scrollTop=100000"
        self.driver.execute_script(js)
        self.sleep(1)

    # 获取当前时间戳
    def get_localtime(self):
        u'''获取当前时间戳 20180118145306 '''
        rq = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        logger.info("Get the localtime is : %s ." % rq)
        return rq

    # 获取元素的文本
    def get_text(self, selector):
        u""" 获取元素的文本 """
        el = self.get_element(selector)
        _text = el.text
        logger.info("Get element text success.")
        return _text

    # 获取元素的元组
    def get_locator_tuple(self, selector):
        """
        获取元组： self.loginbtn_first = "xpath=>//a[contains(.,'登录')]"  # 首页左上角的登录按钮
        返回：selector = （"xpath", "//a[contains(.,'登录')]"）

        id: i  id
        xpath: x  xpath
        name:n  name
        class_name: c  class_name  class name
        link_text: l  link_text  link text
        partial_link_text: p  partial_link_text  partial link text
        tag_name: t  tag_name  tag name
        css: s  css  css_selector  css selector
        """
        try:
            if '=>' not in selector:
                return selector
        except:
            logger.error("元素写法不规范！")

        selector_by = selector.split('=>')[0]
        selector_value = selector.split('=>')[1]

        if selector_by == "i" or selector_by == 'id':
            try:
                locator = ("id", selector_value)
                return locator
            except NoSuchElementException as e:
                logger.error("NoSuchElementException: %s" % e)
                self.get_windows_img()  # take screenshot
        elif selector_by == "x" or selector_by == 'xpath':
            try:
                locator = ("xpath", selector_value)
                return locator
            except NoSuchElementException as e:
                logger.error("异常是: %s" % e)
                self.get_windows_img()
        elif selector_by == "n" or selector_by == 'name':
            try:
                locator = ("name", selector_value)
                return locator
            except NoSuchElementException as e:
                logger.error("异常是: %s" % e)
                self.get_windows_img()
        elif selector_by == "c" or selector_by == 'class_name' or selector_by == 'class name':
            try:
                locator = ("class name", selector_value)
                return locator
            except NoSuchElementException as e:
                logger.error("异常是: %s" % e)
                self.get_windows_img()
        elif selector_by == "l" or selector_by == 'link_text' or selector_by == 'link text':
            try:
                locator = ("link text", selector_value)
                return locator
            except NoSuchElementException as e:
                logger.error("异常是: %s" % e)
                self.get_windows_img()
        elif selector_by == "p" or selector_by == 'partial_link_text' or selector_by == 'partial link text':
            try:
                locator = ("partial link text", selector_value)
                return locator
            except NoSuchElementException as e:
                logger.error("异常是: %s" % e)
                self.get_windows_img()
        elif selector_by == "t" or selector_by == 'tag_name' or selector_by == 'tag name':
            try:
                locator = ("tag name", selector_value)
                return locator
            except NoSuchElementException as e:
                logger.error("异常是: %s" % e)
                self.get_windows_img()
        elif selector_by == "s" or selector_by == 'css' or selector_by == 'css_selector' or selector_by == 'css selector':
            try:
                locator = ("css selector", selector_value)
                return locator
            except NoSuchElementException as e:
                logger.error("异常是: %s" % e)
                self.get_windows_img()
        else:
            self.get_windows_img()
            raise NameError("元素写法错误，请检查元素的语法是否正确，参考 “xpaht=>//input[contains(@systype,'1')]")

    # 定位元素方法
    def get_element(self, selector):
        """
         这个地方为什么是根据=>来切割字符串，请看页面里定位元素的方法
         submit_btn = "id=>su"
         login_lnk = "xpath=>//*[@id='u1']/a[7]"  # 百度首页登录链接定位
         如果采用等号，结果很多xpath表达式中包含一个=，这样会造成切割不准确，影响元素定位
        :param selector:
        :return: element
        """
        timeout = 30  # 超时的时间设置
        poll = 0.5  # 请求频率
        element = ''
        tuple_ = self.get_locator_tuple(selector)  # 获取元组
        try:
            # element = self.driver.find_element_by_id(selector_value)
            element = WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll).until(
                EC.presence_of_element_located(tuple_))
            # logger.info("Find the element successful ! " + selector_by + " value is " + selector_value )  #% (element.text, selector_by, selector_value)
        except NoSuchElementException as e:
            logger.error("NoSuchElementException: %s" % e)
            self.get_windows_img()  # take screenshot

        return element

    # 点击元素
    def click(self, selector):

        el = self.get_element(selector)
        try:
            el.click()
            time.sleep(1)
            # logger.info("The element \' %s \' was clicked." % el.text)
            logger.info("The element " + selector + " was clicked.")
        except NameError as e:
            self.get_windows_img()
            logger.error("Failed to click the element with %s" % e)

    # 输入
    def input_text(self, selector, text):

        el = self.get_element(selector)
        el.clear()
        try:
            # el.send_keys(unicode(text))
            el.send_keys(text)
            logger.info("Input test " + text + " in inputBox")
        except NameError as e:
            self.get_windows_img()
            logger.error("Failed to type in input box with %s" % e)
            self.get_windows_img()

    # 上传文件
    def upload(self, selector, filetype):
        logger.info("上传文件")
        el = self.get_element(selector)
        file_path = os.path.dirname(os.path.abspath('.')) + u'\\data\\测试文件.'
        el.send_keys(file_path + filetype)
        logger.info("Upload file success.")
        self.sleep(3)

    # 清除文本框
    def clear(self, selector):

        el = self.get_element(selector)
        try:
            el.clear()
            logger.info("Clear text in input box before typing.")
        except NameError as e:
            logger.error("Failed to clear in input box with %s" % e)
            self.get_windows_img()

    # 发送向下键
    def down(self, selector):
        _element = self.get_element(selector)
        # print _element
        print(_element)
        action = ActionChains(self.driver).move_to_element(_element)
        action.send_keys(Keys.DOWN).perform()
        logger.info("Send the DOWN key .")
        self.sleep(1)

    # 发送向下键
    def downNum(self, selector, num):
        """按几次向下键"""
        _element = self.get_element(selector)
        action = ActionChains(self.driver).move_to_element(_element)
        # print _element
        print(_element)
        i = 0
        if num < 1 or num > 10:
            action.send_keys(Keys.DOWN).perform()  # 小于1和大于10的数，只进行一次
            logger.info("Send the DOWN key .")
        else:
            while i < num:
                action.send_keys(Keys.DOWN).perform()
                logger.info("Send the DOWN key .")
                i = i + 1
        self.sleep(1)

    # 发送回车键（enter）
    def enter(self, selector):
        _element = self.get_element(selector)
        # print _element
        print(_element)
        action = ActionChains(self.driver).move_to_element(_element)
        action.send_keys(Keys.ENTER).perform()
        logger.info("Send the ENTER key !")
        self.sleep(1)

    # 或取网页标题
    def get_page_title(self):
        logger.info("Current page title is " + self.driver.title)
        return self.driver.title

    @staticmethod
    def timesleep(seconds):
        time.sleep(seconds)
        logger.info("Sleep for %d seconds" % seconds)


        # read the browser type from config.ini file, return the driver

    # 打开浏览器
    def open_browser(self, driver):
        config = configparser.ConfigParser()
        # file_path = os.path.dirname(os.getcwd()) + '/config/config.ini'
        file_path = os.path.dirname(os.path.abspath('.')) + '/config/config.ini'
        config.read(file_path, encoding="utf-8-sig")

        #### 浏览器和测试地址的选择 ###
        browser = self.getinfo.get_browser()
        logger.info("You had select %s browser." % browser)
        url = self.getinfo.get_url()
        logger.info("The test server url1 is: %s" % url)

        if browser == "Firefox":
            # driver = webdriver.Firefox(executable_path=self.firefox_driver_path, firefox_options=self.options_firefox)
            driver = webdriver.Firefox(executable_path=self.firefox_driver_path)
            logger.info("Starting firefox browser.")
        elif browser == "Chrome":
            # driver = webdriver.Chrome(executable_path=self.chrome_driver_path,chrome_options=self.options_chrome)
            driver = webdriver.Chrome(executable_path=self.chrome_driver_path)
            logger.info("Starting Chrome browser.")
        elif browser == "IE":
            driver = webdriver.Ie(self.ie_driver_path)
            logger.info("Starting IE browser.")

        driver.get(url)
        logger.info("Open url1: %s" % url)
        driver.maximize_window()
        logger.info("Maximize the current window.")
        t1 = 10  # 后续可放到config.ini文件中
        driver.implicitly_wait(t1)
        logger.info("Set implicitly wait %d seconds." % t1)

        return driver

    # 退出并关闭浏览器
    def quit_browser(self):
        logger.info("Now! Close and quit the browser.")
        self.driver.quit()
        logger.info("关闭浏览器")

    # 判断元素是否显示出来
    def is_suces(self, selector, text):
        u'''判断元素是否显示出来'''
        # text = self.driver.find_element_by_id("selector").text
        text = self.get_element(selector).text
        return text

    # 切换浏览器窗口
    def switch_window(self):
        u"""切换浏览器窗口"""
        self.sleep(1)
        # print self.driver.current_window_handle  # 输出当前窗口句柄
        handles = self.driver.window_handles  # 获取当前全部窗口句柄集合
        # print handles  # 输出句柄集合

        for handle in handles:  # 切换窗口
            if handle != self.driver.current_window_handle:
                # print 'switch to second window', handle
                # self.driver.close()  # 关闭第一个窗口
                self.driver.switch_to.window(handle)  # 切换到第二个窗口

                # 切换浏览器窗口

    def switch_window1(self):
        u"""切换浏览器窗口只使用与智慧工程项目"""
        handles = self.driver.window_handles  # 获取当前全部窗口句柄集合
        for handle in handles:  # 切换窗口
            self.driver.switch_to.window(handle)  # 切换到主窗口

    #####################################################################

    def is_text_in_value(self, locator, value, timeout=10):
        '''
        判断元素的value值，没定位到元素返回false,定位到返回判断结果布尔值
        result = driver.text_in_element(locator, text)
        '''

        locator_ = self.get_locator_tuple(locator)
        try:
            result = WebDriverWait(self.driver, timeout, 1).until(
                EC.text_to_be_present_in_element_value(locator_, value))
            return result
        except:
            return False

    def is_title(self, title, timeout=10):
        '''判断title完全等于'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.title_is(title))
        return result

    def is_title_contains(self, title, timeout=10):
        '''判断title包含'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.title_contains(title))

    def is_selected(self, locator, timeout=10):
        '''判断元素被选中，返回布尔值,'''
        locator_ = self.get_locator_tuple(locator)
        result = WebDriverWait(self.driver, timeout, 1).until(EC.element_located_to_be_selected(locator_))
        return result

    def is_selected_be(self, locator, selected=True, timeout=10):
        '''判断元素的状态，selected是期望的参数true/False
        返回布尔值'''
        locator_ = self.get_locator_tuple(locator)
        result = WebDriverWait(self.driver, timeout, 1).until(
            EC.element_located_selection_state_to_be(locator_, selected))
        return result

    def is_alert_present(self, timeout=10):
        '''判断页面是否有alert，
        有返回alert(注意这里是返回alert,不是True)
        没有返回False'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.alert_is_present())
        return result

    def is_visibility(self, locator, timeout=10):
        '''元素可见返回本身，不可见返回Fasle'''
        locator_ = self.get_locator_tuple(locator)
        result = WebDriverWait(self.driver, timeout, 1).until(EC.visibility_of_element_located(locator_))
        return result

    def is_invisibility(self, locator, timeout=10):
        '''元素不可见返回True，可见返回本身'''
        locator_ = self.get_locator_tuple(locator)
        result = WebDriverWait(self.driver, timeout, 1).until(EC.invisibility_of_element_located(locator_))
        return result

    def is_clickabke(self, locator, timeout=10):
        '''元素可以点击is_enabled返回本身，不可点击返回Fasle'''
        locator_ = self.get_locator_tuple(locator)
        result = WebDriverWait(self.driver, timeout, 1).until(EC.element_to_be_clickable(locator_))
        return result

    def is_located(self, locator, timeout=10):
        '''判断元素被定为到（并不意味着可见），定为到返回element,没定位到返回False'''
        locator_ = self.get_locator_tuple(locator)
        result = WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located(locator_))
        return result

    def is_exists(self, locator):
        '''判断元素存在'''
        locator_ = self.get_locator_tuple(locator)
        try:
            self.is_located(locator_)
            return True
        except:
            return False

    def is_iframe(self, locator, timeout=10):
        '''locator是tuple类型，locator也可以是id和name名称,返回布尔值'''
        locator_ = self.get_locator_tuple(locator)
        result = WebDriverWait(self.driver, timeout, 1).until(EC.frame_to_be_available_and_switch_to_it(locator_))
        return result

    def move_to_element(self, locator):
        '''鼠标悬停操作'''
        locator_ = self.get_locator_tuple(locator)
        element = self.get_element(locator_)
        # ActionChains(self.driver).context_click()
        ActionChains(self.driver).move_to_element(element).perform()

    def gettext(self, locator):
        '''获取文本'''
        locator_ = self.get_locator_tuple(locator)
        t = self.get_element(locator_).text
        return t

    def get_attribute(self, locator, name):
        '''获取属性'''
        locator_ = self.get_locator_tuple(locator)
        element = self.get_element(locator_)
        return element.get_attribute(name)

    def js_execute(self, js):
        '''执行js'''
        return self.driver.execute_script(js)

    def js_focus_element(self, locator):
        '''聚焦元素'''
        locator_ = self.get_locator_tuple(locator)
        target = self.get_locator_tuple(locator_)
        self.driver.execute_script("arguments[0].scrollIntoView();", target)

    def js_scroll_top(self):
        '''滚动到顶部'''
        js = "window.scrollTo(0,0)"
        self.driver.execute_script(js)

    def js_scroll_end(self):
        '''滚动到底部'''
        js = "window.scrollTo(0,document.body.scrollHeight)"
        self.driver.execute_script(js)

    def select_by_index(self, locator, index=0):
        '''通过索引,index是索引第几个，从0开始，默认选第一个'''
        locator_ = self.get_locator_tuple(locator)
        element = self.get_element(locator_)
        Select(element).select_by_index(index)
        element.click()

    def select_by_value(self, locator, value):
        '''通过value属性'''
        locator_ = self.get_locator_tuple(locator)
        element = self.get_locator_tuple(locator_)
        Select(element).select_by_value(value)

    def select_by_text(self, locator, text):
        '''通过文本值定位'''
        locator_ = self.get_locator_tuple(locator)
        element = self.get_locator_tuple(locator_)
        Select(element).select_by_visible_text(text)

    def deselect_by_index(self, locator, index):
        '''通过index索引'''
        locator_ = self.get_locator_tuple(locator)
        element = self.get_locator_tuple(locator_)
        Select(element).deselect_by_index(index)

    def deselect_all(self, locator):
        '''清除所有的选项'''
        locator_ = self.get_locator_tuple(locator)
        element = self.get_element(locator_)
        Select(element).deselect_all()

    def select_first(self, locator):
        locator_ = self.get_locator_tuple(locator)
        element = self.get_element(locator_)
        return Select(element).first_selected_option

    def select_all(self, locator):
        locator_ = self.get_locator_tuple(locator)
        element = self.get_element(locator_)
        return Select(element).all_selected_options

    def get_current_handle(self):
        '''获取当前的句柄'''
        return self.driver.current_window_handle

    def get_handles(self):
        '''获取所有的句柄'''
        time.sleep(1)
        h = self.driver.window_handles
        if len(h) <= 1:
            print("当前只获取到一个窗口句柄，等待3秒后重新获取")
            time.sleep(3)
            h = self.driver.window_handles
        return h

    def get_name(self):
        '''获取浏览器名称'''
        return self.driver.name

    def get_size(self, locator):
        '''获取元素大小'''
        locator_ = self.get_locator_tuple(locator)
        return self.get_locator_tuple(locator_).size

    def get_screenshot(self, image_path):
        '''获取屏幕截图'''
        nowtime = time.strftime("%Y-%m-%d %H_%M_%S")
        try:
            fpath = os.path.join(image_path, nowtime + ".png")
            self.driver.get_screenshot_as_file(fpath)
            print("screenshot ：%s" % fpath)
        except Exception as a:
            print("Error! screenshot：%s" % a)

    def get_screenasbase64(self):
        return self.driver.get_screenshot_as_base64()

    def get_screenasfile(self, filename):
        return self.driver.get_screenshot_as_file(filename)

    def get_screenaspng(self):
        return self.driver.get_screenshot_as_png()

    def max_window(self):
        return self.driver.maximize_window()

    def set_window(self, width, height):
        return self.driver.set_window_size(width, height)

    def switch_handle(self, window_name):
        self.driver.switch_to.window(window_name)

    def switch_alert(self):
        alert = self.is_alert_present()
        if alert is not False:
            return alert
        else:
            print("not found alert!")

    def switch_iframe(self, locator):
        return self.is_iframe(locator)

