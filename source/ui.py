from tkinter import *
from tkinter import filedialog

window = Tk()
window.title("Welcome to Songs Database")
window.geometry('1000x1000')


def submit_values():
    author_info = author_value.get()
    title_info = title_value.get()
    album_info = album_value.get()
    copyright_info = copyright_value.get()
    print('Submitted: Author: {}, title: {}, album: {}, copyright: {}'.format(author_info, title_info, album_info,
                                                                              copyright_info))


def open_file():
    text_file = filedialog.askopenfile(initialdir="/gui/images", title="Select a text file with song lyrics",
                                       filetypes=[("txt files", "*.txt")])
    filename_text = Text(window, height=4, width=50)
    filename_text.grid(row=4, column=1)
    filename_text.insert(END, text_file.name)

    song_text = text_file.read()
    song_text_scrollable.insert(END, song_text)
    print("Song submitted: \n", song_text)


# TODO: add date field
author_label = Label(window, text="Author").grid(row=0, column=0)
title_label = Label(window, text="Song title").grid(row=1, column=0)
album_label = Label(window, text="Album").grid(row=2, column=0)
copyright_label = Label(window, text="Copyright").grid(row=3, column=0)
filename_label = Label(window, text="Text File:").grid(row=4, column=0)

song_text_scrollable = Text(window, height=15, width=70)
song_text_scrollable.grid(row=6, column=1)

author_value = StringVar()
title_value = StringVar()
album_value = StringVar()
copyright_value = StringVar()

author_field = Entry(window, textvariable=author_value).grid(row=0, column=1)
title_field = Entry(window, textvariable=title_value).grid(row=1, column=1)
album_field = Entry(window, textvariable=album_value).grid(row=2, column=1)
copyright_field = Entry(window, textvariable=copyright_value).grid(row=3, column=1)

open_file_button = Button(window, text="Browse file...", command=open_file).grid(row=4, column=2)
save_button = Button(window, text="Save song", command=submit_values).grid(row=10, column=1)

window.mainloop()
