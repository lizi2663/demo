# 游戏自动化脚本使用说明

## 环境要求
- Python 3.7+
- Windows操作系统

## 安装依赖
```bash
pip install -r requirements.txt
```

## 使用步骤

### 1. 准备模板图片
在 `templates/` 目录下放置以下截图：
- `login_button.png` - 登录按钮
- `username_field.png` - 用户名输入框
- `password_field.png` - 密码输入框
- `game_ready.png` - 游戏加载完成标识
- `monster1.png` - 怪物1图片
- `monster2.png` - 怪物2图片
- `monster3.png` - 怪物3图片
- `low_health.png` - 血量过低提示

### 2. 配置参数
修改 `game_automation.py` 中的配置：
```python
GAME_WINDOW_TITLE = "Your Game Title"  # 游戏窗口标题
USERNAME = "your_username"  # 用户名
PASSWORD = "your_password"  # 密码
```

### 3. 运行脚本
```bash
python game_automation.py
```

## 安全特性
- 鼠标左上角紧急停止
- 自动血量检查
- 错误处理和日志记录

## 注意事项
1. 仅用于合法的游戏自动化
2. 请遵守游戏服务条款
3. 建议在测试环境中先运行
4. 可根据具体游戏调整参数和逻辑