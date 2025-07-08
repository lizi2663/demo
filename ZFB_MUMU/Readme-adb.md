核心功能：
  - LeiDianADBController - 雷电模拟器ADB控制器类
  - find_image_in_screenshot() - 在截图中进行图像识别
  - wait_and_click() - 等待并点击指定图像
  - open_alipay_app() - 通过ADB打开支付宝APP
  - navigate_to_ant_forest() - 导航到蚂蚁森林
  - collect_energy() - 收集能量和好友能量
  - main() - 主函数

  使用前准备：
  1. 安装依赖：pip install opencv-python numpy
  2. 确保ADB工具已安装并在PATH中
  3. 启动雷电模拟器（默认端口5555）
  4. 准备模板图像文件到images/目录

  调用方式：
  # 直接运行（默认端口5555）
  python alipay_forest_adb.py

  # 或在代码中调用
  from alipay_forest_adb import main, LeiDianADBController
  main(adb_path="adb", device_port="5555")

  # 单独使用控制器
  controller = LeiDianADBController()
  controller.connect()
  controller.tap(100, 200)  # 点击坐标

  相比pyautogui的优势：
  - 更稳定的设备连接
  - 精确的坐标控制
  - 更好的性能
  - 支持多设备管理