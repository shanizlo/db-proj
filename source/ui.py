from tkinter import *
from tkinter import filedialog


class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        # Setup Frame
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        # container.columnconfigure(0, weight=1)
        # container.rowconfigure(0, weight=1)

        self.frames = {}

        for F in (HomePage, StatisticsPage, ShowWordsInSongPage, UploadSongPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(HomePage)

    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()


class HomePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        statistics_page = Button(self, text="Statistics 📊", command=lambda: controller.show_frame(StatisticsPage)).grid(row=1, column=2)

        page_show_words = Button(self, text="Show Words in Song 🔤", command=lambda: controller.show_frame(ShowWordsInSongPage)).grid(row=1, column=3)

        page_upload = Button(self, text="Upload Song 🎙", command=lambda: controller.show_frame(UploadSongPage)).grid(row=1, column=1)


class UploadSongPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        def submit_values():
            author_info = author_value.get()
            title_info = title_value.get()
            album_info = album_value.get()
            copyright_info = copyright_value.get()
            song_lyrics = song_text_preview.get("1.0", END)
            print('Submitted: Author: {}, title: {}, album: {}, copyright: {}, song lyrics: {}'.format(author_info,
                                                                                                       title_info,
                                                                                                       album_info,
                                                                                                       copyright_info,
                                                                                                       song_lyrics))

        def open_file():
            text_file = filedialog.askopenfile(initialdir="/gui/images", title="Select a text file with song lyrics",
                                               filetypes=[("txt files", "*.txt")])
            filename_text = Text(self, height=4, width=50)
            filename_text.grid(row=4, column=1)
            filename_text.insert(END, text_file.name)

            song_text = text_file.read()
            song_text_preview.insert(END, song_text)
            print("Song submitted 🤩")

        # TODO: add date field
        page_title_label = Label(self, text="Upload Song 🎙").grid(row=0, column=2)

        author_label = Label(self, text="Author").grid(row=1, column=1)
        title_label = Label(self, text="Song title").grid(row=2, column=1)
        album_label = Label(self, text="Album").grid(row=3, column=1)
        copyright_label = Label(self, text="Copyright").grid(row=4, column=1)
        filename_label = Label(self, text="Text File:").grid(row=5, column=1)

        song_text_preview = Text(self, height=15, width=70)
        song_text_preview.grid(row=7, column=2)

        author_value = StringVar()
        title_value = StringVar()
        album_value = StringVar()
        copyright_value = StringVar()
        song_value = StringVar()

        author_field = Entry(self, textvariable=author_value).grid(row=1, column=2)
        title_field = Entry(self, textvariable=title_value).grid(row=2, column=2)
        album_field = Entry(self, textvariable=album_value).grid(row=3, column=2)
        copyright_field = Entry(self, textvariable=copyright_value).grid(row=4, column=2)

        open_file_button = Button(self, text="Browse file...", command=open_file).grid(row=5, column=3)
        save_button = Button(self, text="Save song", command=submit_values).grid(row=11, column=2)
        home_button = Button(self, text="Home 🏠", command=lambda: controller.show_frame(HomePage)).grid(row=0, column=0)


class StatisticsPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        page_title_label = Label(self, text="Statistics 📊").grid(row=0, column=2)
        home_button = Button(self, text="Home 🏠", command=lambda: controller.show_frame(HomePage)).grid(row=0, column=0)


class ShowWordsInSongPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        page_title_label = Label(self, text="Show Words in Song 🔤").grid(row=0, column=2)
        home_button = Button(self, text="Home 🏠", command=lambda: controller.show_frame(HomePage)).grid(row=0, column=0)

        author_value = StringVar()
        title_value = StringVar()

        author_field = Entry(self, textvariable=author_value).grid(row=1, column=2)
        title_field = Entry(self, textvariable=title_value).grid(row=2, column=2)
        author_label = Label(self, text="Author").grid(row=1, column=1)
        title_label = Label(self, text="Song title").grid(row=2, column=1)




app = App()
app.title("Welcome to Songs Database 🎙")
app.geometry('1000x700')
app.mainloop()
