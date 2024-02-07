import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
import re
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import time
import random

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
        # subsection_name = td_tags_of_one_tr[0].a.text.strip()
        # table_contain.append(subsection_name)
        if (len(td_tags_of_one_tr) == 2):
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

    #bs = BeautifulSoup(response.content, 'html.parser')

    brands = ["alcatel", "apple", "asus", "blu", "htc", "huawei", "infinix", "lenovo", "lg", "nokia", "samsung", "sony",
              "xiaomi", "zte"]
    all_divs = bs.find('div', {'class': 'st-text'})
    if all_divs:
        all_divs_a = all_divs.findAll('a')
        # Your remaining code that relies on all_divs_a
    else:
        print("No div with class 'st-text' found.")
        return
        # Handle this case appropriately based on your requirements

    first_page_of_brands = {}
    for a_tag in all_divs_a:
        href = a_tag.get('href')
        parts = href.split('-')
        brand_name = parts[0]
        if brand_name in brands:
            first_page_of_brands[brand_name] = f"{gsm_base_url}{href}"
    return first_page_of_brands


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
    #print(url)

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
    urls = []

    response = requests.get(first_page_of_brand, headers=headers)

    if response.status_code == 200:
        # Parse the HTML content of the page
        bs_url = BeautifulSoup(response.content, 'html.parser')
    else:
        print(f"Failed to retrieve the first page of brand: {first_page_of_brand}. Status code: {response.status_code}")
        return
    #bs_url = BeautifulSoup(response1.content, 'html.parser')

    page_href = bs_url.find('div', attrs={'class': 'review-nav-v2'}).findAll('a')
    href_last_href = page_href[-2].get('href')
    last_page = href_last_href.split('-')[-1].split('.')[0]
    last_page_number = last_page[-1]
    for page_num_str in last_page_number:
        page_num = int(page_num_str)
        for page_n in range(1, page_num + 1):
            page_count_url = f"{gsm_base_url}{href_of_brand.split('-')[0]}-{href_of_brand.split('-')[1]}-f-{href_of_brand.split('-')[2].split('.')[0]}-0-p{page_n}.php"

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            time.sleep(5)
            response2 = requests.get(page_count_url, headers=headers)
            page_url = BeautifulSoup(response2.content, 'html.parser')
            all_devices = page_url.find('div', {'id': 'review-body', 'class': 'section-body'}).findAll('a')
            for d_index, device in enumerate(all_devices, start=1):
                # if d_index > 2:
                # break
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

urls_of_brands_first_page = extract_first_page_of_brands()

extracted_data_of_one_brand = extract_data_of_one_brand(urls_of_brands_first_page['infinix'])
print(extracted_data_of_one_brand)
print(len(extracted_data_of_one_brand))
df = pd.DataFrame(extracted_data_of_one_brand)
