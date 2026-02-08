import os
import logging

class RuleEngine:
    """规则引擎，根据配置规则对文件进行分类"""
    
    def __init__(self, rules, default_target):
        self.rules = rules
        self.default_target = default_target
        self.logger = logging.getLogger(__name__)
    
    def get_target_for_file(self, file_path):
        """
        根据文件路径获取目标分类
        返回目标分类名称
        """
        # 获取文件扩展名
        _, extension = os.path.splitext(file_path)
        extension = extension.lower()
        
        self.logger.debug(f"文件: {file_path}, 扩展名: {extension}")
        
        # 遍历规则查找匹配项
        for rule in self.rules:
            extensions = rule.get('extensions', [])
            if extension in extensions:
                target = rule.get('target', self.default_target)
                self.logger.debug(f"匹配规则: {rule.get('name', 'Unknown')}, 目标: {target}")
                return target
        
        # 没有匹配的规则，返回默认目标
        self.logger.debug(f"未匹配任何规则，使用默认目标: {self.default_target}")
        return self.default_target
    
    def should_notify(self, file_path):
        """
        检查是否应该对文件移动发送通知
        """
        # 获取文件扩展名
        _, extension = os.path.splitext(file_path)
        extension = extension.lower()
        
        # 遍历规则查找匹配项
        for rule in self.rules:
            extensions = rule.get('extensions', [])
            if extension in extensions:
                # 检查规则是否要求通知
                return rule.get('notify', False)
        
        return False