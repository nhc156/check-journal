# choose_year.py

import streamlit as st
import requests
from bs4 import BeautifulSoup

def def_year_choose(year):
    with st.spinner("Đang cập nhật năm mới nhất..."):
        url_take_year_check = 'https://www.scimagojr.com/journalrank.php'
        response_take_year = requests.get(url_take_year_check)
        soup = BeautifulSoup(response_take_year.content, 'html.parser')
        elements = soup.find_all('a', class_='dropdown-element')
        list_years = [element.text.strip() for element in elements if element.text.strip().isdigit()]
        years = sorted(list_years, reverse=True)[:5]

    if not years:
        st.warning("Không lấy được danh sách năm. Dùng năm hiện tại!")
        return int(year)

    # Nếu chưa có trong session_state thì gán mặc định là năm mới nhất
    if 'year' not in st.session_state or st.session_state['year'] is None:
        st.session_state['year'] = int(years[0])

    selected_year = st.selectbox(
        "Chọn năm tra cứu (5 năm mới nhất):",
        years,
        index=years.index(str(st.session_state['year'])) if str(st.session_state['year']) in years else 0
    )

    if st.button("Xác nhận"):
        st.success(f'Năm đã chọn: {selected_year}')
        with st.spinner(f"Đang tải dữ liệu năm {selected_year} ..."):
            st.info(f"Đã chọn năm {selected_year}!")

        st.session_state['year'] = int(selected_year)

    return int(st.session_state['year'])
