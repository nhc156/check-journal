import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from year_module import (
    def_year_choose,
    def_list_all_subject,
    def_check_in_scopus_sjr_wos,
    def_rank_by_rank_key,
    def_rank_by_Q_key,
    check_rank_by_h_q,
    check_rank_by_name_1_journal
)

def def_rank_by_name_or_issn(year):
    st.subheader(f"Hạng theo TÊN hoặc ISSN (Năm {year})")
    name_or_issn = st.text_input("Nhập TÊN tạp chí hoặc ISSN", key="rank_name_issn")
    if st.button("Tra cứu", key="search_name_issn"):
        if name_or_issn.strip():
            st.write(f"Đang tra cứu bằng hàm chuẩn cho: {name_or_issn} (Năm {year})")
            subject_area_category = ""
            results = check_rank_by_name_1_journal(
                search_name_journal=name_or_issn,
                subject_area_category=subject_area_category,
                year_check=year
            )
            df = pd.DataFrame(results, columns=['STT','Tên tạp chí','Rank','Q','H-index','Position','Total','Percent','Top','Category','ID_Category','Page','Note'])
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                selected = st.number_input("Chọn STT để xem chi tiết:", min_value=1, max_value=len(df), step=1)
                if st.button("Xem Hạng Chi Tiết"):
                    row = df[df['STT'] == selected].iloc[0]
                    st.success(f"Kết quả: Rank: {row['Rank']}, Q: {row['Q']}, Percent: {row['Percent']}, Top: {row['Top']}, Note: {row['Note']}")
            else:
                st.warning("Không tìm thấy tạp chí phù hợp.")
        else:
            st.warning("Vui lòng nhập từ khóa.")

st.set_page_config(layout="wide")

st.title("Đăng nhập qua Email")
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'otp_sent' not in st.session_state:
    st.session_state['otp_sent'] = ''
if 'year' not in st.session_state:
    st.session_state['year'] = 2025

sender_email = st.secrets["EMAIL"] if "EMAIL" in st.secrets else ""
sender_pass = st.secrets["EMAIL_PASS"] if "EMAIL_PASS" in st.secrets else ""

import smtplib
from email.mime.text import MIMEText

def send_email(receiver_email, password):
    msg = MIMEText(f"Mã OTP đăng nhập của bạn: {password}")
    msg['Subject'] = "Mã đăng nhập"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_pass)
        server.send_message(msg)

if not st.session_state['authenticated']:
    user_email = st.text_input("Nhập email của bạn")
    if st.button("Gửi mã OTP"):
        if "@" in user_email:
            otp = str(123456)  # Thay bằng random hoặc gửi thật
            st.session_state['otp_sent'] = otp
            send_email(user_email, otp)
            st.success("Mã OTP đã được gửi.")
        else:
            st.warning("Email không hợp lệ")
    otp_input = st.text_input("Nhập mã OTP", type="password")
    if st.button("Đăng nhập"):
        if otp_input == st.session_state['otp_sent']:
            st.session_state['authenticated'] = True
            st.success("Đăng nhập thành công!")
        else:
            st.error("Mã OTP không đúng.")
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
