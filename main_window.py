import tkinter as tk
from tkinter import filedialog as fd
from tkinter import PhotoImage
import gc
from backend import Backend
import threading
from widgets import CustomButton


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.resizable(False, False)
        self.root.title('Worksheet Extractor')
        self.root.iconbitmap('images/iconforapp.ico')
        self.backend = Backend()

        # Setting size of app
        root.geometry('900x725')

        # adding image for background
        self.background_image = PhotoImage(file='images/Template.png')
        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # label to push items down
        self.placement = tk.Label(self.root, bg='white')
        self.placement.pack(pady=100)

        # btn_select
        # self.btn_select = tk.Button(self.root, text='Click to Select File', command=self.open_dialog,
        # bg='#ff7f27', fg='black')
        self.btn_select = CustomButton(self.root, text='Click to Select File', command=self.open_dialog)
        # self.loadimage = tk.PhotoImage(file="C:/Users/tpsharp/Pictures/Saved Pictures/SaveLocation.png")
        # self.btn_select = tk.Button(self.root, image=self.loadimage)
        # self.btn_select["bg"] = "white"
        # self.btn_select["border"] = "0"
        self.btn_select.pack(pady=10)

        # btn location
        self.btn_location = CustomButton(self.root, text='Save Location', command=self.save_location)
        self.btn_location.pack(pady=10)

        # Frame for keyword entry
        self.frame1 = tk.Frame(root, bg='white')
        self.frame1.pack(pady=10)

        # text entry
        self.text_entry = tk.Entry(self.frame1)
        self.text_entry.grid(row=0, column=0, padx=10)

        # submit keywords
        self.submit_keyword = CustomButton(self.frame1, text='Submit', command=self.add_keyword)
        self.submit_keyword.grid(row=0, column=1, padx=10, sticky=tk.W)

        # btn_run
        self.btn_run = CustomButton(self.root, text='Run', command=self.run)
        self.btn_run.pack(pady=10)

    def open_dialog(self):
        self.backend.select_target_file(fd.askopenfilename())

    def save_location(self):
        self.backend.set_save_folder(fd.askdirectory())

    def add_keyword(self):
        my_string = self.text_entry.get()
        my_list = my_string.split(", ")
        self.backend.add_keywords(my_list)

    def run(self):
        threading.Thread(target=self.backend.run).start()
        gc.collect()

