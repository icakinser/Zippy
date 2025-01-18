import os
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

class FileHandler(FileSystemEventHandler):
    def __init__(self, callback, patterns, min_size):
        super().__init__()
        self.callback = callback
        self.patterns = patterns
        self.min_size = min_size

    def on_created(self, event):
        if not isinstance(event, FileCreatedEvent):
            return
            
        file_path = Path(event.src_path)
        
        # Skip if it's a directory
        if not file_path.is_file():
            return
            
        # Check if file matches any pattern
        if not any(file_path.match(pattern) for pattern in self.patterns):
            return
            
        # Check file size
        try:
            if file_path.stat().st_size < self.min_size:
                return
        except OSError:
            return  # Skip if can't access file
            
        self.callback(str(file_path))

class FolderMonitor(QObject):
    file_found = pyqtSignal(str)
    
    def __init__(self, folder_path, patterns=None, min_size=0):
        super().__init__()
        self.folder_path = str(Path(folder_path))  # Convert to string representation
        self.patterns = patterns or ["*.*"]
        self.min_size = min_size
        self.observer = None
        self.handler = None
        
    def start(self):
        if self.observer:
            return
            
        self.handler = FileHandler(
            lambda f: self.file_found.emit(f),
            self.patterns,
            self.min_size
        )
        
        self.observer = Observer()
        self.observer.schedule(self.handler, self.folder_path, recursive=True)
        
        try:
            self.observer.start()
        except Exception as e:
            print(f"Error starting folder monitor: {e}")
            self.observer = None
    
    def stop(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
