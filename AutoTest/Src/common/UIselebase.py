# -*- coding: utf-8 -*-
# @Time    : now()
# @Author  : AngesZhu
# @File    : .py
# @desc:
# coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import *   # 导入所有的异常类
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import os


class BasePage(object):
    """
    基于原生的selenium框架做了二次封装.
    """
    def __init__(self, driver):
        """
        启动浏览器参数化，
        """
        # self.driver = webdriver.Firefox()
        self.driver = driver

    def open(self, url):
        '''
        使用get打开url后，最大化窗口，判断title符合预期
        '''
        self.driver.get(url)
        self.driver.maximize_window()

    def find_element(self, locator, timeout=10):
        '''定位元素，参数locator是元祖类型'''
        element = WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located(locator))
        return element

    def find_elements(self, locator, timeout=10):
        '''定位一组元素'''
        elements = WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_all_elements_located(locator))
        return elements

    def click(self, locator):
        '''点击操作'''
        element = self.find_element(locator)
        element.click()


    def send_keys(self, locator, text, is_clear=True):
        '''
        发送文本，清空后输入
        Usage:
        locator = ("id","xxx")
        driver.send_keys(locator, text)
        '''
        element = self.find_element(locator)
        if is_clear==True: element.clear()
        element.send_keys(text)

    def is_text_in_element(self, locator, text, timeout=10):
        '''
        判断文本在元素里,没定位到元素返回False，定位到返回判断结果布尔值
        result = driver.text_in_element(locator, text)
        '''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.text_to_be_present_in_element(locator, text))
        return result

    def is_text_in_value(self, locator, value, timeout=10):
        '''
        判断元素的value值，没定位到元素返回false,定位到返回判断结果布尔值
        result = driver.text_in_element(locator, text)
        '''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.text_to_be_present_in_element_value(locator, value))
        return result

    def is_title(self, title, timeout=10):
        '''判断title完全等于'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.title_is(title))
        return result

    def is_title_contains(self, title, timeout=10):
        '''判断title包含'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.title_contains(title))
        return result

    def is_selected(self, locator, timeout=10):
        '''判断元素被选中，返回布尔值,'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.element_located_to_be_selected(locator))
        return result

    def is_selected_be(self, locator, selected=True, timeout=10):
        '''判断元素的状态，selected是期望的参数true/False
        返回布尔值'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.element_located_selection_state_to_be(locator, selected))
        return result

    def is_alert_present(self, timeout=10):
        '''判断页面是否有alert，
        有返回alert(注意这里是返回alert,不是True)
        没有返回False'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.alert_is_present())
        return result

    def is_visibility(self, locator, timeout=10):
        '''元素可见返回本身，不可见返回Fasle'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.visibility_of_element_located(locator))
        return result

    def is_invisibility(self, locator, timeout=10):
        '''元素不可见返回True，可见返回本身'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.invisibility_of_element_located(locator))
        return result

    def is_clickabke(self, locator, timeout=10):
        '''元素可以点击is_enabled返回本身，不可点击返回Fasle'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.element_to_be_clickable(locator))
        return result

    def is_located(self, locator, timeout=10):
        '''判断元素被定为到（并不意味着可见），定为到返回element,没定位到返回False'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located(locator))
        return result

    def is_exists(self, locator):
        '''判断元素存在'''
        try:
            self.is_located(locator)
            return True
        except:
            return False

    def is_iframe(self, locator, timeout=10):
        '''locator是tuple类型，locator也可以是id和name名称,返回布尔值'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.frame_to_be_available_and_switch_to_it(locator))
        return result

    def move_to_element(self, locator):
        '''鼠标悬停操作'''
        element = self.find_element(locator)
        # ActionChains(self.driver).context_click()
        ActionChains(self.driver).move_to_element(element).perform()

    def get_title(self):
        '''获取title'''
        return self.driver.title

    def get_text(self, locator):
        '''获取文本'''
        t = self.find_element(locator).text
        return t

    def get_attribute(self, locator, name):
        '''获取属性'''
        element = self.find_element(locator)
        return element.get_attribute(name)

    def js_execute(self, js):
        '''执行js'''
        return self.driver.execute_script(js)

    def js_focus_element(self, locator):
        '''聚焦元素'''
        target = self.find_element(locator)
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
        element = self.find_element(locator)
        Select(element).select_by_index(index)
        element.click()

    def select_by_value(self, locator, value):
        '''通过value属性'''
        element = self.find_element(locator)
        Select(element).select_by_value(value)

    def select_by_text(self, locator, text):
        '''通过文本值定位'''
        element = self.find_element(locator)
        Select(element).select_by_visible_text(text)

    def deselect_by_index(self, locator, index):
        '''通过index索引'''
        element = self.find_element(locator)
        Select(element).deselect_by_index(index)

    def deselect_all(self, locator):
        '''清除所有的选项'''
        element = self.find_element(locator)
        Select(element).deselect_all()

    def select_first(self, locator):
        element = self.find_element(locator)
        return Select(element).first_selected_option

    def select_all(self, locator):
        element = self.find_element(locator)
        return Select(element).all_selected_options

    def get_current_handle(self):
        return self.driver.current_window_handle

    def get_handles(self):
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
        return self.find_element(locator).size

    def get_screenshot(self, image_path):
        '''获取屏幕截图'''
        nowtime = time.strftime("%Y-%m-%d %H_%M_%S")
        try:
            fpath = os.path.join(image_path, nowtime + ".png")
            self.driver.get_screenshot_as_file(fpath)
            print("screenshot ：%s"%fpath)
        except Exception as a:
            print("Error! screenshot：%s"%a)

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


if __name__ == '__main__':
	driver = webdriver.Firefox()  # 实例1 driver
	base_driver = BasePage(driver)  # 实例2 base_driver
	base_driver.open("https://www.baidu.com")
	input_loc = ("id", "kw")
	base_driver.send_keys(input_loc, "yoyo")
	button_loc = ("id", "su")
	base_driver.click(button_loc)
	print(base_driver.get_title())

	# 调用driver里面的方法
	driver.quit()




