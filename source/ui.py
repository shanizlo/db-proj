from tkinter import *
from tkinter import filedialog

window = Tk()
window.title("Welcome to Songs Database")
window.geometry('700x700')

def submit_values():
    author_info = author_value.get()
    title_info = title_value.get()
    album_info = album_value.get()
    copyright_info = copyright_value.get()
    print('Submitted: Author: {}, title: {}, album: {}, copyright: {}'.format(author_info, title_info, album_info, copyright_info))

def open_file():
    window.filename = filedialog.askopenfile(initialdir="/gui/images", title="Select a text file with song lyrics", filetypes=[("txt files", "*.txt")])
    chosen_file_label = Label(window, text=window.filename).grid(row=4, column=1)

# TODO: add date field
author_label = Label(window, text="Author").grid(row=0, column=0)
title_label = Label(window, text="Song title").grid(row=1, column=0)
album_label = Label(window, text="Album").grid(row=2, column=0)
copyright_label = Label(window, text="Copyright").grid(row=3, column=0)
filename_label = Label(window, text="Text File:").grid(row=4, column=0)

author_value = StringVar()
title_value = StringVar()
album_value = StringVar()
copyright_value = StringVar()
# filename_value =

author_field = Entry(window, textvariable=author_value).grid(row=0, column=1)
title_field = Entry(window, textvariable=title_value).grid(row=1, column=1)
album_field = Entry(window, textvariable=album_value).grid(row=2, column=1)
copyright_field = Entry(window, textvariable=copyright_value).grid(row=3, column=1)

open_file_button = Button(window, text="Browse file...", command=open_file).grid(row=5, column=1)
save_button = Button(window, text="Upload song", command=submit_values).grid(row=8, column=1)




window.mainloop()
