from selenium import webdriver
# from pyvirtualdisplay import Display
from urllib.error import HTTPError
import warnings
warnings.filterwarnings('ignore')


class PolicyScraper:
    """
    爬虫国务院文件
    传入链接，返还链接内的全部内容，生成字典
    """

    def __init__(self, url, seq_id):
        self.url = url
        self.seq_id = seq_id
#         self.display = Display(visible=0, size=(800, 600)).start()
#         self.driver = webdriver.Firefox(executable_path='geckodriver')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(url)

    def get_info(self):
        link = {}
        try:
            link['seq_id'] = self.seq_id  # 序列ID，从0—现有的文件数
            link['pub_url'] = self.url  # 原文链接
            link['index_id'] = self.driver.find_element_by_xpath(
                "//div[@class='wrap']/table[1]//tr[1]/td[2]").text  # 索引号
            link['gov_theme'] = self.driver.find_element_by_xpath(
                "//div[@class='wrap']/table[1]//tr[1]/td[4]").text  # 主题分类
            link['pub_dept'] = self.driver.find_element_by_xpath(
                "//div[@class='wrap']/table[1]//tr[2]/td[2]").text  # 发文机关
            link['orig_date'] = self.driver.find_element_by_xpath(
                "//div[@class='wrap']/table[1]//tr[2]/td[4]").text  # 成文日期
            link['doc_title'] = self.driver.find_element_by_xpath(
                "//div[@class='wrap']/table[1]//tr[3]/td[2]").text  # 标题
            link['pub_id'] = self.driver.find_element_by_xpath(
                "//div[@class='wrap']/table[1]//tr[4]/td[2]").text  # 发文字号
            link['pub_date'] = self.driver.find_element_by_xpath(
                "//div[@class='wrap']/table[1]//tr[4]/td[4]").text  # 发布日期
            link['gov_theme_key_word'] = self.driver.find_element_by_xpath(
                "//div[@class='wrap']/table[1]//table[2]//tr/td[2]").text  # 主题词
            link['effective_thru'] = self.driver.find_element_by_xpath(
                "//div[@class='wrap']/table[1]//table[2]//tr/td[4]").text  # 时效
            link['doc_content'] = self.driver.find_element_by_xpath("//*[@id='UCAP-CONTENT']").text  # 内容
            link['doc_attr_outerHTML'] = self.driver.find_element_by_xpath(
                "/html/body/div[@class='w1100']/div[@class='wrap']/table[1]").get_attribute('outerHTML')  # 属性格式
            link['doc_content_outerHTML'] = self.driver.find_element_by_xpath(
                "/html/body/div[@class='w1100']/div[@class='wrap']/table[2]/tbody/tr/td[1]").get_attribute('outerHTML')  # 内容_格式
#             link['doc_content'] = self.driver.find_element_by_xpath("//*[@id='UCAP-CONTENT']").text  # 内容
#             link['doc_attr_outerHTML'] = self.driver.find_element_by_xpath(
#                 "/html/body/div[6]/div[3]/table[1]").get_attribute('outerHTML')  # 属性格式
#             link['doc_content_outerHTML'] = self.driver.find_element_by_xpath(
#                 "/html/body/div[6]/div[3]/table[2]/tbody/tr/td[1]").get_attribute('outerHTML')  # 内容_格式

        except HTTPError:
            return None

#         self.display.stop()
        self.driver.quit()

        return link
