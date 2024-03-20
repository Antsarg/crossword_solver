from mailbox import mboxMessage
from tkinter import *
import tkinter
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.dialogs import Messagebox
import re
import sys

HIGH_SCORED_LIST = "assets\\spreadthewordlist_unscored_high.txt"
UNSCORED_LIST = ""
WARNING_MESSAGES = [
    "valid pattern",
    "pattern must contain at least 3 totalchar",
    "only letters and ? are allowed in pattern",
    "pattern must contain at least 1 unknown letter",
]
 


# load a list of possible crossword answers
def load_list(fname):
    try:
        with open(fname) as f:
            global word_list
            result = f.readlines()
            return list(map(str.rstrip, result))
    except FileNotFoundError:
        print(f"File {fname} not found")
        sys.exit(1)


# look for words that match a given pattern
def search_words(pattern: str, word_list: list):
    pattern = pattern.replace("?", ".").lower()
    matched = []
    for w in word_list:
        if re.fullmatch(pattern, w):
            matched.append(w)
    return matched


# check if the user entered a valid path
def validate_pattern(s: str):
    if len(s) < 3:
        return 1
    if re.match(r"^[a-z?]+$", s, flags=re.IGNORECASE) == None:
        return 2
    if "?" not in s:
        return 3
    return 0


class HelpWindov(Toplevel):

    
    def __init__(self, master, *args):
        
        super().__init__(master, *args)
        
        self.title("help")
        self.geometry("600x400")
        try:
            with open("assets\\help.txt", "r") as f:
                msg = f.read()
            self.button = tb.Button(self, text="Close", command=self.destroy)
            self.button.pack(pady=10, side=BOTTOM)
            self.text = tb.Text(self, wrap=WORD , background="lightgrey",
                                foreground="black", font="Helvetica, 12")
            self.text.insert("end", msg)
            self.text.config(state="disabled")
            self.text.pack(side=LEFT, fill=BOTH, expand=True, padx = 10)
            self.grab_set()
        except FileNotFoundError:
            Messagebox.show_error(f'help file not found')
        
        


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
        self.display.pack(side=LEFT, fill=BOTH, expand=TRUE, padx=5, pady=5)

        # create shortcut for help window
        self.bind("<F1>", self.show_help)
        self.word_list = load_list(HIGH_SCORED_LIST)

    def show_help(self, e):
        HelpWindov(self)
        # mb = Messagebox.show_info(
        #     "Insert a pattern in the entry box, then press Search ", "App Info"
        # )

    # clear entry field and display area

    def clear_entry(self):
        self.entry_var.set("")
        self.display.delete(*self.display.get_children())
        self.status_bar.configure(text="Press F1 for Help")

    # search words matching pattern
    def search_pattern(self):
        pattern = self.entry_var.get()
        result = validate_pattern(pattern)
        if result == 0:
            words = search_words(pattern, self.word_list)
            self.status_bar.configure(
                text=f"{len(words)} words found for pattern: {pattern}"
            )
            self.display.delete(*self.display.get_children())
            n_col = 3
            for pos in range(0, len(words), n_col):
                self.display.insert("", END, values=words[pos : pos + n_col])
        else:
            mb = Messagebox.show_warning(
                WARNING_MESSAGES[result], "Invalid Pattern"
            )

    def create_frame(self, stringvar):
        top_frame = tb.Frame(self, height=100)
        hint = tb.Label(top_frame, text="Entry Pattern:", font="Calibri,18")
        hint.pack(side=LEFT, padx=20)
        my_entry = tb.Entry(
            top_frame, bootstyle=LIGHT, width=15, font="Calibri, 18"
        )
        my_entry.pack(side=LEFT, pady=20)
        my_entry.configure(textvariable=stringvar)
        clear_button = tb.Button(
            top_frame,
            text="Clear",
            command=self.clear_entry,
            bootstyle="success",
            width=8,
        )
        clear_button.pack(side=LEFT, padx=25)
        search_btn = tb.Button(
            top_frame,
            text="Search",
            command=self.search_pattern,
            bootstyle="primary",
            width=8,
        )
        search_btn.pack(side=LEFT, padx=10)

        return top_frame

    def create_text_area(self):
        my_style = tb.Style()
        my_style.configure(
            "success.Treeview", font="Calibri, 12", rowheight=25
        )
        my_table = tb.Treeview(
            self,
            bootstyle="success",
            columns=["col1", "col2", "col3"],
            style="success.Treeview",
            show="",
        )
        return my_table

    def create_status_bar(self):
        my_label = tb.Label(
            self,
            text="Press F1 for help",
            font="Helvetica, 14",
            bootstyle="inverse",
            relief=SUNKEN,
        )
        return my_label


def main():
    app = App(themename="superhero")
    app.mainloop()


if __name__ == "__main__":
    main()
