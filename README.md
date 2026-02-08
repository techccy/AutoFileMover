# AutoFileMover

[「ENGLISH」](README_EN.md)
一个专为Windows设计的文件自动转移程序，能够监听指定目录并在文件下载完成后根据规则自动分类移动文件。

## 功能特性

- 🎯 **智能监听**：实时监听指定目录的文件变化
- ✅ **完整性检查**：确保文件完全下载后再处理
- 📁 **智能分类**：根据文件类型自动分类移动到相应目录
- 🖥️ **系统托盘**：常驻系统托盘，右键菜单操作
- ⚙️ **灵活配置**：通过YAML配置文件自定义规则
- 🔔 **即时通知**：文件处理完成后发送桌面通知，带"打开文件"按钮
- 🪟 **Windows专用**：专为Windows平台优化设计

## 安装

1. 克隆项目：
```bash
git clone https:\\github.com\techccy\AutoFileMover.git
cd AutoFileMover
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

或者使用pipenv：
```bash
pipenv install
```

## 配置

程序使用 `config.yaml` 文件进行配置：

```yaml
# 监听的目录路径
watch_directory: "E:\Documents\Input"

# 是否启用调试模式
debug: false

# 日志文件路径
log_file: "autofilemover.log"

# 文件完整性检查等待时间（秒）
integrity_check_delay: 2

# 移动后的目标目录
target_directories:
  documents: "E:\Documents\Organized\Documents"
  images: "E:\Documents\Organized\Images"
  videos: "E:\Documents\Organized\Videos"
  music: "E:\Documents\Organized\Music"
  archives: "E:\Documents\Organized\Archives"
  others: "E:\Documents\Organized\Others"

# 文件分类规则
rules:
  - name: "文档文件"
    extensions: [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"]
    target: "documents"
    
  - name: "图片文件"
    extensions: [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"]
    target: "images"
    
  - name: "视频文件"
    extensions: [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"]
    target: "videos"
    
  - name: "音频文件"
    extensions: [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"]
    target: "music"
    
  - name: "压缩文件"
    extensions: [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"]
    target: "archives"
    
  - name: "可执行文件"
    extensions: [".exe", ".msi", ".bat", ".cmd"]
    target: "others"
    notify: true  # 对此类文件移动发送特别通知

# 默认目标目录（未匹配任何规则的文件）
default_target: "others"

# 通知设置
notifications:
  enabled: true
  sound: true
```

## 使用方法

1. 修改 `config.yaml` 配置文件以适应你的需求
2. 运行程序：
```bash
python start.py
```

或者在Windows上双击 `start.bat` 文件。

3. 程序将在系统托盘中运行，右键点击图标可：
   - **打开配置**：打开配置文件进行编辑
   - **刷新配置**：重新加载配置文件（无需重启程序）
   - **停止工作**：退出程序

## 系统托盘菜单

- **打开配置**：快速打开YAML配置文件进行编辑
- **刷新配置**：重新加载配置文件，使更改立即生效
- **停止工作**：安全退出程序

## 通知功能

程序会在文件处理完成后发送桌面通知，通知窗口包含：
- 文件处理结果信息
- "打开文件"按钮，可直接访问处理后的文件
- "确定"按钮关闭通知
- 8秒后自动关闭

## 开发

### 项目结构

```
AutoFileMover\
├── start.py                  # 程序启动脚本
├── start.bat                 # Windows批处理启动文件
├── main.py                   # 主程序入口
├── config_manager.py         # 配置管理器
├── file_watcher.py           # 文件监听器
├── file_integrity_checker.py # 文件完整性检查器
├── rule_engine.py            # 规则引擎
├── file_mover.py             # 文件移动器
├── notification_manager.py   # 通知管理器
├── tray_manager.py           # 系统托盘管理器
├── config.yaml               # 配置文件
├── requirements.txt          # 依赖列表
├── test_functionality.py     # 功能测试脚本
├── build_windows_exe.bat     # Windows打包脚本
├── README.md                 # 说明文档
└── LICENSE                   # 许可证文件
```

### 添加新的文件分类规则

在 `config.yaml` 的 `rules` 部分添加新的规则：

```yaml
  - name: "新文件类型"
    extensions: [".ext1", ".ext2"]
    target: "target_category"
    notify: true  # 可选，对此类文件移动发送通知
```

## 打包为Windows可执行文件

要将程序打包为Windows可执行文件(.exe)，请按照以下步骤操作：

### 方法一：使用PyInstaller命令行（推荐）

1. 安装PyInstaller：
```bash
pip install pyinstaller
```

2. 运行打包命令：
```bash
pyinstaller --onefile --windowed ^
    --name AutoFileMover ^
    --add-data "config.yaml;." ^
    --add-data "icons;icons" ^
    --add-data "README.md;." ^
    --hidden-import tkinter ^
    --hidden-import tkinter.messagebox ^
    --hidden-import PIL ^
    --hidden-import yaml ^
    --hidden-import watchdog ^
    --hidden-import pystray ^
    start.py
```

3. 打包完成后，可在`dist`目录中找到`AutoFileMover.exe`文件。

### 方法二：使用批处理脚本

直接运行项目中的`build_windows_exe.bat`脚本，它会自动完成上述步骤。

## 部署到其他Windows计算机

将以下文件复制到目标计算机即可运行：

1. `dist\AutoFileMover.exe` - 主程序
2. `config.yaml` - 配置文件（可根据需要修改）
3. `start.bat` - 启动脚本（可选）

注意：目标计算机需要有Python环境才能运行某些功能，建议安装完整的Python发行版。


## 许可证

本项目采用MIT许可证，详情请见 [LICENSE](LICENSE) 文件。
