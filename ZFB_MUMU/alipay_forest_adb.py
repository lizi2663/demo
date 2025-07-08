#!/usr/bin/env python3
import subprocess
import cv2
import numpy as np
import time
import os
import tempfile
from typing import Tuple, Optional, List

class LeiDianADBController:
    """雷电模拟器ADB控制器"""
    
    def __init__(self, adb_path: str = "adb", device_port: str = "5555"):
        self.adb_path = adb_path
        self.device = f"127.0.0.1:{device_port}"
        self.connected = False
        
    def connect(self) -> bool:
        """连接到雷电模拟器"""
        try:
            result = subprocess.run([self.adb_path, "connect", self.device], 
                                  capture_output=True, text=True)
            if "connected" in result.stdout:
                self.connected = True
                print(f"成功连接到雷电模拟器: {self.device}")
                return True
            else:
                print(f"连接失败: {result.stdout}")
                return False
        except Exception as e:
            print(f"ADB连接出错: {e}")
            return False
    
    def execute_command(self, command: List[str]) -> Optional[str]:
        """执行ADB命令"""
        if not self.connected:
            print("未连接到设备")
            return None
            
        try:
            full_command = [self.adb_path, "-s", self.device] + command
            result = subprocess.run(full_command, capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            print(f"执行命令出错: {e}")
            return None
    
    def tap(self, x: int, y: int) -> bool:
        """点击屏幕指定位置"""
        result = self.execute_command(["shell", "input", "tap", str(x), str(y)])
        return result is not None
    
    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 300) -> bool:
        """滑动屏幕"""
        result = self.execute_command(["shell", "input", "swipe", 
                                     str(x1), str(y1), str(x2), str(y2), str(duration)])
        return result is not None
    
    def get_screenshot(self) -> Optional[np.ndarray]:
        """获取屏幕截图"""
        try:
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                tmp_path = tmp_file.name
            
            result = self.execute_command(["shell", "screencap", "-p", "/sdcard/screenshot.png"])
            if result is None:
                return None
                
            result = self.execute_command(["pull", "/sdcard/screenshot.png", tmp_path])
            if result is None:
                return None
            
            image = cv2.imread(tmp_path)
            os.unlink(tmp_path)
            return image
        except Exception as e:
            print(f"获取截图出错: {e}")
            return None
    
    def start_app(self, package_name: str) -> bool:
        """启动应用"""
        result = self.execute_command(["shell", "monkey", "-p", package_name, "-v", "1"])
        return result is not None

def find_image_in_screenshot(screenshot: np.ndarray, template_path: str, 
                           confidence: float = 0.8) -> Optional[Tuple[int, int]]:
    """在截图中查找模板图像"""
    try:
        template = cv2.imread(template_path)
        if template is None:
            print(f"无法加载模板图像: {template_path}")
            return None
        
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= confidence:
            center_x = max_loc[0] + template.shape[1] // 2
            center_y = max_loc[1] + template.shape[0] // 2
            return (center_x, center_y)
        return None
    except Exception as e:
        print(f"图像识别出错: {e}")
        return None

def wait_and_click(controller: LeiDianADBController, template_path: str, 
                  confidence: float = 0.8, timeout: int = 10) -> bool:
    """等待并点击指定图像"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        screenshot = controller.get_screenshot()
        if screenshot is None:
            continue
            
        pos = find_image_in_screenshot(screenshot, template_path, confidence)
        if pos:
            controller.tap(pos[0], pos[1])
            print(f"点击位置: {pos}")
            return True
        time.sleep(0.5)
    
    print(f"未找到图像: {template_path}")
    return False

def open_alipay_app(controller: LeiDianADBController) -> bool:
    """打开支付宝APP"""
    print("正在打开支付宝APP...")
    
    # 方法1: 直接启动支付宝包名
    if controller.start_app("com.eg.android.AlipayGphone"):
        time.sleep(3)
        return True
    
    # 方法2: 通过桌面图标点击
    alipay_icon = "images/alipay_icon.png"
    if os.path.exists(alipay_icon):
        if wait_and_click(controller, alipay_icon, confidence=0.8, timeout=5):
            time.sleep(3)
            return True
    
    # 方法3: 通过应用列表查找
    app_drawer = "images/app_drawer.png"
    if os.path.exists(app_drawer):
        if wait_and_click(controller, app_drawer, confidence=0.8, timeout=5):
            time.sleep(2)
            alipay_icon = "images/alipay_icon.png"
            if wait_and_click(controller, alipay_icon, confidence=0.8, timeout=5):
                time.sleep(3)
                return True
    
    print("无法打开支付宝APP")
    return False

def navigate_to_ant_forest(controller: LeiDianADBController) -> bool:
    """导航到蚂蚁森林"""
    print("正在进入蚂蚁森林...")
    
    # 点击更多功能
    more_button = "images/more_button.png"
    if os.path.exists(more_button):
        if wait_and_click(controller, more_button, confidence=0.8, timeout=10):
            time.sleep(2)
            
            # 查找蚂蚁森林图标
            ant_forest_icon = "images/ant_forest_icon.png"
            if os.path.exists(ant_forest_icon):
                if wait_and_click(controller, ant_forest_icon, confidence=0.8, timeout=10):
                    time.sleep(3)
                    return True
    
    # 尝试搜索功能
    search_button = "images/search_button.png"
    if os.path.exists(search_button):
        if wait_and_click(controller, search_button, confidence=0.8, timeout=5):
            time.sleep(1)
            # 输入搜索内容
            controller.execute_command(["shell", "input", "text", "蚂蚁森林"])
            time.sleep(1)
            
            ant_forest_result = "images/ant_forest_search_result.png"
            if os.path.exists(ant_forest_result):
                if wait_and_click(controller, ant_forest_result, confidence=0.8, timeout=5):
                    time.sleep(3)
                    return True
    
    print("无法进入蚂蚁森林")
    return False

def collect_energy(controller: LeiDianADBController) -> int:
    """收集能量"""
    print("开始收集能量...")
    
    collect_count = 0
    energy_ball = "images/energy_ball.png"
    
    if not os.path.exists(energy_ball):
        print(f"能量球模板图像不存在: {energy_ball}")
        return 0
    
    # 收集自己的能量
    for _ in range(10):  # 最多尝试10次
        screenshot = controller.get_screenshot()
        if screenshot is None:
            continue
            
        pos = find_image_in_screenshot(screenshot, energy_ball, confidence=0.7)
        if pos:
            controller.tap(pos[0], pos[1])
            collect_count += 1
            print(f"收集能量球 {collect_count}")
            time.sleep(0.5)
        else:
            break
    
    # 访问好友收集能量
    friends_button = "images/friends_button.png"
    if os.path.exists(friends_button):
        if wait_and_click(controller, friends_button, confidence=0.8, timeout=5):
            time.sleep(2)
            friend_energy_count = collect_friends_energy(controller)
            collect_count += friend_energy_count
    
    print(f"总共收集了 {collect_count} 个能量球")
    return collect_count

def collect_friends_energy(controller: LeiDianADBController) -> int:
    """收集好友能量"""
    print("开始收集好友能量...")
    friend_collect_count = 0
    
    collectable_friend = "images/collectable_friend.png"
    energy_ball = "images/energy_ball.png"
    back_button = "images/back_button.png"
    
    if not all(os.path.exists(f) for f in [collectable_friend, energy_ball, back_button]):
        print("好友能量相关模板图像不完整")
        return 0
    
    # 访问可收集的好友
    for _ in range(5):  # 最多访问5个好友
        screenshot = controller.get_screenshot()
        if screenshot is None:
            continue
            
        pos = find_image_in_screenshot(screenshot, collectable_friend, confidence=0.7)
        if pos:
            controller.tap(pos[0], pos[1])
            time.sleep(2)
            
            # 收集该好友的能量
            for _ in range(5):  # 每个好友最多收集5个能量球
                screenshot = controller.get_screenshot()
                if screenshot is None:
                    continue
                    
                pos = find_image_in_screenshot(screenshot, energy_ball, confidence=0.7)
                if pos:
                    controller.tap(pos[0], pos[1])
                    friend_collect_count += 1
                    time.sleep(0.5)
                else:
                    break
            
            # 返回好友列表
            if wait_and_click(controller, back_button, confidence=0.8, timeout=3):
                time.sleep(1)
        else:
            break
    
    print(f"从好友处收集了 {friend_collect_count} 个能量球")
    return friend_collect_count

def main(adb_path: str = "adb", device_port: str = "5555") -> bool:
    """主函数：自动化收集蚂蚁森林能量"""
    print("开始自动化收集蚂蚁森林能量...")
    
    # 初始化ADB控制器
    controller = LeiDianADBController(adb_path, device_port)
    
    # 连接到雷电模拟器
    if not controller.connect():
        print("连接雷电模拟器失败，程序退出")
        return False
    
    # 打开支付宝APP
    if not open_alipay_app(controller):
        print("打开支付宝失败，程序退出")
        return False
    
    # 导航到蚂蚁森林
    if not navigate_to_ant_forest(controller):
        print("进入蚂蚁森林失败，程序退出")
        return False
    
    # 收集能量
    total_energy = collect_energy(controller)
    
    print(f"自动化完成！总共收集了 {total_energy} 个能量球")
    return True

if __name__ == "__main__":
    main()