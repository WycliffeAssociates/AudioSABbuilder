import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class Watcher():

    def __init__(self, dir):
        self.observer = Observer()
        self.DIRECTORY_TO_WATCH = dir

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while not(Handler.isUpdated):
                time.sleep(1)
        except:
            self.observer.stop()
            print("Error")

        self.observer.stop()

class Handler(PatternMatchingEventHandler):
    patterns = ["*.apk"]
    isUpdated = False

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("File created: %s.", event.src_path)
            Handler.isUpdated = True


        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print("File modified: %s.", event.src_path)
            Handler.isUpdated = True
