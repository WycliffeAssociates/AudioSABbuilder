import threading
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import json
from tinytag import TinyTag, TinyTagException

from src.BookXMLGenerator import BookXMLGenerator
from src.directorywatcher import Watcher


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

        self.outputdir = "/apk" # default APK output
        self.list_audio_files = []    # stores uploaded files with metadata

        self.labelFrame = ttk.LabelFrame(self, text="Open File")
        self.labelFrame.grid(column=0, row=1, padx=50, pady=20)

        self.browsebutton()
        self.submitbutton()
        self.outputbutton()

    def browsebutton(self):
        self.browsebutton = ttk.Button(self.labelFrame, text="Browse Files", command=self.file_dialog)
        self.browsebutton.grid(column=1, row=1)

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

        self.label1 = ttk.Label(self.labelFrame, text="")
        self.label1.configure(text="\n".join(file_names))
        self.label1.grid(column=1, row=2)

    def outputbutton(self):
        self.outputbutton = ttk.Button(self.labelFrame, text="Select Output Folder", command=self.outputdiaglog)
        self.outputbutton.grid(column=3, row=1, padx=10)
        self.label2 = ttk.Label(self.labelFrame, anchor=E, text="(Default: " + self.outputdir + ")")
        self.label2.grid(column=3, row=2, padx=10)

    def outputdiaglog(self):
        outputdir = filedialog.askdirectory(initialdir="\\", title="Select Folder")
        if outputdir != "":
            self.outputdir = outputdir
            self.label2.config(text=self.outputdir)

    def submitbutton(self):
        self.submitbutton = ttk.Button(self.labelFrame, text="Submit", command=self.submit)
        self.submitbutton.grid(column=1, row=4, pady=20)
        self.label3 = ttk.Label(self.labelFrame, anchor=E, justify=LEFT, text="")
        self.label3.grid(column=1, row=5, rowspan=3, padx=10, pady=20)
        self.label3.config(text="Build started...")


    def submit(self):
        print("Build started...")
        threading.Thread(target=self.process).start()
        self.browsebutton.config(state=DISABLED)
        self.outputbutton.config(state=DISABLED)
        self.submitbutton.config(state=DISABLED)

        book_xml_gen = BookXMLGenerator('TIT', 'audio-only', 'NT', self.list_audio_files)
        return book_xml_gen.write_to_app_def_file() # returns the location of the output file

    def process(self):
        watcher = Watcher(self.outputdir)
        watcher.run()
        print("Build completed!")
        self.label3.config(text="Build completed!\nOutput file at: " + watcher.filename)
        self.submitbutton.config(state=NORMAL)
        self.browsebutton.config(state=NORMAL)
        self.outputbutton.config(state=NORMAL)

root = BrowseFile()
root.mainloop()