import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import re

# ========================
# Helper
# ========================

def clear_format(text):
    text = re.sub(r'\W+', ' ', text)
    return ' '.join(text.lower().split())

# ========================
# Hàm rank_h_q
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
# Crawler gốc
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
# === GIAO DIỆN STREAMLIT ===
# ========================

def def_rank_by_name_or_issn(year):
    st.subheader(f"Tìm tạp chí theo Tên/ISSN - Năm {year}")
    keyword = st.text_input("Nhập Tên hoặc ISSN")

    if st.button("Tìm kiếm"):
        df = find_title_or_issn(keyword)
        st.session_state['df_search'] = df  # LƯU vào session
    else:
        df = st.session_state.get('df_search', pd.DataFrame())

    if not df.empty:
        st.dataframe(df)
        choose = st.selectbox("Chọn tạp chí", df['Tên tạp chí'])
        st.session_state['choose_journal'] = choose  # LƯU chọn

        if st.button("Xem hạng"):
            selected = df[df['Tên tạp chí'] == choose].iloc[0]
            id_scopus = selected['ID Scopus']
            name_j, country, cats, pub, issn, cover, home, howpub, mail = id_scopus_to_all(id_scopus)
            df_rank = check_rank_by_name_1_journal(name_j, cats, year)
            st.dataframe(df_rank)


def def_list_all_subject(year):
    st.subheader(f"Danh sách chuyên ngành - Năm {year}")
    url = f'https://www.scimagojr.com/journalrank.php?year={year}'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    areas = soup.find_all('div', class_='area')

    rows = []
    for a in areas:
        area_name = a.find('h4').text.strip()
        for cat in a.find_all('a'):
            cat_name = cat.text.strip()
            cat_link = f"https://www.scimagojr.com/{cat['href']}"
            rows.append([area_name, cat_name, cat_link])

    if rows:
        df = pd.DataFrame(rows, columns=['Lĩnh vực', 'Chuyên ngành', 'Link'])
        st.dataframe(df)
        st.download_button(
            "📥 Tải danh sách chuyên ngành",
            df.to_csv(index=False).encode('utf-8'),
            file_name=f"subject_list_{year}.csv",
            mime='text/csv'
        )
    else:
        st.warning("Không tìm thấy dữ liệu.")

def def_check_in_scopus_sjr_wos(year):
    st.subheader(f"Kiểm tra tạp chí trong Scopus/SJR/WoS - Năm {year}")
    query = st.text_input("Nhập Tên hoặc ISSN để tra cứu")
    if st.button("Kiểm tra"):
        url = f"https://www.scimagojr.com/journalsearch.php?q={query}"
        r = requests.get(url)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.content, 'html.parser')

        title = soup.find('h1').text.strip() if soup.find('h1') else None

        if title:
            st.success(f"✅ Tìm thấy: **{title}**")
            issn = soup.find('h2', string='ISSN')
            issn = issn.find_next('p').text.strip() if issn else 'N/A'
            pub = soup.find('h2', string='Publisher')
            pub = pub.find_next('a').text.strip() if pub else 'N/A'
            coverage = soup.find('h2', string='Coverage')
            coverage = coverage.find_next('p').text.strip() if coverage else 'N/A'

            st.write(f"- **ISSN**: {issn}")
            st.write(f"- **Publisher**: {pub}")
            st.write(f"- **Coverage**: {coverage}")

            st.markdown(f"[🔗 Xem chi tiết trên SJR](https://www.scimagojr.com/journalsearch.php?q={query})")
        else:
            st.warning(f"❌ Không tìm thấy **{query}** trong Scopus/SJR/WoS.")

def def_rank_by_rank_key(year):
    st.subheader(f"Tra cứu tạp chí theo Từ khóa - Năm {year}")
    keyword = st.text_input("Nhập Từ khóa")
    if st.button("Tìm kiếm theo từ khóa"):
        url = f"https://www.scimagojr.com/journalrank.php?year={year}&search={keyword}"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        rows = []
        for row in soup.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) >= 5:
                link = row.find('a')
                if link:
                    name = link.text.strip()
                    q_value = cells[-1].text.strip()
                    rows.append([name, q_value])

        if rows:
            df = pd.DataFrame(rows, columns=['Tên tạp chí', 'Q'])
            st.dataframe(df)
            st.download_button(
                "📥 Tải danh sách",
                df.to_csv(index=False).encode('utf-8'),
                file_name=f"rank_by_keyword_{keyword}_{year}.csv",
                mime='text/csv'
            )
        else:
            st.warning(f"❌ Không tìm thấy kết quả cho từ khóa: **{keyword}**.")

def def_rank_by_Q_key(year):
    st.subheader(f"Lọc tạp chí theo Quartile - Năm {year}")
    quartile = st.selectbox("Chọn Quartile cần lọc", ['Q1', 'Q2', 'Q3', 'Q4'])
    keyword = st.text_input("Nhập Từ khóa (tuỳ chọn)")

    if st.button("Lọc theo Quartile"):
        url = f"https://www.scimagojr.com/journalrank.php?year={year}&search={keyword}"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        rows = []
        for row in soup.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) >= 5:
                link = row.find('a')
                if link:
                    name = link.text.strip()
                    q_value = cells[-1].text.strip()
                    if quartile in q_value:
                        rows.append([name, q_value])

        if rows:
            df = pd.DataFrame(rows, columns=['Tên tạp chí', 'Q'])
            st.dataframe(df)
            st.download_button(
                "📥 Tải danh sách",
                df.to_csv(index=False).encode('utf-8'),
                file_name=f"rank_by_Q_{quartile}_{year}.csv",
                mime='text/csv'
            )
        else:
            st.warning(f"❌ Không tìm thấy tạp chí Q phù hợp ({quartile}).")
