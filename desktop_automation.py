#!/usr/bin/env python3
"""
桌面自动化工具库
提供pyautogui、opencv、win32gui的封装函数
"""

import pyautogui
import cv2
import numpy as np
import win32gui
import win32con
import win32process
import time
import os
from typing import Tuple, Optional, List

# 设置pyautogui安全模式
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

class DesktopAutomation:
    """桌面自动化工具类"""
    
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
    
    # ==================== PyAutoGUI 桌面自动化 ====================
    
    def get_screen_size(self) -> Tuple[int, int]:
        """获取屏幕尺寸"""
        return self.screen_width, self.screen_height
    
    def take_screenshot(self, region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
        """截取屏幕截图
        Args:
            region: 截图区域 (x, y, width, height)
        Returns:
            截图的numpy数组
        """
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    def click_at(self, x: int, y: int, button: str = 'left', clicks: int = 1) -> None:
        """在指定位置点击
        Args:
            x, y: 点击坐标
            button: 按键类型 ('left', 'right', 'middle')
            clicks: 点击次数
        """
        pyautogui.click(x, y, button=button, clicks=clicks)
    
    def drag_to(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.5) -> None:
        """拖拽操作"""
        pyautogui.drag(end_x - start_x, end_y - start_y, duration=duration)
    
    def type_text(self, text: str, interval: float = 0.01) -> None:
        """输入文本"""
        pyautogui.typewrite(text, interval=interval)
    
    def press_key(self, key: str) -> None:
        """按键操作"""
        pyautogui.press(key)
    
    def key_combination(self, *keys: str) -> None:
        """组合键操作"""
        pyautogui.hotkey(*keys)
    
    def scroll(self, clicks: int, x: Optional[int] = None, y: Optional[int] = None) -> None:
        """滚动操作"""
        if x is not None and y is not None:
            pyautogui.scroll(clicks, x=x, y=y)
        else:
            pyautogui.scroll(clicks)
    
    # ==================== OpenCV 图像识别 ====================
    
    def find_image_on_screen(self, template_path: str, confidence: float = 0.8, 
                           region: Optional[Tuple[int, int, int, int]] = None) -> Optional[Tuple[int, int, int, int]]:
        """在屏幕上查找图像
        Args:
            template_path: 模板图像路径
            confidence: 匹配置信度
            region: 搜索区域
        Returns:
            找到的图像位置 (x, y, width, height) 或 None
        """
        if not os.path.exists(template_path):
            print(f"模板图像不存在: {template_path}")
            return None
        
        # 读取模板图像
        template = cv2.imread(template_path)
        if template is None:
            print(f"无法读取模板图像: {template_path}")
            return None
        
        # 截取屏幕
        screen = self.take_screenshot(region)
        
        # 模板匹配
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= confidence:
            h, w = template.shape[:2]
            x, y = max_loc
            if region:
                x += region[0]
                y += region[1]
            return (x, y, w, h)
        
        return None
    
    def find_all_images_on_screen(self, template_path: str, confidence: float = 0.8,
                                 region: Optional[Tuple[int, int, int, int]] = None) -> List[Tuple[int, int, int, int]]:
        """查找屏幕上的所有匹配图像"""
        if not os.path.exists(template_path):
            return []
        
        template = cv2.imread(template_path)
        if template is None:
            return []
        
        screen = self.take_screenshot(region)
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        
        locations = np.where(result >= confidence)
        matches = []
        h, w = template.shape[:2]
        
        for pt in zip(*locations[::-1]):
            x, y = pt
            if region:
                x += region[0]
                y += region[1]
            matches.append((x, y, w, h))
        
        return matches
    
    def wait_for_image(self, template_path: str, timeout: float = 10, 
                      confidence: float = 0.8, check_interval: float = 0.5) -> Optional[Tuple[int, int, int, int]]:
        """等待图像出现"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            result = self.find_image_on_screen(template_path, confidence)
            if result:
                return result
            time.sleep(check_interval)
        
        return None
    
    def click_image(self, template_path: str, confidence: float = 0.8, 
                   button: str = 'left', offset: Tuple[int, int] = (0, 0)) -> bool:
        """点击图像中心位置"""
        result = self.find_image_on_screen(template_path, confidence)
        if result:
            x, y, w, h = result
            center_x = x + w // 2 + offset[0]
            center_y = y + h // 2 + offset[1]
            self.click_at(center_x, center_y, button)
            return True
        return False
    
    # ==================== Win32GUI 窗口操作 ====================
    
    def find_window_by_title(self, title: str) -> Optional[int]:
        """根据标题查找窗口句柄"""
        def enum_handler(hwnd, result_list):
            if win32gui.IsWindowVisible(hwnd) and title in win32gui.GetWindowText(hwnd):
                result_list.append(hwnd)
        
        windows = []
        win32gui.EnumWindows(enum_handler, windows)
        return windows[0] if windows else None
    
    def find_window_by_class(self, class_name: str) -> Optional[int]:
        """根据类名查找窗口句柄"""
        return win32gui.FindWindow(class_name, None)
    
    def get_window_rect(self, hwnd: int) -> Tuple[int, int, int, int]:
        """获取窗口位置和大小"""
        return win32gui.GetWindowRect(hwnd)
    
    def get_window_title(self, hwnd: int) -> str:
        """获取窗口标题"""
        return win32gui.GetWindowText(hwnd)
    
    def activate_window(self, hwnd: int) -> None:
        """激活窗口"""
        win32gui.SetForegroundWindow(hwnd)
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    
    def move_window(self, hwnd: int, x: int, y: int, width: int, height: int) -> None:
        """移动和调整窗口大小"""
        win32gui.MoveWindow(hwnd, x, y, width, height, True)
    
    def minimize_window(self, hwnd: int) -> None:
        """最小化窗口"""
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    
    def maximize_window(self, hwnd: int) -> None:
        """最大化窗口"""
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    
    def close_window(self, hwnd: int) -> None:
        """关闭窗口"""
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    
    def get_window_process_id(self, hwnd: int) -> int:
        """获取窗口进程ID"""
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        return pid
    
    def enum_child_windows(self, hwnd: int) -> List[int]:
        """枚举子窗口"""
        def enum_handler(child_hwnd, result_list):
            result_list.append(child_hwnd)
        
        children = []
        win32gui.EnumChildWindows(hwnd, enum_handler, children)
        return children
    
    # ==================== 高级功能 ====================
    
    def wait_and_click_image(self, template_path: str, timeout: float = 10, 
                           confidence: float = 0.8, button: str = 'left') -> bool:
        """等待图像出现并点击"""
        result = self.wait_for_image(template_path, timeout, confidence)
        if result:
            x, y, w, h = result
            self.click_at(x + w // 2, y + h // 2, button)
            return True
        return False
    
    def focus_window_and_click(self, window_title: str, template_path: str, 
                             confidence: float = 0.8) -> bool:
        """聚焦窗口并点击图像"""
        hwnd = self.find_window_by_title(window_title)
        if hwnd:
            self.activate_window(hwnd)
            time.sleep(0.5)  # 等待窗口激活
            return self.click_image(template_path, confidence)
        return False
    
    def capture_window_screenshot(self, hwnd: int) -> np.ndarray:
        """截取指定窗口的截图"""
        rect = self.get_window_rect(hwnd)
        x, y, right, bottom = rect
        width = right - x
        height = bottom - y
        return self.take_screenshot((x, y, width, height))


# ==================== 使用示例 ====================

def main():
    """使用示例"""
    automation = DesktopAutomation()
    
    # 1. 基本操作示例
    print("屏幕尺寸:", automation.get_screen_size())
    
    # 2. 截图示例
    # screenshot = automation.take_screenshot()
    # cv2.imwrite("screenshot.png", screenshot)
    
    # 3. 窗口操作示例
    notepad_hwnd = automation.find_window_by_title("记事本")
    if notepad_hwnd:
        print(f"找到记事本窗口: {notepad_hwnd}")
        automation.activate_window(notepad_hwnd)
        automation.type_text("Hello, World!")
    
    # 4. 图像识别示例
    # if automation.click_image("button.png", confidence=0.8):
    #     print("成功点击按钮")
    # else:
    #     print("未找到按钮")
    
    # 5. 等待并点击示例
    # if automation.wait_and_click_image("target.png", timeout=5):
    #     print("找到目标并点击")
    # else:
    #     print("超时未找到目标")

if __name__ == "__main__":
    main()