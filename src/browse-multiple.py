from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import json
from tinytag import TinyTag, TinyTagException

from src.BookXMLGenerator import BookXMLGenerator


class AudioFile:
    def __init__(self, filename, anthology, language, version, book, bookNumber, mode, chapter, startv, endv, markers):
        self.filename = filename
        self.languageCode = language
        self.resoureceId = version
        self.bookSlug = book
        self.mode = mode
        self.chapter = chapter
        self.startv = startv
        self.endv = endv
        self.markers = markers


class BrowseFile(Tk):
    def __init__(self):
        super(BrowseFile, self).__init__()
        self.title("Media files to APK")
        self.minsize(600, 400)
        self.maxsize(1000, 600)

        self.list_audio_files = []    # stores uploaded files with metadata

        self.labelFrame = ttk.LabelFrame(self, text="Open File")
        self.labelFrame.grid(column=0, row=1, padx=30, pady=20)

        self.button()
        self.submit_button()

    def button(self):
        self.button = ttk.Button(self.labelFrame, text="Browse Files", command=self.file_dialog)
        self.button.grid(column=1, row=1)

    def file_dialog(self):
        self.list_audio_files = []
        file_names = filedialog.askopenfilenames(
            initialdir="/home/dj/Documents/BibleAudioFiles/tit",
            title="Select Files",
            filetypes= (("Audio files", "*.mp3"), ("all files", "*.*"))
        )

        for file_name in file_names:
            try:
                self.list_audio_files.append(open(file_name))
            except TinyTagException:
                print("Error reading file at " + file_name)

        self.label = ttk.Label(self.labelFrame, text="")
        self.label.configure(text="\n".join(file_names))
        self.label.grid(column=1, row=2)

    def submit_button(self):
        self.submit_button = ttk.Button(self.labelFrame, text="Submit", command=self.submit)
        self.submit_button.grid(column=1, row=3, pady=20)

    def submit(self):
        book_xml_gen = BookXMLGenerator('TIT', 'audio-only', 'NT', self.list_audio_files)
        return book_xml_gen.write_to_app_def_file() # returns the location of the output file

root = BrowseFile()
root.mainloop()