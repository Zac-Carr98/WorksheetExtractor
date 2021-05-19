import tkinter as tk
from tkinter import filedialog as fd
from tkinter import PhotoImage
import gc
from backend import Backend
import threading
from tkinter import Frame


class CustomButton(tk.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(bg='#ff7f27', fg='black')
