import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# ========================
# Hàm chuẩn hoá chuỗi
# ========================
import re

def clear_format(text):
    text = re.sub(r'\W+', ' ', text)
    return ' '.join(text.lower().split())

# ========================
# Hàm tính Rank_HQ
# ========================
def check_rank_by_h_q(total_journals, percent, sjr_quartile):
    if total_journals >= 2000:
        thresholds = [0.5, 1, 5, 10, 18, 30, 43, 56, 69, 82]
    elif 1500 <= total_journals <= 1999:
        thresholds = [0.5, 2, 6, 11, 19, 31, 44, 57, 70, 83]
    elif 1000 <= total_journals <= 1499:
        thresholds = [0.5, 3, 7, 12, 20, 32, 45, 58, 71, 84]
    elif 500 <= total_journals <= 999:
        thresholds = [0.5, 4, 8, 13, 21, 33, 46, 59, 72, 85]
    elif 200 <= total_journals <= 499:
        thresholds = [0.9, 5, 10, 15, 23, 35, 48, 61, 74, 87]
    elif 50 <= total_journals <= 199:
        thresholds = [2.5, 6, 11, 16, 24, 36, 49, 62, 75, 88]
    elif 0 < total_journals < 50:
        thresholds = [3.5, 7, 15, 20, 28, 40, 53, 66, 79, 92]
    else:
        return 'None', 'None', 'Lỗi số lượng tạp chí'

    rank_h = next((i for i, th in enumerate(thresholds, start=0) if percent < th), 10)
    Top_Percent = '< ' + str(thresholds[rank_h]) if rank_h < len(thresholds) else '>= ' + str(thresholds[-1])

    if (rank_h == 0) and (sjr_quartile == 'Q1'):
        return 'Ngoại hạng', Top_Percent, ''
    elif (rank_h == 1) and (sjr_quartile == 'Q1'):
        return 'Hạng 1', Top_Percent, ''
    elif (rank_h == 2) and (sjr_quartile in ['Q1', 'Q2']):
        return 'Hạng 2', Top_Percent, ''
    elif (rank_h == 3) and (sjr_quartile in ['Q1', 'Q2']):
        return 'Hạng 3', Top_Percent, ''
    elif (rank_h == 4) and (sjr_quartile in ['Q1', 'Q2']):
        return 'Hạng 4', Top_Percent, ''
    elif (rank_h == 5) and (sjr_quartile in ['Q1', 'Q2', 'Q3']):
        return 'Hạng 5', Top_Percent, ''
    elif (rank_h == 6) and (sjr_quartile in ['Q1', 'Q2', 'Q3']):
        return 'Hạng 6', Top_Percent, ''
    elif (rank_h == 7) and (sjr_quartile in ['Q1', 'Q2', 'Q3']):
        return 'Hạng 7', Top_Percent, ''
    elif (rank_h == 8) and (sjr_quartile in ['Q1', 'Q2', 'Q3']):
        return 'Hạng 8', Top_Percent, ''
    elif (rank_h == 9) and (sjr_quartile in ['Q1', 'Q2', 'Q3', 'Q4']):
        return 'Hạng 9', Top_Percent, ''
    elif (rank_h == 10) and (sjr_quartile in ['Q1', 'Q2', 'Q3', 'Q4']):
        return 'Hạng 10', Top_Percent, ''
    else:
        return 'Không xếp hạng', Top_Percent, 'Không có Q phù hợp'

# ========================
# Hàm tìm kiếm
# ========================
def find_title_or_issn(name_or_issn):
    url_search_sjr = f"https://www.scimagojr.com/journalsearch.php?q={name_or_issn}"
    response = requests.get(url_search_sjr)
    soup = BeautifulSoup(response.content, 'html.parser')

    new_row = []
    STT = 0

    for link in soup.find_all('a', href=True):
        if 'journalsearch.php?q=' in link['href']:
            title_journal = link.find('span', class_='jrnlname').text
            id_scopus_journal = link['href'].split('q=')[1].split('&')[0]
            url_sjr_journal = f"https://www.scimagojr.com/journalsearch.php?q={id_scopus_journal}&tip=sid&clean=0"

            detail_response = requests.get(url_sjr_journal)
            detail_soup = BeautifulSoup(detail_response.content, 'html.parser')

            issn_sjr_homepage = 'N/A'
            publisher_sjr_homepage = 'N/A'
            STT += 1

            publisher_div = detail_soup.find('h2', string='Publisher')
            if publisher_div:
                publisher_p = publisher_div.find_next('p')
                if publisher_p:
                    publisher_sjr_homepage = publisher_p.text.strip()

            issn_div = detail_soup.find('h2', string='ISSN')
            if issn_div:
                issn_p = issn_div.find_next('p')
                if issn_p:
                    issn_sjr_homepage = issn_p.text.strip()

            new_row.append([STT, title_journal, issn_sjr_homepage, publisher_sjr_homepage, id_scopus_journal])

    df = pd.DataFrame(new_row, columns=['STT', 'Tên tạp chí', 'ISSN', 'Nhà xuất bản', 'ID Scopus'])
    return df

# ========================
# Lấy info chi tiết
# ========================
def id_scopus_to_all(id_scopus_input):
    url = f"https://www.scimagojr.com/journalsearch.php?q={id_scopus_input}&tip=sid&clean=0"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    name_journal = soup.find('h1').text.strip() if soup.find('h1') else 'N/A'

    country_tag = soup.find('h2', string='Country')
    country = country_tag.find_next('a').text.strip() if country_tag else 'N/A'

    treecategory_dict = {}
    subject_area_div = soup.find('h2', string='Subject Area and Category')
    if subject_area_div:
        categories = subject_area_div.find_next_sibling('p').find_all('li', recursive=True)
        for category in categories:
            subcategories = category.find_all('li')
            if subcategories:
                for subcategory in subcategories:
                    subcategory_name = subcategory.find('a').text.strip()
                    subcategory_code = subcategory.find('a')['href'].split('=')[-1]
                    treecategory_dict[subcategory_name] = subcategory_code
            else:
                category_name = category.find('a').text.strip()
                category_code = category.find('a')['href'].split('=')[-1]
                treecategory_dict[category_name] = category_code

    publisher_tag = soup.find('h2', string='Publisher')
    publisher = publisher_tag.find_next('a').text.strip() if publisher_tag else 'N/A'

    issn_tag = soup.find('h2', string='ISSN')
    issn_info = issn_tag.find_next('p').text.strip() if issn_tag else 'N/A'

    coverage_tag = soup.find('h2', string='Coverage')
    coverage = coverage_tag.find_next('p').text.strip() if coverage_tag else 'N/A'

    homepage_tag = soup.find('a', string='Homepage')
    homepage_link = homepage_tag['href'] if homepage_tag else 'N/A'

    how_to_publish_tag = soup.find('a', string='How to publish in this journal')
    how_to_publish_link = how_to_publish_tag['href'] if how_to_publish_tag else 'N/A'

    email_tag = soup.find('a', href=True, string=lambda x: x and '@' in x)
    email_question_journal = email_tag['href'].replace('mailto:', '') if email_tag else 'N/A'

    return name_journal, country, treecategory_dict, publisher, issn_info, coverage, homepage_link, how_to_publish_link, email_question_journal

# ========================
# Tìm hạng theo tên
# ========================
def check_rank_by_name_1_journal(search_name_journal, subject_area_category, year_check):
    row_add = []
    STT = 0

    def fetch_and_parse(url, category, id_category, total_journal, page_number):
        nonlocal STT
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 4:
                name_journal_web = cells[1].text.strip()
                if clear_format(search_name_journal) == clear_format(name_journal_web):
                    STT += 1
                    position_journal_by_name = cells[0].text.strip()
                    SJR_Q_value = cells[3].text.strip()
                    if ' ' in SJR_Q_value:
                        SJR_value, Q_value = SJR_Q_value.split()
                    else:
                        SJR_value, Q_value = SJR_Q_value, 'N/A'
                    h_index_value = cells[4].text.strip()
                    percent_value = round((float(position_journal_by_name) / total_journal * 100), 5)
                    rank_value, top_percent_value, note = check_rank_by_h_q(total_journal, percent_value, Q_value)
                    row_add.append([STT, name_journal_web, rank_value, Q_value, int(h_index_value), int(position_journal_by_name), int(total_journal), percent_value, top_percent_value, category, id_category, int(page_number), note])
                    break

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for category, id_category in subject_area_category.items():
            url_category = f"https://www.scimagojr.com/journalrank.php?category={id_category}&type=j&order=h&ord=desc&year={year_check}"
            response = requests.get(url_category)
            soup = BeautifulSoup(response.content, 'html.parser')
            pagination_div = soup.find('div', class_='pagination')
            total_journals_text = pagination_div.text.strip() if pagination_div else '0'
            total_journal = int(total_journals_text.split()[-1]) if total_journals_text.split() else 0

            for page_number in range(1, int(total_journal / 20) + 2):
                url = f"https://www.scimagojr.com/journalrank.php?category={id_category}&year={year_check}&type=j&order=h&ord=desc&page={page_number}&total_size={total_journal}"
                futures.append(executor.submit(fetch_and_parse, url, category, id_category, total_journal, page_number))

        for future in futures:
            future.result()

    df = pd.DataFrame(row_add, columns=['STT', 'Tên tạp chí', 'Hạng', 'Chỉ số Q', 'H-index', 'Vị trí', 'Tổng số tạp chí', 'Phần trăm', 'Top phần trăm', 'Chuyên ngành', 'ID Chuyên ngành', 'Trang', 'Ghi chú'])
    return df
