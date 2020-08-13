from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from AudioSABbuilder.src.directorywatcher import Watcher
from tinytag import TinyTag, TinyTagException
import json
import threading

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
        self.title("Media file to APK")
        self.minsize(600, 400)
        self.maxsize(1000, 600)

        self.outputdir = "E:\SAB\Output"

        self.labelFrame = ttk.LabelFrame(self, text="Open File")
        self.labelFrame.grid(column=0, row=1, padx=30, pady=20)

        self.browsebutton()
        self.outputbutton()
        self.submitbutton()

    def browsebutton(self):
        self.browsebutton = ttk.Button(self.labelFrame, text="Browse A File", command=self.filedialog)
        self.browsebutton.grid(column=1, row=1)

    def filedialog(self):
        self.filename = filedialog.askopenfilename(initialdir="E:/Downloads/", title="Select A File", filetypes=
        (("Audio files", "*.mp3"), ("all files", "*.*")))
        if self.filename == "":
            return
        self.label1 = ttk.Label(self.labelFrame, text="")
        self.label1.grid(column=1, columnspan=2, row=2, padx=10)
        self.label1.configure(text=self.filename)
        try:
            filetags = TinyTag.get(self.filename)
            json_data = json.loads(filetags.artist)
            self.audiofile = AudioFile(
                self.filename,
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
        except TinyTagException:
            print("Error reading file")

    def outputbutton(self):
        self.outputbutton = ttk.Button(self.labelFrame, text="Select Output Folder", command=self.outputdiaglog)
        self.outputbutton.grid(column=3, row=1, padx=10)
        self.label2 = ttk.Label(self.labelFrame, anchor=E, justify=RIGHT, text="")
        self.label2.grid(column=3, row=2, padx=10)

    def outputdiaglog(self):
        self.outputdir = filedialog.askdirectory(initialdir="E:\SAB\Output", title="Select Folder")
        self.label2.config(text=self.outputdir)
        print(self.outputdir)

    def submitbutton(self):
        self.submitbutton = ttk.Button(self.labelFrame, text="Submit", command=self.submit)
        self.submitbutton.grid(column=1, row=4, pady=20)


    def submit(self):
        print("Build started...")
        # trigger back-end process here
        threading.Thread(target=self.process).start()
        self.submitbutton.config(state=DISABLED)
        self.browsebutton.config(state=DISABLED)
        self.outputbutton.config(state=DISABLED)
        # TODO: run back-end process here


    def process(self):
        watcher = Watcher(self.outputdir)
        watcher.run()
        print("Build completed!")
        self.submitbutton.config(state=NORMAL)
        self.browsebutton.config(state=NORMAL)
        self.outputbutton.config(state=NORMAL)

root = BrowseFile()
root.mainloop()
