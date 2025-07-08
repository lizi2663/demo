核心功能：
  - 自动登录游戏
  - 自动打怪任务
  - 图像识别定位游戏元素
  - 窗口管理和控制

  主要函数：
  - find_window() - 查找游戏窗口
  - find_template() - 图像模板匹配
  - login_game() - 自动登录
  - auto_hunt_monsters() - 自动打怪
  - run_automation() - 完整自动化流程

  使用方法：
  1. 在 templates/ 目录下放置游戏界面截图模板
  2. 修改脚本中的游戏窗口标题、用户名密码
  3. 运行脚本即可开始自动化

  安全特性：
  - 包含 pyautogui.FAILSAFE 紧急停止
  - 错误处理和日志记录
  - 血量检查和回血机制