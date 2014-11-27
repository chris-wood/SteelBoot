import sys
import time
import logging
import threading
import os
import Queue
import Tkinter as tk
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

class SteelBootTkView(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        t = SteelBookTkTable(self)
        t.pack(side="top", fill="x")
        t.set(0,0,"Local Files")
        t.set(0,1,"Remote Files")

class SteelBookTkTable(tk.Frame):
    def __init__(self, parent, rows=10, columns=2):
        tk.Frame.__init__(self, parent, background="black")
        self._widgets = []

        # TK label needs to be fancy...
        localLabel = tk.Label(self, text="Local Files", borderwidth=1, width=15)
        localLabel.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        remoteLabel = tk.Label(self, text="Remote Files", borderwidth=1, width=15)
        remoteLabel.grid(row=0, column=1, sticky="nsew", padx=1, pady=1)
        self._widgets.append([localLabel, remoteLabel])

        # for row in range(rows):
        #     current_row = []
        #     for column in range(columns):
        #         label = tk.Label(self, text="%s/%s" % (row, column), 
        #                          borderwidth=0, width=10)
        #         label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
        #         current_row.append(label)
        #     self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

    def setRows(self, values):
        for i in range(1,len(values)):
            

def main(argv):
    path = argv[1] if len(argv) > 1 else '.'
    if (os.path.isdir(path)):
        queue = Queue.Queue()
        monitor = DirectoryMonitor(path, queue)
        monitor.start()

        app = SteelBootTkView()
        app.mainloop()

        try:
            while True:
                event = queue.get(True, None)
                # TODO: do something with the event here
        except Exception, e:
            print >> sys.stderr, str(e)

if __name__ == "__main__":
    main(sys.argv)