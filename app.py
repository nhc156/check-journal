import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib
from email.mime.text import MIMEText

# ======= Hàm gửi OTP chuẩn bản cũ =======
def send_email(receiver_email, password):
    sender_email = st.secrets["EMAIL"]
    sender_pass = st.secrets["EMAIL_PASS"]
    msg = MIMEText(f"Mã OTP đăng nhập của bạn: {password}")
    msg['Subject'] = "Mã OTP"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_pass)
        server.send_message(msg)

# ======= Hàm chọn năm =======
def def_year_choose(_):
    url = 'https://www.scimagojr.com/journalrank.php'
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    years = sorted({a.text.strip() for a in soup.find_all('a', class_='dropdown-element') if a.text.strip().isdigit()}, reverse=True)[:5]
    year = st.selectbox("Chọn năm", years)
    return year

# ======= Các hàm tra cứu khác (placeholder) =======
def def_list_all_subject(year):
    st.write(f"[Stub] Danh sách chuyên ngành cho năm {year}")

def def_rank_by_name_or_issn(year):
    st.write(f"[Stub] Tra cứu theo tên hoặc ISSN cho năm {year}")

def def_check_in_scopus_sjr_wos(year):
    st.write(f"[Stub] Kiểm tra Scopus/SJR/WoS cho năm {year}")

def def_rank_by_rank_key(year):
    st.write(f"[Stub] Từ khóa & Hạng cho năm {year}")

def def_rank_by_Q_key(year):
    st.write(f"[Stub] Từ khóa & Q cho năm {year}")

# ======= Giao diện =======
st.set_page_config(layout="wide")
st.title("Đăng nhập OTP")
if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False
if 'otp_sent' not in st.session_state: st.session_state['otp_sent'] = ''
if 'year' not in st.session_state: st.session_state['year'] = 2025

if not st.session_state['authenticated']:
    user_email = st.text_input("Nhập email để nhận OTP")
    if st.button("Gửi OTP"):
        otp = "123456"
        st.session_state['otp_sent'] = otp
        send_email(user_email, otp)
        st.success(f"OTP đã gửi tới {user_email}")
    otp_in = st.text_input("Nhập OTP", type="password")
    if st.button("Đăng nhập"):
        if otp_in == st.session_state['otp_sent']:
            st.session_state['authenticated'] = True
            st.success("Đăng nhập thành công")
        else:
            st.error("OTP sai")
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
