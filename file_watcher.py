import time
import os
import threading
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging

class FileHandler(FileSystemEventHandler):
    """文件事件处理器"""
    
    def __init__(self, callback):
        self.callback = callback
        self.logger = logging.getLogger(__name__)
    
    def on_created(self, event):
        """处理文件创建事件"""
        if not event.is_directory:
            self.logger.debug(f"检测到新文件: {event.src_path}")
            # 在新线程中处理文件，避免阻塞事件处理
            threading.Thread(target=self.callback, args=(event.src_path,), daemon=True).start()
    
    def on_moved(self, event):
        """处理文件移动事件"""
        if not event.is_directory:
            self.logger.debug(f"检测到文件移动: {event.dest_path}")
            # 在新线程中处理文件，避免阻塞事件处理
            threading.Thread(target=self.callback, args=(event.dest_path,), daemon=True).start()

class FileWatcher:
    """文件监听器"""
    
    def __init__(self, watch_directory, file_callback):
        self.watch_directory = watch_directory
        self.file_callback = file_callback
        self.observer = Observer()
        self.logger = logging.getLogger(__name__)
        
        # 确保监听目录存在
        Path(watch_directory).mkdir(parents=True, exist_ok=True)
    
    def start(self):
        """启动文件监听"""
        event_handler = FileHandler(self.file_callback)
        self.observer.schedule(event_handler, self.watch_directory, recursive=False)
        self.observer.start()
        self.logger.info(f"开始监听目录: {self.watch_directory}")
    
    def stop(self):
        """停止文件监听"""
        self.observer.stop()
        self.observer.join()
        self.logger.info("文件监听已停止")