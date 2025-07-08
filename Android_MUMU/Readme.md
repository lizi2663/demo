# 雷电模拟器快手自动化脚本

合法自动化工具，用于教育和研究目的。

## 功能特性

### 核心模块
1. **MemuAutomation类** - 雷电模拟器连接管理
   - `start_memu()` - 启动模拟器
   - `is_memu_running()` - 检查运行状态
   - `find_window()` - 查找模拟器窗口

2. **ImageRecognition类** - OpenCV图像识别
   - `find_image_on_screen()` - 屏幕图像查找
   - `wait_for_image()` - 等待图像出现

3. **KuaishouAutomation类** - 快手自动化操作
   - `open_kuaishou()` - 打开快手应用
   - `scroll_videos()` - 滚动浏览视频
   - `like_video()` - 自动点赞
   - `auto_interact()` - 智能互动

### 高级特性
- **配置管理** - 支持JSON配置文件
- **日志系统** - 详细的操作日志记录
- **错误处理** - 完善的异常处理和重试机制
- **安全检查** - 进程监控和窗口验证

## 安装依赖

### 自动安装
```bash
pip install -r requirements.txt
```

### 手动安装
```bash
pip install pyautogui>=0.9.54
pip install opencv-python>=4.5.0
pip install numpy>=1.21.0
pip install pillow>=8.0.0
pip install psutil>=5.8.0
```

### Windows特定依赖（可选）
```bash
pip install pywin32  # 用于窗口检测
```

## 配置说明

### config.json配置文件
```json
{
  "memu": {
    "executable_path": "",           // 雷电模拟器路径（自动检测）
    "startup_timeout": 30,           // 启动超时时间（秒）
    "window_title": "MEmu"           // 窗口标题匹配
  },
  "automation": {
    "video_watch_time": 5,           // 每个视频观看时长（秒）
    "scroll_duration": 0.5,          // 滑动动画时长
    "interaction_delay": 1,          // 操作间隔时间
    "like_probability": 0.3,         // 点赞概率（0-1）
    "follow_probability": 0.1,       // 关注概率（0-1）
    "max_videos": 20                 // 最大观看视频数
  },
  "image_recognition": {
    "confidence_threshold": 0.8,     // 图像匹配置信度
    "template_timeout": 30,          // 等待图像超时时间
    "template_directory": "templates"// 模板图像目录
  },
  "safety": {
    "enable_failsafe": true,         // 启用安全检查
    "pause_between_actions": 1,      // 操作间暂停时间
    "max_retries": 3                 // 最大重试次数
  },
  "logging": {
    "level": "INFO",                 // 日志级别
    "file": "automation.log",        // 日志文件
    "max_size_mb": 10               // 日志文件最大大小
  }
}
```

## 模板图像准备

### 必需模板文件
在 `templates/` 目录下放置以下图像：

1. **kuaishou_icon.png** - 快手应用图标
2. **like_button.png** - 点赞按钮
3. **follow_button.png** - 关注按钮

### 获取模板图像
详细说明请参考：[templates/README.md](templates/README.md)

## 使用方法

### 基本使用
```bash
python kuaishou_automation.py
```

### 程序化调用
```python
from kuaishou_automation import main, ConfigManager, MemuAutomation, KuaishouAutomation

# 加载配置
config = ConfigManager('config.json')

# 初始化组件
memu = MemuAutomation(config)
kuaishou = KuaishouAutomation(config)

# 启动自动化
if memu.start_memu():
    kuaishou.run_automation()
```

### 自定义配置运行
```python
# 修改配置
config = ConfigManager()
config.config['automation']['max_videos'] = 50
config.config['automation']['like_probability'] = 0.5

# 运行自定义配置
memu = MemuAutomation(config)
```

## 项目结构
```
Android_MUMU/
├── kuaishou_automation.py    # 主程序文件
├── config.json              # 配置文件
├── requirements.txt         # 依赖清单
├── Readme.md               # 使用说明
├── automation.log          # 运行日志（自动生成）
└── templates/              # 模板图像目录
    ├── README.md           # 模板获取指南
    ├── kuaishou_icon.png   # 快手图标模板
    ├── like_button.png     # 点赞按钮模板
    └── follow_button.png   # 关注按钮模板
```

## 运行流程

1. **环境检查** - 验证依赖和配置
2. **模拟器启动** - 自动启动或检测雷电模拟器
3. **应用打开** - 识别并打开快手应用
4. **自动化执行** - 按配置执行视频浏览和互动
5. **日志记录** - 记录所有操作和错误信息

## 安全注意事项

- ⚠️ 仅用于学习和研究目的
- ⚠️ 请遵守快手平台使用条款
- ⚠️ 避免过度频繁的自动化操作
- ⚠️ 建议设置合理的操作间隔
- ⚠️ 定期检查和更新模板图像

## 故障排除

### 常见问题

**Q: 找不到雷电模拟器？**
A: 在config.json中手动配置executable_path

**Q: 图像识别失败？**
A: 检查templates目录下的模板图像质量和匹配度

**Q: 操作太快被检测？**
A: 增加automation.interaction_delay值

**Q: 日志文件过大？**
A: 配置logging.max_size_mb限制文件大小

### 调试模式
```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

## 更新日志

### v2.0
- 添加完整的配置管理系统
- 实现详细的日志记录
- 增强错误处理和重试机制
- 支持进程监控和窗口检测
- 提供模板图像获取指南

### v1.0
- 基础自动化功能实现
- 图像识别和操作控制
- 雷电模拟器集成

## 许可证

本项目仅供学习和研究使用，请遵守相关法律法规和平台服务条款。