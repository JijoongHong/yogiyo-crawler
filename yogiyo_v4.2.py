#!/usr/bin/env python
# coding: utf-8

# In[22]:


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
    name = location.split(" ")[1]
    list_url = "https://www.yogiyo.co.kr/mobile/#/"
    parsed_data = pd.read_csv("./"+name+"_"+food_category+".csv")
    parsed_store = parsed_data['가게명'].unique()
    print(parsed_store)
    #### 주소 기준으로 초기화
    driver = webdriver.Chrome('/Users/jijoonghong/Downloads/chromedriver')
    # driver2 = webdriver.Chrome('/Users/jijoonghong/Downloads/chromedriver')

    driver.get(list_url)
    time.sleep(8)
    element = driver.find_element_by_name("address_input")
    element.clear()
    element.send_keys(address)
    btn = driver.find_element_by_css_selector("#button_search_address > button.btn.btn-default.ico-pick")
    btn.click()
    time.sleep(2)

    # 리뷰 많은 순으로 sorting
    driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div[2]/div/select').click()
    driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div[2]/div/select/option[3]').click()
    driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div[2]/div/select').click()
    time.sleep(3)

    # 카테고리 순 접속하고 끝까지 내려가기
    df = pd.DataFrame(columns=['시', '구', '업종명', '가게명', '년', '월', '전체평점', '맛 평점', '양 평점', '배달 평점', '리뷰 내용', '주문 내역'])

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
    print(len(store_list))

    try:
        for i in tqdm(range(1, len(store_list) + 1)):
            time.sleep(3)

            path = '//*[@id="content"]/div/div[5]/div/div/div[' + str(i) + ']/div'

            if i <= 60:
                # id가 something 인 element 를 찾음
                try:
                    n = driver.find_element_by_css_selector(
                        "#content > div > div:nth-child(5) > div > div > div:nth-child(" + str(
                            i) + ") > div > table > tbody > tr > td:nth-child(2) > div > div.stars > span:nth-child(2)").text
                    if n == "" or int(n.split(" ")[1]) < 10:
                        continue
                    # 이미 크롤링 된 데이터면 pass
                    store_name = driver.find_element_by_xpath('//*[@id="content"]/div/div[5]/div/div/div['+str(i)+']/div/table/tbody/tr/td[2]/div/div[1]').text
                    if store_name in parsed_store:
                        continue
                    some_tag = driver.find_element_by_xpath(path)
                except:
                    time.sleep(5)
                    n = driver.find_element_by_css_selector(
                        "#content > div > div:nth-child(5) > div > div > div:nth-child(" + str(
                            i) + ") > div > table > tbody > tr > td:nth-child(2) > div > div.stars > span:nth-child(2)").text
                    if n == "" or int(n.split(" ")[1]) < 10:
                        continue
                    # 이미 크롤링 된 데이터면 pass
                    store_name = driver.find_element_by_xpath('//*[@id="content"]/div/div[5]/div/div/div['+str(i)+']/div/table/tbody/tr/td[2]/div/div[1]').text
                    if store_name in parsed_store:
                        continue
                    some_tag = driver.find_element_by_xpath(path)
                # somthing element 까지 스크롤
                action = ActionChains(driver)
                action.move_to_element(some_tag).perform()
                driver.find_element_by_xpath(path).click()
                print(i)
                time.sleep(2)
            else:
                try:
                    n = driver.find_element_by_css_selector(
                        "#content > div > div:nth-child(5) > div > div > div:nth-child(" + str(
                            i) + ") > div > table > tbody > tr > td:nth-child(2) > div > div.stars > span:nth-child(2)").text
                except:
                    for j in range(int(i // 60)):
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(int(i // 60)*2)
                    # id가 something 인 element 를 찾음

                try:
                    # 리뷰 10개 이하면 pass
                    n = driver.find_element_by_css_selector(
                        "#content > div > div:nth-child(5) > div > div > div:nth-child(" + str(
                            i) + ") > div > table > tbody > tr > td:nth-child(2) > div > div.stars > span:nth-child(2)").text
                    store_name = driver.find_element_by_xpath('//*[@id="content"]/div/div[5]/div/div/div['+str(i)+']/div/table/tbody/tr/td[2]/div/div[1]').text
                    some_tag = driver.find_element_by_xpath(path)

                except:
                    time.sleep(10)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    n = driver.find_element_by_css_selector(
                        "#content > div > div:nth-child(5) > div > div > div:nth-child(" + str(
                            i) + ") > div > table > tbody > tr > td:nth-child(2) > div > div.stars > span:nth-child(2)").text
                    store_name = driver.find_element_by_xpath('//*[@id="content"]/div/div[5]/div/div/div['+str(i)+']/div/table/tbody/tr/td[2]/div/div[1]').text
                    some_tag = driver.find_element_by_xpath(path)

                if n == "" or int(n.split(" ")[1]) < 10:
                    continue

                if store_name in parsed_store:
                    continue

                # somthing element 까지 스크롤
                action = ActionChains(driver)
                action.move_to_element(some_tag).perform()
                driver.find_element_by_xpath(path).click()
                print(i)
                time.sleep(int(i // 60))

            num_of_review = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div[5]/div[2]/div/strong[1]')
            #store_name = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div[1]/div[1]/span').text

            try:
                review = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a')
            except:
                time.sleep(3)
                review = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a')

            driver.execute_script("arguments[0].click();", review)
            time.sleep(1)

            try:
                num_of_review = driver.find_element_by_xpath(
                    '//*[@id="content"]/div[2]/div[1]/div[5]/div[2]/div/strong[1]')
                if num_of_review == '':
                    num_of_review = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a/span')
            except:
                time.sleep(3)
                num_of_review = driver.find_element_by_xpath(
                    '//*[@id="content"]/div[2]/div[1]/div[5]/div[2]/div/strong[1]')
                if num_of_review == '':
                    num_of_review = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a/span')

            j = 0
            idx = 11
            print(int(num_of_review.text))

            if int(num_of_review.text) < 10:
                driver.back()
                continue

            max_idx = int(num_of_review.text) // 10

            while True:
                if j == max_idx:
                    html = driver.page_source
                    break
                try:
                    driver.find_element_by_css_selector('#review > li.list-group-item.btn-more > a').click()
                    time.sleep(1.5)

                    dates = driver.find_element_by_xpath(
                        "// *[ @ id = 'review'] / li[" + str(idx) + "] / div[1] / span[2]").text
                    if "전" in dates or "어제" in dates or int(dates.split("년")[0]) > 2019:
                        pass
                    elif int(dates.split("년")[0]) == 2019 and int(dates.split(" ")[1][:-1]) >= 3:
                        pass
                    else:
                        html = driver.page_source
                        break

                except Exception as e:
                    print(e)
                    time.sleep(3)
                    driver.find_element_by_css_selector('#review > li.list-group-item.btn-more > a').click()
                    time.sleep(1.5)

                    dates = driver.find_element_by_xpath(
                        "// *[ @ id = 'review'] / li[" + str(idx) + "] / div[1] / span[2]").text
                    if "전" in dates or "어제" in dates or int(dates.split("년")[0]) > 2019:
                        pass
                    elif int(dates.split("년")[0]) == 2019 and int(dates.split(" ")[1][:-1]) >= 3:
                        pass
                    else:
                        html = driver.page_source
                        break
                j += 1
                idx += 10

            soup = BeautifulSoup(html, 'html.parser')
            reviews = soup.find_all(class_='list-group-item star-point ng-scope')

            for review in reviews:
                if "전" in review.find(class_="review-time ng-binding").get_text() or (
                        "어제" in review.find(class_="review-time ng-binding").get_text()):
                    year = 2021
                    month = datetime.date.today().month
                else:
                    year = int(review.find(class_="review-time ng-binding").get_text().split("년")[0])
                    month = int(review.find(class_="review-time ng-binding").get_text().split(" ")[1][0])

                comment = review.find('p', attrs={'ng-show': 'review.comment'})
                comment = comment.get_text().replace("\n", " ").replace("  ", " ")
                menu = review.find('div', attrs={'class': "order-items default ng-binding"}).get_text()
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

                row = pd.DataFrame(
                    [(address.split(" ")[0], address.split(" ")[1], food_category, store_name, year, month,
                      len(overall), taste, quantity, delivery, comment, menu)],
                    columns=['시', '구', '업종명', '가게명', '년', '월', '전체평점', '맛 평점', '양 평점', '배달 평점', '리뷰 내용', '주문 내역'])

                df = df.append(row)

            driver.back()
            time.sleep(2)

    except Exception as e:
        name = location.split(" ")[1]
        df_name = "{}_{}".format(name, food_category)
        df.to_csv("./{}2_비정상종료.csv".format(df_name), encoding='utf-8-sig')
        print("종료위치 {} - {} - {}".format(food_category, i, idx))
        print(e)


    df_name = "{}_{}".format(name, food_category)
    df.to_csv("./{}2.csv".format(df_name), encoding='utf-8-sig')


def main():
    #categories = ["프랜차이즈", "치킨", "피자양식", "중국집", "한식", "일식돈까스", "족발보쌈", "야식", "분식", "카페디저트"]
    categories = ["한식", "일식돈까스", "족발보쌈", "야식", "분식", "카페디저트"]
    final_start = datetime.datetime.now()

    for category in categories:
        start = datetime.datetime.now()
        yogiyo_crawling('서울 강남구 학동로 426 강남구청', category)
        end = datetime.datetime.now()
        t = end - start
        hours, remainder = divmod(t.seconds, 3600)
        print("{} : {}시간 {}분".format(category, hours, remainder))

    final_end = datetime.datetime.now()

    t = final_end - final_start
    hours, remainder = divmod(t.seconds, 3600)
    print(final_start)
    print(final_end)
    print("전체소요시간 : {}시간 {}분".format(hours, remainder))


if __name__ == "__main__":
    main()
