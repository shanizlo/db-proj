from tkinter import *
from tkinter import filedialog
from source.helpers_db import *

class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        # Setup Frame
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        #  Important when adding a frame
        for F in (HomePage, StatisticsPage, ShowWordsInSongPage, UploadSongPage, ShowWordByPlace, ShowContext, GroupPage):
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

        page_upload_btn = Button(self, text="Upload Song", command=lambda: controller.show_frame(UploadSongPage)).grid(row=1, column=1)
        page_show_words_btn = Button(self, text="Show Words in Song", command=lambda: controller.show_frame(ShowWordsInSongPage)).grid(row=1, column=2)
        page_upload_btn = Button(self, text="Statistics", command=lambda: controller.show_frame(StatisticsPage)).grid(row=1, column=3)
        find_word_btn = Button(self, text="Find Word", command=lambda: controller.show_frame(ShowWordByPlace)).grid(row=1, column=5)
        word_context_btn = Button(self, text="Show Context", command=lambda: controller.show_frame(ShowContext)).grid(row=2, column=1)
        add_group_btn = Button(self, text="Add a/to group", command=lambda: controller.show_frame(GroupPage)).grid(row=2, column=2)

# TODO: add printing error message
class UploadSongPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        def submit_values():
            author_info = author_value.get()
            title_info = title_value.get()
            album_info = album_value.get()
            copyright_info = copyright_value.get()
            song_lyrics = song_text_preview.get("1.0", END)
            insert_into_database(author_info, title_info, album_info, copyright_info, song_lyrics)
            print('Submitted: Author: {}, title: {}, album: {}, copyright: {}, song lyrics: {}'.format(author_info,
                                                                                                       title_info,
                                                                                                       album_info,
                                                                                                       copyright_info,
                                                                                                       song_lyrics))

        def open_file():
            text_file = filedialog.askopenfile(initialdir="/gui/images", title="Select a text file with song lyrics",
                                               filetypes=[("txt files", "*.txt")])
            filename_text = Text(self, height=3, width=70)
            filename_text.grid(row=5, column=2)
            filename_text.insert(END, text_file.name)

            song_text = text_file.read()
            song_text_preview.insert(END, song_text)
            print("Song submitted")

        page_title_label = Label(self, text="Upload Song").grid(row=0, column=2)

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

        open_file_button = Button(self, text="Browse file...", command=open_file).grid(row=6, column=2)
        save_button = Button(self, text="Save song", command=submit_values).grid(row=11, column=2)
        home_button = Button(self, text="Home", command=lambda: controller.show_frame(HomePage)).grid(row=0, column=0)


class StatisticsPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        page_title_label = Label(self, text="Statistics").grid(row=0, column=2)
        home_button = Button(self, text="Home", command=lambda: controller.show_frame(HomePage)).grid(row=0, column=0)

        author_value = StringVar()
        title_value = StringVar()
        num_words_in_song_value = IntVar()
        avg_chars_in_sentence_value = DoubleVar()
        avg_chars_in_verse_value = DoubleVar()

        author_label = Label(self, text="Author:").grid(row=1, column=1)
        title_label = Label(self, text="Song title:").grid(row=2, column=1)
        author_field = Entry(self, textvariable=author_value).grid(row=1, column=2)
        title_field = Entry(self, textvariable=title_value).grid(row=2, column=2)

        num_words_in_song_label = Label(self, text="Number of words in song:").grid(row=4, column=1)
        avg_chars_in_sentence_label = Label(self, text="Average characters in sentence:").grid(row=4, column=2)
        avg_chars_in_verse_label = Label(self, text="Average characters in verse:").grid(row=4, column=3)

        num_words_in_song = Label(self, textvariable=num_words_in_song_value).grid(row=5, column=1)
        avg_chars_in_sentence = Label(self, textvariable=avg_chars_in_sentence_value).grid(row=5, column=2)
        avg_chars_in_verse = Label(self, textvariable=avg_chars_in_verse_value).grid(row=5, column=3)

        def show_statistics():
            #TODO get statistics from author and title which yields song_id
            #TEST VALUES
            num_words_in_song_value.set(7)
            avg_chars_in_sentence_value.set(3.7)
            avg_chars_in_verse_value.set(4.2)


        statistics_button = Button(self, text="Show statistics", command=show_statistics).grid(row=3, column=1)

class ShowWordsInSongPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        def search_song_words_desc():
            song_words_preview.delete("1.0", "end")
            author = author_value.get()
            title = title_value.get()
            print("searching for song words for author {}, title {}".format(author, title))
            song_words = SearchSongWords(author, title)
            song_words_preview.insert(END, song_words)

        page_title_label = Label(self, text="Show Words in Song").grid(row=0, column=2)
        home_button = Button(self, text="Home", command=lambda: controller.show_frame(HomePage)).grid(row=0, column=0)

        author_value = StringVar()
        title_value = StringVar()

        author_field = Entry(self, textvariable=author_value).grid(row=1, column=2)
        title_field = Entry(self, textvariable=title_value).grid(row=2, column=2)
        author_label = Label(self, text="Author").grid(row=1, column=1)
        title_label = Label(self, text="Song title").grid(row=2, column=1)

        search_button = Button(self, text="Search song", command=search_song_words_desc).grid(row=11, column=2)

        song_words_preview = Text(self, height=15, width=70)
        song_words_preview.grid(row=7, column=2)

class ShowWordByPlace(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        def search_word():
            author = author_value.get()
            title = title_value.get()
            verse = verse_num.get()
            line = line_value.get()
            word_pos = word_num_value.get()
            # TODO: function should return word by its position
            print("searching for word for author {}, title {}, verse {}, line {}, word num {}".format(author, title, verse, line, word_pos))
            #  TODO: add real output from show words
            found_word = "Hello"
            found_word_preview.insert(END, found_word)

        page_title_label = Label(self, text="Find Word by its Position").grid(row=0, column=2)
        home_button = Button(self, text="Home", command=lambda: controller.show_frame(HomePage)).grid(row=0,
                                                                                                         column=0)
        author_value = StringVar()
        title_value = StringVar()
        verse_num = StringVar()
        line_value = StringVar()
        word_num_value = StringVar()

        author_field = Entry(self, textvariable=author_value).grid(row=1, column=2)
        title_field = Entry(self, textvariable=title_value).grid(row=2, column=2)
        author_label = Label(self, text="Author").grid(row=1, column=1)
        title_label = Label(self, text="Song title").grid(row=2, column=1)

        verse_label = Label(self, text="Num of Verse").grid(row=1, column=3)
        line_label = Label(self, text="Num of Line").grid(row=2, column=3)
        word_position_label = Label(self, text="Num of Word").grid(row=3, column=3)

        verse_field = Entry(self, textvariable=verse_num).grid(row=1, column=4)
        line_field = Entry(self, textvariable=line_value).grid(row=2, column=4)
        word_position_field = Entry(self, textvariable=word_num_value).grid(row=3, column=4)

        word_label = Label(self, text="Word found:").grid(row=12, column=1)

        search_button = Button(self, text="Search song", command=search_word).grid(row=11, column=2)

        found_word_preview = Text(self, height=1, width=10)
        found_word_preview.grid(row=12, column=2)

class ShowContext(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        def search_song_words_desc():
            author = author_value.get()
            title = title_value.get()
            # TODO: function should return words of the song in desc order, add necessary query in database.py as needed
            print("searching for song words for author {}, title {}".format(author, title))
            #  TODO: add real output from show words
            song_words = """HTML Tutorial
                CSS Tutorial
                HTML Tutorial
                CSS Tutorial
                JavaScript Tutorial
                How To Tutorial
                SQL Tutorial
                Python Tutorial
                W3.CSS Tutorial
                Bootstrap Tutorial
                PHP Tutorial
                Java Tutorial
                C++ Tutorial
                jQuery TutorialHTML Tutorial
                CSS Tutorial
                JavaScript Tutorial
                How To Tutorial
                SQL Tutorial
                Python Tutorial
                W3.CSS Tutorial
                Bootstrap Tutorial
                PHP Tutorial
                Java Tutorial
                C++ Tutorial
                jQuery Tutorial"""
            song_words_preview.insert(END, song_words)

        def search_word_context():
            #TODO - add search for appearences of the word
            return True

        def set_chosen_word(choice):
            choice = options_words.get()
            print(choice)

        page_title_label = Label(self, text="Show Context of Word. Search for song, then choose the word to show context for.").grid(row=0, column=2)
        home_button = Button(self, text="Home", command=lambda: controller.show_frame(HomePage)).grid(row=0, column=0)

        author_value = StringVar()
        title_value = StringVar()

        author_field = Entry(self, textvariable=author_value).grid(row=1, column=2)
        title_field = Entry(self, textvariable=title_value).grid(row=2, column=2)
        author_label = Label(self, text="Author").grid(row=1, column=1)
        title_label = Label(self, text="Song title").grid(row=2, column=1)

        search_button = Button(self, text="Search song", command=search_song_words_desc).grid(row=4, column=2)

        song_words_preview = Text(self, height=15, width=70)
        song_words_preview.grid(row=11, column=2)

        options_words = StringVar()
        options_words.set("Choose word")

        # TODO: use output of find song words then  list = output.split()
        list = ['HTML', 'Tutorial', 'CSS', 'Tutorial', 'JavaScript', 'Tutorial', 'How', 'To', 'Tutorial', 'SQL', 'Tutorial', 'Python', 'Tutorial', 'W3.CSS', 'Tutorial', 'Bootstrap', 'Tutorial', 'PHP', 'Tutorial', 'Java', 'Tutorial', 'C++', 'Tutorial', 'jQuery', 'Tutorial']
        words_menu = OptionMenu(self, options_words, *list, command=set_chosen_word)
        words_menu.grid(row=5, column=2)

        search_word_contexts = Button(self, text="Search word context", command=search_word_context()).grid(row=6, column=2)

class GroupPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        def add_words_to_group():
            to_add = list(song_words.curselection())
            added = list(d_chosen_words.get(0, END))
            for index in to_add:
                if song_words.get(index) not in added:
                    d_chosen_words.insert(END, song_words.get(index))
                    added.insert(len(added), song_words.get(index))

        def remove_words_chosen():
            selected = d_chosen_words.curselection()
            no_words_deleted = 0
            for index in selected:
                d_chosen_words.delete(index-no_words_deleted)
                no_words_deleted += 1

        author_value = StringVar()
        title_value = StringVar()

        home_btn = Button(self, text="Home", command=lambda: controller.show_frame(HomePage)).grid(row=0, column=0)
        page_title_label = Label(self, text="Choose words out of a chosen song/s. Enter the group name you wish to add to/create.").grid(row=0, column=2)

        author_label = Label(self, text="Author:").grid(row=1, column=1)
        title_label = Label(self, text="Song title:").grid(row=2, column=1)
        author_field = Entry(self, textvariable=author_value).grid(row=1, column=2)
        title_field = Entry(self, textvariable=title_value).grid(row=2, column=2)

        song_word_label = Label(self, text="Words of song:").grid(row=3, column=1)
        song_words = Listbox(self)
        song_words.grid(row=4, column=1)
        #############TEST###############
        song_words.insert(END, "discord")
        song_words.insert(END, "presides")
        song_words.insert(END, "in")
        song_words.insert(END, "society")
        #####################################
        add_btn = Button(self, text="Add chosen words", command=add_words_to_group).grid(row=5, column=1)


        d_chosen_words_label= Label(self, text="Words chosen thus far:").grid(row=3, column=2)
        d_chosen_words = Listbox(self)
        d_chosen_words.grid(row=4, column=2)
        d_remove_btn = Button(self, text="Remove chosen words", command=remove_words_chosen).grid(row=5, column=2)

        #TODO add group name field and "add group to database"







app = App()
app.title("Welcome to Songs Database")
app.geometry('1000x700')
app.mainloop()
