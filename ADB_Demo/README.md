# 雷电模拟器自动化管理工具

一个用于自动化连接和管理雷电模拟器应用的Python脚本。

## 功能特点

- 🔌 自动连接雷电模拟器
- 📱 获取已安装应用列表
- 🛠️ 模块化设计，便于集成到其他项目
- 📊 清晰的输出格式

## 系统要求

- Python 3.6+
- Android SDK (包含adb工具)
- 雷电模拟器

## 安装说明

### 1. 安装ADB工具

#### Windows
1. 下载Android SDK Platform Tools
2. 将adb.exe所在目录添加到系统PATH环境变量

#### macOS
```bash
brew install android-platform-tools
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install android-tools-adb
```

### 2. 验证ADB安装
```bash
adb version
```

## 使用方法

### 基本使用

1. 启动雷电模拟器
2. 运行脚本：
```bash
python3 ldplayer_manager.py
```

### 作为模块调用

```python
from ldplayer_manager import connect_ldplayer, get_installed_apps

# 连接模拟器
if connect_ldplayer():
    # 获取应用列表
    apps = get_installed_apps()
    for app in apps:
        print(f"{app['package_name']} - {app['app_name']}")
```

## API 参考

### 主要函数

#### `check_adb_available() -> bool`
检查系统中是否安装了adb工具。

#### `connect_ldplayer(port: int = 5555) -> bool`
连接雷电模拟器。
- `port`: 连接端口，默认5555

#### `get_connected_devices() -> List[str]`
获取当前连接的所有设备ID列表。

#### `get_installed_apps(device_id: Optional[str] = None) -> List[Dict[str, str]]`
获取已安装的第三方应用列表。
- `device_id`: 指定设备ID，为None时使用默认设备
- 返回: 包含应用信息的字典列表

#### `print_apps_list(apps: List[Dict[str, str]]) -> None`
格式化打印应用列表。

## 输出示例

```
🚀 雷电模拟器自动化管理工具
==================================================
✓ ADB工具检查通过
✓ 成功连接雷电模拟器 (端口: 5555)
✓ 找到设备: 127.0.0.1:5555

📱 已安装应用列表 (共 15 个):
--------------------------------------------------------------------------------
序号 包名                                     应用名
--------------------------------------------------------------------------------
1    com.tencent.mm                          com.tencent.mm
2    com.taobao.taobao                       com.taobao.taobao
3    com.tencent.mobileqq                    com.tencent.mobileqq
```

## 故障排除

### 常见问题

1. **adb命令未找到**
   - 确保已安装Android SDK
   - 检查环境变量PATH设置

2. **无法连接模拟器**
   - 确保雷电模拟器已启动
   - 检查模拟器的ADB端口设置（通常为5555）
   - 尝试手动连接：`adb connect 127.0.0.1:5555`

3. **应用列表为空**
   - 确保模拟器中已安装第三方应用
   - 检查ADB调试权限

### 调试命令

```bash
# 检查ADB设备连接
adb devices

# 手动连接模拟器
adb connect 127.0.0.1:5555

# 查看应用包列表
adb shell pm list packages -3
```

## 许可证

本项目仅供学习和合法用途使用。

## 注意事项

- 本工具仅适用于合法的自动化测试和开发用途
- 请确保遵守相关软件的使用条款
- 建议在使用前备份重要数据

使用方式:
  python3 ldplayer_manager.py

  或作为模块导入：
  from ldplayer_manager import connect_ldplayer, get_installed_apps

  脚本已优化为def函数风格，便于其他代码调用和集成。