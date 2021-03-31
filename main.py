from utils.policy_scraper import PolicyScraper
from utils.js_policy_counter import PolicyCounter
from utils.policy_writer import save_policy
from bs4 import BeautifulSoup
import re
import requests
import pickle
import time


def mapping_sequence(start_index):
    list_1 = []
    for i in range(10):
        list_1.append(start_index)
        start_index -= 1
    list_1 = [x + 10 if x < 0 else x for x in list_1]
    list_2 = [1, 2, 3, 4, 5] * 2

    return dict(zip(list_1, list_2))


def update_index(total_policy):
    """
    This function is for updating the urls need to be scraped.
    
    Inputs:
    :param total_policy: total policy counts
    :index_dict: contains three lists,
                 1. overall_list: all indice
                 2. processed_list: indice already been updated
                 3. unprocessed_list: indice need to be updated(includes those returned errors)
    """
    overall_pickle = open('overall_pickle.pickle', 'rb')
    try:
        while True:
            overall_list = pickle.load(overall_pickle)
    except EOFError:
        pass

    processed_pickle = open('processed_pickle.pickle', 'rb')
    try:
        while True:
            processed_list = pickle.load(processed_pickle)
    except EOFError:
        pass

    unprocessed_pickler = open('unprocessed_pickle.pickle', 'rb')
    try:
        while True:
            unprocessed_list = pickle.load(unprocessed_pickler)
    except EOFError:
        pass

    to_update = list(range(len(overall_list) + 1, total_policy + 1))
    overall_list.extend(to_update)
    unprocessed_list.extend(to_update)

    f = open('overall_pickle.pickle', 'wb')
    pickle.dump(overall_list, f)
    f.close()

    f = open('unprocessed_pickle.pickle', 'wb')
    pickle.dump(unprocessed_list, f)
    f.close()

    return overall_list, processed_list, unprocessed_list


def get_url(total_policy, policy_index):
    start_index = total_policy % 5
    sequence_dict = mapping_sequence(start_index)
    cur_url = f'http://sousuo.gov.cn/data?t=zhengcelibrary_gw&q=&timetype=timeqb&mintime=&maxtime=&sort' \
              f'=pubtime&sortType=1&searchfield=title&pcodeJiguan=&childtype=&subchildtype=&tsbq=&pubtimeyear' \
              f'=&puborg=&pcodeYear=&pcodeNum=&filetype=&p={(total_policy - policy_index) // 5}&n={5}&inpro=&bmfl' \
              f'=&dup=&orpro= '
    response = requests.get(cur_url)
    soup = BeautifulSoup(response.text, "html.parser")
    link = re.findall(r'\b(?:https?://)?(?:(?i:[a-z]+\.)+)[^\s,]+\b', str(soup))[sequence_dict[policy_index % 10] - 1]
    #     start_index if 0 < current_index <= start_index else 5
    return link


if __name__ == "__main__":
    url = 'http://sousuo.gov.cn/s.htm?q=&t=zhengcelibrary_gw&orpro='
    current_status = PolicyCounter(url)
    current_total = current_status.policy_counter()
    _, overall_processed_list, overall_unprocessed_list = update_index(current_total)

    while len(overall_unprocessed_list) > 0:
        current_index = overall_unprocessed_list[0]
        policy_url = get_url(current_total, current_index)
        try:
            if requests.get(policy_url).status_code != 404:
                save_policy(PolicyScraper(policy_url, current_index).get_info())
                overall_processed_list.append(current_index)
                overall_unprocessed_list.remove(current_index)
            else:
                pass

        finally:
            f_processed = open('processed_pickle.pickle', 'wb')
            pickle.dump(overall_processed_list, f_processed)
            f_processed.close()

            f_unprocessed = open('unprocessed_pickle.pickle', 'wb')
            pickle.dump(overall_unprocessed_list, f_unprocessed)
            f_unprocessed.close()
        time.sleep(6)
