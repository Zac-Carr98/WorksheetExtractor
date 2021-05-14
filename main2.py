import tkinter as tk
from tkinter import filedialog as fd
import pdfplumber
from PyPDF2 import PdfFileReader, PdfFileWriter
import gc
import sys

class App:
    def __init__(self):
        self.root = tk.Tk()

    def main(self):
        big_widget = BigWidget(self.root)
        big_widget.grid()
        self.root.mainloop()


class PDFHolder:
    def __init__(self, pdf):
        self.pdf_held = pdf
        self.page_text = None

    def get_page_text(self, i):
        print(f"Reading Page: {i + 1}")
        self.page_text = self.pdf_held.pages[i].extract_text()
        return self.page_text


class BigWidget:
    def __init__(self, root):
        self.root = root
        self.btn_select = tk.Button(self.root, text='Click to Select File', command=self.open_dialog)
        self.btn_open = tk.Button(self.root, text='Run', command=self.open_pdf)
        self.text_entry = tk.Entry(self.root)
        self.submit_keyword = tk.Button(self.root, text='Submit', command=self.add_keyword2)
        self.btn_location = tk.Button(self.root, text='Select Download Location', command=self.download_location)

        self.extracted_text = None
        self.name = None
        self.location = None
        self.key_list = []
        self.rowNo = 1
        self.dict = {}

    def label_maker(self, word):
        self.rowNo += 1
        lbl = tk.Label(text=word)
        lbl.grid(row=self.rowNo, column=0)

    def grid(self):
        self.btn_select.grid(row=0, column=0)
        self.btn_open.grid(row=0, column=1)
        self.text_entry.grid(row=1, column=0)
        self.submit_keyword.grid(row=1, column=1)
        self.btn_location.grid(row=2, column=2)

    def add_keyword(self):
        self.key_list.append(self.text_entry.get())
        self.label_maker(self.text_entry.get())

    def add_keyword2(self):
        my_string = self.text_entry.get()
        my_list = my_string.split(", ")
        self.key_list = my_list
        # self.key_list.append(self.text_entry.get())
        for i in self.key_list:
            self.label_maker(i)

    def open_dialog(self):
        self.name = fd.askopenfilename()
        print(self.name)

    def open_pdf(self):
        self.generate_found_lists()

        self.pdf = PDFHolder(pdfplumber.open(self.name))
        gc.collect()

        for page_num in range(len(self.pdf.pdf_held.pages)):
            self.keyword_search(page_num)
            if page_num % 100 == 0:
                gc.collect()
                print("Happened")

        print(self.dict)

        self.create_pdfs()

    def keyword_search(self, page):
        for keyword in self.key_list:
            if keyword in self.pdf.get_page_text(page):
                self.dict[keyword].append(page)
                continue

    def generate_found_lists(self):
        for keyword in self.key_list:

            self.dict[keyword] = []
        print(self.dict)

    def create_pdfs(self):
        for key, values in self.dict.items():
            self.split(pdf_path=self.name, pages=values, key=key)

    def download_location(self):
        self.location = fd.askdirectory()
        print(self.location)

    def split(self, pdf_path, pages, key):
        pdf = PdfFileReader(pdf_path)

        pdfWriter = PdfFileWriter()

        for page_num in pages:
            pdfWriter.addPage(pdf.getPage(page_num))

        with open(f'{self.location}/{key}.pdf', 'wb') as f:
            pdfWriter.write(f)
            f.close()


if __name__ == "__main__":
    app = App()
    app.main()
