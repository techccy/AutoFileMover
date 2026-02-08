import logging
import platform
import os
import subprocess
import sys
from pathlib import Path
import threading
import time

# 尝试导入tkinter
try:
    import tkinter as tk
    from tkinter import messagebox
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    tk = None
    messagebox = None

class NotificationManager:
    """通知管理器，负责显示系统通知"""
    
    def __init__(self, enable_notifications=True, enable_sound=True):
        self.enable_notifications = enable_notifications
        self.enable_sound = enable_sound
        self.logger = logging.getLogger(__name__)
        self.platform = platform.system().lower()
    
    def send_notification(self, title, message, file_path=None):
        """
        发送系统通知
        :param title: 通知标题
        :param message: 通知内容
        :param file_path: 相关文件路径（可选，用于在支持的平台上打开文件）
        """
        if not self.enable_notifications:
            return
        
        try:
            # Windows平台使用tkinter创建带按钮的弹窗
            if self.platform == "windows" and TKINTER_AVAILABLE and file_path:
                # 在新线程中显示弹窗，避免阻塞主线程
                thread = threading.Thread(
                    target=self._show_tkinter_popup, 
                    args=(title, message, file_path),
                    daemon=True
                )
                thread.start()
            else:
                # 使用系统默认通知
                if self.platform == "windows":
                    try:
                        import winsound
                        # 发送系统通知
                        winsound.MessageBeep(winsound.MB_ICONASTERISK)
                        
                        # 使用Windows命令行工具发送通知
                        cmd = f'powershell -Command "New-BurntToastNotification -Text \'{title}\', \'{message}\'"'
                        subprocess.run(cmd, shell=True, capture_output=True)
                    except Exception as e:
                        self.logger.warning(f"使用Windows通知失败: {e}")
                        # 降级到控制台输出
                        print(f"[通知] {title}: {message}")
                else:
                    # 其他平台降级到控制台输出
                    print(f"[通知] {title}: {message}")
            
            self.logger.info(f"发送通知: {title} - {message}")
            
            # 如果启用声音，播放系统声音
            if self.enable_sound:
                self._play_system_sound()
                
        except Exception as e:
            self.logger.error(f"发送通知失败: {e}")
    
    def _show_tkinter_popup(self, title, message, file_path):
        """
        显示tkinter弹窗通知
        :param title: 通知标题
        :param message: 通知内容
        :param file_path: 文件路径
        """
        try:
            # 创建根窗口
            root = tk.Tk()
            root.withdraw()  # 隐藏主窗口
            root.attributes('-topmost', True)  # 置顶显示
            
            # 创建自定义对话框
            dialog = tk.Toplevel(root)
            dialog.title(title)
            dialog.attributes('-topmost', True)
            dialog.resizable(False, False)
            
            # 设置对话框位置（居中）
            dialog_width = 400
            dialog_height = 150
            screen_width = dialog.winfo_screenwidth()
            screen_height = dialog.winfo_screenheight()
            x = (screen_width - dialog_width) // 2
            y = (screen_height - dialog_height) // 2
            dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
            
            # 消息标签
            message_label = tk.Label(dialog, text=message, wraplength=380, justify="left")
            message_label.pack(pady=10, padx=10)
            
            # 按钮框架
            button_frame = tk.Frame(dialog)
            button_frame.pack(pady=10)
            
            # 打开按钮
            open_button = tk.Button(
                button_frame, 
                text="打开文件", 
                command=lambda: self._open_file(file_path, dialog)
            )
            open_button.pack(side="left", padx=5)
            
            # 确定按钮
            ok_button = tk.Button(
                button_frame, 
                text="确定", 
                command=dialog.destroy
            )
            ok_button.pack(side="left", padx=5)
            
            # 8秒后自动关闭对话框
            dialog.after(8000, dialog.destroy)
            
            # 确保对话框获得焦点
            dialog.focus_set()
            dialog.grab_set()
            
            # 运行对话框
            dialog.mainloop()
            
            # 销毁根窗口
            root.destroy()
            
        except Exception as e:
            self.logger.error(f"显示tkinter弹窗失败: {e}")
            # 降级到控制台输出
            print(f"[通知] {title}: {message}")
    
    def _open_file(self, file_path, dialog):
        """
        打开文件
        :param file_path: 文件路径
        :param dialog: 对话框窗口
        """
        try:
            dialog.destroy()  # 关闭对话框
            if sys.platform == "win32":  # Windows
                os.startfile(file_path)
            else:
                subprocess.run(["xdg-open", file_path])
        except Exception as e:
            self.logger.error(f"打开文件失败: {e}")
    
    def _play_system_sound(self):
        """播放系统声音"""
        try:
            if self.platform == "windows":
                import winsound
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            # 其他平台的声音处理可以在这里添加
        except Exception as e:
            self.logger.warning(f"播放系统声音失败: {e}")

# 全局通知管理器实例
notification_manager = NotificationManager()
