import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib
from email.mime.text import MIMEText

# ======= Hàm tra cứu =======
def def_year_choose(_):
    url = 'https://www.scimagojr.com/journalrank.php'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    years = sorted({a.text.strip() for a in soup.find_all('a', class_='dropdown-element') if a.text.strip().isdigit()}, reverse=True)[:5]
    year = st.selectbox("Chọn năm", years)
    st.success(f"Năm đã chọn: {year}")
    return year

def def_list_all_subject(year):
    st.subheader(f"Danh sách chuyên ngành - Năm {year}")
    url = f'https://www.scimagojr.com/journalrank.php?year={year}'
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    areas = soup.find_all('div', class_='area')
    for area in areas:
        st.write(f"📌 {area.find('h4').text.strip()}")
        for cat in area.find_all('a'):
            st.write(f"- {cat.text.strip()}")

def def_check_in_scopus_sjr_wos(year):
    st.subheader(f"Kiểm tra Scopus/SJR/WoS - {year}")
    q = st.text_input("Nhập tên hoặc ISSN")
    if st.button("Kiểm tra"):
        if q:
            r = requests.get(f"https://www.scimagojr.com/journalsearch.php?q={q}")
            if BeautifulSoup(r.content, 'html.parser').find('h1'):
                st.success(f"Tìm thấy: {q}")
            else:
                st.warning(f"Không tìm thấy: {q}")

def def_rank_by_rank_key(year):
    st.subheader(f"Từ khóa & Hạng - {year}")
    k = st.text_input("Từ khóa")
    if st.button("Tìm Hạng"):
        if k:
            url = f"https://www.scimagojr.com/journalrank.php?year={year}&search={k}"
            soup = BeautifulSoup(requests.get(url).content, 'html.parser')
            rows = soup.find_all('tr', class_='grp')
            for row in rows:
                j = row.find('a').text.strip()
                qv = row.find_all('td')[-1].text.strip()
                st.write(f"🔎 {j} | Q: {qv}")

def def_rank_by_Q_key(year):
    st.subheader(f"Từ khóa & Q - {year}")
    k = st.text_input("Từ khóa Q")
    if st.button("Tìm Q"):
        if k:
            url = f"https://www.scimagojr.com/journalrank.php?year={year}&search={k}"
            soup = BeautifulSoup(requests.get(url).content, 'html.parser')
            rows = soup.find_all('tr', class_='grp')
            for row in rows:
                j = row.find('a').text.strip()
                qv = row.find_all('td')[-1].text.strip()
                st.write(f"🔎 {j} | Q: {qv}")

def check_rank_by_h_q(total, percent, q):
    return "Hạng", "Top", "Note"  # Thay bằng hàm thật

def check_rank_by_name_1_journal(search_name_journal, subject_area_category, year_check):
    return [[1, search_name_journal, "Rank", "Q1", 100, 1, 2000, 0.5, "Top", "Cat", "ID", 1, "Note"]]

def def_rank_by_name_or_issn(year):
    st.subheader(f"Hạng theo TÊN hoặc ISSN ({year})")
    n = st.text_input("Nhập tên hoặc ISSN")
    if st.button("Tra cứu"):
        if n.strip():
            rows = check_rank_by_name_1_journal(n, "", year)
            df = pd.DataFrame(rows, columns=['STT','Tên tạp chí','Rank','Q','H-index','Position','Total','Percent','Top','Category','ID_Category','Page','Note'])
            st.dataframe(df)
            sel = st.number_input("STT:", 1, len(df), 1)
            if st.button("Xem chi tiết"):
                r = df[df['STT']==sel].iloc[0]
                st.success(f"Rank: {r['Rank']}, Q: {r['Q']}, Top: {r['Top']}, Note: {r['Note']}")

st.set_page_config(layout="wide")

st.title("Đăng nhập OTP")
if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False
if 'otp_sent' not in st.session_state: st.session_state['otp_sent'] = ''
if 'year' not in st.session_state: st.session_state['year'] = 2025

sender_email = "test@example.com"
sender_pass = "testpass"

def send_email(to, otp):
    pass  # Không thực

if not st.session_state['authenticated']:
    user_email = st.text_input("Email")
    if st.button("Gửi OTP"):
        otp = "123456"
        st.session_state['otp_sent'] = otp
        send_email(user_email, otp)
        st.success("OTP đã gửi.")
    otp_in = st.text_input("OTP", type="password")
    if st.button("Đăng nhập"):
        if otp_in == st.session_state['otp_sent']:
            st.session_state['authenticated'] = True
        else:
            st.error("OTP sai.")
    st.stop()

if st.session_state['authenticated']:
    st.header("Tra cứu tạp chí")
    tabs = st.tabs(["Năm", "Tên/ISSN", "Chuyên ngành", "Phân loại", "Từ khóa Hạng", "Từ khóa Q"])
    with tabs[0]: st.session_state['year'] = def_year_choose(st.session_state['year'])
    with tabs[1]: def_rank_by_name_or_issn(st.session_state['year'])
    with tabs[2]: def_list_all_subject(st.session_state['year'])
    with tabs[3]: def_check_in_scopus_sjr_wos(st.session_state['year'])
    with tabs[4]: def_rank_by_rank_key(st.session_state['year'])
    with tabs[5]: def_rank_by_Q_key(st.session_state['year'])
