import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import re

# ========================
# Chuẩn hoá chuỗi
# ========================
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

    rank_h = next((i for i, th in enumerate(thresholds) if percent < th), 10)
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
# Hàm chính: tìm tạp chí
# ========================
def find_title_or_issn(name_or_issn):
    url = f"https://www.scimagojr.com/journalsearch.php?q={name_or_issn}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    rows = []
    STT = 0

    for link in soup.find_all('a', href=True):
        if 'journalsearch.php?q=' in link['href']:
            title_journal = link.find('span', class_='jrnlname').text
            id_scopus_journal = link['href'].split('q=')[1].split('&')[0]
            detail_url = f"https://www.scimagojr.com/journalsearch.php?q={id_scopus_journal}&tip=sid&clean=0"
            detail_response = requests.get(detail_url)
            detail_soup = BeautifulSoup(detail_response.content, 'html.parser')

            issn = 'N/A'
            publisher = 'N/A'
            STT += 1

            pub_div = detail_soup.find('h2', string='Publisher')
            if pub_div:
                pub_p = pub_div.find_next('p')
                if pub_p:
                    publisher = pub_p.text.strip()

            issn_div = detail_soup.find('h2', string='ISSN')
            if issn_div:
                issn_p = issn_div.find_next('p')
                if issn_p:
                    issn = issn_p.text.strip()

            rows.append([STT, title_journal, issn, publisher, id_scopus_journal])

    return pd.DataFrame(rows, columns=['STT', 'Tên tạp chí', 'ISSN', 'Nhà xuất bản', 'ID Scopus'])

# ========================
# Lấy chi tiết tạp chí
# ========================
def id_scopus_to_all(id_scopus_input):
    url = f"https://www.scimagojr.com/journalsearch.php?q={id_scopus_input}&tip=sid&clean=0"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    name_journal = soup.find('h1').text.strip() if soup.find('h1') else 'N/A'
    country = soup.find('h2', string='Country').find_next('a').text.strip() if soup.find('h2', string='Country') else 'N/A'

    treecategory_dict = {}
    area = soup.find('h2', string='Subject Area and Category')
    if area:
        cats = area.find_next_sibling('p').find_all('li', recursive=True)
        for cat in cats:
            subcats = cat.find_all('li')
            if subcats:
                for sub in subcats:
                    name = sub.find('a').text.strip()
                    code = sub.find('a')['href'].split('=')[-1]
                    treecategory_dict[name] = code
            else:
                name = cat.find('a').text.strip()
                code = cat.find('a')['href'].split('=')[-1]
                treecategory_dict[name] = code

    publisher = soup.find('h2', string='Publisher').find_next('a').text.strip() if soup.find('h2', string='Publisher') else 'N/A'
    issn = soup.find('h2', string='ISSN').find_next('p').text.strip() if soup.find('h2', string='ISSN') else 'N/A'
    coverage = soup.find('h2', string='Coverage').find_next('p').text.strip() if soup.find('h2', string='Coverage') else 'N/A'
    homepage = soup.find('a', string='Homepage')['href'] if soup.find('a', string='Homepage') else 'N/A'
    howtopublish = soup.find('a', string='How to publish in this journal')['href'] if soup.find('a', string='How to publish in this journal') else 'N/A'
    email = soup.find('a', href=True, string=lambda x: x and '@' in x)
    email = email['href'].replace('mailto:', '') if email else 'N/A'

    return name_journal, country, treecategory_dict, publisher, issn, coverage, homepage, howtopublish, email

# ========================
# Tìm hạng theo tên
# ========================
def check_rank_by_name_1_journal(search_name_journal, subject_area_category, year_check):
    rows = []
    STT = 0

    def fetch(url, category, id_cat, total, page):
        nonlocal STT
        r = requests.get(url)
        s = BeautifulSoup(r.content, 'html.parser')
        for row in s.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) >= 4:
                name = cells[1].text.strip()
                if clear_format(name) == clear_format(search_name_journal):
                    STT += 1
                    pos = cells[0].text.strip()
                    q = cells[3].text.strip().split()[-1]
                    h = cells[4].text.strip()
                    percent = round(float(pos)/total*100, 5)
                    rank, top, note = check_rank_by_h_q(total, percent, q)
                    rows.append([STT, name, rank, q, int(h), int(pos), int(total), percent, top, category, id_cat, int(page), note])
                    break

    with ThreadPoolExecutor(max_workers=10) as ex:
        futures = []
        for cat, id_cat in subject_area_category.items():
            r = requests.get(f"https://www.scimagojr.com/journalrank.php?category={id_cat}&year={year_check}&type=j&order=h&ord=desc")
            s = BeautifulSoup(r.content, 'html.parser')
            total = int(s.find('div', class_='pagination').text.split()[-1]) if s.find('div', class_='pagination') else 0
            for page in range(1, int(total/20)+2):
                url = f"https://www.scimagojr.com/journalrank.php?category={id_cat}&year={year_check}&type=j&order=h&ord=desc&page={page}&total_size={total}"
                futures.append(ex.submit(fetch, url, cat, id_cat, total, page))
        for f in futures:
            f.result()

    return pd.DataFrame(rows, columns=['STT', 'Tên tạp chí', 'Hạng', 'Chỉ số Q', 'H-index', 'Vị trí', 'Tổng số tạp chí', 'Phần trăm', 'Top phần trăm', 'Chuyên ngành', 'ID Chuyên ngành', 'Trang', 'Ghi chú'])

# ========================
# Các hàm giao diện còn lại
# ========================
def def_list_all_subject(year):
    st.subheader(f"Danh sách chuyên ngành - Năm {year}")
    url = f'https://www.scimagojr.com/journalrank.php?year={year}'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    areas = soup.find_all('div', class_='area')
    for a in areas:
        st.write(f"📌 {a.find('h4').text.strip()}")
        for cat in a.find_all('a'):
            st.write(f"- {cat.text.strip()}")

def def_check_in_scopus_sjr_wos(year):
    st.subheader(f"Kiểm tra Scopus/SJR/WoS - Năm {year}")
    query = st.text_input("Nhập Tên hoặc ISSN")
    if st.button("Kiểm tra"):
        if query:
            url = f"https://www.scimagojr.com/journalsearch.php?q={query}"
            r = requests.get(url)
            s = BeautifulSoup(r.content, 'html.parser')
            if s.find('h1'):
                st.success(f"Tìm thấy: {s.find('h1').text.strip()}")
            else:
                st.warning(f"Không tìm thấy '{query}'")

def def_rank_by_rank_key(year):
    st.subheader(f"Tìm theo Từ khóa & Hạng - Năm {year}")
    key = st.text_input("Nhập từ khóa")
    if st.button("Tìm theo Hạng"):
        if key:
            url = f"https://www.scimagojr.com/journalrank.php?year={year}&search={key}"
            r = requests.get(url)
            s = BeautifulSoup(r.content, 'html.parser')
            rows = s.find_all('tr', class_='grp')
            if rows:
                for row in rows:
                    j = row.find('a').text.strip()
                    q = row.find_all('td')[-1].text.strip()
                    st.write(f"🔎 {j} | Q: {q}")
            else:
                st.warning(f"Không tìm thấy '{key}'")

def def_rank_by_Q_key(year):
    st.subheader(f"Tìm theo Từ khóa & Quartile - Năm {year}")
    key = st.text_input("Nhập từ khóa Q")
    if st.button("Tìm Quartile"):
        if key:
            url = f"https://www.scimagojr.com/journalrank.php?year={year}&search={key}"
            r = requests.get(url)
            s = BeautifulSoup(r.content, 'html.parser')
            rows = s.find_all('tr', class_='grp')
            if rows:
                for row in rows:
                    j = row.find('a').text.strip()
                    q = row.find_all('td')[-1].text.strip()
                    st.write(f"🔎 {j} | Q: {q}")
            else:
                st.warning(f"Không tìm thấy Q cho '{key}'")
