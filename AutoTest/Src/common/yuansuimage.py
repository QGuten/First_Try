# coding:utf-8

from selenium import webdriver
import time
from PIL import Image

driver = webdriver.Firefox()
driver.get("http://www.baidu.com")
time.sleep(2)
driver.maximize_window()

driver.save_screenshot('button.png')

d = driver.find_element_by_id("kw")
print(d.location)
print(d.size)

left = d.location['x']
top = d.location['y']
right = d.location['x']+d.size['width']
bottom = d.location['y']+d.size['height']
print(left, top, right, bottom)

im = Image.open('button.png')
im = im.crop((left, top, right, bottom))
im.save('button.png')

time.sleep(2)
driver.quit()
