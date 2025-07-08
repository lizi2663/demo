#!/usr/bin/env python3
import pyautogui
import cv2
import numpy as np
import time
import subprocess
import os
from typing import Tuple, Optional

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True

def find_image_on_screen(template_path: str, confidence: float = 0.8) -> Optional[Tuple[int, int]]:
    """
    在屏幕上查找指定图像的位置
    
    Args:
        template_path: 模板图像路径
        confidence: 匹配置信度 (0-1)
    
    Returns:
        匹配位置的坐标 (x, y)，未找到返回 None
    """
    try:
        screenshot = pyautogui.screenshot()
        screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        template = cv2.imread(template_path)
        if template is None:
            print(f"无法加载模板图像: {template_path}")
            return None
            
        result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= confidence:
            center_x = max_loc[0] + template.shape[1] // 2
            center_y = max_loc[1] + template.shape[0] // 2
            return (center_x, center_y)
        return None
    except Exception as e:
        print(f"图像识别出错: {e}")
        return None

def click_if_found(template_path: str, confidence: float = 0.8, timeout: int = 10) -> bool:
    """
    查找并点击指定图像
    
    Args:
        template_path: 模板图像路径
        confidence: 匹配置信度
        timeout: 超时时间(秒)
    
    Returns:
        是否成功点击
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        pos = find_image_on_screen(template_path, confidence)
        if pos:
            pyautogui.click(pos[0], pos[1])
            print(f"点击位置: {pos}")
            return True
        time.sleep(0.5)
    print(f"未找到图像: {template_path}")
    return False

def start_leidian_simulator():
    """
    启动雷电模拟器
    """
    try:
        # 这里需要根据实际安装路径修改
        leidian_path = r"C:\LDPlayer\LDPlayer4.0\dnplayer.exe"
        if os.path.exists(leidian_path):
            subprocess.Popen([leidian_path])
            print("正在启动雷电模拟器...")
            time.sleep(10)  # 等待模拟器启动
            return True
        else:
            print("未找到雷电模拟器，请手动启动")
            return False
    except Exception as e:
        print(f"启动模拟器出错: {e}")
        return False

def open_alipay_app():
    """
    打开支付宝APP
    """
    print("正在打开支付宝APP...")
    
    # 方法1: 通过桌面图标点击
    alipay_icon = "images/alipay_icon.png"  # 需要准备支付宝图标截图
    if click_if_found(alipay_icon, confidence=0.8, timeout=5):
        time.sleep(3)
        return True
    
    # 方法2: 通过应用列表查找
    app_drawer = "images/app_drawer.png"  # 应用列表图标
    if click_if_found(app_drawer, confidence=0.8, timeout=5):
        time.sleep(2)
        # 搜索支付宝
        search_bar = "images/search_bar.png"
        if click_if_found(search_bar, confidence=0.8, timeout=5):
            pyautogui.write("支付宝")
            time.sleep(1)
            if click_if_found(alipay_icon, confidence=0.8, timeout=5):
                time.sleep(3)
                return True
    
    print("无法打开支付宝APP")
    return False

def navigate_to_ant_forest():
    """
    导航到蚂蚁森林
    """
    print("正在进入蚂蚁森林...")
    
    # 点击更多功能
    more_button = "images/more_button.png"
    if click_if_found(more_button, confidence=0.8, timeout=10):
        time.sleep(2)
        
        # 查找蚂蚁森林图标
        ant_forest_icon = "images/ant_forest_icon.png"
        if click_if_found(ant_forest_icon, confidence=0.8, timeout=10):
            time.sleep(3)
            return True
    
    # 如果在首页没找到，尝试搜索
    search_button = "images/search_button.png"
    if click_if_found(search_button, confidence=0.8, timeout=5):
        pyautogui.write("蚂蚁森林")
        time.sleep(1)
        ant_forest_result = "images/ant_forest_search_result.png"
        if click_if_found(ant_forest_result, confidence=0.8, timeout=5):
            time.sleep(3)
            return True
    
    print("无法进入蚂蚁森林")
    return False

def collect_energy():
    """
    收集能量
    """
    print("开始收集能量...")
    
    # 收集自己的能量
    collect_count = 0
    energy_ball = "images/energy_ball.png"
    
    # 尝试收集多个能量球
    for i in range(10):  # 最多尝试10次
        if click_if_found(energy_ball, confidence=0.7, timeout=2):
            collect_count += 1
            print(f"收集能量球 {collect_count}")
            time.sleep(0.5)
        else:
            break
    
    # 访问好友收集能量
    friends_button = "images/friends_button.png"
    if click_if_found(friends_button, confidence=0.8, timeout=5):
        time.sleep(2)
        
        # 收集好友能量
        friend_energy_count = collect_friends_energy()
        collect_count += friend_energy_count
    
    print(f"总共收集了 {collect_count} 个能量球")
    return collect_count

def collect_friends_energy():
    """
    收集好友能量
    """
    print("开始收集好友能量...")
    friend_collect_count = 0
    
    # 查找可收集的好友
    collectable_friend = "images/collectable_friend.png"
    
    for i in range(5):  # 最多访问5个好友
        if click_if_found(collectable_friend, confidence=0.7, timeout=3):
            time.sleep(2)
            
            # 收集该好友的能量
            energy_ball = "images/energy_ball.png"
            for j in range(5):  # 每个好友最多收集5个能量球
                if click_if_found(energy_ball, confidence=0.7, timeout=1):
                    friend_collect_count += 1
                    time.sleep(0.5)
                else:
                    break
            
            # 返回好友列表
            back_button = "images/back_button.png"
            if click_if_found(back_button, confidence=0.8, timeout=3):
                time.sleep(1)
        else:
            break
    
    print(f"从好友处收集了 {friend_collect_count} 个能量球")
    return friend_collect_count

def main():
    """
    主函数：自动化收集蚂蚁森林能量
    """
    print("开始自动化收集蚂蚁森林能量...")
    
    # 启动模拟器（可选）
    start_leidian_simulator()
    
    # 打开支付宝APP
    if not open_alipay_app():
        print("打开支付宝失败，程序退出")
        return False
    
    # 导航到蚂蚁森林
    if not navigate_to_ant_forest():
        print("进入蚂蚁森林失败，程序退出")
        return False
    
    # 收集能量
    total_energy = collect_energy()
    
    print(f"自动化完成！总共收集了 {total_energy} 个能量球")
    return True

if __name__ == "__main__":
    main()