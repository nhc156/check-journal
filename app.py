import streamlit as st
import os
import smtplib
from email.mime.text import MIMEText
import random
from dotenv import load_dotenv
from year_module import (
    def_year_choose,
    def_list_all_subject,
    def_check_in_scopus_sjr_wos,
    def_rank_by_rank_key,
    def_rank_by_Q_key
)
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(layout="wide")
load_dotenv()

sender_email = os.getenv('EMAIL')
sender_pass = os.getenv('EMAIL_PASS')

def send_email(receiver_email, password):
    msg = MIMEText(f"Mã OTP đăng nhập của bạn: {password}")
    msg['Subject'] = "Mã đăng nhập"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_pass)
        server.send_message(msg)

# --- Phiên bản đầy đủ: def_rank_by_name_or_issn gọi crawl thật ---
def def_rank_by_name_or_issn(year):
    st.subheader(f"Hạng theo TÊN hoặc ISSN (Năm {year})")
    name_or_issn = st.text_input("Nhập TÊN tạp chí hoặc ISSN", key="rank_name_issn")
    if st.button("Tra cứu", key="search_name_issn"):
        if name_or_issn.strip():
            st.write(f"Đang tra cứu thông tin cho: {name_or_issn} (Năm {year})")
            # Crawl Scimago như file gốc
            url = f"https://www.scimagojr.com/journalsearch.php?q={name_or_issn}"
            response = requests.get(url)
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
            df = pd.DataFrame(new_row, columns=['STT','Tên tạp chí', 'ISSN', 'Nhà xuất bản', 'ID Scopus'])
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Không tìm thấy tạp chí phù hợp.")
        else:
            st.warning("Vui lòng nhập TÊN hoặc ISSN để tra cứu.")

st.title("Đăng nhập qua Email")
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'otp_sent' not in st.session_state:
    st.session_state['otp_sent'] = ''
if 'year' not in st.session_state:
    st.session_state['year'] = 2025

if not st.session_state['authenticated']:
    user_email = st.text_input("Nhập email của bạn")
    if st.button("Gửi mã OTP"):
        if "@" in user_email:
            otp = str(random.randint(100000, 999999))
            st.session_state['otp_sent'] = otp
            send_email(user_email, otp)
            st.success("Mã OTP đã được gửi đến email của bạn.")
        else:
            st.warning("Email không hợp lệ")
    otp_input = st.text_input("Nhập mã OTP", type="password")
    if st.button("Đăng nhập"):
        if otp_input == st.session_state['otp_sent'] and otp_input != '':
            st.session_state['authenticated'] = True
            st.success("Đăng nhập thành công!")
        else:
            st.error("Mã OTP không đúng hoặc chưa gửi mã!")
    st.stop()

if st.session_state['authenticated']:
    st.header("📚 Tra cứu thông tin tạp chí")
    tabs = st.tabs([
        "Chọn năm tra cứu",
        "Hạng theo tên hoặc ISSN",
        "Danh sách chuyên ngành",
        "Phân loại tạp chí",
        "Từ khóa và Hạng",
        "Từ khóa và Q"
    ])

    with tabs[0]:
        st.session_state['year'] = def_year_choose(st.session_state['year'])

    with tabs[1]:
        def_rank_by_name_or_issn(st.session_state['year'])

    with tabs[2]:
        def_list_all_subject(st.session_state['year'])

    with tabs[3]:
        def_check_in_scopus_sjr_wos(st.session_state['year'])

    with tabs[4]:
        def_rank_by_rank_key(st.session_state['year'])

    with tabs[5]:
        def_rank_by_Q_key(st.session_state['year'])
