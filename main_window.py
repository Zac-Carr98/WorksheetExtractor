import tkinter as tk
from tkinter import filedialog as fd
import pdfplumber
from PyPDF2 import PdfFileReader, PdfFileWriter
import gc
import sys
from backend import Backend
import threading


class MainWindow:
    def __init__(self, root):
        self.root = root

        self.backend = Backend()

        self.btn_select = tk.Button(self.root, text='Click to Select File', command=self.open_dialog)
        self.btn_run = tk.Button(self.root, text='Run', command=self.run)
        self.btn_location = tk.Button(self.root, text='Save Location', command=self.save_location)
        
        self.text_entry = tk.Entry(self.root)
        self.submit_keyword = tk.Button(self.root, text='Submit', command=self.add_keyword)

    def grid(self):
        self.btn_select.grid(row=0, column=0, sticky=tk.EW)
        self.btn_run.grid(row=0, column=2)
        self.text_entry.grid(row=1, column=0)
        self.submit_keyword.grid(row=1, column=1, sticky=tk.W)
        self.btn_location.grid(row=0, column=1)

    def open_dialog(self):
        self.backend.select_target_file(fd.askopenfilename())

    def save_location(self):
        print("happens")
        self.backend.set_save_folder(fd.askdirectory())

    def add_keyword(self):
        my_string = self.text_entry.get()
        my_list = my_string.split(", ")
        self.backend.add_keywords(my_list)

    def run(self):
        threading.Thread(target=self.backend.run).start()
        gc.collect()
