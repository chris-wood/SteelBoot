import sys
import time
import logging
import threading
import os
import Queue
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

class ChangeEvent(FileSystemEventHandler):
    def __init__(self, queue):
        self.queue = queue

    def on_any_event(self, event):
        print "on_any_event"
        self.queue.put(event)

    def on_created(self, event):
        print "on_created"
        self.queue.put(event)

    def on_deleted(self, event):
        print "on_deleted"
        self.queue.put(event)

    def on_modified(self, event):
        print "on_modified"
        self.queue.put(event)

    def on_moved(self, event):
        print "on_moved"
        self.queue.put(event)

class DirectoryMonitor(threading.Thread):
    def __init__(self, dirName, queue):  
        threading.Thread.__init__(self)  
        self.dirName = dirName
        self.queue = queue

    def run(self):
        event_handler = ChangeEvent(self.queue)
        observer = Observer()
        observer.schedule(event_handler, self.dirName, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

def main(argv):
    path = argv[1] if len(argv) > 1 else '.'
    if (os.path.isdir(path)):
        queue = Queue.Queue()
        monitor = DirectoryMonitor(path, queue)
        monitor.start()

        try:
            while True:
                event = queue.get(True, None)
                # TODO: do something with the event here
        except Exception, e:
            print >> sys.stderr, str(e)

if __name__ == "__main__":
    main(sys.argv)