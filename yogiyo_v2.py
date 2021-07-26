from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import pandas as pd
import time
import datetime

region = "서울특별시"
post_num = 140201
address = '수송동 146-12'
# category = ["1인분주문", "프랜차이즈", "치킨", "피자양식", "중국집", "한식",
#            "일식돈까스", "족발보쌈", "야식", "분식", "카페디저트", "편의점마트"]
category = ["한식"]
list_url = "https://www.yogiyo.co.kr/mobile/#/"

#### 주소 기준으로 초기화
driver = webdriver.Chrome('/Users/jijoonghong/Downloads/chromedriver')
# driver2 = webdriver.Chrome('/Users/jijoonghong/Downloads/chromedriver')

driver.get(list_url)
time.sleep(4)
element = driver.find_element_by_name("address_input")
element.clear()
element.send_keys(address)
btn = driver.find_element_by_css_selector("#button_search_address > button.btn.btn-default.ico-pick")
btn.click()
time.sleep(1)

# 리뷰 많은 순으로 sorting
driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div[2]/div/select').click()
driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div[2]/div/select/option[3]').click()
driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div[2]/div/select').click()
time.sleep(1)

# 카테고리 순 접속하고 끝까지 내려가기
df = pd.DataFrame(columns=['시', '구', '업종명', '가게명', '년', '월', '전체평점', '맛 평점', '양 평점', '배달 평점', '리뷰 내용'])

for c in category:
    driver.get(list_url + c)
    last_height = driver.execute_script("return document.body.scrollHeight")
    # print(last_height)

    while True:

        scroll_down = 0
        while scroll_down < 10:
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
            scroll_down += 1

        new_height = driver.execute_script("return document.body.scrollHeight")
        # print("new"+str(new_height))
        if new_height == last_height:
            print("끝")
            break

        last_height = new_height

    # height = driver.find_elements_by_css_selector('#content > div > div:nth-child(4) > div > div.restaurant-list')
    store_list = driver.find_elements_by_xpath("//div[@class='item clearfix']")

    # print(l.text)
    # store = driver.find_element_by_css_selector("#content > div > div:nth-child(4) > div > div.restaurant-list > div:nth-child(1)")
    print(store_list)

    for i in range(70, len(store_list)):
        path = '//*[@id="content"]/div/div[5]/div/div/div[' + str(i) + ']/div'

        if i // 60 == 0:
            # id가 something 인 element 를 찾음
            some_tag = driver.find_element_by_xpath(path)
            # somthing element 까지 스크롤
            action = ActionChains(driver)
            action.move_to_element(some_tag).perform()
            driver.find_element_by_xpath(path).click()
            print(i)
            time.sleep(2)
        else:
            for j in range(int(i // 60)):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(int(i // 60))
            # id가 something 인 element 를 찾음
            try:
                some_tag = driver.find_element_by_xpath(path)
            except:
                time.sleep(int(i // 60))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                some_tag = driver.find_element_by_xpath(path)
            # somthing element 까지 스크롤
            action = ActionChains(driver)
            action.move_to_element(some_tag).perform()
            driver.find_element_by_xpath(path).click()
            print(i)
            time.sleep(int(i // 60))

        review = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a')
        driver.execute_script("arguments[0].click();", review)
        time.sleep(1)
        num_of_review = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div[5]/div[2]/div/strong[1]')

        i = 0
        idx = 12
        print(int(num_of_review.text))
        if int(num_of_review.text) < 10:
            break

        while True:
            if i == int(int(num_of_review.text) / 10):
                break
            xpath = '//*[@id="review"]/li[' + str(idx) + ']/a'
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            get_next = driver.find_element_by_xpath(xpath).click()

            # driver.execute_script("arguments[0].click();", get_next)
            time.sleep(1.5)
            i += 1
            idx += 10

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        reviews = soup.find_all(class_='list-group-item star-point ng-scope')

        for review in reviews:
            if "전" in review.find(class_="review-time ng-binding").get_text() or (
                    "어제" in review.find(class_="review-time ng-binding").get_text()) or (
                    2019 <= int(review.find(class_="review-time ng-binding").get_text().split("년")[0]) and 3 <= int(
                    review.find(class_="review-time ng-binding").get_text().split(" ")[1][0])):
                if "전" in review.find(class_="review-time ng-binding").get_text() or (
                        "어제" in review.find(class_="review-time ng-binding").get_text()):
                    year = 2021
                    month = datetime.date.today().month
                else:
                    year = int(review.find(class_="review-time ng-binding").get_text().split("년")[0])
                    month = int(review.find(class_="review-time ng-binding").get_text().split(" ")[1][0])

                #comments = review.find_all(class_="ng-binding")
                comment = review.find('p', attrs={'ng-show': 'review.comment'})
                #comment = comments[-1].get_text().replace("\n", " ").replace("  ", " ")
                comment = comment.get_text().replace("\n", " ").replace("  ", " ")

                overall = review.find_all(class_="full ng-scope")
                points = review.find_all(class_="points ng-binding")
                try:
                    taste = int(points[0].get_text())
                except:
                    taste = ""
                try:
                    quantity = int(points[1].get_text())
                except:
                    quantity = ""
                try:
                    delivery = int(points[2].get_text())
                except:
                    delivery = ""
                store_name = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div[1]/div[1]/span').text
                row = pd.DataFrame([(address.split(" ")[0], address.split(" ")[1], c, store_name, year, month,
                                     len(overall), taste, quantity, delivery, comment)],
                                   columns=['시', '구', '업종명', '가게명', '년', '월', '전체평점', '맛 평점', '양 평점', '배달 평점', '리뷰 내용'])

                df = df.append(row)
        driver.back()
        time.sleep(2)

df.to_csv("./test.csv", encoding='utf-8-sig')

#### 전체 가게 리스트 뽑아오기

#### 기준 충족하는 가게인지 확인하고 <div class="restaurants-info">
# 가게 이름 :<div class="restaurant-name ng-binding" ng-bind="restaurant.name" title="만년닭강정-봉천점">만년닭강정-봉천점</div>
# 전 별점 :<span class="ico-star1 ng-binding" ng-show="restaurant.review_avg > 0">★ 4.8</span>
# 리뷰 갯수 :<span class="review_num ng-binding" ng-show="restaurant.review_count > 0">


#### 내부로 들어가서 리뷰탭으로 들어가기(동적)

#### 리뷰 끝까지 내려가기
# <li class="list-group-item btn-more ng-hide" ng-show="check_more_review()">
#           <a ng-click="get_next_reviews()"><span>더 보기<i class="arr-down"></i></span></a>
#         </li>


#### 리뷰 리스트 뽑아오기 (동적)
# <ul id="review" class="list-group review-list"> 내부의
# <li class="list-group-item ng-hide" ng-show="restaurant.reviews.length < 1">…</li> 제외하고
# <li class="list-group-item star-point ng-scope" ng-repeat="review in restaurant.reviews" on-finish-render="scrollCartArea()">…</li>

#### 리뷰 리스트에서 리뷰글, 전체평점, 맛, 양, 배달 점수 가져오기
# 리뷰글 <p ng-show="review.comment" ng-bind-html="review.comment|strip_html" class="ng-binding"> 리뷰내용 </p>
# 평점 <div class="star-point">
# 전체평점 <span class="total">에서 <span class="full ng-score"의 갯수
# 각 평점 <span class="category">에서 <span class="points ng-binding">
# 맛 : <span class="points ng-binding" ng-show="review.rating_taste > 0"> 점수 </span>
# 양 : <span class="points ng-binding" ng-show="review.rating_quantity > 0">5</span>
# 배달 : <span class="points ng-binding" ng-show="review.rating_delivery > 0">5</span>

# 구가 하나 끝나면 데이터 저장하기