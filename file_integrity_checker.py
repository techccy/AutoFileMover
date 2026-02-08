import time
import os
import logging

class FileIntegrityChecker:
    """文件完整性检查器"""
    
    def __init__(self, check_delay=2):
        self.check_delay = check_delay
        self.logger = logging.getLogger(__name__)
    
    def is_file_complete(self, file_path):
        """
        检查文件是否完整
        通过在短时间内检查文件大小是否发生变化来判断
        """
        if not os.path.exists(file_path):
            self.logger.debug(f"文件不存在: {file_path}")
            return False
        
        try:
            # 获取初始文件大小
            initial_size = os.path.getsize(file_path)
            self.logger.debug(f"初始文件大小: {initial_size} bytes")
            
            # 等待一段时间
            time.sleep(self.check_delay)
            
            # 再次检查文件大小
            current_size = os.path.getsize(file_path)
            self.logger.debug(f"当前文件大小: {current_size} bytes")
            
            # 如果文件大小没有变化，则认为文件传输完成
            if initial_size == current_size:
                self.logger.debug(f"文件传输完成: {file_path}")
                return True
            else:
                self.logger.debug(f"文件仍在传输中: {file_path}")
                return False
        except OSError as e:
            self.logger.error(f"检查文件完整性时发生错误: {e}")
            return False
        except Exception as e:
            self.logger.error(f"检查文件完整性时发生未知错误: {e}")
            return False
    
    def wait_for_file_complete(self, file_path, max_wait_time=30):
        """
        等待文件传输完成
        返回 True 表示文件完整，False 表示超时或文件不完整
        """
        elapsed_time = 0
        while elapsed_time < max_wait_time:
            if self.is_file_complete(file_path):
                return True
            elapsed_time += self.check_delay
        
        self.logger.warning(f"等待文件完成超时: {file_path}")
        return False