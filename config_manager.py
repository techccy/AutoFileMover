import yaml
import os
import logging
from pathlib import Path

class ConfigManager:
    """配置管理器，负责读取和解析YAML配置文件"""
    
    def __init__(self, config_path="config.yaml"):
        self.config_path = config_path
        self.config = {}
        self.logger = logging.getLogger(__name__)
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                self.config = yaml.safe_load(file)
            self.logger.info(f"配置文件加载成功: {self.config_path}")
        except FileNotFoundError:
            self.logger.error(f"配置文件未找到: {self.config_path}")
            raise
        except yaml.YAMLError as e:
            self.logger.error(f"配置文件格式错误: {e}")
            raise
        except Exception as e:
            self.logger.error(f"加载配置文件时发生未知错误: {e}")
            raise
    
    def reload_config(self):
        """重新加载配置文件"""
        self.logger.info("重新加载配置文件")
        self.load_config()
    
    def get(self, key, default=None):
        """获取配置项"""
        keys = key.split('.')
        value = self.config
        try:
            for k in keys:
                value = value[k]
            return value
        except KeyError:
            return default
    
    def get_watch_directory(self):
        """获取监听目录路径"""
        watch_dir = self.get('watch_directory', '~/Downloads')
        return os.path.expanduser(watch_dir)
    
    def get_target_directories(self):
        """获取目标目录映射"""
        targets = self.get('target_directories', {})
        # 展开用户目录
        expanded_targets = {}
        for key, path in targets.items():
            expanded_targets[key] = os.path.expanduser(path)
        return expanded_targets
    
    def get_rules(self):
        """获取文件分类规则"""
        return self.get('rules', [])
    
    def get_default_target(self):
        """获取默认目标目录"""
        return self.get('default_target', 'others')
    
    def get_integrity_check_delay(self):
        """获取文件完整性检查延迟时间"""
        return self.get('integrity_check_delay', 2)
    
    def is_debug_mode(self):
        """检查是否为调试模式"""
        return self.get('debug', False)
    
    def get_log_file(self):
        """获取日志文件路径"""
        log_file = self.get('log_file', 'autofilemover.log')
        return log_file
    
    def is_notification_enabled(self):
        """检查是否启用通知"""
        return self.get('notifications.enabled', True)
    
    def is_sound_enabled(self):
        """检查是否启用声音"""
        return self.get('notifications.sound', True)

# 全局配置管理器实例
config_manager = ConfigManager()