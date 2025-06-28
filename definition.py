import streamlit as st
import requests
from bs4 import BeautifulSoup

def def_list_all_subject(year):
    st.subheader(f"Danh sách chuyên ngành - Năm {year}")
    url = f'https://www.scimagojr.com/journalrank.php?year={year}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    areas = soup.find_all('div', class_='area')
    for area in areas:
        area_name = area.find('h4').text.strip()
        st.write(f"📌 {area_name}")
        categories = area.find_all('a')
        for cat in categories:
            st.write(f"- {cat.text.strip()}")

def def_check_in_scopus_sjr_wos(year):
    st.subheader(f"Kiểm tra Scopus/SJR/WoS - Năm {year}")
    query = st.text_input("Nhập tên hoặc ISSN để kiểm tra")
    if st.button("Kiểm tra", key='check_in_sjr'):
        if query:
            url = f"https://www.scimagojr.com/journalsearch.php?q={query}"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            if soup.find('h1'):
                st.success(f"Tìm thấy tạp chí: {soup.find('h1').text.strip()}")
            else:
                st.warning(f"Không tìm thấy '{query}' trong Scopus/SJR/WoS")

def def_rank_by_rank_key(year):
    st.subheader(f"Tra cứu Từ khóa & Hạng - Năm {year}")
    keyword = st.text_input("Nhập từ khóa")
    if st.button("Tìm kiếm", key='find_rank_key'):
        if keyword:
            url = f"https://www.scimagojr.com/journalrank.php?year={year}&search={keyword}"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            rows = soup.find_all('tr', class_='grp')
            if rows:
                for row in rows:
                    journal = row.find('a').text.strip()
                    sjr_q = row.find_all('td')[-1].text.strip()
                    st.write(f"🔎 {journal} | Q: {sjr_q}")
            else:
                st.warning(f"Không tìm thấy tạp chí phù hợp cho từ khóa '{keyword}'")

def def_rank_by_Q_key(year):
    st.subheader(f"Tra cứu Từ khóa & Quartile - Năm {year}")
    keyword = st.text_input("Nhập từ khóa Q")
    if st.button("Tìm Quartile", key='find_q_key'):
        if keyword:
            url = f"https://www.scimagojr.com/journalrank.php?year={year}&search={keyword}"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            rows = soup.find_all('tr', class_='grp')
            if rows:
                for row in rows:
                    journal = row.find('a').text.strip()
                    sjr_q = row.find_all('td')[-1].text.strip()
                    st.write(f"🔎 {journal} | Q: {sjr_q}")
            else:
                st.warning(f"Không tìm thấy Q cho từ khóa '{keyword}'")

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
