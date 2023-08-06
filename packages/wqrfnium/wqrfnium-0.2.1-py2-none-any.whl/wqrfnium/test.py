# -*- coding:utf-8 -*-
from selenium import webdriver
from wqrfnium import *

begin_wqrf('MyElements2.xls')

driver = webdriver.Chrome()
driver.get("http://www.baidu.com/")
time.sleep(2)
getelement(driver,"searchinput").send_keys('xiaozhu')


