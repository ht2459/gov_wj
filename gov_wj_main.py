#!/usr/bin/env python
# coding: utf-8


from utils.policy_scraper import PolicyScraper
from utils.js_policy_counter import PolicyCounter, extract_url
from utils.policy_writer import save_policy
import requests
import pickle
import time
import math

previous_page_count = 0
previous_policy_count = 0

url = 'http://sousuo.gov.cn/s.htm?q=&t=zhengcelibrary_gw&orpro='

gov_wj = {}
error_dict = {}

while True:
    current_status = PolicyCounter(url)

    current_policy_count = current_status.policy_counter()
    policy2update = current_policy_count - previous_policy_count
    #     current_page_count = current_status.page_counter()
    #     page2update = current_page_count - previous_page_count

    for page in range(math.ceil(policy2update / 5)):
        n = min(5, policy2update)
        policy_urls = extract_url(page, n)
        current_status.clean_up()
        for index, policy_url in enumerate(policy_urls):
            if requests.get(policy_url).status_code != 404:
                gov_wj[policy2update - index] = PolicyScraper(policy_url, policy2update - index).get_info()
                save_policy(gov_wj[policy2update - index])
            else:
                gov_wj[policy2update - index] = policy_url
                error_dict[policy2update - index] = policy_url
            time.sleep(15)  # 建议设置久一点
        policy2update -= n

    previous_policy_count = current_policy_count

    with open('gov_wj.pickle', 'wb') as handle:
        pickle.dump(gov_wj, handle)

    with open('error_dict.pickle', 'wb') as handle:
        pickle.dump(error_dict, handle)

    time.sleep(43200)

    for error_index, error_url in error_dict.items():
        if requests.get(error_url).status_code != 404:
            gov_wj[error_index].update({gov_wj[error_index]: PolicyScraper(error_url, error_index).get_info()})
            save_policy(gov_wj[error_index])
            del error_dict[error_index]
        else:
            pass

# import mysql.connector
# import pandas as pd

# con = mysql.connector.connect(host='localhost',
#                     port =3306,
#                     database='gov_policy',
#                     user='你的用户名',
#                     password='你的密码',
#                     connect_timeout=20)
# my_cursor = con.cursor()

# my_cursor.execute("""CREATE TABLE gwy_wj (seq_id int, pub_url VARCHAR(255), index_id VARCHAR(255),
#                             gov_theme VARCHAR(255), pub_dept VARCHAR(255), orig_date VARCHAR(255),
#                             doc_title VARCHAR(255), pub_id VARCHAR(255), pub_date  VARCHAR(255),
#                             gov_theme_key_word  VARCHAR(255), doc_content LONGBLOB ,
#                             doc_attr_outerHTML LONGBLOB , doc_content_outerHTML LONGBLOB )""")


# In[ ]:


# pd.read_sql('SELECT * FROM gwy_wj',con)
# df.doc_content.decode("utf-8")
