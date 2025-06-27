# 👉 Đây là file year_module.py tách riêng

# Ví dụ tách sẵn các hàm stub

def def_year_choose(current_year):
    import streamlit as st
    year = st.selectbox("Chọn năm tra cứu", [2025, 2024, 2023, 2022, 2021], index=0)
    st.success(f"Năm đã chọn: {year}")
    return year

def def_rank_by_name_or_issn(year):
    import streamlit as st
    st.write(f"Hạng theo Tên/ISSN cho năm {year} — Chức năng đang chạy.")

def def_list_all_subject(year):
    import streamlit as st
    st.write(f"Danh sách chuyên ngành cho năm {year} — Chức năng đang chạy.")

def def_check_in_scopus_sjr_wos(year):
    import streamlit as st
    st.write(f"Phân loại Scopus/SJR/WoS cho năm {year} — Chức năng đang chạy.")

def def_rank_by_rank_key(year):
    import streamlit as st
    st.write(f"Từ khóa và Hạng cho năm {year} — Chức năng đang chạy.")

def def_rank_by_Q_key(year):
    import streamlit as st
    st.write(f"Từ khóa và Q cho năm {year} — Chức năng đang chạy.")
