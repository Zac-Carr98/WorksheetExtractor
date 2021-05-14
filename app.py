import tkinter as tk
from tkinter import filedialog as fd
import pdfplumber
from PyPDF2 import PdfFileReader, PdfFileWriter
import gc
import sys
from main_window import MainWindow

class App:
    def __init__(self):
        self.root = tk.Tk()

    def main(self):
        big_widget = MainWindow(self.root)
        big_widget.grid()
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.main()