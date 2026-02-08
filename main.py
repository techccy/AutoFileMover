import os
import sys
import logging
import threading
import time
import subprocess
from pathlib import Path

from config_manager import config_manager
from file_watcher import FileWatcher
from file_integrity_checker import FileIntegrityChecker
from rule_engine import RuleEngine
from file_mover import FileMover
from notification_manager import notification_manager
from tray_manager import TrayManager

class AutoFileMover:
    """文件自动转移主程序"""
    
    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # 初始化组件
        self.init_components()
        
        # 初始化状态
        self.running = False
        self.watcher_thread = None
        
        # 初始化系统托盘
        self.tray_manager = TrayManager(
            on_open_config=self.open_config,
            on_reload_config=self.reload_config,
            on_exit=self.stop
        )
    
    def setup_logging(self):
        """设置日志"""
        log_file = config_manager.get_log_file()
        debug_mode = config_manager.is_debug_mode()
        
        # 创建日志目录
        log_path = Path(log_file).parent
        log_path.mkdir(parents=True, exist_ok=True)
        
        # 配置日志格式
        log_level = logging.DEBUG if debug_mode else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def init_components(self):
        """初始化核心组件"""
        # 初始化配置管理器
        self.config_manager = config_manager
        
        # 初始化文件完整性检查器
        check_delay = config_manager.get_integrity_check_delay()
        self.integrity_checker = FileIntegrityChecker(check_delay)
        
        # 初始化规则引擎
        rules = config_manager.get_rules()
        default_target = config_manager.get_default_target()
        self.rule_engine = RuleEngine(rules, default_target)
        
        # 初始化文件移动器
        target_directories = config_manager.get_target_directories()
        self.file_mover = FileMover(target_directories)
        
        # 初始化通知管理器
        enable_notifications = config_manager.is_notification_enabled()
        enable_sound = config_manager.is_sound_enabled()
        self.notification_manager = notification_manager
        self.notification_manager.enable_notifications = enable_notifications
        self.notification_manager.enable_sound = enable_sound
    
    def reload_config(self):
        """重新加载配置"""
        try:
            self.config_manager.reload_config()
            self.init_components()
            
            # 如果正在运行，重启监听器
            if self.running:
                self.restart_watcher()
            
            self.logger.info("配置已重新加载")
            self.notification_manager.send_notification(
                "配置已更新", 
                "AutoFileMover 配置已成功重新加载"
            )
        except Exception as e:
            self.logger.error(f"重新加载配置失败: {e}")
            self.notification_manager.send_notification(
                "配置更新失败", 
                f"重新加载配置时发生错误: {str(e)}"
            )
    
    def open_config(self):
        """打开配置文件"""
        config_path = self.config_manager.config_path
        try:
            if sys.platform == "darwin":  # macOS
                subprocess.run(["open", config_path])
            elif sys.platform == "win32":  # Windows
                os.startfile(config_path)
            else:  # Linux
                subprocess.run(["xdg-open", config_path])
            self.logger.info(f"已打开配置文件: {config_path}")
        except Exception as e:
            self.logger.error(f"打开配置文件失败: {e}")
            self.notification_manager.send_notification(
                "打开配置失败", 
                f"无法打开配置文件: {str(e)}"
            )
    
    def process_new_file(self, file_path):
        """处理新文件"""
        self.logger.info(f"开始处理新文件: {file_path}")
        
        # 检查文件是否完整
        if not self.integrity_checker.wait_for_file_complete(file_path):
            self.logger.warning(f"文件未完整或超时，跳过处理: {file_path}")
            return
        
        # 获取目标分类
        target_category = self.rule_engine.get_target_for_file(file_path)
        
        # 移动文件
        moved_path = self.file_mover.move_file(file_path, target_category)
        
        if moved_path:
            # 发送通知
            filename = os.path.basename(moved_path)
            message = f"文件已移动到: {target_category}\n{filename}"
            
            # 检查是否需要特别通知
            should_notify = self.rule_engine.should_notify(file_path)
            
            if should_notify or self.notification_manager.enable_notifications:
                self.notification_manager.send_notification(
                    "文件已处理", 
                    message,
                    moved_path
                )
        else:
            self.logger.error(f"文件移动失败: {file_path}")
            self.notification_manager.send_notification(
                "文件处理失败", 
                f"无法移动文件: {os.path.basename(file_path)}"
            )
    
    def start_watcher(self):
        """启动文件监听器"""
        watch_directory = self.config_manager.get_watch_directory()
        self.watcher = FileWatcher(watch_directory, self.process_new_file)
        self.watcher.start()
    
    def stop_watcher(self):
        """停止文件监听器"""
        if hasattr(self, 'watcher'):
            self.watcher.stop()
    
    def restart_watcher(self):
        """重启文件监听器"""
        self.stop_watcher()
        self.start_watcher()
    
    def start(self):
        """启动程序"""
        if self.running:
            self.logger.warning("程序已在运行中")
            return
        
        try:
            # 启动文件监听器
            self.start_watcher()
            self.running = True
            
            self.logger.info("AutoFileMover 已启动")
            self.notification_manager.send_notification(
                "AutoFileMover 已启动", 
                f"正在监听目录: {self.config_manager.get_watch_directory()}"
            )
            
            # 创建并运行系统托盘图标
            self.tray_icon = self.tray_manager.create_icon()
            if self.tray_icon:
                # 在新线程中运行系统托盘图标
                tray_thread = threading.Thread(target=self.tray_manager.run, daemon=True)
                tray_thread.start()
                
                # 在当前线程中运行Tk事件循环
                if hasattr(self.notification_manager, 'root') and self.notification_manager.root:
                    self.notification_manager.root.mainloop()
            
        except Exception as e:
            self.logger.error(f"启动程序失败: {e}")
            self.notification_manager.send_notification(
                "启动失败", 
                f"AutoFileMover 启动失败: {str(e)}"
            )
    
    def stop(self):
        """停止程序"""
        if not self.running:
            self.logger.warning("程序未在运行中")
            return
        
        try:
            # 停止文件监听器
            self.stop_watcher()
            self.running = False
            
            # 停止系统托盘
            self.tray_manager.stop()
            
            self.logger.info("AutoFileMover 已停止")
            self.notification_manager.send_notification(
                "AutoFileMover 已停止", 
                "程序已正常退出"
            )
            
            # 退出程序
            sys.exit(0)
            
        except Exception as e:
            self.logger.error(f"停止程序失败: {e}")

def main():
    """主函数"""
    app = AutoFileMover()
    app.start()

if __name__ == "__main__":
    main()
