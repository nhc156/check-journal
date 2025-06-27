import streamlit as st
import os
import smtplib
from email.mime.text import MIMEText
import random
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv

# Cài đặt full width
st.set_page_config(layout="wide")

# Load .env
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

def find_title_or_issn(name_or_issn):
    url_search_sjr = f"https://www.scimagojr.com/journalsearch.php?q={name_or_issn}"
    response = requests.get(url_search_sjr)
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
    return df

def issn_to_all(issn):
    url = f"https://www.scimagojr.com/journalsearch.php?q={issn}&tip=sid&clean=0"
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.content, 'html.parser')
    name_journal = soup.find('h1').text.strip() if soup.find('h1') else 'N/A'
    country_tag = soup.find('h2', string='Country')
    country = country_tag.find_next('a').text.strip() if country_tag else 'N/A'
    treecategory_dict = {}
    subject_area_div = soup.find('h2', string='Subject Area and Category')
    if subject_area_div:
        categories = subject_area_div.find_next_sibling('p').find_all('li', recursive=True)
        for category in categories:
            subcategories = category.find_all('li')
            if subcategories:
                for subcategory in subcategories:
                    subcategory_name = subcategory.find('a').text.strip()
                    subcategory_code = subcategory.find('a')['href'].split('=')[-1]
                    treecategory_dict[subcategory_name] = subcategory_code
            else:
                category_name = category.find('a').text.strip()
                category_code = category.find('a')['href'].split('=')[-1]
                treecategory_dict[category_name] = category_code
    publisher_tag = soup.find('h2', string='Publisher')
    publisher = publisher_tag.find_next('a').text.strip() if publisher_tag else 'N/A'
    h_index_tag = soup.find('h2', string='H-Index')
    h_index = h_index_tag.find_next('p', class_='hindexnumber').text.strip() if h_index_tag else 'N/A'
    issn_tag = soup.find('h2', string='ISSN')
    issn_info = issn_tag.find_next('p').text.strip() if issn_tag else 'N/A'
    coverage_tag = soup.find('h2', string='Coverage')
    coverage = coverage_tag.find_next('p').text.strip() if coverage_tag else 'N/A'
    homepage_tag = soup.find('a', string='Homepage')
    homepage_link = homepage_tag['href'] if homepage_tag else 'N/A'
    how_to_publish_tag = soup.find('a', string='How to publish in this journal')
    how_to_publish_link = how_to_publish_tag['href'] if how_to_publish_tag else 'N/A'
    email_tag = soup.find('a', href=True, string=lambda x: x and '@' in x)
    email_question_journal = email_tag['href'].replace('mailto:', '') if email_tag else 'N/A'
    return name_journal, country, treecategory_dict, publisher, h_index, issn_info, coverage, homepage_link, how_to_publish_link, email_question_journal

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

st.header("📚 Tra cứu thông tin tạp chí")
query = st.text_input("Nhập TÊN tạp chí hoặc ISSN")
if st.button("Tìm kiếm"):
    if query.strip() != "":
        df_result = find_title_or_issn(query.strip())
        if df_result.empty:
            st.warning("Không tìm thấy tạp chí phù hợp.")
        else:
            st.success(f"Tìm thấy {len(df_result)} kết quả:")
            st.dataframe(df_result, use_container_width=True)
            selected_index = st.number_input("Nhập số STT để xem chi tiết:", min_value=1, max_value=len(df_result), step=1)
            if st.button("Xem chi tiết"):
                selected_row = df_result[df_result['STT'] == selected_index]
                if not selected_row.empty:
                    selected_issn = selected_row['ISSN'].values[0]
                    name, country, subjects, publisher, h_index, issn_info, coverage, homepage, how_to_publish, email = issn_to_all(selected_issn)
                    st.subheader(f"📄 Chi tiết tạp chí: {name}")
                    st.write(f"**Quốc gia:** {country}")
                    st.write(f"**Nhà xuất bản:** {publisher}")
                    st.write(f"**H-Index:** {h_index}")
                    st.write(f"**ISSN:** {issn_info}")
                    st.write(f"**Coverage:** {coverage}")
                    st.write(f"**Homepage:** [{homepage}]({homepage})")
                    st.write(f"**Hướng dẫn xuất bản:** [{how_to_publish}]({how_to_publish})")
                    st.write(f"**Email liên hệ:** {email}")
                    st.write("**Danh mục ngành:**")
                    st.json(subjects)
    else:
        st.warning("Vui lòng nhập từ khoá tìm kiếm.")
