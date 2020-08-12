from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import json
from tinytag import TinyTag, TinyTagException


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

        self.listAudioFiles = []    # stores uploaded files with metadata

        self.labelFrame = ttk.LabelFrame(self, text="Open File")
        self.labelFrame.grid(column=0, row=1, padx=30, pady=20)

        self.button()
        self.submitbutton()

    def button(self):
        self.button = ttk.Button(self.labelFrame, text="Browse Files", command=self.filedialog)
        self.button.grid(column=1, row=1)

    def filedialog(self):
        fileNames = filedialog.askopenfilenames(initialdir="E:/Downloads/", title="Select Files", filetypes=
        (("Audio files", "*.mp3"), ("all files", "*.*")))

        for file in fileNames:
            try:
                fileinfo = TinyTag.get(file)
                json_data = json.loads(fileinfo.artist)
                audiofile = AudioFile(
                    file,
                    json_data["anthology"],
                    json_data["language"],
                    json_data["version"],
                    json_data["book"],
                    json_data["book_number"],
                    json_data["mode"],
                    json_data["chapter"],
                    json_data["startv"],
                    json_data["endv"],
                    json_data["markers"]
                )
                self.listAudioFiles.append(audiofile)
            except TinyTagException:
                print("Error reading file at " + file)

        self.label = ttk.Label(self.labelFrame, text="")
        self.label.configure(text="\n".join(fileNames))
        self.label.grid(column=1, row=2)

    def submitbutton(self):
        self.submitbutton = ttk.Button(self.labelFrame, text="Submit", command=self.submit)
        self.submitbutton.grid(column=1, row=3, pady=20)

    def submit(self):
        # trigger back-end process here
        return self.listAudioFiles

root = BrowseFile()
root.mainloop()