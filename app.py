import streamlit as st
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import random

# Tải biến môi trường
load_dotenv()
sender_email = os.getenv('EMAIL')
sender_pass = os.getenv('EMAIL_PASS')

# Hàm gửi email
def send_email(receiver_email, password):
    msg = MIMEText(f"Mã OTP đăng nhập của bạn: {password}")
    msg['Subject'] = "Mã đăng nhập"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_pass)
        server.send_message(msg)

# Giao diện Streamlit
st.title("Đăng nhập qua Email")

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if 'otp_sent' not in st.session_state:
    st.session_state['otp_sent'] = ''

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

st.write("👉 Bạn đã đăng nhập thành công, hãy thêm tính năng chính ở đây!")
