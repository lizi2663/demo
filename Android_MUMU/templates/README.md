# 模板图像获取指南

## 概述
本自动化脚本需要模板图像来识别快手应用中的各种UI元素。以下是获取和准备模板图像的详细指南。

## 需要的模板图像

### 1. kuaishou_icon.png
- **用途**: 识别快手应用图标
- **获取方法**: 
  - 在雷电模拟器桌面截取快手应用图标
  - 尺寸建议: 64x64 到 128x128 像素
  - 确保图标清晰，背景干净

### 2. like_button.png
- **用途**: 识别视频点赞按钮
- **获取方法**:
  - 打开快手视频播放界面
  - 截取右侧点赞按钮（心形图标）
  - 尺寸建议: 40x40 到 60x60 像素
  - 包含未点赞状态的按钮

### 3. follow_button.png
- **用途**: 识别关注按钮
- **获取方法**:
  - 在视频播放界面找到关注按钮
  - 截取"+"号或"关注"文字按钮
  - 尺寸建议: 60x30 到 80x40 像素

## 截图工具推荐

### 1. Windows截图工具
```bash
# 使用系统自带截图工具
Win + Shift + S
```

### 2. 专业截图软件
- **Snipaste**: 精确截图和标注
- **PicPick**: 功能丰富的截图工具
- **Greenshot**: 开源截图软件

### 3. Python自动截图脚本
```python
import pyautogui
import cv2
import numpy as np

def capture_template(name, x, y, width, height):
    """
    捕获指定区域作为模板图像
    :param name: 保存的文件名
    :param x, y: 截图区域左上角坐标
    :param width, height: 截图区域宽高
    """
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot.save(f'templates/{name}.png')
    print(f'已保存模板: templates/{name}.png')

# 示例用法
# capture_template('kuaishou_icon', 100, 200, 64, 64)
```

## 模板图像质量要求

### 1. 清晰度
- 图像应清晰，无模糊
- 避免截图时的抖动
- 确保UI元素完整显示

### 2. 颜色
- 保持原始颜色
- 避免过度压缩导致颜色失真
- 建议使用PNG格式保持质量

### 3. 背景
- 尽量包含最少的背景元素
- 确保目标元素突出
- 避免包含会变化的背景内容

## 目录结构
```
templates/
├── kuaishou_icon.png      # 快手应用图标
├── like_button.png        # 点赞按钮
├── follow_button.png      # 关注按钮
└── README.md             # 本说明文件
```

## 测试模板
运行以下代码测试模板图像是否可用：

```python
from kuaishou_automation import ImageRecognition

# 测试模板识别
ir = ImageRecognition()
position = ir.find_image_on_screen('templates/kuaishou_icon.png')
if position:
    print(f'找到快手图标位置: {position}')
else:
    print('未找到快手图标，请检查模板图像')
```

## 常见问题

### Q: 模板识别失败怎么办？
A: 
1. 检查模板图像质量
2. 降低置信度阈值（在config.json中修改confidence_threshold）
3. 重新截取更清晰的模板
4. 确保截图时UI元素状态一致

### Q: 不同分辨率下模板失效？
A: 
1. 为不同分辨率准备多套模板
2. 使用相对较小的关键元素作为模板
3. 考虑使用缩放匹配算法

### Q: 模板更新频率？
A: 
- 快手UI更新时需要重新截取
- 建议定期检查模板有效性
- 可准备备用模板文件

## 自动化模板获取

可以使用以下脚本半自动获取模板：

```python
import pyautogui
import time

def interactive_template_capture():
    """交互式模板捕获"""
    templates = [
        ('kuaishou_icon', '请将鼠标移到快手图标上'),
        ('like_button', '请将鼠标移到点赞按钮上'),
        ('follow_button', '请将鼠标移到关注按钮上')
    ]
    
    for name, instruction in templates:
        print(f'\n{instruction}')
        print('3秒后开始截图...')
        time.sleep(3)
        
        # 获取鼠标位置
        x, y = pyautogui.position()
        
        # 截取鼠标周围区域
        screenshot = pyautogui.screenshot(region=(x-32, y-32, 64, 64))
        screenshot.save(f'templates/{name}.png')
        print(f'已保存: templates/{name}.png')

# 运行交互式捕获
# interactive_template_capture()
```