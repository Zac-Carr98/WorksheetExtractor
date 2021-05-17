import pdfplumber
from PyPDF2 import PdfFileReader, PdfFileWriter
import time


def find_missing(lst):
    missing = [x for x in range(lst[0], lst[-1] + 1)
            if x not in lst]
    corrected = lst.extend(missing)
    if len(corrected) < 15:
        return sorted(corrected)
    else:
        return lst


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
                # self.search_page_two(page_num)

    def search_page(self, page_num):
        for keyword in self.key_words:
            if keyword in self.page_text:
                self.dict[keyword].append(page_num)
                continue

    def search_page_quicker(self, page_num):
        self.page_text = sorted(self.page_text.split())
        for keyword in self.key_words:
            if self.binary_search(keyword):
                self.dict[keyword].append(page_num)

    def binary_search(self, keyword):
        first = 0
        last = len(self.page_text) - 1
        found = False
        while first <= last and not found:
            middle = (first + last) // 2
            if self.page_text[middle] == keyword:
                found = True
            else:
                if keyword < self.page_text[middle]:
                    last = middle - 1
                else:
                    first = middle + 1
        return found

    def run(self):
        t0 = time.time()

        self.open_pdf()
        self.get_num_pages()
        self.page_loop()

        print(self.dict)

        self.create_pdfs()

        t1 = time.time()
        total_t = t1-t0
        print(f'Seconds:{round(total_t, 5)}, Minutes: {round(total_t/60, 5)}')

    def create_pdfs(self):
        pdf = PdfFileReader(self.target_file_name)
        for key, values in self.dict.items():
            self.split(pdf=pdf, pages=values, key=key)

    def split(self, pdf, pages, key):

        pages_opened = []
        for i in pages:
            if i not in pages_opened:
                pages_opened.append(i)

        pages_opened = find_missing(pages_opened)

        pdfWriter = PdfFileWriter()

        for page_num in pages_opened:
            pdfWriter.addPage(pdf.getPage(page_num))

        with open(f'{self.save_folder_name}/{key}.pdf', 'wb') as f:
            pdfWriter.write(f)
            f.close()
