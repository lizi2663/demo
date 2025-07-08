# 植物大战僵尸自动化脚本

## 功能特点

- 自动窗口检测和聚焦
- 智能图像识别（OpenCV）
- 自动收集阳光
- 自动种植向日葵和豌豆射手
- 僵尸检测和自动防御
- 模块化函数设计，易于扩展

## 依赖安装

```bash
pip install -r requirements.txt
```

## 使用方法

1. 启动植物大战僵尸游戏
2. 运行脚本：
   ```bash
   python pvz_automation.py
   ```
3. 按 Ctrl+C 停止脚本

## 主要函数

- `find_game_window()`: 查找游戏窗口
- `focus_game_window()`: 聚焦游戏窗口
- `take_screenshot()`: 截取游戏屏幕
- `find_template()`: 模板匹配
- `collect_sun()`: 收集阳光
- `detect_zombies()`: 检测僵尸
- `auto_plant_sunflowers()`: 自动种植向日葵
- `auto_plant_peashooters()`: 自动种植豌豆射手
- `auto_defense()`: 自动防御
- `run_automation()`: 主自动化循环

## 注意事项

- 确保游戏窗口标题包含"Plants vs. Zombies"
- 游戏分辨率和坐标可能需要根据实际情况调整
- 建议在1024x768或更高分辨率下运行
- 脚本仅用于合法的游戏自动化用途