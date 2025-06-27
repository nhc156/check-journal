import streamlit as st
import os
import smtplib
from email.mime.text import MIMEText
import random
from dotenv import load_dotenv
from App_check_journal_and_support_25_6_5 import (
    def_year_choose,
    def_rank_by_name_or_issn,
    def_list_all_subject,
    def_check_in_scopus_sjr_wos,
    def_rank_by_rank_key,
    def_rank_by_Q_key
)

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

# === App ===
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

# === Tabs ===
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
