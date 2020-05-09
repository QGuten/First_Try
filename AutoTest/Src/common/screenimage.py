# coding:utf-8
import os
import time
from PIL import Image
from selenium import webdriver

class screenImage():

    # 获取当前当前文件夹的路径
    def __getPath(self):
        file_path = os.path.dirname(os.path.realpath(__file__))
        return file_path

    # 截取全屏图片
    @classmethod
    def screenFull(self, driver, *path, imagename):
        '''判断元素是否是字符串'''
        if isinstance(path, str):
            imagepath = os.path.join(path, imagename)
            driver.save_screenshot(imagepath)
        else:
            path = self.__getPath
            imagepath = os.path.join(str(path), imagename)
            driver.save_screenshot(imagepath)
        return imagepath

    # 截取元素图片
    @classmethod
    def screenLocal(self, *coordinate, imagepath):
        '''
        参数传所需要截图的坐标list
        '''
        l = []
        for i in coordinate:
            l.append(i)
        left = l[0]
        top = l[1]
        right = l[2]
        bottom = l[3]
        im = Image.open(imagepath)
        im = im.crop((left, top, right, bottom))
        im.save(imagepath)

if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.get("http://www.baidu.com")
    time.sleep(2)
    driver.maximize_window()
    screenImage.screenFull(driver=driver, imagename='search')
    d = driver.find_element_by_id("kw")
    list = []
    list.append(d.location['x'])
    list.append(d.location['y'])
    list.append(d.location['x'] + d.size['width'])
    list.append(d.location['y'] + d.size['height'])
    # screenImage.screenLocal(list, imagepath='search')
