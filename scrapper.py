from selenium import webdriver
import time
import re
import pandas as pd
driver = webdriver.Chrome('/Users/mat_c/Downloads/chromedriver.exe')
driver.get('https://www.yogiyo.co.kr/mobile/#/%EA%B2%BD%EA%B8%B0%EB%8F%84/456820/')

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
    
df = pd.DataFrame(columns=['Restaurant','Review','ReviewCount','Reply'])
for s in range(len(ratings_name)):
    result = re.sub("[^\d\.\ ]", "", ratings_test[s].text) 
    temp_str = (ratings_name[s].text + " " + " ".join(result.split())).split()
    while len(temp_str) < 4:
        temp_str.insert(len(temp_str), None)
    temp_df = pd.DataFrame([temp_str], columns = ['Restaurant','Review','ReviewCount','Reply'])
    df = df.append(temp_df)

    
driver.close()
    
# #<div class="stars">
                     #<div class="stars">
#                       <span>
#                         <span class="ico-star1 ng-binding" ng-show="restaurant.review_avg > 0">★ 3.9</span>
#                       </span>
#                       <span class="review_num ng-binding" ng-show="restaurant.review_count > 0">
#                           리뷰 22
#                       </span>
#                       <span class="review_num ng-binding ng-hide" ng-show="restaurant.owner_reply_count > 0">
#                           사장님댓글 0
#                       </span>
#                       <span ng-show="restaurant.review_count < 1" class="ng-hide">
#                           첫번째 리뷰를 남겨주세요!
#                       </span>
#                     </div>
#                     <div class="stars">
#                       <span>
#                         <span class="ico-star1 ng-binding" ng-show="restaurant.review_avg > 0">★ 4.7</span>
#                       </span>
#                       <span class="review_num ng-binding" ng-show="restaurant.review_count > 0">
#                           리뷰 170
#                       </span>
#                       <span class="review_num ng-binding" ng-show="restaurant.owner_reply_count > 0">
#                           
#                       <span ng-show="restaurant.review_count < 1" class="ng-hide">
#                           첫번째 리뷰사장님댓글 169
#                       </span>를 남겨주세요!
#                     </span>
#                     </div>#