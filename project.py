from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.dialogs import Messagebox
import re

HIGH_SCORED_LIST = "assets\spreadthewordlist_unscored_high.txt"
UNSCORED_LIST = ""


# load a list of possible crossword answers
def load_list(fname):
    with open(fname) as f:
        global word_list
        result = f.readlines()
        return list(map(str.rstrip, result))


# look for words that match a given pattern
def search_words(pattern: str, word_list: list):
    pattern = pattern.replace("?", ".").lower()
    matched = []
    for w in word_list:
        if re.fullmatch(pattern, w):
            matched.append(w)
    return matched


def validate_pattern(s: str):
    if len(s) < 3:
        return 1
    if re.match(r"^[a-z?]+$", s, flags=re.IGNORECASE) == None:
        return 2
    if "?" not in s:
        return 3
    return 0


class App(tb.Window):
    def __init__(self, themename):
        super().__init__(self, themename)
        self.title("Crossword solver")
        self.geometry("800x600")
        self.entry_var = tb.StringVar(self)
        self.top_frame = self.create_frame(self.entry_var)
        self.top_frame.pack(side=TOP, fill=X)
        self.status_bar = self.create_status_bar()
        self.status_bar.pack(side=BOTTOM, fill=X)
        self.display = self.create_text_area()
        self.display.pack(side=LEFT, fill=BOTH, expand=TRUE)

        # create shortcut for help window
        self.bind("<F1>", self.show_help)

        self.word_list = load_list(HIGH_SCORED_LIST)

    def show_help(self, e):
        mb = Messagebox.show_info(
            "Insert a pattern in the entry ox, then press Search ", "App Info"
        )

    def search_pattern(self):
        pattern = self.entry_var.get()
        words = search_words(pattern, self.word_list)
        self.status_bar.configure(
            text=f"{len(words)} words found for pattern: {pattern}"
        )
        self.display.insert(END, "\n".join(words))

    def create_frame(self, stringvar):
        top_frame = tb.Frame(self, height=100, relief=SUNKEN)
        hint = tb.Label(top_frame, text="Insert Pattern:", font="Calibri,18")
        hint.pack(side=LEFT, padx=20)
        my_entry = tb.Entry(top_frame, bootstyle=LIGHT, width=15, font="Calibri, 18")
        my_entry.pack(side=LEFT, pady=20)
        my_entry.configure(textvariable=stringvar)
        search_btn = tb.Button(
            top_frame, text="Search", command=self.search_pattern, bootstyle="primary"
        )
        search_btn.pack(side=LEFT, padx=25)

        return top_frame

    def create_text_area(self):
        my_text = ScrolledText(self, bootstyle="success", autohide=True)
        return my_text

    def create_status_bar(self):
        my_label = tb.Label(
            self,
            text="Characters: 0",
            font="Helvetica, 14",
            bootstyle="inverse",
            relief=SUNKEN,
        )
        return my_label


def main():
    word_list = load_list("assets\spreadthewordlist_unscored_high.txt")
    app = App(themename="superhero")
    app.mainloop()


if __name__ == "__main__":
    main()
