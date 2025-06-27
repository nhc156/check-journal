# 📌 year_module.py — BẢN CHUẨN
import streamlit as st
import requests
from bs4 import BeautifulSoup

def def_year_choose(_):
    st.info("Đang lấy danh sách năm từ web SJR...")
    url_take_year_check = 'https://www.scimagojr.com/journalrank.php'
    response_take_year = requests.get(url_take_year_check)
    soup = BeautifulSoup(response_take_year.content, 'html.parser')
    elements = soup.find_all('a', class_='dropdown-element')
    list_years = [element.text.strip() for element in elements if element.text.strip().isdigit()]
    years = sorted(list_years, reverse=True)[:5]
    year = st.selectbox("Chọn năm tra cứu (5 năm mới nhất)", years)
    st.success(f"Năm đã chọn: {year}")
    return year

def def_rank_by_name_or_issn(year):
    st.write(f"[Stub] Hạng theo TÊN/ISSN cho năm {year}")

def def_list_all_subject(year):
    st.write(f"[Stub] Danh sách chuyên ngành cho năm {year}")

def def_check_in_scopus_sjr_wos(year):
    st.write(f"[Stub] Phân loại Scopus/SJR/WoS cho năm {year}")

def def_rank_by_rank_key(year):
    st.write(f"[Stub] Từ khóa và Hạng cho năm {year}")

def def_rank_by_Q_key(year):
    st.write(f"[Stub] Từ khóa và Q cho năm {year}")
