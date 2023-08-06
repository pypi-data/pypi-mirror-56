# -*- coding: utf-8 -*-
import os,sys
import re,time
import Levenshtein
import os,platform
import configparser
import requests
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass
#----------------------------------

def get_elements(icon):
    url = str(get_api_url).replace('***',icon)
    try:
        ele = requests.get(url=url).json()
    except:
        print('Please make sure your get_api_url can return json ！')
        exit(0)
    if ele['icon'] == '':
        print("can't find the element: [ %s ],please fixed it by yourself..." % icon)
        exit(0)
    else:
        return ele

def update_elements(icon,new_wqrfnium_ele):
    url = str(update_api_url).replace('***',icon)
    try:requests.post(url=url,data=new_wqrfnium_ele)
    except:print('your update_api having something wrong!')

def input_html_element(icon,new_element):
    url = str(update_api_url).replace('***',icon)
    try: requests.post(url=url,data=new_element)
    except:print('your update_api having something wrong!')

def likescore(oldstr,newstr):
    score = Levenshtein.ratio(str(oldstr), str(newstr))
    return score

def search_new(driver,old_html):
    try:old_id = re.findall(r'id="(.*?)"',old_html)[0]
    except:old_id = None
    try:old_name = re.findall(r'name="(.*?)"',old_html)[0]
    except:old_name=None
    try:old_class = re.findall(r'class="(.*?)"',old_html)[0]
    except:old_class=None
    try:old_text = re.findall(r'>(.*?)<',old_html)[0]
    except:old_text=''
    try:old_value = re.findall(r'value="(.*?)"',old_html)[0]
    except:old_value=''
    try:old_onclick = re.findall(r'onclick="(.*?)"',old_html)[0]
    except:old_onclick=None
    try:old_style = re.findall(r'style="(.*?)"',old_html)[0]
    except:old_style=''
    try:old_placeholder = re.findall(r'placeholder="(.*?)"', old_html)[0]
    except:old_placeholder=None
    try:old_href = re.findall(r'href="(.*?)"',old_html)[0]
    except:old_href=None
    try:old_type = re.findall(r'type="(.*?)"',old_html)[0]
    except:old_type = None
    #--------------------------------------------------------get all par
    bq = re.findall(r'<(.+?) ',old_html)[0]
    new_elements = driver.find_elements_by_tag_name(bq)
    end_element = new_elements[0]
    end_index = 0
    tmp_score = 0
    for i in range(len(new_elements)):
        score = 0
        new_id = new_elements[i].get_attribute("id")
        new_name = new_elements[i].get_attribute("name")
        new_class = new_elements[i].get_attribute("class")
        new_text = new_elements[i].text
        new_value = new_elements[i].get_attribute("value")
        new_onclick = new_elements[i].get_attribute("onclick")
        new_style = new_elements[i].get_attribute("style")
        new_placeholder = new_elements[i].get_attribute("placeholder")
        new_href = new_elements[i].get_attribute("href")
        try:new_type = re.findall(r'type="(.*?)"',new_elements[i].get_attribute("outerHTML"))[0]
        except:new_type = None
        score += likescore(old_id, new_id)
        score += likescore(old_name, new_name)
        score += likescore(old_class, new_class)
        score += likescore(old_text, new_text)
        score += likescore(old_value, new_value)
        score += likescore(old_onclick, new_onclick)
        score += likescore(str(old_style).replace(' ',''), str(new_style).replace(' ',''))
        score += likescore(old_placeholder, new_placeholder)
        score += likescore(old_href, new_href)
        score += likescore(old_type,new_type)
        if score > tmp_score:
            end_element = new_elements[i]
            end_index = i
            tmp_score = score
    new_html = end_element.get_attribute("outerHTML")
    new_tmp = 'tag name' #use id,name
    new_tmp_value = bq
    new_index = end_index
    return [end_element,new_tmp,new_tmp_value,new_index,new_html]

def getelement(driver,icon):
    time1 = time.time()
    element = get_elements(icon)
    print('find: %s ...'%icon)
    old_html = element['html_element']
    try:
        el = driver.find_elements(element['tmp_find_method'],element['tmp_find_value'])[int(element['index'])]
        print('success in %s s'%str(time.time()-time1)[:5])
        if old_html == '':
            new_html = el.get_attribute("outerHTML")
            element['html_element'] = new_html
            input_html_element(icon,element)
        return el
    except Exception:
        new_wqrfnium_ele = {}
        print('find_faild,begin fix....')
        newel_detail = search_new(driver,old_html)
        newel = newel_detail[0]
        new_wqrfnium_ele['icon'] =icon
        new_wqrfnium_ele['tmp_find_method'] = newel_detail[1]
        new_wqrfnium_ele['tmp_find_value'] =newel_detail[2]
        new_wqrfnium_ele['index'] =newel_detail[3]
        new_wqrfnium_ele['html_element'] =newel_detail[4]
        update_elements(icon=icon,new_wqrfnium_ele=new_wqrfnium_ele)
        print('find success in %s s'%str(time.time()-time1)[:5])
        return newel

try:
    cfp = configparser.ConfigParser()
    cfp.read('wqrfnium.ini')
    get_api_url = cfp.get('Api','get_api_url')
    update_api_url = cfp.get('Api','update_api_url')
except: # create wqrfnium.ini
    cfp = configparser.ConfigParser()
    cfp['Api']={"get_api_url":"","update_api_url":""}
    with open('wqrfnium.ini','w') as fp:
        cfp.write(fp)
    get_api_url = cfp.get('Api', 'get_api_url')
    update_api_url = cfp.get('Api', 'update_api_url')

def begin_wqrf(get_api_url,update_api_url):
    try:
        cfp.set("Api","get_api_url",get_api_url)
        cfp.set("Api","update_api_url",update_api_url)
        with open("wqrfnium.ini","w+") as f:
            cfp.write(f)
    except:
        exit(0)

if get_api_url == '' or update_api_url=='': #no api
    # begin to set the elements
    print('You are first use wqrfnium and chose the wqrfnium_api,you mast set the get_api_url and update_api_url,then play wqrfnium after!')
    print('You can use code [begin_wqrf("your get_api_url","your update_api_url")] to diy your get_api_url and update_api_url!')
    print('Your get_api_url url must like this: http(s)://yourhost/.../%s/ ,%s is your element\'s icon')
    print('Your get_api_url must responsebody like this: {"icon":"","tmp_find_method":"","tmp_find_value":"","index":"","html_element":"",}')
    print('Your update_api_url url must like this: http(s)://yourhost/.../%s/ ,%s is your element\'s icon')
    print('Your update_api_url requestbody must like this: {"tmp_find_method":"","tmp_find_value":"","index":"","html_element":"",}')
    print("You can also read the README to get help or wirte email to 1074321997@qq.com")
else:
    print('You had set the get_api_url and update_api_url')