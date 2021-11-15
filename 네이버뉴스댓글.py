from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime

import time
import csv
import os


# crawling comments on the Naver News politics section of 중앙일보.
def get_comments(url, imp_time=5, delay_time=0.1):
    comment_url = url + '&m_view=1'
    # Web driver
    driver_loc = '/Users/kwounsulee/PycharmProjects/study/chromedriver'
    driver = webdriver.Chrome(driver_loc)
    driver.implicitly_wait(imp_time)
    driver.get(url)

    # check if it's politics news
    section = driver.find_element_by_css_selector('em.guide_categorization_item').text
    if section != '정치':
        return []

    driver.get(comment_url)
    # click '더보기'
    while True:
        try:
            view_more = driver.find_element_by_css_selector('a.u_cbox_btn_more')
            view_more.click()
            time.sleep(delay_time)
        except:
            break

    # BeautifulSoup
    html = driver.page_source
    bs = BeautifulSoup(html, 'lxml')

    # get comments
    comments = bs.select('span.u_cbox_contents')
    comments = [comment.text for comment in comments]

    driver.quit()
    os.system("killall -9 'Google Chrome'")

    return comments


if __name__ == '__main__':
    comment_data_list = []
    page_num_last_three = 863

    count = 0
    while count < 10:  # 뉴스 개수
        newspaper = '025'  # 중앙일보
        page_num = '0003098' + str(page_num_last_three)
        url = f'https://news.naver.com/main/read.nhn?sid1=100&oid={newspaper}&aid={page_num}'
        comment_data = get_comments(url, 5, 0.1)

        # count when it's in politics section and has any comments
        page_num_last_three -= 1
        if len(comment_data) > 0:
            comment_data_list.append(comment_data)
            count += 1

    # Write CSV file
    now = datetime.now()

    with open('politics_news_comments.csv', 'w', encoding='utf-8-sig', newline='') as f:
        fieldnames = ['comment']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for comment_data in comment_data_list:
            for comment in comment_data:
                writer.writerow({'comment': comment})
© 2021 GitHub, Inc.
Terms
Privacy
Security
Status
Docs
