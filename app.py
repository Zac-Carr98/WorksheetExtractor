import tkinter as tk
from main_window import MainWindow

# TODO - make unit test


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