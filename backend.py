import tkinter as tk
from tkinter import filedialog as fd
import pdfplumber
from PyPDF2 import PdfFileReader, PdfFileWriter
import gc
import sys


class Backend:
    def __init__(self):
        self.target_file_name = None
        self.save_folder_name = None
        self.key_words = []
        self.pdf = None
        self.num_pages = None
        self.pages = []
        self.page_text = ""
        self.dict = {}

    def select_target_file(self, name):
        self.target_file_name = name
        print(name)

    def set_save_folder(self, name):
        self.save_folder_name = name
        print(name)

    def add_keywords(self, keys_list):
        self.key_words.extend(keys_list)
        self.generate_found_lists()
        print(self.key_words)

    def generate_found_lists(self):
        for keyword in self.key_words:
            self.dict[keyword] = []

    def open_pdf(self):
        self.pdf = pdfplumber.open(self.target_file_name)
        pass

    def get_num_pages(self):
        self.num_pages = len(self.pdf.pages)

    def page_loop(self):
        for page_num in range(self.num_pages):
            print(f"Searching Page: {page_num+1}")
            page = self.pdf.pages[page_num]
            self.page_text = page.extract_text()
            page.close()
            if self.page_text:
                self.search_page(page_num)

    def search_page(self, page_num):
        for keyword in self.key_words:
            if keyword in self.page_text:
                self.dict[keyword].append(page_num)
                continue

    def run(self):
        self.open_pdf()
        self.get_num_pages()
        self.page_loop()

        print(self.dict)

        self.create_pdfs()

    def create_pdfs(self):
        for key, values in self.dict.items():
            self.split(pdf_path=self.target_file_name, pages=values, key=key)

    def split(self, pdf_path, pages, key):
        pdf = PdfFileReader(pdf_path)

        pdfWriter = PdfFileWriter()

        for page_num in pages:
            pdfWriter.addPage(pdf.getPage(page_num))

        with open(f'{self.save_folder_name}/{key}.pdf', 'wb') as f:
            pdfWriter.write(f)
            f.close()

