import json
import time
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

results = []

def parse(response):
    for comment in response.css('div.comment-item'):
        result = {}
        user_name = comment.css('div.comment-header div.user-name a::text').extract_first().strip()
        user_comment = comment.css('div.comment-body::text').extract_first().strip()
        #print(user_comment)
        result[user_name] = user_comment
        results.append(result)

def has_next_page(response):
    page_class = response.xpath('//ul[@class="pagination"]/li[2]/@class').extract_first().strip()
    return 'disabled' not in page_class

def goto_next_page(driver):
    #time.sleep(5) 
    link = driver.find_element_by_xpath('//ul[@class="pagination"]/li[2]')
    link.click()


def wait_page_return(driver,page):
    nextPage = driver.find_element_by_partial_link_text('下一页')
    driver.execute_script("arguments[0].scrollIntoView(false);", nextPage)
    time.sleep(5)
    #WebDriverWait(driver,10).until(EC.presence_of_element_located((By.LINK_TEXT,'下一页')))
    

def spider():
    driver = webdriver.Chrome()
    url = 'https://www.shiyanlou.com/courses/427'
    driver.get(url)
    page = 1
    while True:
        print('crawl page {}'.format(page))
        wait_page_return(driver,page)
        html = driver.page_source
        response = HtmlResponse(url=url,body=html.encode('utf8'))
        parse(response)
        if not has_next_page(response):
            break
        page += 1
        goto_next_page(driver)
    with open('comments.json','w') as f:
        f.write(json.dumps(results))

if __name__ == '__main__':
    spider()



