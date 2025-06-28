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

# Tải biến môi trường
load_dotenv()
sender_email = os.getenv('EMAIL')
sender_pass = os.getenv('EMAIL_PASS')
# Hàm gửi OTP
def send_email(receiver_email, otp):
    msg = MIMEText(f"Mã OTP đăng nhập của bạn: {otp}")
    msg['Subject'] = "Mã đăng nhập"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_pass)
        server.send_message(msg)

# Hàm lấy năm chuẩn
def main():
    st.title("Tra cứu năm mới nhất - Scimago")
    def_year_choose()

# Các hàm placeholder giữ nguyên
def def_list_all_subject(year):
    st.write(f"Danh sách chuyên ngành - {year}")

def def_rank_by_name_or_issn(year):
    st.write(f"Hạng theo TÊN/ISSN - {year}")

def def_check_in_scopus_sjr_wos(year):
    st.write(f"Phân loại - {year}")

def def_rank_by_rank_key(year):
    st.write(f"Từ khóa & Hạng - {year}")

def def_rank_by_Q_key(year):
    st.write(f"Từ khóa & Q - {year}")

# Giao diện chuẩn
st.set_page_config(layout="wide")
st.title("Chào mừng bạn đến với công cụ tra thông tin tạp chí \n Tác giả: Nguyễn Hữu Cần")

if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False
if 'otp_sent' not in st.session_state: st.session_state['otp_sent'] = ''
if 'year' not in st.session_state: st.session_state['year'] = 2025

if not st.session_state['authenticated']:
    user_email = st.text_input("Nhập email @tdtu.edu.vn để nhận OTP")
    if st.button("Gửi OTP"):
        if "@tdtu.edu.vn" in user_email:
            otp = str(random.randint(100, 200))
            st.session_state['otp_sent'] = otp
            send_email(user_email, otp)
            st.success(f"Mã OTP {otp} đã được gửi đến email của bạn.")
        else:
            st.warning("Bạn chỉ được nhập email @tdtu.edu.vn")
    otp_in = st.text_input("Nhập OTP", type="password")
    if st.button("Đăng nhập"):
        if otp_in == st.session_state['otp_sent']:
            st.session_state['authenticated'] = True
            st.success("Đăng nhập thành công!")
        else:
            st.error("Mã OTP không đúng hoặc chưa gửi mã!")
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
