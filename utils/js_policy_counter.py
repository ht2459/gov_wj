from selenium import webdriver
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re
import os


def extract_url(page, n):
    policy_url = f'http://sousuo.gov.cn/data?t=zhengcelibrary_gw&q=&timetype=timeqb&mintime=&maxtime=&sort' \
                 f'=pubtime&sortType=1&searchfield=title&pcodeJiguan=&childtype=&subchildtype=&tsbq=&pubtimeyear' \
                 f'=&puborg=&pcodeYear=&pcodeNum=&filetype=&p={page}&n={n}&inpro=&bmfl=&dup=&orpro= '
    response = requests.get(policy_url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = re.findall(r'\b(?:https?://)?(?:(?i:[a-z]+\.)+)[^\s,]+\b', str(soup))

    return links


class PolicyCounter:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.PhantomJS(
            executable_path='/utils/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')  # 设置phantomjs的路径
        self.driver.get(url)

    def policy_counter(self):
        policy_count = self.driver.find_element_by_xpath("//div[@class='middle_result']/ul").text
        policy_count = int(re.findall(r"\d+", policy_count)[0])

        return policy_count

    def page_counter(self):
        page_count = self.driver.find_element_by_xpath("/html/body/div[6]/div[6]/div[2]/div[3]/span[1]").text
        page_count = int(re.findall(r"\d+", page_count)[0])

        return page_count

    def take_log(self):
        if not os.path.exists('/updating_log.txt'):
            file = open('updating_log.txt', 'w+')

        else:
            file = open('updating_log.txt', 'a')

        file.write(f'\n当前时间 {str(datetime.now())} 国务院文件共计 {self.page_counter()} 页，文件共计 {self.policy_counter()} 条')
        file.close()

    def clean_up(self):
        self.driver.quit()
