import os
import shutil
import logging
from pathlib import Path

class FileMover:
    """文件移动器，负责将文件移动到目标目录"""
    
    def __init__(self, target_directories):
        self.target_directories = target_directories
        self.logger = logging.getLogger(__name__)
        
        # 确保所有目标目录都存在
        self._ensure_target_directories_exist()
    
    def _ensure_target_directories_exist(self):
        """确保所有目标目录都存在"""
        for name, path in self.target_directories.items():
            try:
                Path(path).mkdir(parents=True, exist_ok=True)
                self.logger.debug(f"确保目标目录存在: {path}")
            except Exception as e:
                self.logger.error(f"创建目标目录失败 {path}: {e}")
    
    def move_file(self, file_path, target_category):
        """
        将文件移动到目标目录
        返回移动后的文件路径，如果移动失败则返回None
        """
        if not os.path.exists(file_path):
            self.logger.error(f"源文件不存在: {file_path}")
            return None
        
        # 获取目标目录路径
        target_dir = self.target_directories.get(target_category)
        if not target_dir:
            self.logger.error(f"目标目录未定义: {target_category}")
            return None
        
        # 确保目标目录存在
        try:
            Path(target_dir).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.logger.error(f"创建目标目录失败 {target_dir}: {e}")
            return None
        
        # 获取文件名
        filename = os.path.basename(file_path)
        
        # 构建目标文件路径
        target_path = os.path.join(target_dir, filename)
        
        # 处理文件名冲突
        target_path = self._resolve_filename_conflict(target_path)
        
        # 移动文件
        try:
            shutil.move(file_path, target_path)
            self.logger.info(f"文件移动成功: {file_path} -> {target_path}")
            return target_path
        except Exception as e:
            self.logger.error(f"文件移动失败 {file_path} -> {target_path}: {e}")
            return None
    
    def _resolve_filename_conflict(self, target_path):
        """
        解决文件名冲突，通过添加数字后缀
        """
        if not os.path.exists(target_path):
            return target_path
        
        # 分离文件名和扩展名
        base_name, extension = os.path.splitext(target_path)
        counter = 1
        
        # 循环查找可用的文件名
        while True:
            new_path = f"{base_name}_{counter}{extension}"
            if not os.path.exists(new_path):
                return new_path
            counter += 1