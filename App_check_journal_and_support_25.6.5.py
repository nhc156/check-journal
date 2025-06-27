version_app = '25.6.4'
title_app = f"Tra cứu thông tin tạp chí và hỗ trợ NCKH - Phiên bản {version_app}"
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QInputDialog, QProgressDialog, QLabel, QMessageBox, QFileDialog, QCheckBox, QMainWindow, QDialog
from PyQt6.QtGui import QIcon, QPalette, QColor
from PyQt6.QtCore import Qt
from PyQt6 import QtWidgets, QtCore
import os
import webbrowser
import pandas as pd
import datetime
import time
import re
import webbrowser
#from docx import Document
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
#from urllib.parse import urlparse, parse_qs
#
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Get infor
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
import sys
import socket
import platform
import csv
import threading
# Read file gg drive
from google.oauth2 import service_account
from googleapiclient.discovery import build
import unicodedata

# Xác định nếu script đang chạy từ file .exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

# Setup view
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', 30)
pd.set_option('display.width', None)
pd.set_option('display.expand_frame_repr', True)
pd.set_option('colheader_justify', 'right')

# Setup time
now = datetime.datetime.now()
y_m_d = now.strftime("%Y.%m.%d")
time_check_full = now.strftime("%Y.%m.%d_%Hh%Mm%Ss")
# Định dạng ngày tháng năm
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")
# Định dạng giờ và phút
hour = now.strftime("%H")
minute = now.strftime("%M")
second = now.strftime("%S")

# start mới ==============================================================================================================
def clear_format(text):
    # Xóa mọi ký tự không phải chữ cái và số, đưa về chữ thường, cắt bỏ các khoảng trống dư thừa
    text = re.sub(r'\W+', ' ', text)
    return ' '.join(text.lower().split())

def check_rank_by_h_q(total_journals, percent, sjr_quartile):
        # Xác định rank_h dựa trên total_journals và Percent
        if total_journals >= 2000:
            thresholds = [0.5, 1, 5, 10, 18, 30, 43, 56, 69, 82]
        elif 1500 <= total_journals <= 1999:
            thresholds = [0.5, 2, 6, 11, 19, 31, 44, 57, 70, 83]
        elif 1000 <= total_journals <= 1499:
            thresholds = [0.5, 3, 7, 12, 20, 32, 45, 58, 71, 84]
        elif 500 <= total_journals <= 999:
            thresholds = [0.5, 4, 8, 13, 21, 33, 46, 59, 72, 85]
        elif 200 <= total_journals <= 499:
            thresholds = [0.9, 5, 10, 15, 23, 35, 48, 61, 74, 87]
        elif 50 <= total_journals <= 199:
            thresholds = [2.5, 6, 11, 16, 24, 36, 49, 62, 75, 88]
        elif 0 < total_journals < 50:
            thresholds = [3.5, 7, 15, 20, 28, 40, 53, 66, 79, 92]
        else:
            return 'None', 'None', 'Lỗi trong thống kê số lượng tạp chí'
        rank_h = next((i for i, th in enumerate(thresholds, start=0) if percent < th), 10)
        if rank_h < len(thresholds):
            Top_Percent = '< ' + str(thresholds[rank_h])
        else:
            Top_Percent = '>= ' + str(thresholds[-1])
        if (rank_h == 0) and (sjr_quartile == 'Q1'):
            return 'Ngoại hạng chuyên ngành', Top_Percent, ''
        elif (rank_h == 1) and  (sjr_quartile == 'Q1'):
            return 'Hạng 1', Top_Percent, ''
        elif (rank_h == 2) and  (sjr_quartile == 'Q1' or sjr_quartile == 'Q2'):
            return 'Hạng 2', Top_Percent, ''
        elif (rank_h == 3) and  (sjr_quartile == 'Q1' or sjr_quartile == 'Q2'):
            return 'Hạng 3', Top_Percent, ''
        elif (rank_h == 4) and  (sjr_quartile == 'Q1' or sjr_quartile == 'Q2'):
            return 'Hạng 4', Top_Percent, ''
        elif (rank_h == 5) and  (sjr_quartile == 'Q1' or sjr_quartile == 'Q2' or sjr_quartile == 'Q3'):
            return 'Hạng 5', Top_Percent, ''
        elif (rank_h == 6) and  (sjr_quartile == 'Q1' or sjr_quartile == 'Q2' or sjr_quartile == 'Q3'):
            return 'Hạng 6', Top_Percent, ''
        elif (rank_h == 7) and  (sjr_quartile == 'Q1' or sjr_quartile == 'Q2' or sjr_quartile == 'Q3'):
            return 'Hạng 7', Top_Percent, ''
        elif (rank_h == 8) and  (sjr_quartile == 'Q1' or sjr_quartile == 'Q2' or sjr_quartile == 'Q3'):
            return 'Hạng 8', Top_Percent, ''
        elif (rank_h == 9) and  (sjr_quartile == 'Q1' or sjr_quartile == 'Q2' or sjr_quartile == 'Q3' or sjr_quartile == 'Q4'):
            return 'Hạng 9', Top_Percent, ''
        elif (rank_h == 10) and (sjr_quartile == 'Q1' or sjr_quartile == 'Q2' or sjr_quartile == 'Q3' or sjr_quartile == 'Q4'):
            return 'Hạng 10', Top_Percent, ''
        elif (0 <= rank_h <= 1) and (sjr_quartile == 'Q2'):
            return f'Hạng 2', Top_Percent, f"Rớt từ Hạng {rank_h} vì Q2"
        elif (0 <= rank_h <= 4) and (sjr_quartile == 'Q3'):
            return f'Hạng 5', Top_Percent, f"Rớt từ Hạng {rank_h} vì Q3"
        elif (0 <= rank_h <= 8) and (sjr_quartile == 'Q4'):
            return f'Hạng 9', Top_Percent, f"Rớt từ Hạng {rank_h} vì Q4"
        else:
            return 'Không xếp hạng', Top_Percent, 'Không có Q'

def issn_to_all(issn):
    url = f"https://www.scimagojr.com/journalsearch.php?q={issn}&tip=sid&clean=0"
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extracting the required information with checks
    name_journal = soup.find('h1').text.strip() if soup.find('h1') else 'N/A'
    # Extracting country
    country_tag = soup.find('h2', string='Country')
    country = country_tag.find_next('a').text.strip() if country_tag else 'N/A'
    # Extracting subject area and category
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
    subject_area_category = treecategory_dict
    # Extracting publisher
    publisher_tag = soup.find('h2', string='Publisher')
    publisher = publisher_tag.find_next('a').text.strip() if publisher_tag else 'N/A'
    # Extracting H-Index
    h_index_tag = soup.find('h2', string='H-Index')
    h_index = h_index_tag.find_next('p', class_='hindexnumber').text.strip() if h_index_tag else 'N/A'
    # Extracting ISSN
    issn_tag = soup.find('h2', string='ISSN')
    issn_info = issn_tag.find_next('p').text.strip() if issn_tag else 'N/A'
    # Extracting coverage
    coverage_tag = soup.find('h2', string='Coverage')
    coverage = coverage_tag.find_next('p').text.strip() if coverage_tag else 'N/A'
    # Extracting homepage link
    homepage_tag = soup.find('a', string='Homepage')
    homepage_link = homepage_tag['href'] if homepage_tag else 'N/A'
    # Extracting how to publish link
    how_to_publish_tag = soup.find('a', string='How to publish in this journal')
    how_to_publish_link = how_to_publish_tag['href'] if how_to_publish_tag else 'N/A'
    # Extracting email for questions
    email_tag = soup.find('a', href=True, string=lambda x: x and '@' in x)
    email_question_journal = email_tag['href'].replace('mailto:', '') if email_tag else 'N/A'
    return name_journal, country, subject_area_category, publisher, h_index, issn_info, coverage, homepage_link, how_to_publish_link, email_question_journal

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
            # Fetch ISSN and Publisher from the detailed page
            detail_response = requests.get(url_sjr_journal)
            detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
            # Initialize ISSN and Publisher
            issn_sjr_homepage = 'ISSN not available'
            publisher_sjr_homepage = 'Publisher not available'
            STT = STT + 1
            # Find Publisher
            publisher_div = detail_soup.find('h2', string='Publisher')
            if publisher_div:
                publisher_p = publisher_div.find_next('p')
                if publisher_p:
                    publisher_sjr_homepage = publisher_p.text.strip()
            # Find ISSN
            issn_div = detail_soup.find('h2', string='ISSN')
            if issn_div:
                issn_p = issn_div.find_next('p')
                if issn_p:
                    issn_sjr_homepage = issn_p.text.strip()
            new_row.append([STT, title_journal, issn_sjr_homepage, publisher_sjr_homepage, id_scopus_journal])
    # Create DataFrame
    df = pd.DataFrame(new_row, columns=['STT','Tên tạp chí', 'ISSN', 'Nhà xuất bản', 'ID Scopus'])
    #df.index += 1  # Start index from 1
    return df

def id_scopus_to_all(id_scopus_input):
    url = f"https://www.scimagojr.com/journalsearch.php?q={id_scopus_input}&tip=sid&clean=0"
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extracting the required information with checks
    name_journal = soup.find('h1').text.strip() if soup.find('h1') else 'N/A'
    # Extracting country
    country_tag = soup.find('h2', string='Country')
    country = country_tag.find_next('a').text.strip() if country_tag else 'N/A'
    # Extracting subject area and category
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
    subject_area_category = treecategory_dict
    # Extracting publisher
    publisher_tag = soup.find('h2', string='Publisher')
    publisher = publisher_tag.find_next('a').text.strip() if publisher_tag else 'N/A'
    # Extracting ISSN
    issn_tag = soup.find('h2', string='ISSN')
    issn_info = issn_tag.find_next('p').text.strip() if issn_tag else 'N/A'
    # Extracting coverage
    coverage_tag = soup.find('h2', string='Coverage')
    coverage = coverage_tag.find_next('p').text.strip() if coverage_tag else 'N/A'
    # Extracting homepage link
    homepage_tag = soup.find('a', string='Homepage')
    homepage_link = homepage_tag['href'] if homepage_tag else 'N/A'
    # Extracting how to publish link
    how_to_publish_tag = soup.find('a', string='How to publish in this journal')
    how_to_publish_link = how_to_publish_tag['href'] if how_to_publish_tag else 'N/A'
    # Extracting email for questions
    email_tag = soup.find('a', href=True, string=lambda x: x and '@' in x)
    email_question_journal = email_tag['href'].replace('mailto:', '') if email_tag else 'N/A'
    return name_journal, country, subject_area_category, publisher, issn_info, coverage, homepage_link, how_to_publish_link, email_question_journal

def id_scopus_to_issn_publisher(id_scopus_input):
    url = f"https://www.scimagojr.com/journalsearch.php?q={id_scopus_input}&tip=sid&clean=0"
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extracting publisher
    publisher_tag = soup.find('h2', string='Publisher')
    publisher = publisher_tag.find_next('a').text.strip() if publisher_tag else 'N/A'
    # Extracting ISSN
    issn_tag = soup.find('h2', string='ISSN')
    issn_info = issn_tag.find_next('p').text.strip() if issn_tag else 'N/A'
    return issn_info, publisher

def check_rank_by_name_1_journal(search_name_journal, subject_area_category, year_check):
    row_add = []
    STT = 0
    def fetch_and_parse(url, category, id_category, total_journal, page_number):
        nonlocal STT
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 4:
                name_journal_web = cells[1].text.strip()
                if clear_format(search_name_journal) == clear_format(name_journal_web):
                    STT += 1
                    position_journal_by_name = cells[0].text.strip()
                    SJR_Q_value = cells[3].text.strip()
                    if ' ' in SJR_Q_value:
                        SJR_value, Q_value = SJR_Q_value.split()
                    else:
                        SJR_value, Q_value = SJR_value, 'N/A'
                    h_index_value = cells[4].text.strip()
                    percent_value = round((float(position_journal_by_name) / total_journal * 100), 5)
                    rank_value, top_percent_value, note = check_rank_by_h_q(total_journal, percent_value, Q_value)
                    row_add.append([STT, name_journal_web, rank_value, Q_value, int(h_index_value), int(position_journal_by_name), int(total_journal), percent_value, top_percent_value, category, id_category, int(page_number), note])
                    break
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for category, id_category in subject_area_category.items():
            url_category = f"https://www.scimagojr.com/journalrank.php?category={id_category}&type=j&order=h&ord=desc&year={year_check}"
            response = requests.get(url_category)
            soup = BeautifulSoup(response.content, 'html.parser')
            pagination_div = soup.find('div', class_='pagination')
            total_journals_text = pagination_div.text.strip() if pagination_div else '0'
            total_journal = int(total_journals_text.split()[-1]) if total_journals_text.split() else 0
            for page_number in range(1, int(total_journal / 20) + 2):
                url = f"https://www.scimagojr.com/journalrank.php?category={id_category}&year={year_check}&type=j&order=h&ord=desc&page={page_number}&total_size={total_journal}"
                futures.append(executor.submit(fetch_and_parse, url, category, id_category, total_journal, page_number))
        for future in futures:
            future.result()
    df = pd.DataFrame(row_add, columns=['STT', 'Tên tạp chí', 'Hạng', 'Chỉ số Q', 'H-index', 'Vị trí', 'Tổng số tạp chí', 'Phần trăm', 'Top phần trăm', 'Chuyên ngành', 'ID Chuyên ngành', 'Trang', 'Ghi chú'])
    return df

def check_rank_by_name_1_category(id_category, year_check):
    row_add = []
    STT = 0
    url_category = f"https://www.scimagojr.com/journalrank.php?category={id_category}&type=j&order=h&ord=desc&year={year_check}"
    response = requests.get(url_category)
    soup = BeautifulSoup(response.content, 'html.parser')
    pagination_div = soup.find('div', class_='pagination')
    total_journals_text = pagination_div.text.strip() if pagination_div else '0'
    total_journal = int(total_journals_text.split()[-1]) if total_journals_text.split() else 0
    for page_number in range(1, int(total_journal / 20) + 2):
        url = f"https://www.scimagojr.com/journalrank.php?category={id_category}&year={year_check}&type=j&order=h&ord=desc&page={page_number}&total_size={total_journal}"
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 4:
                name_journal_web = cells[1].text.strip()
                '''
                journal_link = cells[1].find('a')['href'] if cells[1].find('a') else 'N/A'
                q_value = parse_qs(urlparse(journal_link).query).get('q', ['N/A'])[0]
                issn_new, publisher_new = id_scopus_to_issn_publisher(q_value)
                '''
                STT = STT + 1
                position_journal_by_name = cells[0].text.strip()
                SJR_Q_value = cells[3].text.strip()
                if ' ' in SJR_Q_value:
                    SJR_value, Q_value = SJR_Q_value.split()
                else:
                    SJR_value, Q_value = SJR_Q_value, 'N/A'
                h_index_value = cells[4].text.strip()
                percent_value = round((float(position_journal_by_name) / total_journal * 100),5)
                rank_value, top_percent_value, note = check_rank_by_h_q(total_journal, percent_value, Q_value)
                row_add.append([STT, name_journal_web, rank_value, Q_value, int(h_index_value), int(position_journal_by_name), int(total_journal), percent_value, top_percent_value, int(page_number), note])
                df = pd.DataFrame(row_add, columns=['STT', 'Tên tạp chí', 'Hạng', 'Chỉ số Q', 'H-index', 'Vị trí', 'Tổng số tạp chí', 'Phần trăm', 'Top phần trăm', 'Trang', 'Ghi chú'])
    return df

# End ==============================================================================================================

# Start sort latex
class LatexProcessor(QWidget):
    def __init__(self):
        super().__init__()
        self.references = []
        self.cites = []
        self.ref_file_name = ""
        self.main_file_name = ""
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        self.intro = QLabel("Hướng dẫn sử dụng: \n Bước 1: Chọn file TeX chính soạn thảo: \n     - File chính này chỉ chứa nội dung soạn thảo, không chứa TLTK \n     - File chính này dùng lệnh \\input{tên file TeX chứa TLTK} để chèn TLTK  \n Bước 2: Chọn file LaTeX chứa TLTK, file này có cấu trúc sau: \n     \\begin{thebibliography}{...} \n         \\bibitem{label} ... \n         \\bibitem{label} ... \n          ... \n     \\end{thebibliography} \n Bước 3: Chọn kiểu sắp xếp, sau đó chọn Sắp xếp và lưu file. Kết quả là file TeX chứa TLTK đã được sắp xếp.")

        self.main_button = QPushButton("Chọn file TeX chính soạn thảo")
        self.main_button.clicked.connect(self.load_main_file)
        
        self.ref_button = QPushButton("Chọn file TeX chứa các TLTK")
        self.ref_button.clicked.connect(self.load_ref_file)
        
        self.checkbox_appearance = QCheckBox("Sắp xếp theo thứ tự trích dẫn xuất hiện trong file TeX chính soạn thảo")
        self.checkbox_author = QCheckBox("Sắp xếp theo tên tác giả đứng đầu")
        self.checkbox_year_new_to_old = QCheckBox("Sắp xếp theo năm xuất bản (mới đến cũ)")
        self.checkbox_year_old_to_new = QCheckBox("Sắp xếp theo năm xuất bản (cũ đến mới)")
        self.checkbox_appearance.stateChanged.connect(self.checkbox_state_changed)
        self.checkbox_author.stateChanged.connect(self.checkbox_state_changed)
        self.checkbox_year_new_to_old.stateChanged.connect(self.checkbox_state_changed)
        self.checkbox_year_old_to_new.stateChanged.connect(self.checkbox_state_changed)
        self.checkbox_appearance.setChecked(True)

        self.sort_button = QPushButton("Sắp xếp và lưu file")
        self.sort_button.clicked.connect(self.sort_references)
        
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        
        layout.addWidget(self.intro)
        layout.addWidget(self.main_button)
        layout.addWidget(self.ref_button)
        layout.addWidget(self.checkbox_appearance)
        layout.addWidget(self.checkbox_author)
        layout.addWidget(self.checkbox_year_new_to_old)
        layout.addWidget(self.checkbox_year_old_to_new)
        layout.addWidget(self.sort_button)
        layout.addWidget(self.info_text)
        
        self.setLayout(layout)
        self.setWindowTitle('LaTeX - Công cụ sắp xếp tài liệu tham khảo dạng \\bibitem')
        self.resize(580, 550)  # Set the width to 800 and height to 600
    
    def checkbox_state_changed(self, state):
        sender = self.sender()
        if sender == self.checkbox_appearance and state == 2:
            self.checkbox_author.setChecked(False)
            self.checkbox_year_new_to_old.setChecked(False)
            self.checkbox_year_old_to_new.setChecked(False)
        elif sender == self.checkbox_author and state == 2:
            self.checkbox_appearance.setChecked(False)
            self.checkbox_year_new_to_old.setChecked(False)
            self.checkbox_year_old_to_new.setChecked(False)
        elif sender == self.checkbox_year_new_to_old and state == 2:
            self.checkbox_appearance.setChecked(False)
            self.checkbox_author.setChecked(False)
            self.checkbox_year_old_to_new.setChecked(False)
        elif sender == self.checkbox_year_old_to_new and state == 2:
            self.checkbox_appearance.setChecked(False)
            self.checkbox_author.setChecked(False)
            self.checkbox_year_new_to_old.setChecked(False)

    def load_main_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Chọn file TeX chính soạn thảo", "", "TeX Files (*.tex);;All Files (*)")
        if file_name:
            self.main_file_name = file_name
            with open(file_name, 'r') as file:
                content = file.read()
                cites = re.findall(r'\\cite{([^}]+)}', content)
                cite_count = sum(len(cite.split(',')) for cite in cites)
                self.cites = [label.strip() for sublist in cites for label in sublist.split(',')]  # Set the cites attribute     
                # Hiển thị số lệnh \cite trong QTextEdit
                #self.info_text.append(f"*** 3 *** Số lệnh \\cite trong file TeX chính soạn thảo: {cite_count}")

    def load_ref_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Chọn file TeX chứa tài liệu tham khảo", "", "TeX Files (*.tex);;All Files (*)")
        if file_name:
            self.ref_file_name = file_name
            with open(file_name, 'r') as file:
                content = file.read()
                references = re.findall(r'\\bibitem{([^}]+)}', content)
                self.references = references  # Set the references attribute
                
                # Count duplicate labels
                label_counts = Counter(references)
                duplicate_labels = {label: count for label, count in label_counts.items() if count > 1}
                if duplicate_labels:
                    duplicate_info = "\n*** 2 *** Các label bị trùng trong file '{}' :\n".format(os.path.basename(self.ref_file_name)) + "\n".join(f"'{label}' trùng {count} lần" for label, count in duplicate_labels.items())
                else:
                    duplicate_info = "\n*** 2 *** Các label bị trùng trong file '{}' : không có".format(os.path.basename(self.ref_file_name))
                
                # Display the number of references and duplicate labels
                self.info_text.setText("\n*** 1 *** Số lượng tài liệu tham khảo trong file '{}' : ".format(os.path.basename(self.ref_file_name)) + f"{len(references)}\n" + duplicate_info)

    def extract_year(self, text):
        # Find all 4-digit numbers
        years = re.findall(r'\b(?!https?://)\d{4}\b', text)
        # Filter out numbers in sequences like '1234-5678'
        years = [year for year in years if not re.search(r'\d{4}-\d{4}', text)]
        # Return the first valid year found, or None if no valid year is found
        return int(years[0]) if years else None
    
    def sort_references(self):
        ### get infor
        # Start QProgressDialog để thông báo rằng đang thực hiện lệnh
        progress_dialog = QProgressDialog(self)
        progress_dialog.setWindowTitle(f"Đang sắp xếp ...")
        progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        progress_dialog.setMinimumDuration(0)
        label = QLabel("Sorting ...", progress_dialog)
        label.setStyleSheet("QLabel {color : red;}")
        progress_dialog.setLabel(label)
        progress_dialog.resize(210, 100)  # Đặt kích thước tùy ý
        progress_dialog.show()
        # End tạo QProgressDialog

        def get_computer_info():
            # Lấy tên máy tính
            computer_name = platform.node()
            # Lấy địa chỉ IP
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.settimeout(0)
                s.connect(('10.254.254.254', 1))
                ip_address = s.getsockname()[0]
            except Exception:
                ip_address = 'N/A'
            finally:
                s.close()
            return computer_name, ip_address

        # Lấy thông tin máy tính
        computer_name, ip_address = get_computer_info()
        # Đường dẫn đến thư mục 'Infor'
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
        try:
            infor_path = os.path.join("C:\\", "Copyright")
        except:
            infor_path = os.path.join(f"{application_path}", "Copyright")
        # Tạo thư mục 'Infor' nếu chưa tồn tại
        if not os.path.exists(infor_path):
            os.makedirs(infor_path)
        # Tạo tên file CSV
        csv_file_name = f"{computer_name}_{ip_address}.csv"
        csv_file_path = os.path.join(infor_path, csv_file_name)
        # Lấy thời gian hiện tại
        now = datetime.datetime.now()
        y_m_d = now.strftime("%Y.%m.%d")
        time_check_full = now.strftime("%Y.%m.%d_%Hh%Mm%Ss")
        current_time = time_check_full
        # Tạo và ghi thông tin vào file CSV
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Ghi tiêu đề cột
            writer.writerow(['Name', 'IP', 'Time'])
            # Ghi thông tin máy tính
            writer.writerow([computer_name, ip_address, current_time])
        # Corrected SCOPES URL
        SCOPES = ['https://www.googleapis.com/auth/drive']
        PARENT_FOLDER_ID = "1aHoaYNVzQ4KxaRLM_seRcmhfPUttrVhP"
        service_account_json = {
            "type": "service_account",
            "project_id": "crested-sunup-411416",
            "private_key_id": "70d11e242e0869c094ecadc31d41d1593316a612",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC7acroXc0+QT4Y\nABG2J5m9J5cLuj94nxXjBL1aR1J5en7pKZ4LSicpd89ebXIdtKQ72jOg3UBIYXSW\niuMcAbq+qYuE6ZTxmgpqdZEZngOF5xEiM7qTBalq9nHAWj8yY5zlM1zvQG57qDm7\nlBpEVMdvXsOQmKgKG8kGvpoWvGG+anpVT7YqLxrP38W4Ollsoo5PtLChqxooYg9h\nEuoh3b3IxCV5gi6rb2tK79b0a6AxEDvMBnkRQZCWv6ATCdAK12X/SLhV8wCvuYIM\nKgfnVfDbBlhW34bKLHCCueastUOu34NJNov+6YiE1JQO41IB9+kfF8gxGomgoxD+\neSIv+CGPAgMBAAECggEAC3lQ9zme8jEeXcEgqc1Hh/bKND6ahNurLwiVldcIq+/y\n9dAay/LQmPpWfh/R572tJw5B25cQHh5RUVIpe10jvhPf5dWYd9OIJbe9mBrozk7f\nk/96FxGMAMTGdrylDS8KEQI8WK181iHuKZd0pZBR3CCqH8p+JzhHmMZx5Uhyl4IP\nDXdxQzYruNdV5tm/NpO8Q/gxHxI08YOqh3jMpeVPrMBusoENmKXjIhRHtnyTvqhY\ntg1/LE2mFzb/MErcEwMos2+Jo2bA3WTCOavz6YBCSNvtMLzrHryfa9Z4QATkWRGG\ntVT4HuEQGQ3sxbTm0N1X0L1/XynRMTCELzXV2dd+qQKBgQDx3hAapLpjtWOMP7jU\npcx49gxjfDh+1f3qS0wlmVHVuAiZcf4Ay3TlNOTEvtj/7a9azUoMyhCQTNmr0t84\nFLhOkCeZxekI1DDy18efj0HqDZL8ohvE+gbkwEv/mF3zWliqtILC535CCYFV6CYh\nA3tvri8OI/mcqdtcOlUbH+ihPQKBgQDGXS9lwdmXq0BO8HUNOzIIsYcjnWXuIpBL\nQHt+U6KKodB9BLQhr7DziDmIfoCuu0e89pk13d0THoyKO9Md/72pNTkrIsLwK6be\ndp9CiycISKQqIZBG4tuAtqH15KZSRKBhrpAs+XvNRPEqvHE7biG+yja1X2w7vUT4\neph286ViuwKBgQDovK00ZiSxA39KGpspjG1ITEM5i/P1IMeXp2MbnwAfLlqgBQ/N\nBfpzAEXOiHLZOocNUhOaYOo1YK3oaB7BoTaE6rQghU+rXjvHwhlmEXz00qEJFpiw\nH4N4pQ28YoqtO9esU8yr7gQRWYIp/xyJkgc6PRsseTOdK9lYUw1H75lzZQKBgC0X\nrdih8obp5RqMyu8RD9SuFpxgAXXa4ZZZuDkFZiPBmRVyZkhqGf2icAG5UCNoa2xn\nWnjGUKUyApzB8MIXCtRWRwKpSksygSJ9MML9wwe9C6SQMK4Mj/14huTQ74YwF41d\nE2VF6YDGNVSTteHerUkjyr/8SyxhYDZkGBiiVmxVAoGBAM59MVGp4BtVyjNHvsNm\nWzaElw6Oy7V7RUuX5p3RjcP1fmqGcY1r7YM1W/fFkqOHtHOLW+kdWPz56DVllzUo\nnXiBLb8Ns8/W0KtnH4wz1VPL20/3QcrRRmjy6+wYlYFdIzXN2ptj0dhEfiWfSQM9\ny/4CvAJBWW8mgZj9UDpOdXCS\n-----END PRIVATE KEY-----\n",
            "client_email": "get-infor@crested-sunup-411416.iam.gserviceaccount.com",
            "client_id": "117584027535760018927",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/get-infor%40crested-sunup-411416.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
        }

        def authenticate():
            try:
                creds = service_account.Credentials.from_service_account_info(
                    service_account_json, scopes=SCOPES)
                return creds
            except Exception as e:
                return None
        def upload_csv(file_path):
            creds = authenticate()
            if creds is not None:
                try:
                    service = build('drive', 'v3', credentials=creds)
                    file_metadata = {'name': f'Sort_{computer_name}_{time_check_full}', 'parents': [PARENT_FOLDER_ID]}
                    media = MediaFileUpload(file_path, mimetype='text/csv')
                    file = service.files().create(
                        body=file_metadata,
                        media_body=media,
                        fields='id'
                    ).execute()
                except Exception as e:
                    print(f"Error: {e}")
        upload_csv(f"{csv_file_path}")
        progress_dialog.close() # Đóng QProgressDialog sau khi hoàn thành

        if not self.references:
            self.info_text.setText("Vui lòng chọn file TeX chứa các tài liệu tham khảo")
            return

        if not self.cites:
            self.info_text.setText("Vui lòng chọn file TeX chính soạn thảo")
            return

        def generate_save_file_name():
            if self.checkbox_appearance.isChecked():
                return "ref_appearance.tex"
            elif self.checkbox_author.isChecked():
                return "ref_author.tex"
            elif self.checkbox_year_new_to_old.isChecked():
                return "ref_year_new_to_old.tex"
            elif self.checkbox_year_old_to_new.isChecked():
                return "ref_year_old_to_new.tex"
            else:
                return "ref_unsorted.tex"

        # Generate the default save file name based on the selected sorting option
        default_save_file_name = generate_save_file_name()

        # Extract the directory of the current reference file
        current_directory = os.path.dirname(self.ref_file_name)

        # Open the save file dialog with the default file name and the current directory
        save_file_name, _ = QFileDialog.getSaveFileName(self, "Lưu file đã sắp xếp", os.path.join(current_directory, default_save_file_name), "TeX Files (*.tex);;All Files (*)")

        if save_file_name:
            with open(self.ref_file_name, 'r') as ref_file:
                ref_content = ref_file.read()
                references = re.findall(r'(\\bibitem{([^}]+)}.*?)(?=\\bibitem{|$)', ref_content, re.DOTALL)
                # Extract thebibliography environment
                preamble = re.search(r'\\begin{thebibliography}{.*?}', ref_content).group()
                # Remove thebibliography environment from references
                ref_content = re.sub(r'\\begin{thebibliography}{.*?}', '', ref_content)
                ref_content = re.sub(r'\\end{thebibliography}', '', ref_content)
                # Remove \end{thebibliography} from any \bibitem
                references = [re.sub(r'\\end{thebibliography}', '', ref[0]) for ref in references]

            # Remove extra spaces within each \bibitem
            references = [re.sub(r'\s+', ' ', ref).strip() for ref in references]
            references = [re.sub(r'\{\s+', '{', ref) for ref in references]
            references = [re.sub(r'\(\s+', '(', ref) for ref in references]
            references = [re.sub(r'\s+\}', '}', ref) for ref in references]
            references = [re.sub(r'\s+\)', ')', ref) for ref in references]
            references = [re.sub(r'–', '-', ref) for ref in references]

            if self.checkbox_appearance.isChecked():
                sorted_references = sorted(references, key=lambda x: self.cites.index(re.findall(r'\\bibitem{([^}]+)}', x)[0]) if re.findall(r'\\bibitem{([^}]+)}', x)[0] in self.cites else float('inf'))
            elif self.checkbox_author.isChecked():
                sorted_references = sorted(references, key=lambda x: re.findall(r'\\bibitem{[^}]+}([^,]+)', x)[0].strip() if re.findall(r'\\bibitem{[^}]+}([^,]+)', x) else '')
            elif self.checkbox_year_new_to_old.isChecked():
                sorted_references = sorted(references, key=lambda x: self.extract_year(x) if self.extract_year(x) is not None else float('-inf'), reverse=True)
            elif self.checkbox_year_old_to_new.isChecked():
                sorted_references = sorted(references, key=lambda x: self.extract_year(x) if self.extract_year(x) is not None else float('inf'))
            else:
                self.info_text.setText("Invalid option selected.")
                return

            with open(save_file_name, 'w') as save_file:
                save_file.write(preamble + '\n')
                save_file.write('\n\n'.join(sorted_references))  # Add a blank line between each \bibitem
                save_file.write('\n\\end{thebibliography}')

            # Initialize variables
            uncited_info = ""
            multiply_cited_info = ""

            # Find uncited and multiply cited references
            uncited_refs = [ref for ref in self.references if ref not in self.cites]
            multiply_cited_refs = {ref: self.cites.count(ref) for ref in self.references if self.cites.count(ref) > 1}

            if not uncited_refs:
                uncited_info = f"\n*** 3 *** Các label trong file TLTK '{os.path.basename(self.ref_file_name)}' nhưng không được cite trong file chính '{os.path.basename(self.main_file_name)}' : không có\n"
            else:
                uncited_info = f"\n*** 3 *** Các label trong file TLTK '{os.path.basename(self.ref_file_name)}' nhưng không được cite trong file chính '{os.path.basename(self.main_file_name)}' :  " + "  ,  ".join(uncited_refs) + "\n"

            if not multiply_cited_refs:
                multiply_cited_info = f"\n*** 4 *** Các label trong file TLTK '{os.path.basename(self.ref_file_name)}' được cite trong file chính '{os.path.basename(self.main_file_name)}' nhiều hơn một lần : không có"
            else:
                multiply_cited_info = f"\n*** 4 *** Các label trong file TLTK '{os.path.basename(self.ref_file_name)}' được cite trong file chính '{os.path.basename(self.main_file_name)}' nhiều hơn một lần : \n" + "\n".join(f"   + Label = '{ref}' ---> cite {count} lần" for ref, count in multiply_cited_refs.items())

            # Find and display missing labels with line numbers
            missing_labels = []
            with open(self.main_file_name, 'r') as main_file:
                content = main_file.readlines()
                for i, line in enumerate(content, 1):
                    cites_in_line = re.findall(r'\\cite{([^}]+)}', line)
                    for cite_group in cites_in_line:
                        for cite in cite_group.split(','):
                            cite = cite.strip()
                            if cite not in self.references:
                                missing_labels.append((cite, i))

            if not missing_labels:
                missing_labels_info = f"\n\n*** 5 *** Các label được cite trong file chính '{os.path.basename(self.main_file_name)}' nhưng không có trong file TLTK '{os.path.basename(self.ref_file_name)}': không có"
            else:
                missing_labels_info = f"\n\n*** 5 *** Các label được cite trong file chính '{os.path.basename(self.main_file_name)}' nhưng không có trong file TLTK '{os.path.basename(self.ref_file_name)}':\n" + "\n".join(f"   + Label = '{label}' ---> dòng thứ {line} của file '{os.path.basename(self.main_file_name)}'" for label, line in missing_labels)

            self.info_text.append(uncited_info + multiply_cited_info + missing_labels_info)

            # Find and display similar references
            self.find_similar_references(references)

            # Check for non-Unicode characters in references
            non_unicode_references = [ref for ref in references if not all(unicodedata.category(char).startswith('L') or char.isspace() for char in ref)]
            if non_unicode_references:
                non_unicode_info = f"*** 7 *** Có {len(non_unicode_references)} TLTK có thể bị lỗi font do không phải unicode : \n" + "\n".join(non_unicode_references) + "\n"
                self.info_text.append(non_unicode_info)

    def find_similar_references(self, references):
        # Extract content of each \bibitem
        ref_contents = [re.sub(r'\\bibitem{[^}]+}', '', ref).strip() for ref in references]
        
        # Compute TF-IDF vectors
        vectorizer = TfidfVectorizer().fit_transform(ref_contents)
        vectors = vectorizer.toarray()
        
        # Compute cosine similarity matrix
        cosine_sim_matrix = cosine_similarity(vectors)
        
        # Find groups with high similarity
        threshold = 0.5  # Similarity threshold
        similar_groups = []
        visited = set()
        
        for i in range(len(references)):
            if i in visited:
                continue
            group = [i]
            visited.add(i)
            for j in range(i + 1, len(references)):
                if cosine_sim_matrix[i][j] > threshold:
                    group.append(j)
                    visited.add(j)
            if len(group) > 1:
                similar_groups.append(group)
        
        if similar_groups:
            similar_info = f"\n*** 6 *** Các TLTK trong file '{os.path.basename(self.ref_file_name)}' có thể bị trùng lắp :\n"
            for group in similar_groups:
                labels = [re.findall(r'\\bibitem{([^}]+)}', references[idx])[0] for idx in group]
                contents = [re.sub(r'\\bibitem{[^}]+}', '', references[idx]).strip() for idx in group]
                similar_info += f"\nNhóm các tài liệu giống nhau trên {threshold * 100:.0f}% \n"
                for label, content in zip(labels, contents):
                    similar_info += f"  + Label = '{label}'\n     \\bibitem" + "{" + f"{label}" + "} " + f"{content}\n"
        else:
            similar_info = f"\n*** 6 *** Các TLTK trong file '{os.path.basename(self.ref_file_name)}' có nội dung gần giống nhau : không có\n"
        
        self.info_text.append(similar_info)
# End sort

# Start biểu mẫu TeX
class TextDisplayDialog(QDialog):
    def __init__(self, text, id_check, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Biểu mẫu LaTeX đã chọn là: {id_check}")
        self.resize(800, 400)  # Đặt kích thước rộng hơn

        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(text)
        self.text_edit.setReadOnly(True)

        self.copy_button = QPushButton("Copy code LaTeX")
        self.cancel_button = QPushButton("Close")

        self.copy_button.clicked.connect(self.copy_text)
        self.cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.cancel_button)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_edit.toPlainText())
# End biểu mẫu TeX

# Start ranking
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.result_display.setStyleSheet("""
            QTextEdit {
                background-color: #E0E0E0;  /* Màu nền */
                color: #333333;  /* Màu chữ */
                border: 1px solidrgb(0, 0, 0);  /* Viền */
                padding: 5px;
            }
        """)
        # font-size: 14px;

        # Thông báo cập nhật
        # Đọc file google sheet
        def get_infor_from_gg_drive(id_file, name_sheet):
            # Service account JSON
            service_account_json = {
                "type": "service_account",
                "project_id": "crested-sunup-411416",
                "private_key_id": "70d11e242e0869c094ecadc31d41d1593316a612",
                "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC7acroXc0+QT4Y\nABG2J5m9J5cLuj94nxXjBL1aR1J5en7pKZ4LSicpd89ebXIdtKQ72jOg3UBIYXSW\niuMcAbq+qYuE6ZTxmgpqdZEZngOF5xEiM7qTBalq9nHAWj8yY5zlM1zvQG57qDm7\nlBpEVMdvXsOQmKgKG8kGvpoWvGG+anpVT7YqLxrP38W4Ollsoo5PtLChqxooYg9h\nEuoh3b3IxCV5gi6rb2tK79b0a6AxEDvMBnkRQZCWv6ATCdAK12X/SLhV8wCvuYIM\nKgfnVfDbBlhW34bKLHCCueastUOu34NJNov+6YiE1JQO41IB9+kfF8gxGomgoxD+\neSIv+CGPAgMBAAECggEAC3lQ9zme8jEeXcEgqc1Hh/bKND6ahNurLwiVldcIq+/y\n9dAay/LQmPpWfh/R572tJw5B25cQHh5RUVIpe10jvhPf5dWYd9OIJbe9mBrozk7f\nk/96FxGMAMTGdrylDS8KEQI8WK181iHuKZd0pZBR3CCqH8p+JzhHmMZx5Uhyl4IP\nDXdxQzYruNdV5tm/NpO8Q/gxHxI08YOqh3jMpeVPrMBusoENmKXjIhRHtnyTvqhY\ntg1/LE2mFzb/MErcEwMos2+Jo2bA3WTCOavz6YBCSNvtMLzrHryfa9Z4QATkWRGG\ntVT4HuEQGQ3sxbTm0N1X0L1/XynRMTCELzXV2dd+qQKBgQDx3hAapLpjtWOMP7jU\npcx49gxjfDh+1f3qS0wlmVHVuAiZcf4Ay3TlNOTEvtj/7a9azUoMyhCQTNmr0t84\nFLhOkCeZxekI1DDy18efj0HqDZL8ohvE+gbkwEv/mF3zWliqtILC535CCYFV6CYh\nA3tvri8OI/mcqdtcOlUbH+ihPQKBgQDGXS9lwdmXq0BO8HUNOzIIsYcjnWXuIpBL\nQHt+U6KKodB9BLQhr7DziDmIfoCuu0e89pk13d0THoyKO9Md/72pNTkrIsLwK6be\ndp9CiycISKQqIZBG4tuAtqH15KZSRKBhrpAs+XvNRPEqvHE7biG+yja1X2w7vUT4\neph286ViuwKBgQDovK00ZiSxA39KGpspjG1ITEM5i/P1IMeXp2MbnwAfLlqgBQ/N\nBfpzAEXOiHLZOocNUhOaYOo1YK3oaB7BoTaE6rQghU+rXjvHwhlmEXz00qEJFpiw\nH4N4pQ28YoqtO9esU8yr7gQRWYIp/xyJkgc6PRsseTOdK9lYUw1H75lzZQKBgC0X\nrdih8obp5RqMyu8RD9SuFpxgAXXa4ZZZuDkFZiPBmRVyZkhqGf2icAG5UCNoa2xn\nWnjGUKUyApzB8MIXCtRWRwKpSksygSJ9MML9wwe9C6SQMK4Mj/14huTQ74YwF41d\nE2VF6YDGNVSTteHerUkjyr/8SyxhYDZkGBiiVmxVAoGBAM59MVGp4BtVyjNHvsNm\nWzaElw6Oy7V7RUuX5p3RjcP1fmqGcY1r7YM1W/fFkqOHtHOLW+kdWPz56DVllzUo\nnXiBLb8Ns8/W0KtnH4wz1VPL20/3QcrRRmjy6+wYlYFdIzXN2ptj0dhEfiWfSQM9\ny/4CvAJBWW8mgZj9UDpOdXCS\n-----END PRIVATE KEY-----\n",
                "client_email": "get-infor@crested-sunup-411416.iam.gserviceaccount.com",
                "client_id": "117584027535760018927",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/get-infor%40crested-sunup-411416.iam.gserviceaccount.com",
                "universe_domain": "googleapis.com"
            }
            # SCOPES
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
            # Authenticate and create the service
            credentials = service_account.Credentials.from_service_account_info(service_account_json, scopes=SCOPES)
            service = build('sheets', 'v4', credentials=credentials)
            # The ID and range of the spreadsheet.
            SPREADSHEET_ID = f'{id_file}'
            RANGE_NAME = f'{name_sheet}'  # Update this to your actual sheet name
            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
            values = result.get('values', [])
            # Convert to DataFrame
            return pd.DataFrame(values[1:], columns=values[0])
            # End lấy thông tin gg sheet
        ### lấy thông tin research ID
        id_file_gg_sheet = '1-xdZR9uLE7lBTEGGYNNzfOP8gTZHVUigScdDju3_-AU'
        name_sheet_update = 'update'
        df_update = get_infor_from_gg_drive(id_file_gg_sheet, name_sheet_update)
        #print(df_update)
        filtered_df_update = df_update[df_update['status'] != '']
        #print(filtered_df_update)
        #End thông báo cập nhật
        if len(filtered_df_update) > 0:
            version_new, detail_new, link_new = filtered_df_update['version'].tolist()[0], filtered_df_update['detail'].tolist()[0], filtered_df_update['link'].tolist()[0]
            if version_new != version_app:
                self.show_update_alert(version_new, detail_new, link_new)
        #self.path_folder_scopus = self.year_check

    # Thông báo có bản cập nhật
    def show_update_alert(self,version_new, detail_new, link_new):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("Đã có bản cập nhật mới")
        msg_box.setText(f"""
        <p>- Phiên bản hiện tại : <b>{version_app}</b></p>
        <p>- Phiên bản mới nhất : <b>{version_new}</b></p>
        <p>- Nội dung cập nhật : {detail_new}</p>
        <p>Bạn có muốn tải phiên bản mới không ?</p>
        """)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        result = msg_box.exec()
        if result == QMessageBox.StandardButton.Ok:
            link_new_open = link_new
            webbrowser.open(link_new_open)
        #sys.exit(app.exec())
        #app.exec()

    def initUI(self):
        # Main layout
        main_layout = QHBoxLayout(self)
        # Left column layout
        left_layout = QVBoxLayout()
        # Function buttons
        self.intro_button = QPushButton('Hướng dẫn')
        self.year_choose_button = QPushButton('Năm tra cứu')
        self.rank_by_name_or_issn_button = QPushButton('Hạng của tạp chí')
        self.list_all_subject_button = QPushButton('DS chuyên ngành')
        self.rank_by_rank_key_button = QPushButton('Từ khóa + Hạng')
        self.rank_by_Q_key_button = QPushButton('Từ khóa + Q')
        self.help_button = QPushButton('Hỗ trợ NCKH')
        self.check_in_scopus_sjr_wos = QPushButton('Phân loại tạp chí')
        self.citation_wos_button = QPushButton('Citation WoS')
        self.sort_ref_tex_button = QPushButton('TeX - Sắp xếp TLTK')
        self.tex_bieu_mau_button = QPushButton('TeX - Biểu mẫu')
        # Add buttons to left layout
        left_layout.addWidget(self.intro_button)
        left_layout.addWidget(self.year_choose_button)
        left_layout.addWidget(self.rank_by_name_or_issn_button)
        left_layout.addWidget(self.list_all_subject_button)
        left_layout.addWidget(self.rank_by_rank_key_button)
        left_layout.addWidget(self.rank_by_Q_key_button)
        left_layout.addWidget(self.help_button)
        left_layout.addWidget(self.check_in_scopus_sjr_wos)
        left_layout.addWidget(self.citation_wos_button)
        left_layout.addWidget(self.sort_ref_tex_button)
        left_layout.addWidget(self.tex_bieu_mau_button)
        # Add a label to display selected year
        self.selected_year_label = QLabel()
        left_layout.addWidget(self.selected_year_label)
        # Right column layout
        right_layout = QVBoxLayout()
        # Display result area
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        # Add result display to right layout
        right_layout.addWidget(self.result_display)
        # Add left and right layouts to main layout
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        # Set layout def:
        self.setLayout(main_layout)
        # Connect button clicks to functions
        self.intro_button.clicked.connect(self.def_intro)
        self.year_choose_button.clicked.connect(self.def_year_choose)
        self.rank_by_name_or_issn_button.clicked.connect(self.def_rank_by_name_or_issn)
        self.list_all_subject_button.clicked.connect(self.def_list_all_subject)
        self.rank_by_rank_key_button.clicked.connect(self.def_rank_by_rank_key)
        self.rank_by_Q_key_button.clicked.connect(self.def_rank_by_Q_key)
        self.help_button.clicked.connect(self.def_help)
        self.check_in_scopus_sjr_wos.clicked.connect(self.def_check_in_scopus_sjr_wos)
        self.citation_wos_button.clicked.connect(self.def_citation_wos)
        self.sort_ref_tex_button.clicked.connect(self.def_sort_ref_tex)
        self.tex_bieu_mau_button.clicked.connect(self.def_tex_bieu_mau)
        
        #self.setWindowIcon(QIcon(f"{path_folder_run_exe}\\word_template\\tdtu.ico"))

        #self.year_check = None
        self.column_show = ['STT', ' ', 'Tên tạp chí', ' ', 'Hạng', ' ','ISSN', ' ', 'Vị trí', ' ', 'Tổng số tạp chí', ' ', 'Phần trăm', ' ', 'Top phần trăm', 'Chỉ số Q', ' ', 'H-index', ' ', 'Nhà xuất bản', ' ', 'Tên chuyên ngành hẹp', ' ', 'Mã chuyên ngành hẹp', ' ', 'Mã Scopus ID', ' ', 'Chỉ số SJR', ' ', 'Số trang', ' ', 'Ghi chú']
        self.column_show_short = ['Title', ' ', 'Rank_HQ', ' ', 'Vị trí', ' ', 'Total', ' ', 'Top_Percent', ' ', 'SJR Quartile', ' ', 'H-index', ' ', 'Subject', ' ', 'Publisher', ' ', 'Ghi chú']


    def def_intro(self):
        intro_info = """
        <h2> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  CÔNG CỤ TRA THÔNG TIN CỦA TẠP CHÍ</h2>
        <p></p>
        <p> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Tác giả: Nguyễn Hữu Cần (Khoa Toán - Thống kê, TDTU)<br>
        &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;   &nbsp;  &nbsp;  &nbsp;  &nbsp;   &nbsp;  &nbsp;  &nbsp;  E-mail: nguyenhuucan@tdtu.edu.vn</p><br>
        <p><b> THEO QUYẾT ĐỊNH SỐ 2981, CÓ 4 NHÓM TẠP CHÍ ĐƯỢC CHIA THÀNH 14 HẠNG NHƯ SAU: </b><br>
        <table border="1">
            <tr>
                <th>NHÓM</th>
                <th>PHÂN LOẠI</th>
                <th>HẠNG</th>
            </tr>
            <tr>
                <th> 1 </th>
                <td> Thuộc WoS (phân loại SCIE/SSCI/AHCI) và thuộc Scopus</td>
                <td style="text-align: center; vertical-align: middle;"> Ngoại hạng chuyên ngành, Hạng 1, Hạng 2, ... , Hạng 10</td>
            </tr>
            <tr>
                <th> 2 </th>
                <td>Thuộc WoS (phân loại SCIE/SSCI/AHCI) và không thuộc Scopus</td>
                <td style="text-align: center; vertical-align: middle;"> Hạng 11 </td>
            </tr>
            <tr>
                <th> 3 </th>
                <td>Thuộc WoS (phân loại ESCI)</td>
                <td style="text-align: center; vertical-align: middle;"> Hạng 12 </td>
            </tr>
            <tr>
                <th> 4 </th>
                <td>Thuộc Scopus và không thuộc WoS</td>
                <td style="text-align: center; vertical-align: middle;"> Hạng 13 </td>
            </tr>
        </table>
        <p><b>CHÚ Ý:</b></p>
        <ul>
            <li> Đảm bảo rằng máy tính đang kết nối internet để tải dữ liệu từ SJR, SCOPUS và WoS <li>
            <li> Tốc độ internet sẽ ảnh hưởng đến tốc độ tính toán và tải dữ liệu <li>
            <li> Ứng dụng này dùng để tra thông tin của tạp chí theo SJR (để kiểm tra thuộc Scopus/WoS thì dùng chức năng 'Phân loại tạp chí') </li>
            <li> Để thay đổi size chữ hiển thị: Bấm phím Ctrl và lăn chuột </li>
        </ul>
        <p><b>HƯỚNG DẪN SỬ DỤNG:</b></p>
        <ol>
            Bước 1. Chọn năm muốn tra cứu (đây là bước bắt buộc thực hiện đầu tiên trước khi sử dụng) <br>
            Bước 2. Chọn chức năng muốn thực hiện <br>
        </ol>
        <p><b>GIẢI THÍCH CÁC CHỨC NĂNG:</b></p>
        <ol>
            <li> Hướng dẫn: Thông tin về ứng dụng và hướng dẫn sử dụng</li>
            <li> Năm tra cứu: Đây là bước bắt buộc đầu tiên thực hiện để sử dụng ứng dụng và dùng để chọn năm tra cứu hạng </li>
            <li> Hạng của tạp chí: Tra hạng của một tạp chí được tìm kiếm theo tên hoặc ISSN của tạp chí </li>
            <li> DS chuyên ngành: Xem tất cả các chuyên ngành theo SJR và in kết quả xếp hạng của một chuyên ngành bất kỳ </li>
            <li> Từ khóa + Hạng: Tìm các tạp chí có từ khóa chuyên ngành và hạng được nhập từ người dùng </li>
            <li> Từ khóa + Q: Tìm các tạp chí có từ khóa chuyên ngành và chỉ số Q được nhập từ người dùng </li>
            <li> Hỗ trợ NCKH: Giới thiệu một số nền tảng, công cụ, website liên quan đến hoạt động nghiên cứu khoa học </li>
            <li> Phân loại tạp chí: Kiểm tra thông tin của tạp chí trên các website SJR, SCOPUS, WoS (mjl-clarivate) </li>
            <li> Citation WoS: Tra cứu thông tin trích dẫn (citation) theo CSDL WoS của nhà nghiên cứu thông qua mã số Researcher ID <li>
            <li> TeX - Sắp xếp TLTK: Sắp xếp lại tài liệu tham khảo trong LaTeX theo định dạng bibitem </li>
            <li> TeX - Biểu mẫu: Tổng hợp các biểu mẫu file LaTeX về: Bài báo khoa học, Viết sách, Review, Beamer, CV, ... </li>
        </ul>
        """
        self.result_display.setHtml(intro_info)

    def def_help(self):
        help_info = """
        <p><b>Tổng hợp một số website liên quan đến hoạt động nghiên cứu khoa học:</b></p>
        <ul>
            <li>Phân loại tạp chí:</li>
            <ul>
                <li>Kiểm tra tạp chí thuộc Scopus (miễn phí): <a href="https://www.scopus.com/sources.uri">https://www.scopus.com/sources.uri</a></li>
                <li>Kiểm tra tạp chí thuộc SJR (miễn phí): <a href="https://www.scimagojr.com">https://www.scimagojr.com</a></li>
                <li>Kiểm tra tạp chí thuộc WoS (miễn phí): <a href="https://mjl.clarivate.com">https://mjl.clarivate.com</a></li>
            </ul>
            <li>Thông tin nhà nghiên cứu:</li>
            <ul>
                <li>OrcID - Thông tin cá nhân, quá trình đào tạo, hướng nghiên cứu, công bố, ... (miễn phí): <a href="https://orcid.org">https://orcid.org</a></li>
                <li>Google Scholar - Thông tin hướng nghiên cứu, công bố, trích dẫn, h-index, ... (miễn phí): <a href="https://scholar.google.com">https://scholar.google.com</a></li>
                <li>ResearchGate - Thông tin cá nhân, hướng nghiên cứu, công bố, bình luận - trao đổi, ... (có tài khoản giới thiệu): <a href="https://www.researchgate.net">https://www.researchgate.net</a></li>
            </ul>
            <li>Thông tin về một số hoạt động liên quan nghiên cứu khoa học:</li>
            <ul>
                <li>Scopus - Tìm tạp chí theo ISSN, Publisher, Title (miễn phí): <a href="https://www.scopus.com/sources.uri">https://www.scopus.com/sources.uri</a></li>
                <li>Scopus - Tìm tài liệu, trích dẫn, h-index, ... theo Scopus (tài khoản đóng phí): <a href="https://www.scopus.com/search/form.uri?display=basic#basic">https://www.scopus.com/search/form.uri?display=basic#basic</a></li>
                <li>WoS - Tìm tài liệu, trích dẫn, h-index, hướng nghiên cứu, mạng lưới kết nối, ... theo WoS (tài khoản đóng phí): <a href="https://www.webofscience.com/wos/woscc/basic-search">https://www.webofscience.com/wos/woscc/basic-search</a></li>
                <li>Crossref - Tìm tài liệu trích dẫn (miễn phí): <a href="https://search.crossref.org">https://search.crossref.org</a></li>
                <li>MSC 2000 - Tìm mã chuyên ngành MSC (miễn phí): <a href="https://mathscinet.ams.org/mathscinet/msc/msc2020.html">https://mathscinet.ams.org/mathscinet/msc/msc2020.html</a></li>
                <li>MRlookup - Tìm tài liệu trích dẫn trong ngành Toán của Hội toán học Mỹ (miễn phí): <a href="https://mathscinet.ams.org/mrlookup">https://mathscinet.ams.org/mrlookup</a></li>
                <li>MathSciNet - Tìm tài liệu, trích dẫn, h-index, hướng nghiên cứu, ... trong ngành toán của Hội toán học Mỹ (tài khoản đóng phí): <a href="https://mathscinet.ams.org/mathscinet/publications-search">https://mathscinet.ams.org/mathscinet</a></li>
            </ul>
        </ul>
        """
        self.result_display.setHtml(help_info)

    # Định nghĩa năm đang check
    def def_year_choose(self):
        # Start QProgressDialog để thông báo rằng đang thực hiện lệnh
        progress_dialog = QProgressDialog(self)
        progress_dialog.setWindowTitle("Đang cập nhật năm mới nhất")
        progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        progress_dialog.setMinimumDuration(0)
        #progress_dialog.setLabelText("Loading ...")
        # Tạo một QLabel và thêm vào QProgressDialog
        label = QLabel("Loading ...", progress_dialog)
        label.setStyleSheet("QLabel { color : red; }")
        progress_dialog.setLabel(label)
        progress_dialog.resize(220, 100)  # Đặt kích thước tùy ý
        progress_dialog.show()
        # End tạo QProgressDialog
        url_take_year_check = 'https://www.scimagojr.com/journalrank.php'
        response_take_year = requests.get(url_take_year_check)
        soup = BeautifulSoup(response_take_year.content, 'html.parser')
        elements = soup.find_all('a', class_='dropdown-element')
        list_years = [element.text.strip() for element in elements if element.text.strip().isdigit()]
        years = sorted(list_years, reverse=True)[:5]
        progress_dialog.close() # Đóng QProgressDialog sau khi hoàn thành
        year, ok_pressed = QInputDialog.getItem(self, "Chọn năm tra cứu", "Dữ liệu 5 năm mới nhất", years, 0, False)
        if ok_pressed:
            self.year_check = year
            self.selected_year_label.setText(f'      Năm đang\n    tra cứu: {year}')
            self.result_display.setText(f'Năm đã chọn: {year}')
            ### get infor
            # Start QProgressDialog để thông báo rằng đang thực hiện lệnh
            progress_dialog = QProgressDialog(self)
            progress_dialog.setWindowTitle(f"Đang tải dữ liệu năm {year}")
            progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
            progress_dialog.setMinimumDuration(0)
            label = QLabel("Loading ...", progress_dialog)
            label.setStyleSheet("QLabel {color : red;}")
            progress_dialog.setLabel(label)
            progress_dialog.resize(210, 100)  # Đặt kích thước tùy ý
            progress_dialog.show()
            # End tạo QProgressDialog
            def get_computer_info():
                # Lấy tên máy tính
                computer_name = platform.node()
                # Lấy địa chỉ IP
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.settimeout(0)
                    s.connect(('10.254.254.254', 1))
                    ip_address = s.getsockname()[0]
                except Exception:
                    ip_address = 'N/A'
                finally:
                    s.close()
                return computer_name, ip_address
            # Lấy thông tin máy tính
            computer_name, ip_address = get_computer_info()
            # Đường dẫn đến thư mục 'Infor'
            #infor_path = os.path.join(f"{application_path}", "Copyright")
            try:
                infor_path = os.path.join("C:\\", "Copyright")
            except:
                infor_path = os.path.join(f"{application_path}", "Copyright")
            # Tạo thư mục 'Infor' nếu chưa tồn tại
            if not os.path.exists(infor_path):
                os.makedirs(infor_path)
            # Tạo tên file CSV
            csv_file_name = f"{computer_name}_{ip_address}.csv"
            csv_file_path = os.path.join(infor_path, csv_file_name)
            # Lấy thời gian hiện tại
            current_time = time_check_full
            # Tạo và ghi thông tin vào file CSV
            with open(csv_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                # Ghi tiêu đề cột
                writer.writerow(['Name', 'IP', 'Time'])
                # Ghi thông tin máy tính
                writer.writerow([computer_name, ip_address, current_time])
            # Corrected SCOPES URL
            SCOPES = ['https://www.googleapis.com/auth/drive']
            #SERVICE_ACCOUNT_FILE = f'{application_path}\\service_account.json'
            PARENT_FOLDER_ID = "1aHoaYNVzQ4KxaRLM_seRcmhfPUttrVhP"
            service_account_json = {"type": "service_account",
                                "project_id": "crested-sunup-411416",
                                "private_key_id": "70d11e242e0869c094ecadc31d41d1593316a612",
                                "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC7acroXc0+QT4Y\nABG2J5m9J5cLuj94nxXjBL1aR1J5en7pKZ4LSicpd89ebXIdtKQ72jOg3UBIYXSW\niuMcAbq+qYuE6ZTxmgpqdZEZngOF5xEiM7qTBalq9nHAWj8yY5zlM1zvQG57qDm7\nlBpEVMdvXsOQmKgKG8kGvpoWvGG+anpVT7YqLxrP38W4Ollsoo5PtLChqxooYg9h\nEuoh3b3IxCV5gi6rb2tK79b0a6AxEDvMBnkRQZCWv6ATCdAK12X/SLhV8wCvuYIM\nKgfnVfDbBlhW34bKLHCCueastUOu34NJNov+6YiE1JQO41IB9+kfF8gxGomgoxD+\neSIv+CGPAgMBAAECggEAC3lQ9zme8jEeXcEgqc1Hh/bKND6ahNurLwiVldcIq+/y\n9dAay/LQmPpWfh/R572tJw5B25cQHh5RUVIpe10jvhPf5dWYd9OIJbe9mBrozk7f\nk/96FxGMAMTGdrylDS8KEQI8WK181iHuKZd0pZBR3CCqH8p+JzhHmMZx5Uhyl4IP\nDXdxQzYruNdV5tm/NpO8Q/gxHxI08YOqh3jMpeVPrMBusoENmKXjIhRHtnyTvqhY\ntg1/LE2mFzb/MErcEwMos2+Jo2bA3WTCOavz6YBCSNvtMLzrHryfa9Z4QATkWRGG\ntVT4HuEQGQ3sxbTm0N1X0L1/XynRMTCELzXV2dd+qQKBgQDx3hAapLpjtWOMP7jU\npcx49gxjfDh+1f3qS0wlmVHVuAiZcf4Ay3TlNOTEvtj/7a9azUoMyhCQTNmr0t84\nFLhOkCeZxekI1DDy18efj0HqDZL8ohvE+gbkwEv/mF3zWliqtILC535CCYFV6CYh\nA3tvri8OI/mcqdtcOlUbH+ihPQKBgQDGXS9lwdmXq0BO8HUNOzIIsYcjnWXuIpBL\nQHt+U6KKodB9BLQhr7DziDmIfoCuu0e89pk13d0THoyKO9Md/72pNTkrIsLwK6be\ndp9CiycISKQqIZBG4tuAtqH15KZSRKBhrpAs+XvNRPEqvHE7biG+yja1X2w7vUT4\neph286ViuwKBgQDovK00ZiSxA39KGpspjG1ITEM5i/P1IMeXp2MbnwAfLlqgBQ/N\nBfpzAEXOiHLZOocNUhOaYOo1YK3oaB7BoTaE6rQghU+rXjvHwhlmEXz00qEJFpiw\nH4N4pQ28YoqtO9esU8yr7gQRWYIp/xyJkgc6PRsseTOdK9lYUw1H75lzZQKBgC0X\nrdih8obp5RqMyu8RD9SuFpxgAXXa4ZZZuDkFZiPBmRVyZkhqGf2icAG5UCNoa2xn\nWnjGUKUyApzB8MIXCtRWRwKpSksygSJ9MML9wwe9C6SQMK4Mj/14huTQ74YwF41d\nE2VF6YDGNVSTteHerUkjyr/8SyxhYDZkGBiiVmxVAoGBAM59MVGp4BtVyjNHvsNm\nWzaElw6Oy7V7RUuX5p3RjcP1fmqGcY1r7YM1W/fFkqOHtHOLW+kdWPz56DVllzUo\nnXiBLb8Ns8/W0KtnH4wz1VPL20/3QcrRRmjy6+wYlYFdIzXN2ptj0dhEfiWfSQM9\ny/4CvAJBWW8mgZj9UDpOdXCS\n-----END PRIVATE KEY-----\n",
                                "client_email": "get-infor@crested-sunup-411416.iam.gserviceaccount.com",
                                "client_id": "117584027535760018927",
                                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                                "token_uri": "https://oauth2.googleapis.com/token",
                                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/get-infor%40crested-sunup-411416.iam.gserviceaccount.com",
                                "universe_domain": "googleapis.com"
                        }
            def authenticate():
                try:
                    creds = service_account.Credentials.from_service_account_info(
                        service_account_json, scopes=SCOPES)
                    return creds
                except Exception as e:
                    #print(f"An error occurred during authentication: {e}")
                    return None
            def upload_csv(file_path):
                creds = authenticate()
                if creds is not None:
                    try:
                        service = build('drive', 'v3', credentials=creds)
                        file_metadata = {'name': f'{computer_name}_{time_check_full}', 'parents': [PARENT_FOLDER_ID]}
                        media = MediaFileUpload(file_path, mimetype='text/csv')
                        file = service.files().create(
                            body=file_metadata,
                            media_body=media,
                            fields='id'
                        ).execute()
                    except Exception as e:
                        print(f"Error: {e}")
            upload_csv(f"{csv_file_path}")
            progress_dialog.close() # Đóng QProgressDialog sau khi hoàn thành

    # Liệt kê tất cả các chuyên ngành
    def def_list_all_subject(self):
        try:
            # Tạo một QProgressDialog để thông báo rằng đang thực hiện lệnh
            progress_dialog = QProgressDialog(self)
            progress_dialog.setWindowTitle("Đang tải danh sách tất cả các chuyên ngành")
            progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
            progress_dialog.setMinimumDuration(0)
            progress_dialog.setLabelText("Loading ...")
            progress_dialog.resize(300, 100)  # Đặt kích thước tùy ý
            progress_dialog.show()
            # End tạo QProgressDialog
            # URL của trang web
            url = "https://www.scimagojr.com/journalrank.php?type=j&order=h&ord=desc"
            # Gửi yêu cầu HTTP để lấy nội dung trang web
            response = requests.get(url)
            html_content = response.content
            # Phân tích nội dung HTML bằng BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            # Tìm thẻ <li> chứa "All subject categories"
            all_subject_categories = None
            for li in soup.find_all('li'):
                a_tag = li.find('a')
                if a_tag and 'All subject categories' in a_tag.get_text():
                    all_subject_categories = li
                    break
            # Kiểm tra nếu tìm thấy thẻ "All subject categories"
            # Tìm tất cả các thẻ <li> con của thẻ "All subject categories"
            list_items = all_subject_categories.find_next_siblings('li')
            # Lấy văn bản và data-code từ mỗi thẻ <li>
            categories = []
            for item in list_items:  
                a_tag = item.find('a')
                if a_tag:
                    category = item.get_text()
                    data_code = a_tag['href'].split('=')[-1]
                    categories.append((category, data_code))
            # Hiển thị dạng bảng với 3 cột
            list_string = f"Danh sách tất cả các chuyên ngành của năm {self.year_check}\n"
            list_string += "="*80 + "\n"
            list_string += f"{'STT':<17} {'Tên chuyên ngành':<100} {'ID Chuyên ngành':<10} \n"
            list_string += "="*80 + "\n"
            for idx, (category, data_code) in enumerate(categories, start=1):
                idx_str = str(idx).zfill(3)  # Convert idx to a string and pad with leading zeros
                list_string += f"{idx_str}/{len(categories):<10} {category:<150} {data_code:<10} \n"
            # Convert to HTML table
            html_string = """
            <table border="1">
                <tr>
                    <th>STT</th>
                    <th>Tên chuyên ngành</th>
                    <th>Mã chuyên ngành</th>
                </tr>
            """
            for idx, (category, data_code) in enumerate(categories, start=1):
                idx_str = str(idx).zfill(3)
                html_string += f"""
                <tr>
                    <td>{idx_str}/{len(categories)}</td>
                    <td>{category}</td>
                    <td>{data_code}</td>
                </tr>
                """
            html_string += "</table>"
            # Display the HTML table
            self.result_display.setHtml(html_string)
            # Đóng QProgressDialog sau khi hoàn thành
            progress_dialog.close() 
            # Display the list in the GUI
            #self.result_display.setText(list_string)
            # Tạo danh sách lựa chọn từ bảng
            choices = [f"{str(idx+1)}. {category} - {data_code}" for idx, (category, data_code) in enumerate(categories)]
            #choose_line, ok_pressed = QInputDialog.getItem(self, "Choose", "Chọn chuyên ngành hoặc chọn Cancel để bỏ qua bước này", [f"{str(index)}. {str(file_name)}" for # Hiển thị hộp thoại lựa chọn
            choose_line, ok_pressed = QInputDialog.getItem(self, f"Đã tìm thấy {len(categories)} chuyên ngành - Năm {self.year_check}", "Chọn chuyên ngành để kiểm tra hạng và mở website SJR", choices, 0, False)
            if ok_pressed:
                selected_data_sjr_code = choose_line.split(' - ')[1].strip()
                selected_name_category = re.search(r'\. (.*?)\ -', choose_line).group(1)
                # Placeholder for actual search functionality
                self.result_display.setText(f"- Tên chuyên ngành đã chọn: '{selected_name_category}' với mã số SJR '{selected_data_sjr_code}'")
                # Check category
                # Tạo một QProgressDialog để thông báo rằng đang thực hiện lệnh
                progress_dialog = QProgressDialog(self)
                progress_dialog.setWindowTitle(f"Đang kiểm tra hạng các tạp chí thuộc chuyên ngành '{selected_name_category}'")
                progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
                progress_dialog.setMinimumDuration(0)
                progress_dialog.setLabelText("Loading ...")
                progress_dialog.resize(500, 100)  # Đặt kích thước tùy ý
                progress_dialog.show()
                # End tạo một QProgressDialog để thông báo rằng đang thực hiện lệnh
                df_category = check_rank_by_name_1_category(selected_data_sjr_code, self.year_check)
                progress_dialog.close() # Đóng QProgressDialog sau khi hoàn thành
                self.column_show_1_category = ['STT', 'Tên tạp chí', 'Hạng', 'Chỉ số Q', 'H-index', 'Vị trí', 'Tổng số tạp chí', 'Top phần trăm', 'Trang', 'Ghi chú']
                html_table_category = df_category[self.column_show_1_category].to_html(index=False, justify='center')    # Chú ý  đổi column_show_choose_journal
                # Add a title to the table
                html_table_category_with_title = f"<h3>Kết quả xếp hạng của chuyên ngành '{selected_name_category}'. Theo dữ liệu SJR năm: {self.year_check}\n </h3>{html_table_category}"
                self.result_display.setHtml(html_table_category_with_title)
                # Thông tin
                info_text = (
                    f"Đã mở website SJR chuyên ngành '{selected_name_category}'. Theo dữ liệu SJR năm {self.year_check} \n"
                )
                self.result_display.append(info_text)  # Append the information text
                def save_dataframe_as_excel(df):
                    # Hỏi người dùng có muốn lưu file không
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Icon.Question)
                    msg_box.setWindowTitle('Save file')
                    msg_box.setText('Bạn có muốn lưu kết quả tìm kiếm này không?')
                    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                    response = msg_box.exec()
                    if response == QMessageBox.StandardButton.Ok:
                        file_dialog = QFileDialog()
                        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
                        file_dialog.setDefaultSuffix('xlsx')
                        default_filename = f"result_1_category_{selected_name_category}_{time_check_full}.xlsx"
                        # Hỏi người dùng vị trí lưu file
                        file_path, _ = file_dialog.getSaveFileName(None, "Save File", default_filename, "Excel Files (*.xlsx)")
                        if file_path:
                            df.to_excel(file_path, index=False)
                            self.result_display.append(f"Kết quả đã được lưu thành file excel tại {file_path}")
                        else:
                            self.result_display.append("Kết quả tìm kiếm đã không được lưu. Mời bạn tiếp tục sử dụng ứng dụng.")
                    else:
                        self.result_display.append("Kết quả tìm kiếm đã không được lưu. Mời bạn tiếp tục sử dụng ứng dụng.")
                save_dataframe_as_excel(df_category)
                ###
                # Open website 
                open_link_sjr = f"https://www.scimagojr.com/journalrank.php?category={selected_data_sjr_code}&type=j&order=h&ord=desc&year={self.year_check}"
                # Start hỏi mở website
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Icon.Question)
                msg_box.setWindowTitle(f"Đã có kết quả tra cứu")
                msg_box.setText(f"Bạn có muốn mở website chuyên ngành '{selected_name_category}' không?")
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                response = msg_box.exec()
                if response == QMessageBox.StandardButton.Ok:
                    webbrowser.open(open_link_sjr)
                # End hỏi mở website
        except Exception as e:
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Icon.Warning)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText(f">>> Cảnh báo lỗi >>> {str(e)}")
            error_dialog.exec()

    # Tra hạng theo tên
    def def_rank_by_name_or_issn(self):
        try:
            keyword, ok_pressed_1 = QInputDialog.getText(self, "Kiểm tra hạng", "Nhập tên hoặc ISSN của tạp chí")
            name_journal = keyword # .strip() removes any leading/trailing whitespace
            if ok_pressed_1 and keyword:
                # Placeholder for actual search functionality
                self.result_display.setText(f'Tên hoặc ISSN đã điền: {keyword}')
                # Tạo một QProgressDialog để thông báo rằng đang thực hiện lệnh
                progress_dialog = QProgressDialog(self)
                progress_dialog.setWindowTitle(f"Đang tìm tạp chí theo thông tin '{keyword}'")
                progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
                progress_dialog.setMinimumDuration(0)
                progress_dialog.setLabelText("Loading ...")
                progress_dialog.resize(300, 100)  # Đặt kích thước tùy ý
                progress_dialog.show()
                # End tạo một QProgressDialog để thông báo rằng đang thực hiện lệnh
                df_1 = find_title_or_issn(name_journal)
                #'''
                # Lấy chỉ số của các dòng có giá trị trống trong cột 'Nhà xuất bản'
                empty_indices = df_1[df_1['ISSN'].str.len() < 4].index.tolist()
                #print(empty_indices)
                # Xóa các dòng có chỉ số này
                for i in empty_indices:
                    df_1.drop(index=i, inplace=True)
                #'''
                # Tạo cửa sổ chọn tạp chí cần tra hạng
                self.column_show_choose_journal = ['STT','Tên tạp chí', 'ISSN', 'Nhà xuất bản', 'ID Scopus']
                html_table_1 = df_1[self.column_show_choose_journal].to_html(index=False, justify='center')    # Chú ý  đổi column_show_choose_journal
                self.result_display.setHtml(html_table_1)
                progress_dialog.close() # Đóng QProgressDialog sau khi hoàn thành
                choose_line_1, ok_pressed_1 = QInputDialog.getItem(self, f"Đã tìm thấy {len(df_1)} kết quả - Năm {self.year_check}", f"Chọn tạp chí muốn tra hạng", [f"{a} - {b} - ISSN: {c} - NXB: {d} - ID Scopus: {e}" for a, b, c, d, e in zip(df_1['STT'], df_1['Tên tạp chí'], df_1['ISSN'], df_1['Nhà xuất bản'], df_1['ID Scopus'])], 0, False)
                if ok_pressed_1:
                    choose_line_1 = choose_line_1.split(' - ')[0]
                    selected_row_1 = df_1.iloc[int(choose_line_1)-1]
                    info_text_1 = (f"{selected_row_1}")
                    self.result_display.append(info_text_1)
                    id_scopus_choose = selected_row_1['ID Scopus']
                    #nxb_sjr = selected_row_1['Nhà xuất bản']
                # Kết thúc cửa sổ chọn tạp chí cần tra hạng
                progress_dialog = QProgressDialog(self) # Mở cửa sổ QProgressDialog để thông báo rằng đang thực hiện lệnh
                progress_dialog.setWindowTitle("Đang tải thông tin ...")
                progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
                progress_dialog.setMinimumDuration(0)
                progress_dialog.setLabelText("Loading ...")
                progress_dialog.resize(400, 100)  # Đặt kích thước tùy ý
                progress_dialog.show()
                name_journal_check, country, subject_area_category_check, publisher, h_index, issn_check, coverage, homepage_link, how_to_publish_link, email_question_journal = issn_to_all(id_scopus_choose)
                progress_dialog.close() # Đóng QProgressDialog sau khi hoàn thành
                progress_dialog = QProgressDialog(self) # Mở cửa sổ QProgressDialog để thông báo rằng đang thực hiện lệnh
                progress_dialog.setWindowTitle("Đang kiểm tra hạng ...")
                progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
                progress_dialog.setMinimumDuration(0)
                progress_dialog.setLabelText("Loading ...")
                progress_dialog.resize(200, 100)  # Đặt kích thước tùy ý
                progress_dialog.show()
                df_2 = check_rank_by_name_1_journal(name_journal_check, subject_area_category_check, self.year_check)
                progress_dialog.close() # Đóng QProgressDialog sau khi hoàn thành
                
                df_2.insert(df_2.columns.get_loc('Tên tạp chí') + 1, 'ISSN', issn_check)
                df_2.insert(df_1.columns.get_loc('ISSN') + 1, 'Nhà xuất bản', publisher)
                df_2.insert(df_2.columns.get_loc('ID Chuyên ngành') + 1, 'ID Scopus', id_scopus_choose)

                self.column_show_2_journal = ['STT', 'Tên tạp chí', 'ISSN', 'Hạng', 'Chỉ số Q', 'H-index', 'Nhà xuất bản', 'Vị trí', 'Tổng số tạp chí', 'Phần trăm', 'Top phần trăm', 'Chuyên ngành', 'ID Chuyên ngành', 'ID Scopus', 'Trang', 'Ghi chú']
                html_table_2 = df_2[self.column_show_2_journal].to_html(index=False, justify='center')    # Chú ý  đổi column_show_choose_journal
                # Add a title to the table
                html_table_2_with_title = f"<h3>Tạp chí '{df_2['Tên tạp chí'].iloc[0]}' thuộc {len(df_2)} chuyên ngành, nên có {len(df_2)} thứ hạng sau: \n </h3>{html_table_2}"
                self.result_display.setHtml(html_table_2_with_title)
                # Mở cửa sổ in minh chứng
                choose_line_2, ok_pressed_2 = QInputDialog.getItem(self, f"In minh chứng", f"Chọn dòng để in", [f"{a} - {b} - Chuyên ngành: {c}" for a, b, c in zip(df_2['STT'], df_2['Hạng'], df_2['Chuyên ngành'])], 0, False)
                if ok_pressed_2:
                    choose_line_2 = choose_line_2.split('-')[0]
                    selected_row_2 = df_2.iloc[int(choose_line_2)-1]
                    info_text_2 = (
                        f"-----------------------------------------------------------------------------------------------------\n"
                        f"- Thông tin trong biên bản nghiệm thu - Theo dữ liệu SJR năm {self.year_check}\n"
                        f"  + Tên tạp chí: {selected_row_2['Tên tạp chí']}\n"
                        f"  + ISSN: {selected_row_2['ISSN']}\n"
                        f"  + Nhà xuất bản: {publisher}\n"
                        f"  + {selected_row_2['Hạng']} (WoS), SJR: {selected_row_2['Chỉ số Q']}, H-Index: {selected_row_2['H-index']}, thuộc top {selected_row_2['Top phần trăm']}% (thứ tự {selected_row_2['Vị trí']}) trong {selected_row_2['Tổng số tạp chí']} tạp chí về {selected_row_2['Chuyên ngành']}, truy xuất lúc {hour}h{minute} ngày {day}/{month}/{year}\n"
                    )
                    info_text_3 = (
                        f"-----------------------------------------------------------------------------------------------------\n"
                        f"- Website Scopus, WoS, SJR của tạp chí '{selected_row_2['Tên tạp chí']}':\n"
                        f"  + Đã mở website Scopus của tạp chí '{selected_row_2['Tên tạp chí']}'\n"
                        f"  + Đã mở website WoS của tạp chí '{selected_row_2['Tên tạp chí']}'\n"
                        f"  + Đã mở website SJR chuyên ngành '{selected_row_2['Chuyên ngành']}' của tạp chí '{selected_row_2['Tên tạp chí']}'\n"
                    )
                    self.result_display.append(info_text_2)
                    # Open website 
                    open_link_sjr = f"https://www.scimagojr.com/journalrank.php?category={selected_row_2['ID Chuyên ngành']}&year={self.year_check}&type=j&order=h&ord=desc&page={selected_row_2['Trang']}&total_size={selected_row_2['Tổng số tạp chí']}"
                    open_link_scopus = f"https://www.scopus.com/sourceid/{selected_row_2['ID Scopus']}"
                    open_link_wos = f"https://mjl.clarivate.com://search-results?issn={selected_row_2['ISSN']}&hide_exact_match_fl=true&utm_source=mjl&utm_medium=share-by-link&utm_campaign=search-results-share-this-journal"
                    # Start hỏi mở website
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Icon.Question)
                    msg_box.setWindowTitle(f"Đã có kết quả tra cứu")
                    msg_box.setText(f"Bạn có muốn mở website Scopus, SJR, WoS của tạp chí '{selected_row_2['Tên tạp chí']}' không?")
                    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                    response = msg_box.exec()
                    if response == QMessageBox.StandardButton.Ok:
                        webbrowser.open(open_link_scopus)
                        webbrowser.open(open_link_wos)
                        webbrowser.open(open_link_sjr)
                        self.result_display.append(info_text_3)
                    # End hỏi mở website
        except Exception as e:
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Icon.Warning)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText(f">>> Cảnh báo lỗi >>> {str(e)}")
            error_dialog.exec()

    # Định nghĩa hàm check theo hạng và tên chuyên ngành
    def def_check_in_scopus_sjr_wos(self):
        try:
            keyword, ok_pressed_1 = QInputDialog.getText(self, "Phân loại tạp chí", "Nhập tên hoặc ISSN của tạp chí")
            name_journal = keyword.strip() #removes any leading/trailing whitespace
            if ok_pressed_1 and keyword:
                #self.result_display.setText(f'Tên hoặc ISSN đã điền: {keyword}')
                # Tạo một QProgressDialog để thông báo rằng đang thực hiện lệnh
                progress_dialog = QProgressDialog(self)
                progress_dialog.setWindowTitle(f"Đang tìm tạp chí theo thông tin '{keyword}'")
                progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
                progress_dialog.setMinimumDuration(0)
                progress_dialog.setLabelText("Loading ...")
                progress_dialog.resize(300, 100)  # Đặt kích thước tùy ý
                progress_dialog.show()
                # Đóng tạo QProgressDialog
                df_1 = find_title_or_issn(name_journal)
                #'''
                # Lấy chỉ số của các dòng có giá trị trống trong cột 'Nhà xuất bản'
                empty_indices = df_1[df_1['ISSN'].str.len() < 4].index.tolist()
                #print(empty_indices)
                # Xóa các dòng có chỉ số này
                for i in empty_indices:
                    df_1.drop(index=i, inplace=True)
                #'''
                progress_dialog.close() # Đóng QProgressDialog sau khi hoàn thành
                self.column_show_choose_journal = ['STT','Tên tạp chí', 'ISSN', 'Nhà xuất bản', 'ID Scopus']
                html_table_1 = df_1[self.column_show_choose_journal].to_html(index=False, justify='center')    # Chú ý  đổi column_show_choose_journal
                self.result_display.setHtml(html_table_1)
                choose_line_1, ok_pressed_1 = QInputDialog.getItem(self, f"Đã tìm thấy {len(df_1)} kết quả -  Năm {self.year_check}", f"Chọn tạp chí muốn tra cứu", [f"{a} - {b} - {c} - {d} - {e}" for a, b, c, d, e in zip(df_1['STT'], df_1['Tên tạp chí'], df_1['Nhà xuất bản'], df_1['ISSN'], df_1['ID Scopus'])], 0, False)
                if ok_pressed_1:
                    choose_line_1 = choose_line_1.split(' - ')[0]
                    selected_row_1 = df_1.iloc[int(choose_line_1)-1]
                    #info_text_1 = (f"{selected_row_1}")
                    #self.result_display.append(info_text_1)
                    id_scopus_choose = selected_row_1['ID Scopus']
                # Tạo một QProgressDialog để thông báo rằng đang thực hiện lệnh
                progress_dialog = QProgressDialog(self)
                progress_dialog.setWindowTitle("Đang mở website")
                progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
                progress_dialog.setMinimumDuration(0)
                progress_dialog.setLabelText("Loading ...")
                progress_dialog.resize(100, 100)  # Đặt kích thước tùy ý
                progress_dialog.show()
                name_journal_check, country, subject_area_category_check, publisher, h_index, issn_check, coverage, homepage_link, how_to_publish_link, email_question_journal = issn_to_all(id_scopus_choose)
                ten_chuyen_nganh = [key for key in subject_area_category_check.keys()]
                chuoi_chuyen_nganh = ", ".join(ten_chuyen_nganh)
                # Open website 
                open_link_sjr = f"https://www.scimagojr.com/journalsearch.php?q={id_scopus_choose}&tip=sid&clean=0"
                open_link_scopus = f"https://www.scopus.com/sourceid/{id_scopus_choose}"
                open_link_wos = f"https://mjl.clarivate.com://search-results?issn={issn_check}&hide_exact_match_fl=true&utm_source=mjl&utm_medium=share-by-link&utm_campaign=search-results-share-this-journal"
                webbrowser.open(open_link_scopus)
                webbrowser.open(open_link_sjr)
                webbrowser.open(open_link_wos)
                self.result_display.append(f"\n Đã mở các website SCOPUS, SJR, WOS của tạp chí '{name_journal_check}'. ISSN: {issn_check}. Nhà xuất bản: {publisher}")
                progress_dialog.close() # Đóng QProgressDialog sau khi hoàn thành
        except Exception as e:
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Icon.Warning)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText(f">>> Cảnh báo lỗi >>> {str(e)}")
            error_dialog.exec()

    # check citation
    def def_citation_wos(self):
        try:
            class CheckDialog(QtWidgets.QDialog):
                def __init__(self, list_abc, title, new_fill, parent=None):
                    super().__init__(parent)
                    self.setWindowTitle(f"{title}")
                    self.layout = QtWidgets.QVBoxLayout(self)
                    self.checkboxes = []
                    for item in list_abc:
                        checkbox = QtWidgets.QCheckBox(item)
                        self.checkboxes.append(checkbox)
                        self.layout.addWidget(checkbox)
                    self.new_info_input = QtWidgets.QLineEdit()
                    self.new_info_input.setPlaceholderText(new_fill)
                    self.layout.addWidget(self.new_info_input)
                    self.buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
                    self.buttons.accepted.connect(self.accept)
                    self.buttons.rejected.connect(self.reject)
                    self.layout.addWidget(self.buttons)
                    self.setFixedSize(380, 450)
                def getItem(self):
                    if self.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                        selected_items = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]
                        new_info = self.new_info_input.text()
                        if len(new_info) > 0:
                            selected_items.append(new_info)
                        return selected_items, True
                    else:
                        return [], False
            # Đọc file google sheet
            def get_infor_from_gg_drive(id_file, name_sheet):
                # Service account JSON
                service_account_json = {
                }
                # SCOPES
                SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
                # Authenticate and create the service
                credentials = service_account.Credentials.from_service_account_info(service_account_json, scopes=SCOPES)
                service = build('sheets', 'v4', credentials=credentials)
                # The ID and range of the spreadsheet.
                SPREADSHEET_ID = f'{id_file}'
                RANGE_NAME = f'{name_sheet}'  # Update this to your actual sheet name
                # Call the Sheets API
                sheet = service.spreadsheets()
                result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
                values = result.get('values', [])
                # Convert to DataFrame
                return pd.DataFrame(values[1:], columns=values[0])
                # End lấy thông tin gg sheet
            #'''
            progress_dialog = QProgressDialog(self) # Mở cửa sổ QProgressDialog để thông báo rằng đang thực hiện lệnh
            progress_dialog.setWindowTitle("Đang tải danh sách các ID")
            progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
            progress_dialog.setMinimumDuration(0)
            progress_dialog.setLabelText("Loading ...")
            progress_dialog.resize(210, 100)  # Đặt kích thước tùy ý
            progress_dialog.show()
            #'''
            ### lấy thông tin research ID
            id_file_gg_sheet = '1-xdZR9uLE7lBTEGGYNNzfOP8gTZHVUigScdDju3_-AU'
            name_sheet_researcher_id = 'researcher_id'
            df_researcher_id = get_infor_from_gg_drive(id_file_gg_sheet, name_sheet_researcher_id)
            ### End lấy thông tin research id
            # list id rearcher
            list_research_id = dict(zip(df_researcher_id['id'], df_researcher_id['link']))
            
            def login_to_website(url: str, username: str, password: str, time_lose_web) -> str:
                chrome_options = Options()
                chrome_options.add_argument("--incognito")
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
                logout_url = "https://www.webofscience.com/wos/my/sign-out?param=closeSessionAndLogout"
                driver.get(logout_url)
                try:
                    driver.get(url)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mat-input-0")))
                    email_field = driver.find_element(By.ID, "mat-input-0")
                    email_field.clear()
                    email_field.send_keys(username)
                    password_field = driver.find_element(By.ID, "mat-input-1")
                    password_field.clear()
                    password_field.send_keys(password)
                    password_field.send_keys(Keys.RETURN)
                    WebDriverWait(driver, 10).until(EC.url_changes(url))
                    url_pass = "https://www.webofknowledge.com/?app=wos&referrer=mode=Nextgen&path=%2Fwos%2Fwoscc%2Fcitation-report%2F27453b39-338e-456f-a572-4eb9f7247615-0145d5570a%3Fpage%3D1&DestApp=UA&action=transfer&authCode=xt3bjyB5x5BNWgDfdBGl0BRVO0VJa7heWd2GzhjviIk&auth=RoamingExistingSession&eSID=EUW1ED0F3CtmCZhRL4L2KRuv62S7q"
                    driver.get(url_pass)
                    WebDriverWait(driver, 10).until(EC.url_changes(url_pass))
                    driver.get(url)
                    return driver.current_url
                except Exception as e:
                    return None
                finally:
                    time.sleep(time_lose_web)
                    driver.quit()
            ### lấy tk wos
            id_file = '1-xdZR9uLE7lBTEGGYNNzfOP8gTZHVUigScdDju3_-AU'
            name_sheet = 'account_wos'
            df_account_wos = get_infor_from_gg_drive(id_file, name_sheet)
            # In ra user và password đầu tiên
            username = df_account_wos.loc[0, 'user']
            password = df_account_wos.loc[0, 'password']
            # End đọc file
            progress_dialog.close() # Đóng QProgressDialog sau khi hoàn thành
            research_id_input, ok_pressed = CheckDialog(list_research_id, "Chọn mã số Research ID", "Điền mã số Research ID khác tại đây").getItem()
            if ok_pressed:
                research_id_input = [re.sub(r'\s*\(.*?\)', '', research_id_input[0])]
                for id_check in research_id_input:
                    if id_check in list_research_id:
                        url_citation_open = list_research_id[id_check]
                        text_show_citation = f"\n Đang mở website WoS - Citation của Research ID: '{research_id_input[0]}'. Vui lòng đợi xíu để trình duyệt tự mở lên."
                        self.result_display.append(text_show_citation)
                        threading.Thread(target=login_to_website, args=(url_citation_open, username, password, 200)).start()
                    else:
                        #url_citation_open = 'https://www.webofscience.com/wos/woscc/citation-report'
                        text_show_citation = f"\n Research ID: '{research_id_input[0]}' không tồn tại trong CSDL, vui lòng liên hệ admin để cập nhật"
                        self.result_display.append(text_show_citation)
        except Exception as e:
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Icon.Warning)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText(f">>> Cảnh báo lỗi >>> {str(e)}")
            error_dialog.exec()

    # Tìm tạp chí theo hạng và từ khóa
    def def_rank_by_rank_key(self):
        try:
            # Custom CheckDialog class with size parameters
            class CheckDialog(QtWidgets.QDialog):
                def __init__(self, list_abc, title, new_fill, width, height, parent=None):
                    super().__init__(parent)
                    self.setWindowTitle(f"{title}")
                    self.layout = QtWidgets.QVBoxLayout(self)
                    self.checkboxes = []
                    for item in list_abc:
                        checkbox = QtWidgets.QCheckBox(item)
                        self.checkboxes.append(checkbox)
                        self.layout.addWidget(checkbox)
                    self.new_info_input = QtWidgets.QLineEdit()
                    self.new_info_input.setPlaceholderText(new_fill)
                    self.layout.addWidget(self.new_info_input)
                    # Add OK and Cancel buttons
                    self.buttons = QtWidgets.QDialogButtonBox(
                        QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel
                    )
                    self.buttons.accepted.connect(self.accept)
                    self.buttons.rejected.connect(self.reject)
                    self.layout.addWidget(self.buttons)
                    self.setFixedSize(width, height)  # Set custom width and height

                def getItem(self):
                    if self.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                        selected_items = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]
                        new_info = self.new_info_input.text()
                        if len(new_info) > 0:
                            selected_items.append(new_info)
                        return selected_items, True
                    else:
                        return [], False

            # Use CheckDialog for keywords input with custom size
            keywords, ok_pressed = CheckDialog(
                ["math", "analysis", "numerical", "optimization", "control", "algebra", "geometry", "statistics", "probability", "computer", "computation", "engineering"],
                "Từ khóa nằm trong tên chuyên ngành",
                "Tick chọn các từ khóa ở trên (có thể chọn nhiều từ khóa) hoặc nhập từ khóa khác tại đây",
                510, 500  # Custom size for keywords dialog
            ).getItem()
            if not ok_pressed:
                return  # User cancelled, do nothing

            # Use CheckDialog for rank options input with custom size
            rank_options = ["Ngoại hạng chuyên ngành"] + [f"Hạng {i}" for i in range(1, 11)]
            rank_option, ok_pressed = CheckDialog(
                rank_options,
                "Chọn hạng để lọc tạp chí",
                "Tick vào ô chọn hạng ở trên, có thể chọn nhiều hạng khác nhau",
                380, 450  # Custom size for rank options dialog
            ).getItem()

            if not ok_pressed:
                return  # User cancelled, do nothing

            keywords = list(filter(lambda x: x != "", keywords))  # Remove empty keywords
            keywords = [k.strip() for k in keywords]  # Trim whitespace

            if ok_pressed and keywords:
                # Create a QProgressDialog to indicate the operation is in progress
                progress_dialog = QProgressDialog(self)
                progress_dialog.setWindowTitle("Đang tải dữ liệu")
                progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
                progress_dialog.setMinimumDuration(0)
                progress_dialog.setLabelText("Loading ...")
                progress_dialog.resize(100, 100)  # Đặt kích thước tùy ý
                progress_dialog.show()

                result_4 = pd.DataFrame()
                url = "https://www.scimagojr.com/journalrank.php?type=j&order=h&ord=desc"
                response = requests.get(url)
                html_content = response.content
                soup = BeautifulSoup(html_content, 'html.parser')

                all_subject_categories = None
                for li in soup.find_all('li'):
                    a_tag = li.find('a')
                    if a_tag and 'All subject categories' in a_tag.get_text():
                        all_subject_categories = li
                        break

                list_items = all_subject_categories.find_next_siblings('li')
                categories = []
                for item in list_items:
                    a_tag = item.find('a')
                    if a_tag:
                        category = item.get_text()
                        category_id = a_tag['href'].split('=')[-1]
                        categories.append((category, category_id))

                progress_dialog.close()

                for category, category_id in categories:
                    for name_key in keywords:
                        if clear_format(name_key) in clear_format(category):
                            progress_dialog = QProgressDialog(self)
                            progress_dialog.setWindowTitle(f"Đang kiểm tra chuyên ngành '{category}'")
                            progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
                            progress_dialog.setMinimumDuration(0)
                            progress_dialog.setLabelText("Loading ...")
                            progress_dialog.resize(400, 100)  # Đặt kích thước tùy ý
                            progress_dialog.show()

                            df_category = check_rank_by_name_1_category(category_id, self.year_check)
                            for r in rank_option:
                                filtered_df_category = df_category[df_category['Hạng'] == r]
                                filtered_df_category.insert(filtered_df_category.columns.get_loc('Top phần trăm') + 1, 'Chuyên ngành', category)
                                filtered_df_category.insert(filtered_df_category.columns.get_loc('Chuyên ngành') + 1, 'ID Chuyên ngành', category_id)
                                result_4 = pd.concat([result_4, filtered_df_category], ignore_index=True)

                            progress_dialog.close()

                result_4['STT'] = range(1, len(result_4) + 1)
                self.column_show_1_category = ['STT', 'Tên tạp chí', 'Hạng', 'Chỉ số Q', 'H-index', 'Vị trí', 'Tổng số tạp chí', 'Top phần trăm', 'Chuyên ngành', 'Ghi chú']
                html_table_category = result_4[self.column_show_1_category].to_html(index=False, justify='center')

                ten_rank_option = [key for key in rank_option]
                chuoi_rank_option = ", ".join(ten_rank_option)
                html_table_category_with_title = f"<h3>Tìm thấy {len(result_4)} kết quả lọc các tạp chí '{chuoi_rank_option}' với từ khóa chuyên ngành: '{', '.join(keywords)}'. Theo dữ liệu SJR năm {self.year_check}\n </h3>{html_table_category}"
                self.result_display.setHtml(html_table_category_with_title)

                def save_dataframe_as_excel(df):
                    # Hỏi người dùng có muốn lưu file không
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Icon.Question)
                    msg_box.setWindowTitle('Save file')
                    msg_box.setText('Bạn có muốn lưu kết quả tìm kiếm này không?')
                    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                    response = msg_box.exec()
                    if response == QMessageBox.StandardButton.Ok:
                        file_dialog = QFileDialog()
                        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
                        file_dialog.setDefaultSuffix('xlsx')
                        default_filename = f"Result_Rank ({chuoi_rank_option})_Keyword ({', '.join(keywords)})_{time_check_full}.xlsx"
                        # Hỏi người dùng vị trí lưu file
                        file_path, _ = file_dialog.getSaveFileName(None, "Save File", default_filename, "Excel Files (*.xlsx)")
                        if file_path:
                            df.to_excel(file_path, index=False)
                            self.result_display.append(f"Kết quả đã được lưu thành file excel tại {file_path}")
                        else:
                            self.result_display.append("Kết quả tìm kiếm đã không được lưu. Mời bạn tiếp tục sử dụng ứng dụng.")
                    else:
                        self.result_display.append("Kết quả tìm kiếm đã không được lưu. Mời bạn tiếp tục sử dụng ứng dụng.")

                save_dataframe_as_excel(result_4)

        except Exception as e:
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Icon.Warning)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText(f">>> Cảnh báo lỗi >>> {str(e)}")
            error_dialog.exec()

    # Tìm tạp chí theo Q và từ khóa
    def def_rank_by_Q_key(self):
        try:
            # Custom CheckDialog class with size parameters
            class CheckDialog(QtWidgets.QDialog):
                def __init__(self, list_abc, title, new_fill, width, height, parent=None):
                    super().__init__(parent)
                    self.setWindowTitle(f"{title}")
                    self.layout = QtWidgets.QVBoxLayout(self)
                    self.checkboxes = []
                    for item in list_abc:
                        checkbox = QtWidgets.QCheckBox(item)
                        self.checkboxes.append(checkbox)
                        self.layout.addWidget(checkbox)
                    self.new_info_input = QtWidgets.QLineEdit()
                    self.new_info_input.setPlaceholderText(new_fill)
                    self.layout.addWidget(self.new_info_input)
                    # Add OK and Cancel buttons
                    self.buttons = QtWidgets.QDialogButtonBox(
                        QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel
                    )
                    self.buttons.accepted.connect(self.accept)
                    self.buttons.rejected.connect(self.reject)
                    self.layout.addWidget(self.buttons)
                    self.setFixedSize(width, height)  # Set custom width and height
                def getItem(self):
                    if self.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                        selected_items = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]
                        new_info = self.new_info_input.text()
                        if len(new_info) > 0:
                            selected_items.append(new_info)
                        return selected_items, True
                    else:
                        return [], False

            # Use CheckDialog for keywords input with custom size
            keyword_suggestions = ["math", "analysis", "numerical", "optimization", "control", "algebra", "geometry", "statistics", "probability", "computer", "computation", "engineering"]
            keywords, ok_pressed = CheckDialog(
                keyword_suggestions,
                "Từ khóa nằm trong tên chuyên ngành",
                "Tick chọn các từ khóa ở trên (có thể chọn nhiều từ khóa) hoặc nhập từ khóa khác tại đây",
                510, 500  # Custom size for keywords dialog
            ).getItem()

            # Use CheckDialog for rank options input with custom size
            rank_options = [f"Q{i}" for i in range(1, 5)]
            rank_option, ok_pressed = CheckDialog(
                rank_options,
                "Chọn chỉ số Q để lọc tạp chí",
                "Tick vào ô chọn chỉ số Q ở trên, có thể chọn nhiều Q khác nhau",
                380, 200  # Custom size for rank options dialog
            ).getItem()

            if not ok_pressed:
                return  # User cancelled, do nothing

            keywords = list(filter(lambda x: x != "", keywords))  # Remove empty keywords
            keywords = [k.strip() for k in keywords]  # Trim whitespace

            if ok_pressed and keywords:
                # Create a QProgressDialog to indicate the operation is in progress
                progress_dialog = QProgressDialog(self)
                progress_dialog.setWindowTitle("Đang tải dữ liệu")
                progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
                progress_dialog.setMinimumDuration(0)
                progress_dialog.setLabelText("Loading ...")
                progress_dialog.resize(100, 100)  # Đặt kích thước tùy ý
                progress_dialog.show()

                result_4 = pd.DataFrame()
                url = "https://www.scimagojr.com/journalrank.php?type=j&order=h&ord=desc"
                response = requests.get(url)
                html_content = response.content
                soup = BeautifulSoup(html_content, 'html.parser')
                all_subject_categories = None

                for li in soup.find_all('li'):
                    a_tag = li.find('a')
                    if a_tag and 'All subject categories' in a_tag.get_text():
                        all_subject_categories = li
                        break

                list_items = all_subject_categories.find_next_siblings('li')
                categories = []

                for item in list_items:
                    a_tag = item.find('a')
                    if a_tag:
                        category = item.get_text()
                        category_id = a_tag['href'].split('=')[-1]
                        categories.append((category, category_id))

                progress_dialog.close()

                for category, category_id in categories:
                    for name_key in keywords:
                        if clear_format(name_key) in clear_format(category):
                            progress_dialog = QProgressDialog(self)
                            progress_dialog.setWindowTitle(f"Đang kiểm tra chuyên ngành '{category}'")
                            progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
                            progress_dialog.setMinimumDuration(0)
                            progress_dialog.setLabelText("Loading ...")
                            progress_dialog.resize(400, 100)  # Đặt kích thước tùy ý
                            progress_dialog.show()

                            df_category = check_rank_by_name_1_category(category_id, self.year_check)
                            for r in rank_option:
                                filtered_df_category = df_category[df_category['Chỉ số Q'] == r]
                                filtered_df_category.insert(filtered_df_category.columns.get_loc('Top phần trăm') + 1, 'Chuyên ngành', category)
                                filtered_df_category.insert(filtered_df_category.columns.get_loc('Chuyên ngành') + 1, 'ID Chuyên ngành', category_id)
                                result_4 = pd.concat([result_4, filtered_df_category], ignore_index=True)

                            progress_dialog.close()

                result_4['STT'] = range(1, len(result_4) + 1)
                self.column_show_1_category = ['STT', 'Tên tạp chí', 'Hạng', 'Chỉ số Q', 'H-index', 'Vị trí', 'Tổng số tạp chí', 'Top phần trăm', 'Chuyên ngành', 'Ghi chú']
                html_table_category = result_4[self.column_show_1_category].to_html(index=False, justify='center')
                ten_rank_option = [key for key in rank_option]
                chuoi_rank_option = ", ".join(ten_rank_option)
                html_table_category_with_title = f"<h3>Tìm thấy {len(result_4)} kết quả lọc các tạp chí có chỉ số '{chuoi_rank_option}' với từ khóa chuyên ngành: '{', '.join(keywords)}'. Theo dữ liệu SJR năm : {self.year_check}\n </h3>{html_table_category}"
                self.result_display.setHtml(html_table_category_with_title)

                def save_dataframe_as_excel(df):
                    # Hỏi người dùng có muốn lưu file không
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Icon.Question)
                    msg_box.setWindowTitle('Save as')
                    msg_box.setText('Bạn có muốn lưu kết quả này không?')
                    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                    response = msg_box.exec()
                    if response == QMessageBox.StandardButton.Ok:
                        file_dialog = QFileDialog()
                        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
                        file_dialog.setDefaultSuffix('xlsx')
                        default_filename = f"Result_{chuoi_rank_option}_Keyword ({', '.join(keywords)})_{time_check_full}.xlsx"
                        # Hỏi người dùng vị trí lưu file
                        file_path, _ = file_dialog.getSaveFileName(None, "Save File", default_filename, "Excel Files (*.xlsx)")
                        if file_path:
                            df.to_excel(file_path, index=False)
                            self.result_display.append(f"Kết quả đã được lưu thành file excel tại {file_path}")
                        else:
                            self.result_display.append("Kết quả tìm kiếm đã không được lưu. Mời bạn tiếp tục sử dụng ứng dụng.")
                    else:
                        self.result_display.append("Kết quả tìm kiếm đã không được lưu. Mời bạn tiếp tục sử dụng ứng dụng.")

                save_dataframe_as_excel(result_4)

        except Exception as e:
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Icon.Warning)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText(f">>> Cảnh báo lỗi >>> {str(e)}")
            error_dialog.exec()

    def def_sort_ref_tex(self):
        # Khởi tạo và hiển thị đối tượng LatexProcessor
        self.latex_processor = LatexProcessor()
        self.latex_processor.show()

    def def_tex_bieu_mau(self):
        try:
            class CheckDialog(QtWidgets.QDialog):
                def __init__(self, list_abc, title, parent=None):
                    super().__init__(parent)
                    self.setWindowTitle(f"{title}")
                    self.layout = QtWidgets.QVBoxLayout(self)
                    self.checkboxes = []

                    for item in list_abc:
                        checkbox = QtWidgets.QCheckBox(item)
                        checkbox.clicked.connect(self.make_exclusive)
                        self.checkboxes.append(checkbox)
                        self.layout.addWidget(checkbox)

                    self.new_info_input = QtWidgets.QLineEdit()
                    #self.new_info_input.setPlaceholderText(new_fill)
                    self.layout.addWidget(self.new_info_input)

                    self.buttons = QtWidgets.QDialogButtonBox(
                        QtWidgets.QDialogButtonBox.StandardButton.Ok |
                        QtWidgets.QDialogButtonBox.StandardButton.Cancel
                    )
                    self.buttons.accepted.connect(self.accept)
                    self.buttons.rejected.connect(self.reject)
                    self.layout.addWidget(self.buttons)

                    self.setFixedWidth(250)

                def make_exclusive(self, checked):
                    sender = self.sender()
                    if checked:
                        for cb in self.checkboxes:
                            if cb != sender:
                                cb.setChecked(False)

                def getItem(self):
                    if self.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                        selected_items = [cb.text() for cb in self.checkboxes if cb.isChecked()]
                        new_info = self.new_info_input.text()
                        if len(new_info) > 0:
                            selected_items.append(new_info)
                        return selected_items, True
                    else:
                        return [], False
        
            # Đọc file google sheet
            def get_infor_from_gg_drive(id_file, name_sheet):
                # Service account JSON
                service_account_json = {
                    "type": "service_account",
                    "project_id": "crested-sunup-411416",
                    "private_key_id": "70d11e242e0869c094ecadc31d41d1593316a612",
                    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC7acroXc0+QT4Y\nABG2J5m9J5cLuj94nxXjBL1aR1J5en7pKZ4LSicpd89ebXIdtKQ72jOg3UBIYXSW\niuMcAbq+qYuE6ZTxmgpqdZEZngOF5xEiM7qTBalq9nHAWj8yY5zlM1zvQG57qDm7\nlBpEVMdvXsOQmKgKG8kGvpoWvGG+anpVT7YqLxrP38W4Ollsoo5PtLChqxooYg9h\nEuoh3b3IxCV5gi6rb2tK79b0a6AxEDvMBnkRQZCWv6ATCdAK12X/SLhV8wCvuYIM\nKgfnVfDbBlhW34bKLHCCueastUOu34NJNov+6YiE1JQO41IB9+kfF8gxGomgoxD+\neSIv+CGPAgMBAAECggEAC3lQ9zme8jEeXcEgqc1Hh/bKND6ahNurLwiVldcIq+/y\n9dAay/LQmPpWfh/R572tJw5B25cQHh5RUVIpe10jvhPf5dWYd9OIJbe9mBrozk7f\nk/96FxGMAMTGdrylDS8KEQI8WK181iHuKZd0pZBR3CCqH8p+JzhHmMZx5Uhyl4IP\nDXdxQzYruNdV5tm/NpO8Q/gxHxI08YOqh3jMpeVPrMBusoENmKXjIhRHtnyTvqhY\ntg1/LE2mFzb/MErcEwMos2+Jo2bA3WTCOavz6YBCSNvtMLzrHryfa9Z4QATkWRGG\ntVT4HuEQGQ3sxbTm0N1X0L1/XynRMTCELzXV2dd+qQKBgQDx3hAapLpjtWOMP7jU\npcx49gxjfDh+1f3qS0wlmVHVuAiZcf4Ay3TlNOTEvtj/7a9azUoMyhCQTNmr0t84\nFLhOkCeZxekI1DDy18efj0HqDZL8ohvE+gbkwEv/mF3zWliqtILC535CCYFV6CYh\nA3tvri8OI/mcqdtcOlUbH+ihPQKBgQDGXS9lwdmXq0BO8HUNOzIIsYcjnWXuIpBL\nQHt+U6KKodB9BLQhr7DziDmIfoCuu0e89pk13d0THoyKO9Md/72pNTkrIsLwK6be\ndp9CiycISKQqIZBG4tuAtqH15KZSRKBhrpAs+XvNRPEqvHE7biG+yja1X2w7vUT4\neph286ViuwKBgQDovK00ZiSxA39KGpspjG1ITEM5i/P1IMeXp2MbnwAfLlqgBQ/N\nBfpzAEXOiHLZOocNUhOaYOo1YK3oaB7BoTaE6rQghU+rXjvHwhlmEXz00qEJFpiw\nH4N4pQ28YoqtO9esU8yr7gQRWYIp/xyJkgc6PRsseTOdK9lYUw1H75lzZQKBgC0X\nrdih8obp5RqMyu8RD9SuFpxgAXXa4ZZZuDkFZiPBmRVyZkhqGf2icAG5UCNoa2xn\nWnjGUKUyApzB8MIXCtRWRwKpSksygSJ9MML9wwe9C6SQMK4Mj/14huTQ74YwF41d\nE2VF6YDGNVSTteHerUkjyr/8SyxhYDZkGBiiVmxVAoGBAM59MVGp4BtVyjNHvsNm\nWzaElw6Oy7V7RUuX5p3RjcP1fmqGcY1r7YM1W/fFkqOHtHOLW+kdWPz56DVllzUo\nnXiBLb8Ns8/W0KtnH4wz1VPL20/3QcrRRmjy6+wYlYFdIzXN2ptj0dhEfiWfSQM9\ny/4CvAJBWW8mgZj9UDpOdXCS\n-----END PRIVATE KEY-----\n",
                    "client_email": "get-infor@crested-sunup-411416.iam.gserviceaccount.com",
                    "client_id": "117584027535760018927",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/get-infor%40crested-sunup-411416.iam.gserviceaccount.com",
                    "universe_domain": "googleapis.com"
                }
                # SCOPES
                SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
                # Authenticate and create the service
                credentials = service_account.Credentials.from_service_account_info(service_account_json, scopes=SCOPES)
                service = build('sheets', 'v4', credentials=credentials)
                # The ID and range of the spreadsheet.
                SPREADSHEET_ID = f'{id_file}'
                RANGE_NAME = f'{name_sheet}'  # Update this to your actual sheet name
                # Call the Sheets API
                sheet = service.spreadsheets()
                result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
                values = result.get('values', [])
                # Convert to DataFrame
                return pd.DataFrame(values[1:], columns=values[0])
                # End lấy thông tin gg sheet
            #'''
            progress_dialog = QProgressDialog(self) # Mở cửa sổ QProgressDialog để thông báo rằng đang thực hiện lệnh
            progress_dialog.setWindowTitle("Đang tải ...")
            progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
            progress_dialog.setMinimumDuration(0)
            progress_dialog.setLabelText("Loading ...")
            progress_dialog.resize(210, 100)  # Đặt kích thước tùy ý
            progress_dialog.show()
            #'''
            ### lấy thông tin research ID
            id_file_gg_sheet = '1-xdZR9uLE7lBTEGGYNNzfOP8gTZHVUigScdDju3_-AU'
            name_sheet_researcher_id = 'tex'
            df_researcher_id = get_infor_from_gg_drive(id_file_gg_sheet, name_sheet_researcher_id)
            ### End lấy thông tin research id
            # list id rearcher
            list_research_id = dict(zip(df_researcher_id['list'], df_researcher_id['content']))
            # End đọc file
            progress_dialog.close() # Đóng QProgressDialog sau khi hoàn thành
            research_id_input, ok_pressed = CheckDialog(list_research_id, "Chọn biểu mẫu LaTeX").getItem()
            if ok_pressed:
                research_id_input = [re.sub(r'\s*\(.*?\)', '', research_id_input[0])]
                for id_check in research_id_input:
                    if id_check in list_research_id:
                        url_citation_open = list_research_id[id_check]
                        # Hiển thị hộp thoại chứa nội dung trích dẫn
                        dialog = TextDisplayDialog(url_citation_open, id_check, self)
                        dialog.exec()
                    else:
                        text_show_citation = f"Nội dung đang được cập nhật"
                        self.result_display.append(text_show_citation)
        except Exception as e:
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Icon.Warning)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText(f">>> Cảnh báo lỗi >>> {str(e)}")
            error_dialog.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Chỉnh màu sắc giao diện
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#87CEEB"))  # Màu nút bấm (xanh dương nhạt)
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#000000"))  # Màu chữ (đen)
    palette.setColor(QPalette.ColorRole.Button, QColor("#000000"))  # Màu nền cửa sổ (đen)
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("#FF0000"))  # Màu chữ trên nút (đỏ)
    app.setPalette(palette)
    #
    window = MyApp()
    window.setWindowTitle(f"{title_app}")
    window.setGeometry(0, 30, 1000, 500) # (x, y, width, height)
    window.show()
    sys.exit(app.exec())

# auto-py-to-exe
# Lỗi: "Advanced" > "Additional imports (hidden imports)": scipy._lib.array_api_compat.numpy.fft
