
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import time
import pickle


def extract_string_between(original_string, start_string, end_string):
    start_index = original_string.find(start_string)
    if start_index == -1:
        return None
    start_index += len(start_string)
    end_index = original_string.find(end_string, start_index)
    if end_index == -1:
        return None
    return original_string[start_index:end_index]


def extract_table(one_table_html):
    table_contain = {}
    table_name = None
    tr_tags_of_table = one_table_html.find_all('tr')
    table_name = tr_tags_of_table[0].th.text

    for tr_tag in tr_tags_of_table:
        td_tags_of_one_tr = tr_tag.find_all('td')
        if len(td_tags_of_one_tr) == 2:
            table_contain[td_tags_of_one_tr[0].text] = td_tags_of_one_tr[1].text
        else:
            None
    return table_name, table_contain


def extract_first_page_of_brands():
    url = 'https://www.gsmarena.com/makers.php3'
    gsm_base_url = 'https://www.gsmarena.com/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    time.sleep(10)

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse the HTML content of the page
        bs = BeautifulSoup(response.content, 'html.parser')
    else:
        print(f"Failed to retrieve the page: {url}. Status code: {response.status_code}")
        return


    brands = ["alcatel", "apple", "asus", "blu", "htc", "huawei", "infinix", "lenovo", "lg", "nokia", "samsung", "sony",
              "xiaomi", "zte"]
    all_divs = bs.find('div', {'class': 'st-text'})
    if all_divs:
        all_divs_a = all_divs.findAll('a')
    else:
        print("No div with class 'st-text' found.")
        return

    first_page_of_brands = {}
    for a_tag in all_divs_a:
        href = a_tag.get('href')
        parts = href.split('-')
        brand_name = parts[0]
        if brand_name in brands:
            first_page_of_brands[brand_name] = f"{gsm_base_url}{href}"
    return first_page_of_brands

def make_it_one_dictionary(one_device):
    sub_dict = {}

    for sub_dict_key, sub_dict_value in one_device.items():
        if isinstance(sub_dict_value, dict):
            if sub_dict_key in ['Tests','Display' , 'Battery','Main Camera', 'Selfie camera']:
                for key, value in sub_dict_value.items():
                    new_key = f"{sub_dict_key} {key}"
                    sub_dict[new_key] = value
            else:
                for key, value in sub_dict_value.items():
                    sub_dict[key] = value
        else:
            sub_dict[sub_dict_key] = sub_dict_value
    if '\xa0' in sub_dict:
        del sub_dict['\xa0']

    return sub_dict
def extract_data(url):
    soup = BeautifulSoup()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    phone_name = extract_string_between(url, 'https://www.gsmarena.com/', '-').replace("_", " ")
    time.sleep(1)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
    else:
        print(f"Failed to extract data from page. Status code: {response.status_code}")
        return
    tables = soup.find_all('table', {'cellspacing': '0'})
    tables_extracted_data = {}
    tables_extracted_data['phone_name'] = phone_name
    print('------------------------')

    for table in tables:
        table_name, table_contain = extract_table(table)
        tables_extracted_data[table_name] = table_contain
    return tables_extracted_data


def extract_data_of_one_brand(first_page_of_brand):
    extracted_data_of_brand = []
    count = 0
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    time.sleep(1)
    gsm_base_url = 'https://www.gsmarena.com/'
    print(extract_string_between(first_page_of_brand , gsm_base_url , '-'))
    href_of_brand = first_page_of_brand[len(gsm_base_url):]

    response = requests.get(first_page_of_brand, headers=headers)

    if response.status_code == 200:
        # Parse the HTML content of the page
        bs_url = BeautifulSoup(response.content, 'html.parser')
    else:
        print(f"Failed to retrieve the first page of brand: {first_page_of_brand}. Status code: {response.status_code}")
        return

    page_href = bs_url.find('div', attrs={'class': 'review-nav-v2'}).findAll('a')
    href_last_href = page_href[-2].get('href')
    last_page = href_last_href.split('-')[-1].split('.')[0]
    last_page_number = int(last_page.replace('p' , ''))
    for page_n in range(1, last_page_number + 1):

        page_count_url = f"{gsm_base_url}{href_of_brand.split('-')[0]}-{href_of_brand.split('-')[1]}-f-{href_of_brand.split('-')[2].split('.')[0]}-0-p{page_n}.php"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        time.sleep(5)
        response2 = requests.get(page_count_url, headers=headers)
        page_url = BeautifulSoup(response2.content, 'html.parser')
        all_devices = page_url.find('div', {'id': 'review-body', 'class': 'section-body'}).findAll('a')
        for d_index, device in enumerate(all_devices, start=1):
            device_href = device.get('href')
            gsm_base_url = 'https://www.gsmarena.com/'
            device_url = f"{gsm_base_url}{device_href}"
            count += 1
            print(count)
            print(extract_data(device_url))
            extracted_data_of_brand.append(extract_data(device_url))
    return extracted_data_of_brand

brands = ["alcatel", "apple", "asus", "blu", "htc", "huawei", "infinix", "lenovo", "lg", "nokia", "samsung", "sony",
              "xiaomi", "zte"]
one_dic_list = []

urls_of_brands_first_page = extract_first_page_of_brands()

extracted_data_of_one_brand = extract_data_of_one_brand(urls_of_brands_first_page['samsung'])
for device in extracted_data_of_one_brand:
    one_dic_list.append(make_it_one_dictionary(device))

with open('samsung.pkl', 'wb') as file:
        pickle.dump(one_dic_list, file)
