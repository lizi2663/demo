#!/usr/bin/env python3
"""
植物大战僵尸自动化脚本
使用pyautogui、opencv和win32gui实现游戏自动化
"""

import time
import cv2
import numpy as np
import pyautogui
import win32gui
import win32con
from typing import Tuple, Optional, List


class PVZAutomation:
    """植物大战僵尸自动化控制类"""
    
    def __init__(self):
        self.window_title = "Plants vs. Zombies"
        self.window_handle = None
        self.game_region = None
        
        # 游戏设置
        pyautogui.PAUSE = 0.1
        pyautogui.FAILSAFE = True
        
    def find_game_window(self) -> bool:
        """查找游戏窗口"""
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                if self.window_title in window_text:
                    windows.append(hwnd)
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        if windows:
            self.window_handle = windows[0]
            return True
        return False
    
    def focus_game_window(self) -> bool:
        """聚焦游戏窗口"""
        if not self.window_handle:
            if not self.find_game_window():
                return False
        
        try:
            win32gui.SetForegroundWindow(self.window_handle)
            win32gui.ShowWindow(self.window_handle, win32con.SW_RESTORE)
            time.sleep(0.5)
            return True
        except:
            return False
    
    def get_game_region(self) -> Optional[Tuple[int, int, int, int]]:
        """获取游戏窗口区域"""
        if not self.window_handle:
            return None
        
        try:
            rect = win32gui.GetWindowRect(self.window_handle)
            self.game_region = rect
            return rect
        except:
            return None
    
    def take_screenshot(self) -> np.ndarray:
        """截取游戏屏幕"""
        if not self.game_region:
            self.get_game_region()
        
        if self.game_region:
            screenshot = pyautogui.screenshot(region=self.game_region)
        else:
            screenshot = pyautogui.screenshot()
        
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    def find_template(self, template_path: str, threshold: float = 0.8) -> Optional[Tuple[int, int]]:
        """使用模板匹配查找图像"""
        screenshot = self.take_screenshot()
        template = cv2.imread(template_path)
        
        if template is None:
            return None
        
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= threshold:
            offset_x = self.game_region[0] if self.game_region else 0
            offset_y = self.game_region[1] if self.game_region else 0
            return (max_loc[0] + offset_x, max_loc[1] + offset_y)
        
        return None
    
    def click_at_position(self, x: int, y: int) -> None:
        """在指定位置点击"""
        pyautogui.click(x, y)
    
    def select_plant(self, plant_slot: int) -> bool:
        """选择植物(1-10)"""
        if not (1 <= plant_slot <= 10):
            return False
        
        # 植物选择区域大概位置 (需要根据实际游戏调整)
        base_x = 100
        base_y = 100
        slot_width = 50
        
        x = base_x + (plant_slot - 1) * slot_width
        y = base_y
        
        self.click_at_position(x, y)
        return True
    
    def place_plant(self, row: int, col: int) -> bool:
        """在指定位置放置植物"""
        if not (1 <= row <= 5) or not (1 <= col <= 9):
            return False
        
        # 游戏区域网格位置计算 (需要根据实际游戏调整)
        grid_start_x = 250
        grid_start_y = 180
        grid_width = 80
        grid_height = 100
        
        x = grid_start_x + (col - 1) * grid_width
        y = grid_start_y + (row - 1) * grid_height
        
        self.click_at_position(x, y)
        return True
    
    def collect_sun(self) -> int:
        """收集阳光"""
        collected = 0
        screenshot = self.take_screenshot()
        
        # 使用颜色检测查找阳光 (黄色)
        hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])
        
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if 500 < area < 2000:  # 阳光大小范围
                x, y, w, h = cv2.boundingRect(contour)
                center_x = x + w // 2
                center_y = y + h // 2
                
                if self.game_region:
                    center_x += self.game_region[0]
                    center_y += self.game_region[1]
                
                self.click_at_position(center_x, center_y)
                collected += 1
                time.sleep(0.1)
        
        return collected
    
    def detect_zombies(self) -> List[Tuple[int, int]]:
        """检测僵尸位置"""
        screenshot = self.take_screenshot()
        zombies = []
        
        # 使用颜色检测查找僵尸 (灰绿色)
        hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
        lower_zombie = np.array([40, 40, 40])
        upper_zombie = np.array([80, 255, 255])
        
        mask = cv2.inRange(hsv, lower_zombie, upper_zombie)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:  # 僵尸大小阈值
                x, y, w, h = cv2.boundingRect(contour)
                center_x = x + w // 2
                center_y = y + h // 2
                
                # 转换为游戏网格坐标
                if self.game_region:
                    center_x += self.game_region[0]
                    center_y += self.game_region[1]
                
                zombies.append((center_x, center_y))
        
        return zombies
    
    def auto_plant_sunflowers(self) -> None:
        """自动种植向日葵"""
        self.select_plant(1)  # 选择向日葵
        
        # 在前两列种植向日葵
        for row in range(1, 6):
            for col in range(1, 3):
                if self.place_plant(row, col):
                    time.sleep(0.5)
    
    def auto_plant_peashooters(self) -> None:
        """自动种植豌豆射手"""
        self.select_plant(2)  # 选择豌豆射手
        
        # 在第三列开始种植豌豆射手
        for row in range(1, 6):
            for col in range(3, 6):
                if self.place_plant(row, col):
                    time.sleep(0.5)
    
    def auto_defense(self) -> None:
        """自动防御"""
        zombies = self.detect_zombies()
        
        if zombies:
            # 如果发现僵尸，优先种植攻击植物
            self.select_plant(2)  # 豌豆射手
            
            for _, zombie_y in zombies:
                # 计算僵尸所在行
                row = min(5, max(1, (zombie_y - 180) // 100 + 1))
                
                # 在僵尸前方种植防御植物
                for col in range(1, 6):
                    if self.place_plant(row, col):
                        break
    
    def run_automation(self) -> None:
        """运行自动化脚本"""
        if not self.focus_game_window():
            print("未找到游戏窗口")
            return
        
        print("开始自动化脚本...")
        
        # 初始化植物布局
        time.sleep(2)
        self.auto_plant_sunflowers()
        time.sleep(1)
        self.auto_plant_peashooters()
        
        # 主游戏循环
        while True:
            try:
                # 收集阳光
                collected = self.collect_sun()
                if collected > 0:
                    print(f"收集了 {collected} 个阳光")
                
                # 自动防御
                self.auto_defense()
                
                time.sleep(1)
                
            except KeyboardInterrupt:
                print("自动化脚本已停止")
                break
            except Exception as e:
                print(f"错误: {e}")
                time.sleep(2)


def main():
    """主函数"""
    automation = PVZAutomation()
    automation.run_automation()


if __name__ == "__main__":
    main()