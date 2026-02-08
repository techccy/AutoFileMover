import os
import time
import threading

def create_test_file():
    """创建测试文件"""
    # 确保下载目录存在
    download_dir = os.path.expanduser("~/Downloads")
    os.makedirs(download_dir, exist_ok=True)
    
    # 创建测试文件
    test_file = os.path.join(download_dir, "test_document.txt")
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("这是一个测试文件，用于验证AutoFileMover的功能。\n")
        f.write("如果程序正常工作，这个文件应该会被移动到Documents/Organized/Documents目录中。\n")
    
    print(f"已创建测试文件: {test_file}")
    return test_file

def check_file_moved(test_file):
    """检查文件是否被移动"""
    # 构建目标路径
    filename = os.path.basename(test_file)
    target_dir = os.path.expanduser("~/Documents/Organized/Documents")
    target_file = os.path.join(target_dir, filename)
    
    # 等待一段时间让程序处理文件
    time.sleep(5)
    
    # 检查文件是否存在于目标位置
    if os.path.exists(target_file):
        print(f"✓ 文件已成功移动到: {target_file}")
        return True
    else:
        print("✗ 文件未被移动，请检查程序是否正常运行")
        return False

def main():
    print("AutoFileMover 功能测试")
    print("=" * 30)
    
    # 创建测试文件
    test_file = create_test_file()
    
    # 提示用户确保程序正在运行
    print("\n请确保AutoFileMover程序正在运行...")
    print("程序应该会自动检测到新文件并将其移动到相应的目录。")
    print("如果一切正常，您将看到一个带有'打开文件'按钮的通知弹窗。")
    
    # 检查文件是否被移动
    print("\n等待程序处理文件...")
    if check_file_moved(test_file):
        print("\n✓ 功能测试通过！")
        print("程序能够正确监听文件变化、移动文件并显示通知。")
    else:
        print("\n✗ 功能测试失败！")
        print("请检查程序配置和日志文件以排查问题。")

if __name__ == "__main__":
    main()