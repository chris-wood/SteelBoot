import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

class ChangeEvent(FileSystemEventHandler):
    def on_any_event(self, event):
        print "on_any_event"

    def on_created(self, event):
        print "on_created"

    def on_deleted(self, event):
        print "on_deleted"

    def on_modified(self, event):
        print "on_modified"

    def on_moved(self, event):
        print "on_moved"

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = ChangeEvent()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()