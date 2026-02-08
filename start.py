import sys
import os
import threading
import time

# 将当前目录添加到Python路径中
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_autofilemover():
    """在单独的线程中运行AutoFileMover"""
    from main import AutoFileMover
    app = AutoFileMover()
    app.start()

if __name__ == "__main__":
    # 在新线程中运行AutoFileMover
    autofilemover_thread = threading.Thread(target=run_autofilemover, daemon=True)
    autofilemover_thread.start()
    
    # 保持主线程活跃
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("程序已退出")
