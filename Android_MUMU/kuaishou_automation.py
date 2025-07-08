#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
雷电模拟器快手视频自动化脚本
合法自动化工具，用于教育和研究目的
"""

import time
import cv2
import numpy as np
import pyautogui
import subprocess
import os
import json
import logging
import psutil
from typing import Tuple, Optional, List, Dict, Any

# 禁用pyautogui安全检查，允许鼠标移动到屏幕角落
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 1

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self._get_default_config()
        except Exception as e:
            logging.error(f"加载配置文件失败: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "memu": {
                "executable_path": "",
                "startup_timeout": 30,
                "window_title": "MEmu"
            },
            "automation": {
                "video_watch_time": 5,
                "scroll_duration": 0.5,
                "interaction_delay": 1,
                "like_probability": 0.3,
                "follow_probability": 0.1,
                "max_videos": 20
            },
            "image_recognition": {
                "confidence_threshold": 0.8,
                "template_timeout": 30,
                "template_directory": "templates"
            },
            "safety": {
                "enable_failsafe": True,
                "pause_between_actions": 1,
                "max_retries": 3
            },
            "logging": {
                "level": "INFO",
                "file": "automation.log",
                "max_size_mb": 10
            }
        }
    
    def get(self, key_path: str, default=None):
        """获取配置值"""
        keys = key_path.split('.')
        value = self.config
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

class Logger:
    """日志管理器"""
    
    def __init__(self, config: ConfigManager):
        self.config = config
        self._setup_logger()
    
    def _setup_logger(self):
        """设置日志"""
        log_level = getattr(logging, self.config.get('logging.level', 'INFO'))
        log_file = self.config.get('logging.file', 'automation.log')
        max_size = self.config.get('logging.max_size_mb', 10) * 1024 * 1024
        
        # 配置日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 文件处理器
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_size, backupCount=3, encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # 配置根日志器
        logging.basicConfig(
            level=log_level,
            handlers=[file_handler, console_handler]
        )

class MemuAutomation:
    """雷电模拟器自动化类"""
    
    def __init__(self, config: ConfigManager):
        """
        初始化雷电模拟器自动化
        :param config: 配置管理器
        """
        self.config = config
        self.memu_path = self.config.get('memu.executable_path') or self._find_memu_path()
        self.screen_size = pyautogui.size()
        self.max_retries = self.config.get('safety.max_retries', 3)
        
    def _find_memu_path(self) -> str:
        """自动查找雷电模拟器安装路径"""
        common_paths = [
            "C:\\Program Files\\Microvirt\\MEmu\\MEmu.exe",
            "D:\\Program Files\\Microvirt\\MEmu\\MEmu.exe",
            "C:\\MEmu\\MEmu.exe"
        ]
        for path in common_paths:
            if os.path.exists(path):
                logging.info(f"找到雷电模拟器: {path}")
                return path
        logging.warning("未找到雷电模拟器安装路径")
        return ""
    
    def is_memu_running(self) -> bool:
        """检查雷电模拟器是否正在运行"""
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if 'MEmu' in proc.info['name']:
                    return True
            return False
        except Exception as e:
            logging.error(f"检查模拟器运行状态失败: {e}")
            return False
    
    def start_memu(self) -> bool:
        """启动雷电模拟器"""
        retries = 0
        while retries < self.max_retries:
            try:
                if self.is_memu_running():
                    logging.info("雷电模拟器已运行")
                    return True
                    
                if self.memu_path and os.path.exists(self.memu_path):
                    logging.info("启动雷电模拟器...")
                    subprocess.Popen([self.memu_path])
                    
                    # 等待启动
                    timeout = self.config.get('memu.startup_timeout', 30)
                    start_time = time.time()
                    while time.time() - start_time < timeout:
                        if self.is_memu_running():
                            logging.info("雷电模拟器启动成功")
                            time.sleep(5)  # 额外等待确保完全启动
                            return True
                        time.sleep(2)
                    
                    logging.error(f"雷电模拟器启动超时 ({timeout}秒)")
                    return False
                else:
                    logging.error("未找到雷电模拟器，请手动启动或配置路径")
                    return False
                    
            except Exception as e:
                retries += 1
                logging.error(f"启动雷电模拟器失败 (尝试 {retries}/{self.max_retries}): {e}")
                if retries < self.max_retries:
                    time.sleep(5)
                    
        return False
    
    def find_window(self) -> Optional[Tuple[int, int, int, int]]:
        """查找雷电模拟器窗口位置"""
        try:
            import win32gui
            
            def enum_windows_proc(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_text = win32gui.GetWindowText(hwnd)
                    if "MEmu" in window_text:
                        rect = win32gui.GetWindowRect(hwnd)
                        windows.append(rect)
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_proc, windows)
            
            if windows:
                logging.info(f"找到雷电模拟器窗口: {windows[0]}")
                return windows[0]
            else:
                logging.warning("未找到雷电模拟器窗口")
                return None
                
        except ImportError:
            logging.warning("win32gui模块未安装，无法获取窗口位置")
            return None
        except Exception as e:
            logging.error(f"查找窗口失败: {e}")
            return None

class ImageRecognition:
    """图像识别工具类"""
    
    @staticmethod
    def find_image_on_screen(template_path: str, confidence: float = 0.8) -> Optional[Tuple[int, int]]:
        """
        在屏幕上查找指定图像
        :param template_path: 模板图像路径
        :param confidence: 匹配置信度
        :return: 找到的位置坐标 (x, y)
        """
        try:
            # 截取当前屏幕
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)
            
            # 读取模板图像
            if not os.path.exists(template_path):
                print(f"模板图像不存在: {template_path}")
                return None
                
            template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
            if template is None:
                print(f"无法读取模板图像: {template_path}")
                return None
            
            # 模板匹配
            result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= confidence:
                # 返回模板中心点坐标
                h, w = template.shape
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                return (center_x, center_y)
            else:
                return None
                
        except Exception as e:
            print(f"图像识别失败: {e}")
            return None
    
    @staticmethod
    def wait_for_image(template_path: str, timeout: int = 30, confidence: float = 0.8) -> Optional[Tuple[int, int]]:
        """
        等待图像出现
        :param template_path: 模板图像路径
        :param timeout: 超时时间（秒）
        :param confidence: 匹配置信度
        :return: 找到的位置坐标
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            position = ImageRecognition.find_image_on_screen(template_path, confidence)
            if position:
                return position
            time.sleep(1)
        print(f"等待图像超时: {template_path}")
        return None

class KuaishouAutomation:
    """快手自动化操作类"""
    
    def __init__(self):
        self.image_recognition = ImageRecognition()
    
    def open_kuaishou(self) -> bool:
        """打开快手应用"""
        try:
            # 查找快手图标
            kuaishou_icon = self.image_recognition.wait_for_image("templates/kuaishou_icon.png", timeout=10)
            if kuaishou_icon:
                pyautogui.click(kuaishou_icon)
                time.sleep(3)
                return True
            else:
                print("未找到快手图标")
                return False
        except Exception as e:
            print(f"打开快手失败: {e}")
            return False
    
    def scroll_videos(self, count: int = 10) -> None:
        """
        滚动浏览视频
        :param count: 滚动次数
        """
        try:
            for i in range(count):
                # 向上滑动切换到下一个视频
                pyautogui.swipe(400, 600, 400, 200, duration=0.5)
                # 观看视频一段时间
                time.sleep(5)
                print(f"已观看视频 {i+1}/{count}")
        except Exception as e:
            print(f"滚动视频失败: {e}")
    
    def like_video(self) -> bool:
        """点赞当前视频"""
        try:
            like_button = self.image_recognition.find_image_on_screen("templates/like_button.png")
            if like_button:
                pyautogui.click(like_button)
                time.sleep(1)
                return True
            return False
        except Exception as e:
            print(f"点赞失败: {e}")
            return False
    
    def follow_user(self) -> bool:
        """关注当前视频作者"""
        try:
            follow_button = self.image_recognition.find_image_on_screen("templates/follow_button.png")
            if follow_button:
                pyautogui.click(follow_button)
                time.sleep(1)
                return True
            return False
        except Exception as e:
            print(f"关注失败: {e}")
            return False
    
    def auto_interact(self, like_probability: float = 0.3, follow_probability: float = 0.1) -> None:
        """
        自动互动（点赞、关注）
        :param like_probability: 点赞概率
        :param follow_probability: 关注概率
        """
        import random
        
        if random.random() < like_probability:
            if self.like_video():
                print("已点赞")
        
        if random.random() < follow_probability:
            if self.follow_user():
                print("已关注")

def create_template_directory():
    """创建模板图像目录"""
    template_dir = "templates"
    if not os.path.exists(template_dir):
        os.makedirs(template_dir)
        print(f"已创建模板目录: {template_dir}")
        print("请将以下模板图像放入templates目录：")
        print("- kuaishou_icon.png (快手应用图标)")
        print("- like_button.png (点赞按钮)")
        print("- follow_button.png (关注按钮)")

def main():
    """主函数"""
    print("=== 雷电模拟器快手自动化脚本 ===")
    
    # 创建模板目录
    create_template_directory()
    
    # 初始化组件
    memu = MemuAutomation()
    kuaishou = KuaishouAutomation()
    
    try:
        # 启动雷电模拟器
        print("启动雷电模拟器...")
        if not memu.start_memu():
            print("请手动启动雷电模拟器")
            input("启动完成后按回车键继续...")
        
        # 等待模拟器完全启动
        print("等待模拟器启动完成...")
        time.sleep(10)
        
        # 打开快手
        print("打开快手应用...")
        if kuaishou.open_kuaishou():
            print("快手已打开，开始自动浏览...")
            
            # 自动浏览视频
            video_count = 20  # 观看视频数量
            for i in range(video_count):
                print(f"\n观看第 {i+1} 个视频...")
                
                # 观看当前视频
                time.sleep(5)
                
                # 随机互动
                kuaishou.auto_interact()
                
                # 切换到下一个视频
                pyautogui.swipe(400, 600, 400, 200, duration=0.5)
                time.sleep(2)
                
        else:
            print("无法打开快手应用")
            
    except KeyboardInterrupt:
        print("\n用户中断操作")
    except Exception as e:
        print(f"运行错误: {e}")
    
    print("脚本执行完成")

if __name__ == "__main__":
    main()