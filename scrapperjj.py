from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import pandas as pd
from datetime import date

today = date.today()
df = pd.DataFrame(columns=['Restaurant','Review','ReviewCount','Reply','type','minprice'])

driver = webdriver.Chrome('/Users/mat_c/Downloads/chromedriver.exe')
driver.get('https://www.yogiyo.co.kr/mobile')
search_bar = driver.find_elements_by_css_selector('input[placeholder="건물명, 도로명, 지번으로 검색하세요."')
search_bar[0].clear()
search_bar[0].send_keys("경기도 안성시 공도읍 용두리 752 주은풍림아파트")
time.sleep(1)
search_bar[0].send_keys(Keys.ENTER)
url = driver.current_url
pointer = 0
food_list = ["치킨", "피자양식", "중식", "한식", "일식돈까스", "족발보쌈", "야식", "분식", "카페디저트", "편의점","프랜차이즈"]
while pointer < len(food_list):
    driver.get(url + food_list[pointer])
    loaded = driver.find_elements_by_xpath('//div[@class="restaurants-info"]')
    
    #Sometimes Yogiyo refuses to show information unless you refresh an unknown amount of time
    while loaded == []:
        driver.refresh()
        time.sleep(1)
        #check if the restaurant info has loaded
        loaded = driver.find_elements_by_xpath('//div[@class="restaurants-info"]')
    
    SCROLL_PAUSE_TIME = 0.5
    
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        
    ratings_name = driver.find_elements_by_xpath('//div[@class="restaurant-name ng-binding"]')
    
    ratings_test = driver.find_elements_by_xpath('//div[@class="stars"]')
    
    min_price = driver.find_elements_by_xpath('//li[@class="min-price ng-binding"]')
    
    delivery_fee = driver.find_elements_by_xpath('//div[@class=""]')
       

    for s in range(len(ratings_name)):
        result = re.sub("[^\d\.\ ]", "", ratings_test[s].text) 
        temp_str = (ratings_name[s].text + " " + " ".join(result.split())).split()
        while len(temp_str) < 4:
            temp_str.insert(len(temp_str), 0)
        temp_str.insert(len(temp_str), food_list[pointer])
        temp_str.insert(len(temp_str), min_price[s].text)
        temp_df = pd.DataFrame([temp_str], columns = ['Restaurant','Review','ReviewCount','Reply','type','minprice'])
        df = df.append(temp_df)
    print(food_list[pointer] + " completed")
    pointer = pointer + 1
    

driver.close()

df.to_excel(r''+str(today) + '.xlsx', index=False, header=True)

