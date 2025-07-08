#!/usr/bin/env python3
"""
Game Automation Script
自动化登录PC游戏并执行打怪任务
"""

import pyautogui
import cv2
import numpy as np
import win32gui
import win32con
import time
import os
import logging
from typing import Tuple, Optional

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 全局配置
pyautogui.FAILSAFE = True  # 鼠标移动到左上角停止
pyautogui.PAUSE = 0.1  # 操作间隔


class GameAutomation:
    """游戏自动化主类"""
    
    def __init__(self, game_window_title: str = "Game"):
        self.game_window_title = game_window_title
        self.game_hwnd = None
        self.templates_dir = "templates"
        
        # 创建模板图片目录
        os.makedirs(self.templates_dir, exist_ok=True)
        
    def find_window(self, window_title: str) -> Optional[int]:
        """查找窗口句柄"""
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if window_title.lower() in title.lower():
                    windows.append(hwnd)
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        return windows[0] if windows else None
    
    def activate_window(self, hwnd: int) -> bool:
        """激活窗口"""
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.5)
            return True
        except Exception as e:
            logger.error(f"激活窗口失败: {e}")
            return False
    
    def get_window_rect(self, hwnd: int) -> Tuple[int, int, int, int]:
        """获取窗口坐标"""
        return win32gui.GetWindowRect(hwnd)
    
    def screenshot_window(self, hwnd: int) -> np.ndarray:
        """截取窗口截图"""
        rect = self.get_window_rect(hwnd)
        screenshot = pyautogui.screenshot(region=rect)
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    def find_template(self, template_path: str, threshold: float = 0.8, 
                     screenshot: Optional[np.ndarray] = None) -> Optional[Tuple[int, int]]:
        """在屏幕上查找模板图片"""
        if not os.path.exists(template_path):
            logger.error(f"模板文件不存在: {template_path}")
            return None
        
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None:
            logger.error(f"无法读取模板文件: {template_path}")
            return None
        
        if screenshot is None:
            if self.game_hwnd:
                screenshot = self.screenshot_window(self.game_hwnd)
            else:
                screenshot = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
        
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= threshold:
            h, w = template.shape[:2]
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            
            # 如果是窗口截图，需要转换为屏幕坐标
            if self.game_hwnd:
                rect = self.get_window_rect(self.game_hwnd)
                center_x += rect[0]
                center_y += rect[1]
            
            return (center_x, center_y)
        
        return None
    
    def click_template(self, template_path: str, threshold: float = 0.8) -> bool:
        """点击模板图片位置"""
        position = self.find_template(template_path, threshold)
        if position:
            pyautogui.click(position[0], position[1])
            logger.info(f"点击位置: {position}")
            return True
        else:
            logger.warning(f"未找到模板: {template_path}")
            return False
    
    def wait_for_template(self, template_path: str, timeout: int = 30, 
                         threshold: float = 0.8) -> bool:
        """等待模板出现"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.find_template(template_path, threshold):
                return True
            time.sleep(1)
        return False
    
    def safe_click(self, x: int, y: int, clicks: int = 1, button: str = 'left'):
        """安全点击，避免误操作"""
        try:
            pyautogui.click(x, y, clicks=clicks, button=button)
            time.sleep(0.1)
        except Exception as e:
            logger.error(f"点击失败: {e}")
    
    def safe_type(self, text: str, interval: float = 0.01):
        """安全输入文本"""
        try:
            pyautogui.typewrite(text, interval=interval)
            time.sleep(0.1)
        except Exception as e:
            logger.error(f"输入失败: {e}")
    
    def initialize_game(self) -> bool:
        """初始化游戏窗口"""
        self.game_hwnd = self.find_window(self.game_window_title)
        if not self.game_hwnd:
            logger.error(f"未找到游戏窗口: {self.game_window_title}")
            return False
        
        if not self.activate_window(self.game_hwnd):
            logger.error("激活游戏窗口失败")
            return False
        
        logger.info("游戏窗口初始化成功")
        return True
    
    def login_game(self, username: str, password: str) -> bool:
        """自动登录游戏"""
        try:
            # 等待登录界面
            if not self.wait_for_template(f"{self.templates_dir}/login_button.png", timeout=10):
                logger.error("未找到登录按钮")
                return False
            
            # 点击用户名输入框
            if self.click_template(f"{self.templates_dir}/username_field.png"):
                pyautogui.hotkey('ctrl', 'a')  # 全选
                self.safe_type(username)
            
            # 点击密码输入框
            if self.click_template(f"{self.templates_dir}/password_field.png"):
                pyautogui.hotkey('ctrl', 'a')  # 全选
                self.safe_type(password)
            
            # 点击登录按钮
            if self.click_template(f"{self.templates_dir}/login_button.png"):
                logger.info("登录请求已发送")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"登录失败: {e}")
            return False
    
    def wait_for_game_ready(self, timeout: int = 60) -> bool:
        """等待游戏加载完成"""
        return self.wait_for_template(f"{self.templates_dir}/game_ready.png", timeout)
    
    def find_monster(self) -> Optional[Tuple[int, int]]:
        """查找怪物"""
        monster_templates = [
            f"{self.templates_dir}/monster1.png",
            f"{self.templates_dir}/monster2.png",
            f"{self.templates_dir}/monster3.png"
        ]
        
        for template in monster_templates:
            position = self.find_template(template, threshold=0.7)
            if position:
                logger.info(f"发现怪物: {template}")
                return position
        
        return None
    
    def attack_monster(self, monster_position: Tuple[int, int]) -> bool:
        """攻击怪物"""
        try:
            # 点击怪物
            self.safe_click(monster_position[0], monster_position[1])
            time.sleep(0.5)
            
            # 使用技能攻击
            pyautogui.press('1')  # 假设1是攻击技能
            time.sleep(2)
            
            return True
            
        except Exception as e:
            logger.error(f"攻击失败: {e}")
            return False
    
    def check_character_health(self) -> bool:
        """检查角色血量"""
        # 检查血量是否过低
        if self.find_template(f"{self.templates_dir}/low_health.png", threshold=0.8):
            logger.warning("血量过低，使用回血道具")
            pyautogui.press('r')  # 假设r是回血快捷键
            time.sleep(3)
            return False
        return True
    
    def auto_hunt_monsters(self, duration: int = 3600) -> None:
        """自动打怪"""
        start_time = time.time()
        logger.info(f"开始自动打怪，持续时间: {duration}秒")
        
        while time.time() - start_time < duration:
            try:
                # 检查角色状态
                if not self.check_character_health():
                    continue
                
                # 查找怪物
                monster_pos = self.find_monster()
                if monster_pos:
                    self.attack_monster(monster_pos)
                    time.sleep(1)
                else:
                    # 没有怪物，移动角色
                    self.move_character_randomly()
                    time.sleep(2)
                
                # 避免过度占用CPU
                time.sleep(0.5)
                
            except KeyboardInterrupt:
                logger.info("用户中断打怪")
                break
            except Exception as e:
                logger.error(f"打怪过程中出错: {e}")
                time.sleep(5)
    
    def move_character_randomly(self) -> None:
        """随机移动角色"""
        directions = ['w', 'a', 's', 'd']
        direction = np.random.choice(directions)
        
        pyautogui.keyDown(direction)
        time.sleep(np.random.uniform(0.5, 2.0))
        pyautogui.keyUp(direction)
    
    def run_automation(self, username: str, password: str, hunt_duration: int = 3600) -> bool:
        """运行完整的自动化流程"""
        try:
            # 初始化游戏
            if not self.initialize_game():
                return False
            
            # 登录游戏
            if not self.login_game(username, password):
                logger.error("登录失败")
                return False
            
            # 等待游戏准备就绪
            if not self.wait_for_game_ready():
                logger.error("游戏加载超时")
                return False
            
            # 开始自动打怪
            self.auto_hunt_monsters(hunt_duration)
            
            logger.info("自动化流程完成")
            return True
            
        except Exception as e:
            logger.error(f"自动化流程失败: {e}")
            return False


def main():
    """主函数"""
    # 配置参数
    GAME_WINDOW_TITLE = "Your Game Title"  # 替换为实际游戏窗口标题
    USERNAME = "your_username"  # 替换为实际用户名
    PASSWORD = "your_password"  # 替换为实际密码
    HUNT_DURATION = 3600  # 打怪持续时间（秒）
    
    # 创建自动化实例
    automation = GameAutomation(GAME_WINDOW_TITLE)
    
    # 运行自动化
    success = automation.run_automation(USERNAME, PASSWORD, HUNT_DURATION)
    
    if success:
        logger.info("自动化执行成功")
    else:
        logger.error("自动化执行失败")


if __name__ == "__main__":
    main()