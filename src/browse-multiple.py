import threading
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tinytag import TinyTag, TinyTagException
import json
import os

from BookXMLGenerator import BookXMLGenerator
from directorywatcher import Watcher

def get_anthology(file):
    file_info = TinyTag.get(file.name)
    return str(json.loads(file_info.artist)['anthology'])

def get_book_slug(file):
    file_info = TinyTag.get(file.name)
    return str(json.loads(file_info.artist)['book'])

class BrowseFile(Tk):
    def __init__(self):
        super(BrowseFile, self).__init__()
        self.title("Media files to APK")
        self.minsize(600, 400)
        self.maxsize(1000, 600)

        self.outputdir = "~/" # default APK output
        self.list_audio_files = [] # stores uploaded files with metadata

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
            initialdir="~/",
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
        outputdir = filedialog.askdirectory(initialdir=self.outputdir, title="Select Folder")
        if outputdir != "":
            self.outputdir = outputdir
            self.label2.config(text=self.outputdir)

    def submitbutton(self):
        self.submitbutton = ttk.Button(self.labelFrame, text="Submit", command=self.submit)
        self.submitbutton.grid(column=1, row=4, pady=20)
        self.label3 = ttk.Label(self.labelFrame, anchor=E, justify=LEFT, text="")
        self.label3.grid(column=1, row=5, rowspan=3, padx=10, pady=20)

    def submit(self):
        self.label3.config(text="Build started...")
        print("Build started...")
        threading.Thread(target=self.process).start()
        self.browsebutton.config(state=DISABLED)
        self.outputbutton.config(state=DISABLED)
        self.submitbutton.config(state=DISABLED)

        first_file = self.list_audio_files[0]

        anthology = get_anthology(first_file)
        book_slug = get_book_slug(first_file)

        book_xml_gen = BookXMLGenerator(book_slug, 'audio-only', anthology, self.list_audio_files)
        out_app_def_file_path = book_xml_gen.write_to_app_def_file()

        # get directory to bind mount for audio files
        audio_files_host_dir = os.path.dirname(self.list_audio_files[0].name)

        print(out_app_def_file_path)
        print(audio_files_host_dir)
        print(self.outputdir)

        print("docker run -it --rm -v {}:/audio -v {}:'/root/App Builder/Scripture Apps/Apk Output' -v {}:'/root/App Builder/Scripture Apps/App Projects/AudioBible/AudioBible.appDef' sabaudio".format(audio_files_host_dir, self.outputdir, out_app_def_file_path))
        os.system("docker run -it --rm -v {}:/audio -v {}:'/root/App Builder/Scripture Apps/Apk Output' -v {}:'/root/App Builder/Scripture Apps/App Projects/AudioBible/AudioBible.appDef' sabaudio".format(audio_files_host_dir, self.outputdir, out_app_def_file_path))

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