from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from tqdm import tqdm
import pandas as pd
import time
import datetime


def yogiyo_crawling(location, food_category):
    address = location
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

    driver.get(list_url + food_category)
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

    for i in tqdm(range(70, len(store_list))):
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

                comment = review.find('p', attrs={'ng-show': 'review.comment'})
                comment = comment.get_text().replace("\n", " ").replace("  ", " ")
                print(comment)
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
                row = pd.DataFrame(
                    [(address.split(" ")[0], address.split(" ")[1], food_category, store_name, year, month,
                      len(overall), taste, quantity, delivery, comment)],
                    columns=['시', '구', '업종명', '가게명', '년', '월', '전체평점', '맛 평점', '양 평점', '배달 평점', '리뷰 내용'])

                df = df.append(row)

            else:
                break
        driver.back()
        time.sleep(2)
    df_name = "{}_{}".format(location, food_category)
    df.to_csv("./{}.csv".format(df_name), encoding='utf-8-sig')


yogiyo_crawling('수송동 146-12', '한식')