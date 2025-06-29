import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib
from email.mime.text import MIMEText
import random
import os
from dotenv import load_dotenv
from choose_year import def_year_choose
from definition import def_rank_by_name_or_issn, def_list_all_subject, def_check_in_scopus_sjr_wos, def_rank_by_rank_key, def_rank_by_Q_key

# Tải biến môi trường
load_dotenv()
sender_email = os.getenv('EMAIL')
sender_pass = os.getenv('EMAIL_PASS')

# Hàm gửi OTP
def send_email(receiver_email, otp):
    msg = MIMEText(f"\n Chào bạn, \n Tôi là Nguyễn Hữu Cần - Tác giả của ứng ụng này. \n Mã OTP đăng nhập của bạn là: {otp}")
    msg['Subject'] = "Mã OTP đăng nhập ứng dụng tra cứu thông tin tạp chí"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_pass)
        server.send_message(msg)

# Giao diện chuẩn
st.set_page_config(layout="wide")
st.title("Chào mừng bạn đến với công cụ tra thông tin tạp chí \n Tác giả: Nguyễn Hữu Cần")

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'otp_sent' not in st.session_state:
    st.session_state['otp_sent'] = ''
if 'year' not in st.session_state:
    st.session_state['year'] = 2025

if not st.session_state['authenticated']:
    user_email = st.text_input("Nhập email @tdtu.edu.vn để nhận OTP")
    if st.button("Gửi OTP"):
        if "@tdtu.edu.vn" in user_email:
            otp = str(random.randint(100, 200))
            st.session_state['otp_sent'] = otp
            send_email(user_email, otp)
            st.success(f"Mã OTP {otp} đã được gửi đến email của bạn")
            #st.success(f"Mã OTP có 3 chữ số đã được gửi đến email của bạn.")
        else:
            st.warning("Bạn chỉ được nhập email @tdtu.edu.vn")
    otp_in = st.text_input("Nhập OTP", type="password")
    if st.button("Đăng nhập"):
        if otp_in == st.session_state['otp_sent']:
            st.session_state['authenticated'] = True
            st.success("Đăng nhập thành công! Hãy bấm Đăng nhập lần nữa để sử dụng ứng dụng")
        else:
            st.error("Mã OTP không đúng hoặc chưa gửi mã!")
    st.stop()

if st.session_state['authenticated']:
    st.header("Tra cứu tạp chí")
    tabs = st.tabs([
        "Năm tra cứu",
        "Tên tạp chí hoặc ISSN",
        "Danh sách chuyên ngành",
        "Phân loại tạp chí",
        "Lọc tạp chí theo Từ khóa và Hạng",
        "Lọc tạp chí theo Từ khóa và Q"
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
