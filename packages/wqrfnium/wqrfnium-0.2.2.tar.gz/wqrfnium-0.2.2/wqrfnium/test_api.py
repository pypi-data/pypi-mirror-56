# -*- coding:utf-8 -*-
from selenium import webdriver
from wqrfnium_api import *

get_api_url = "http://xxxx/xxx/get_element_test/***/"
update_api_url = "http://xxxx/update_element_test/***/"
begin_wqrf(get_api_url,update_api_url)

driver = webdriver.Chrome()
driver.get("http://www.baidu.com/")
time.sleep(2)
getelement(driver,"searchinput").send_keys('xiaozhu')


