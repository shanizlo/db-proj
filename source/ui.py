from tkinter import *
from tkinter import filedialog, Canvas

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame

from helpers_db import *
import csv
import matplotlib.pyplot as plt

class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        # Setup Frame
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        #  Important when adding a frame
        for F in (HomePage, StatisticsPage, ShowWordsInSongPage, UploadSongPage, ShowWordByPlace, ShowContext, GroupPage
                  , ShowGroupPage, PhraseFromText, UploadDatasetPage, ShowAllWords, ShowAllSongs):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(HomePage)

    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()

        if context == HomePage:
            frame.on_focus()


class HomePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        b_width = 15
        b_padx = 2
        b_pady = 4
        first_row = 2
        second_row = 3
        third_row = 4
        fourth_row = 5
        fifth_row = 6
        six_row = 7

        page_title_label = Label(self, text="Project by Shani Zlotnik & Daniel Meriaz", fg='orange').grid(row=first_row, column=2, padx=10, pady=10)
        self.totalSongsText = StringVar()
        self.totalAuthorsText = StringVar()
        self.totalWordsText = StringVar()
        self.total_songs_num_label = Label(self, textvariable=self.totalSongsText, background='orange', width=25, fg='white').grid(row=second_row, column=1, padx=b_padx, pady=b_pady)
        total_authors_num_label = Label(self, textvariable=self.totalAuthorsText, background='orange', width=25, fg='white').grid(row=second_row, column=2, padx=b_padx, pady=b_pady)
        total_words_num_label = Label(self, textvariable=self.totalWordsText, background='orange', width=25, fg='white').grid(row=second_row, column=3, padx=b_padx, pady=b_pady)

        page_upload_btn = Button(self, text="Upload Song", width=b_width, command=lambda: controller.show_frame(UploadSongPage)).grid(row=third_row, column=1, padx=b_padx, pady=b_pady)
        page_upload_csv_btn = Button(self, text="Upload songs dataset", width=b_width, command=lambda: controller.show_frame(UploadDatasetPage)).grid(row=third_row, column=2, padx=b_padx, pady=b_pady)
        page_show_all_words_in_db = Button(self, text="Show all Words in DB", width=b_width,command=lambda: controller.show_frame(ShowAllWords)).grid(row=third_row, column=3, padx=b_padx, pady=b_pady)

        page_show_words_btn = Button(self, text="Show Words in Song", width=b_width, command=lambda: controller.show_frame(ShowWordsInSongPage)).grid(row=fourth_row, column=1, padx=b_padx, pady=b_pady)
        find_word_btn = Button(self, text="Find Word", width=b_width, command=lambda: controller.show_frame(ShowWordByPlace)).grid(row=fourth_row, column=2, padx=b_padx, pady=b_pady)
        word_context_btn = Button(self, text="Show Context", width=b_width, command=lambda: controller.show_frame(ShowContext)).grid(row=fourth_row, column=3, padx=b_padx, pady=b_pady)

        add_group_btn = Button(self, text="Add a/to group", width=b_width, command=lambda: controller.show_frame(GroupPage)).grid(row=fifth_row, column=1, padx=b_padx, pady=b_pady)
        group_words_btn = Button(self, text="Show words in group", width=b_width, command=lambda: controller.show_frame(ShowGroupPage)).grid(row=fifth_row, column=2, padx=b_padx, pady=b_pady)
        phrase_from_dropdown_btn = Button(self, text="Make phrase", width=b_width, command=lambda: controller.show_frame(PhraseFromText)).grid(row=fifth_row, column=3, padx=b_padx, pady=b_pady)

        page_stats_btn = Button(self, text="Statistics", width=b_width, command=lambda: controller.show_frame(StatisticsPage)).grid(row=six_row, column=1, padx=b_padx, pady=b_pady)
        show_all_songds_btn = Button(self, text="Show all songs", width=b_width, command=lambda: controller.show_frame(ShowAllSongs)).grid(row=six_row, column=2, padx=b_padx, pady=b_pady)

    def on_focus(self):
        global needRedrawHome
        if needRedrawHome:
            self.showGraph()
            self.totalSongsText.set(f"Total number of songs in DB: {getCountOfAllSongs()[0]}")
            self.totalAuthorsText.set(f"Total number of authors in DB: {getCountOfAllAuthors()[0]}")
            self.totalWordsText.set(f"Total number of words in DB: {getCountOfAllWords()[0]}")
            needRedrawHome = False

    def showGraph(self):
        # Graph
        top10 = getTop10SongsAndValues()
        if top10 is None:
            return
        top10songs = top10[0]
        top10count = top10[1]

        data1 = {'The song': top10songs, 'Num of words': top10count}
        df1 = DataFrame(data1, columns=['Num of words', 'The song'])

        figure1 = plt.Figure(figsize=(10, 11), dpi=80)
        plt.tight_layout()
        plt.rcParams["figure.autolayout"] = True
        figure1.autofmt_xdate(rotation=45)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, self)
        bar1.get_tk_widget().grid(row=73, columnspan=4)
        df1 = df1.sort_values('Num of words')
        df1.plot('The song', kind='bar', legend=True, ax=ax1, color='orange')
        ax1.set_title('Words per song - top 10')


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
            message = insert_into_database(author_info, title_info, album_info, copyright_info, song_lyrics)
            global needRedrawHome
            needRedrawHome = True
            self.submittedMessage = StringVar()
            messageLabel = Label(self, textvariable=self.submittedMessage, fg='green').grid(row=12, column=2, padx=10, pady=10)
            if isinstance(message, int):
                successMessage = Label(self, text=f"Your song is saved successfully! Song id is {message}", fg='green').grid(row=12, column=2, padx=10, pady=10)
            else:
                song_text_preview.delete("1.0", "end")
                song_text_preview.insert(END, f"Error saving your song! {message}")

        def open_file():
            text_file = filedialog.askopenfile(initialdir="/gui/images", title="Select a text file with song lyrics",
                                               filetypes=[("txt files", "*.txt")])
            filename_text = Text(self, height=3, width=70)
            filename_text.grid(row=5, column=2)

            filename_text.delete("1.0", "end")
            song_text_preview.delete("1.0", "end")

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

class UploadDatasetPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        page_title_label = Label(self, text="Upload Csv").grid(row=0, column=2)
        filename_label = Label(self, text="CSV File:").grid(row=5, column=1)
        song_value = StringVar()
        open_file_button = Button(self, text="Browse file...", command=self.open_file).grid(row=6, column=2)
        save_button = Button(self, text="Save dataset", command=self.submit_values).grid(row=11, column=2)
        home_button = Button(self, text="Home", command=lambda: controller.show_frame(HomePage)).grid(row=0, column=0)

    def submit_values(self):
        global needRedrawHome
        file = open(self.dataset_file.name)
        csvreader = csv.reader(file)
        header = next(csvreader)
        print(header)
        addedCounter = 0
        for row in csvreader:
            author = row[0]
            title = row[1]
            lyrics = row[2]
            if author and title and lyrics:
                insert_into_database(title, author, "", "", lyrics)
                addedCounter = addedCounter + 1
        Label(self, text=f"Successfully submitted {addedCounter} songs to DB", fg='green').grid(row=10, column=2)
        file.close()
        needRedrawHome = True

    def open_file(self):
        self.dataset_file = filedialog.askopenfile(initialdir="/gui/images", title="Select a csv file with song lyrics dataset",
                                           filetypes=[("csv files", "*.csv")])
        filename_text = Text(self, height=3, width=70)
        filename_text.grid(row=5, column=2)

        filename_text.delete("1.0", "end")

        filename_text.insert(END, self.dataset_file.name)
        print(self.dataset_file.name)

class StatisticsPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        page_title_label = Label(self, text="Statistics").grid(row=0, column=2)
        home_button = Button(self, text="Home", command=lambda: controller.show_frame(HomePage)).grid(row=0, column=0)

        # all variables pertaining to the different fields in the page #
        author_value = StringVar()
        title_value = StringVar()
        num_words_in_song_value = IntVar()
        avg_chars_in_sentence_value = DoubleVar()
        avg_chars_in_verse_value = DoubleVar()
        output_message = StringVar()

        # all parts
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

        output_message_label = Label(self, textvariable=output_message).grid(row=6, column=2)
        def show_statistics():
            author = author_value.get()
            title = title_value.get()
            if stringOk(author) and stringOk(title):
                output = StatisticsOutput(author, title)
                if output is not None:  # song found
                    num_words_in_song_value.set(output[0])
                    avg_chars_in_sentence_value.set(output[1])
                    avg_chars_in_verse_value.set(output[2])
                    song_id = output[3]
                    output_message.set("Found your wanted song.")

                    # Graph
                    top10 = getTop10Words(song_id)
                    top10songs = top10[0]
                    top10count = top10[1]

                    data1 = {'words': top10songs, 'Num of words': top10count}
                    df1 = DataFrame(data1, columns=['Num of words', 'words'])

                    figure1 = plt.Figure(figsize=(8, 8), dpi=80)
                    plt.tight_layout()
                    plt.rcParams["figure.autolayout"] = True
                    figure1.autofmt_xdate(rotation=45)
                    ax1 = figure1.add_subplot(111)
                    bar1 = FigureCanvasTkAgg(figure1, self)
                    bar1.get_tk_widget().grid(row=73, columnspan=4)
                    df1 = df1.sort_values('Num of words')
                    df1.plot('words', kind='bar', legend=True, ax=ax1, color='green')
                    ax1.set_title('Words per this song - top 10')

                else:  # song not found
                    output_message.set("Unable to find the wanted song.")
            else:  # input was bad
                output_message.set("Please type valid input (nothing empty).")

        statistics_button = Button(self, text="Show statistics", command=show_statistics).grid(row=3, column=2)

class ShowWordsInSongPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        page_title_label = Label(self, text="Show Words in Song").grid(row=0, column=2)
        home_button = Button(self, text="Home", command=lambda: controller.show_frame(HomePage)).grid(row=0, column=0)

        self.author_value = StringVar()
        self.title_value = StringVar()

        self.author_field = Entry(self, textvariable=self.author_value).grid(row=1, column=2)
        self.title_field = Entry(self, textvariable=self.title_value).grid(row=2, column=2)
        self.author_label = Label(self, text="Author").grid(row=1, column=1)
        self.title_label = Label(self, text="Song title").grid(row=2, column=1)

        search_button = Button(self, text="Search song", command=self.search_song_words_desc).grid(row=11, column=2)

        self.song_words_preview = Text(self, height=15, width=70)
        self.song_words_preview.grid(row=7, column=2)

    def search_song_words_desc(self):
        self.song_words_preview.delete("1.0", "end")
        author = self.author_value.get()
        title = self.title_value.get()
        print("searching for song words for author {}, title {}".format(author, title))
        song_words = SearchSongWords(author, title)
        self.song_words_preview.insert(END, song_words)

class ShowAllWords(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        page_title_label = Label(self, text="Show All Words in DB").grid(row=0, column=2)
        home_button = Button(self, text="Home", command=lambda: controller.show_frame(HomePage)).grid(row=0, column=0)

        show_button = Button(self, text="Show words sorted A-Z", command=self.search_all_words_asc_az).grid(row=3, column=2)
        show_button = Button(self, text="Show words sorted by count of appearence", command=self.search_all_words_desc_count).grid(row=3, column=5)

        self.all_words_preview_az = Text(self, height=60, width=30)
        self.all_words_preview_az.grid(row=7, column=2)

        self.all_words_preview_count = Text(self, height=60, width=30)
        self.all_words_preview_count.grid(row=7, column=5)

    def search_all_words_asc_az(self):
        self.all_words_preview_az.delete("1.0", "end")
        print("searching for all words")
        all_words = getAllwordsInDbAscAz()
        self.all_words_preview_az.insert(END, all_words)

    def search_all_words_desc_count(self):
        self.all_words_preview_count.delete("1.0", "end")
        print("searching for all words")
        all_words = getAllwordsInDbDescCount()
        self.all_words_preview_count.insert(END, all_words)

class ShowAllSongs(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        page_title_label = Label(self, text="Show All Songs in DB").grid(row=0, column=2)
        home_button = Button(self, text="Home", command=lambda: controller.show_frame(HomePage)).grid(row=0, column=0)

        show_button = Button(self, text="Show songs sorted by title", command=self.search_all_songs, width=25).grid(row=3, column=2)
        show_button = Button(self, text="Show songs sorted by author name", command=self.search_all_songs_by_author, width=25).grid(row=4, column=2)
        show_button = Button(self, text="Show songs sorted by count of words", command=self.search_all_songs_by_count, width=25).grid(row=5, column=2)

        self.all_songs_preview = Text(self, height=60, width=80)
        self.all_songs_preview.grid(row=8, column=2, pady=5)

    def search_all_songs(self):
        self.all_songs_preview.delete("1.0", "end")
        print("searching for all songs")
        all_songs = getAllSongsInDbByTitle()
        self.all_songs_preview.insert(END, all_songs)

    def search_all_songs_by_author(self):
        self.all_songs_preview.delete("1.0", "end")
        print("searching for all songs")
        all_songs = getAllSongsByAuthor()
        self.all_songs_preview.insert(END, all_songs)

    def search_all_songs_by_count(self):
        self.all_songs_preview.delete("1.0", "end")
        print("searching for all songs")
        all_songs = getAllSongsByCount()
        self.all_songs_preview.insert(END, all_songs)

class ShowWordByPlace(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        def search_word():
            found_word_preview.delete("1.0", "end")
            author = author_value.get()
            title = title_value.get()
            verse = verse_num.get()
            line = line_value.get()
            word_pos = word_num_value.get()
            word_found = SearchWordByPositionInSong(author, title, verse, line, word_pos)
            found_word = word_found
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

        search_button = Button(self, text="Search word", command=search_word).grid(row=11, column=2)

        found_word_preview = Text(self, height=1, width=70)
        found_word_preview.grid(row=12, column=2)


class ShowContext(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.list_found_words = []

        self.page_title_label = Label(self, text="Show Context of Word. Search for song, then choose the word to show context for.").grid(row=0, column=2)
        home_button = Button(self, text="Home", command=lambda: controller.show_frame(HomePage)).grid(row=0, column=0)

        self.author_value = StringVar()
        self.title_value = StringVar()

        self.author_field = Entry(self, textvariable=self.author_value).grid(row=1, column=2)
        self.title_field = Entry(self, textvariable=self.title_value).grid(row=2, column=2)
        self.author_label = Label(self, text="Author").grid(row=1, column=1)
        self.title_label = Label(self, text="Song title").grid(row=2, column=1)

        self.search_button = Button(self, text="Search song", command=self.search_song_words_desc).grid(row=4, column=2)

        self.context_preview = Text(self, height=30, width=100)
        self.context_preview.grid(row=11, column=2)

        self.options_words = StringVar()
        self.options_words.set("Choose word")

        self.list = [""]
        self.words_menu = OptionMenu(self, self.options_words, self.list, command=self.set_chosen_word)
        self.words_menu.grid(row=5, column=2)
        self.choice = ""

        self.search_word_contexts = Button(self, text="Search word context", command=self.search_word_context).grid(row=6, column=2)

    def set_chosen_word(self, opt):
        self.choice = opt
        print(self.choice)

    def search_word_context(self):
        self.context_preview.delete("1.0", "end")
        author = self.author_value.get()
        title = self.title_value.get()
        # to avoid crash at first init:
        if (author == "" or title == ""):
            self.context_preview.insert(INSERT, """Search for song and then choose word to show its context""")
        else:
            context_found = ReturnWordContext(author, title, self.choice)
            print(context_found)
            self.context_preview.insert(INSERT, context_found)

    def search_song_words_desc(self):
        # TODO - add errors handling (in case song not found, etc)
        self.context_preview.delete("1.0", "end")
        author = self.author_value.get()
        title = self.title_value.get()
        if author == "" or title == "":
            self.context_preview.insert(INSERT, "Please enter author and title.")
        found_words = SearchSongWordsOrReturnNone(author, title)
        if found_words == None:
            self.context_preview.insert(INSERT, "Song with this author and title not found.")
        else:
            self.context_preview.insert(INSERT,
                                   """Choose word from the dropdown and then click "Search word context" button.""")
            list_found_words = found_words
            words_menu = OptionMenu(self, self.options_words, *list_found_words, command=self.set_chosen_word)
            words_menu.grid(row=5, column=2)


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

        def get_words_from_input():
            # first remove the stuff that is already there
            song_words.delete(0, END)
            # now add from input the song words
            song_words_list = SearchSongWords(author_value.get(), title_value.get()).split('\n')
            if song_words_list[0] == "Song with this title and author not found.":
                input_checker_text.set("Song with this title and author not found.")
            else:
                for w in song_words_list:
                    song_words.insert(END, w)

        def group_ui_into_db():
            if group_name_str.get() is None or group_name_str.get() == "" or d_chosen_words.size() == 0:
                input_checker_text.set("Please enter valid group name and choose at least one word.")
            else:
                words = [d_chosen_words.get(i) for i in range(d_chosen_words.size())]
                if From_UI_Into_Group(group_name_str.get().lower(), words):
                    input_checker_text.set("Inserted the words successfully into the existing group.")
                else:
                    input_checker_text.set("Created a new group with these given words.")

        # author and title strings #
        author_value = StringVar()
        title_value = StringVar()

        # home button and title label #
        home_btn = Button(self, text="Home", command=lambda: controller.show_frame(HomePage)).grid(row=0, column=0)
        page_title_label = Label(self, text="Choose words out of a chosen song/s. Enter the group name you wish to add to/create.").grid(row=0, column=1)

        # all that has to do with author and title #
        author_label = Label(self, text="Author:").grid(row=1, column=0)
        title_label = Label(self, text="Song title:").grid(row=2, column=0)
        author_field = Entry(self, textvariable=author_value).grid(row=1, column=1)
        title_field = Entry(self, textvariable=title_value).grid(row=2, column=1)

        # all that has to do with the words of song that is inputted from the user #
        find_song_words_btn = Button(self, text="Find song words", command=get_words_from_input).grid(row=3, column=1)
        song_word_label = Label(self, text="Words of song:").grid(row=4, column=0)
        song_words = Listbox(self, selectmode="multiple")
        song_words.grid(row=5, column=0)

        add_btn = Button(self, text="Add chosen words", command=add_words_to_group).grid(row=6, column=0)

        # all that has to do with the words chosen to be added to the group #
        d_chosen_words_label = Label(self, text="Words chosen thus far:").grid(row=4, column=1)
        d_chosen_words = Listbox(self, selectmode="multiple")
        d_chosen_words.grid(row=5, column=1)
        d_remove_btn = Button(self, text="Remove chosen words", command=remove_words_chosen).grid(row=6, column=1)

        # all that has to do with the group definition #
        group_name_str = StringVar()
        group_name_label = Label(self, text="Group name:").grid(row=7, column=0)
        group_name_field = Entry(self, textvariable=group_name_str).grid(row=7, column=1)
        add_group_btn = Button(self, text="Add words to given group", command=group_ui_into_db).grid(row=8, column=0)

        # input checker #
        input_checker_text = StringVar()
        input_checker_label = Label(self, textvariable=input_checker_text).grid(row=8, column=1)


class ShowGroupPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        def get_group():
            group_words_preview.delete(1.0, END)
            if group_name_value.get() is None or group_name_value.get() == "":
                output_label_str.set("Invalid group name.")
            else:
                words_in_group = Get_All_Indices_From_Words_In_Group(group_name_value.get().lower())
                if words_in_group is None:
                    output_label_str.set("Group with this name not found.")
                elif words_in_group == 0:
                    output_label_str.set("No songs in database.")
                else:
                    words_in_group = sorted(words_in_group)
                    for w in words_in_group:
                        group_words_preview.insert(END,  "Found word \"" + w[2] + "\" in song " + w[0] + " by " + w[1]
                                                   + " at verse " + str(w[3]) + " in sentence " + str(w[4]) +
                                                   " at position " + str(w[5]) + ".\n")
                    output_label_str.set("The words in the group in all their places in all songs:")

        # Page definitions #
        home_btn = Button(self, text="Home", command=lambda: controller.show_frame(HomePage)).grid(row=0, column=0)
        page_title_label = Label(self,
                                 text="Input the name of the group and this'll show you the words in it.").grid(
            row=0, column=1)

        # Group entry and button #
        group_name_value = StringVar()
        group_name_label = Label(self, text="Group name:").grid(row=1, column=0)
        group_entry = Entry(self, textvariable=group_name_value).grid(row=1, column=1)
        check_group = Button(self, text="Find group", command=get_group).grid(row=1, column=2)

        # output gotten or not label #
        output_label_str = StringVar()
        output_label = Label(self, textvariable=output_label_str).grid(row=2, column=1)
        # words in the group preview
        group_words_preview = Text(self, height=20, width=70)
        group_words_preview.grid(row=7, column=1)

class PhraseFromText(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Page definitions #
        self.home_btn = Button(self, text="Home", command=lambda: controller.show_frame(HomePage)).grid(row=0, column=0)
        self.page_title_label = Label(self,
                                      text="Highlight words out of a given song/s to create a new phrase.").grid(
            row=0, column=1)

        # author and title strings #
        self.author_value = StringVar()
        self.title_value = StringVar()

        # all that has to do with author and title #
        self.author_label = Label(self, text="Author:").grid(row=1, column=0)
        self.title_label = Label(self, text="Song title:").grid(row=2, column=0)
        self.author_field = Entry(self, textvariable=self.author_value).grid(row=1, column=1)
        self.title_field = Entry(self, textvariable=self.title_value).grid(row=2, column=1)

        self.song_text_btn = Button(self, text="Find song", command=self.get_song_words).grid(row=3, column=1)
        self.song_txt = Text(self, height=30, width=100)
        self.song_txt.grid(row=4, column=1)
        self.song_txt.config(state='disabled')

    def get_song_words(self):
        lyrics = Deparse(self.author_value.get().lower(), self.title_value.get().lower())
        self.song_txt.config(state='normal')
        self.song_txt.delete(1.0, END)
        if lyrics is not None:
            self.song_txt.insert(INSERT, lyrics)
        else:
            self.song_txt.insert(INSERT, "No such song was found or the input was bad.")
        self.song_txt.config(state='disabled')


class PhraseFromDropdown(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Page definitions #
        self.home_btn = Button(self, text="Home", command=lambda: controller.show_frame(HomePage)).grid(row=0, column=0)
        self.page_title_label = Label(self,
                                 text="Choose words out of a given song/s to create a new phrase.").grid(
            row=0, column=1)

        # author and title strings #
        self.author_value = StringVar()
        self.title_value = StringVar()

        # all that has to do with author and title #
        self.author_label = Label(self, text="Author:").grid(row=1, column=0)
        self.title_label = Label(self, text="Song title:").grid(row=2, column=0)
        self.author_field = Entry(self, textvariable=self.author_value).grid(row=1, column=1)
        self.title_field = Entry(self, textvariable=self.title_value).grid(row=2, column=1)

        # all that has to do with the words of song that is inputted from the user #
        self.find_song_words_btn = Button(self, text="Find song words", command=self.get_words_from_input).grid(row=3, column=1)
        self.song_word_label = Label(self, text="Words of song:").grid(row=4, column=0)
        self.song_words = Listbox(self)
        self.song_words.grid(row=5, column=0)

        self.add_btn = Button(self, text="Add chosen words", command=self.add_words_to_phrase).grid(row=6, column=0)

        # all that has to do with the words chosen to be added to the group #
        self.d_chosen_words_label = Label(self, text="Words chosen thus far:").grid(row=4, column=1)
        self.d_chosen_words = Listbox(self, selectmode="multiple")
        self.d_chosen_words.grid(row=5, column=1)
        self.d_remove_btn = Button(self, text="Remove chosen words", command=self.remove_words_chosen).grid(row=6, column=1)

        # all that has to do with the phrase definition #
        self.phrase_name_str = StringVar()
        self.phrase_name_label = Label(self, text="Phrase name:").grid(row=7, column=0)
        self.phrase_name_field = Entry(self, textvariable=self.phrase_name_str).grid(row=7, column=1)
        self.phrase_btn = Button(self, text="Add words to given phrase", command=self.phrase_ui_into_db).grid(row=8, column=0)

        # input checker #
        self.input_checker_text = StringVar()
        self.input_checker_label = Label(self, textvariable=self.input_checker_text).grid(row=8, column=1)

    def add_words_to_phrase(self):
        to_add = list(self.song_words.curselection())
        added = list(self.d_chosen_words.get(0, END))
        for index in to_add:
            if self.song_words.get(index) not in added:
                self.d_chosen_words.insert(END, self.song_words.get(index))
                added.insert(len(added), self.song_words.get(index))
        self.song_words.selection_clear(0, END)

    def remove_words_chosen(self):
        selected = self.d_chosen_words.curselection()
        no_words_deleted = 0
        for index in selected:
            self.d_chosen_words.delete(index - no_words_deleted)
            no_words_deleted += 1

    def get_words_from_input(self):
        # first remove the stuff that is already there
        self.song_words.delete(0, END)
        # now add from input the song words
        song_words_list = SearchSongWords(self.author_value.get(), self.title_value.get()).split('\n')
        if song_words_list[0] == "Song with this title and author not found.":
            self.input_checker_text.set("Song with this title and author not found.")
        else:
            for w in song_words_list:
                self.song_words.insert(END, w)

    def phrase_ui_into_db(self):
        if (not stringOk(self.phrase_name_str.get())) or self.d_chosen_words.size() == 0:
            self.input_checker_text.set("Please enter valid phrase name and choose at least one word.")
        else:
            words = [self.d_chosen_words.get(i) for i in range(self.d_chosen_words.size())]
            if From_UI_Into_Phrase(self.phrase_name_str.get().lower(), words):
                self.input_checker_text.set("Inserted the words successfully into a new phrase, namely")
            else:
                self.input_checker_text.set("Phrase with this name already exists and hence nothing was saved.")

global needRedrawHome
needRedrawHome = True
app = App()
app.title("Welcome to Songs Database")
app.geometry('900x900')
# app.geometry('1000x700')
app.mainloop()
