#!/usr/bin/env python3
"""
安装依赖库的脚本
"""

import subprocess
import sys

def install_packages():
    """安装所需的Python包"""
    packages = [
        'pyautogui',
        'opencv-python',
        'numpy',
        'pywin32'
    ]
    
    print("正在安装桌面自动化所需的依赖包...")
    
    for package in packages:
        try:
            print(f"安装 {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ {package} 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"✗ {package} 安装失败: {e}")
    
    print("\n依赖包安装完成!")
    print("现在可以运行 desktop_automation.py 了")

if __name__ == "__main__":
    install_packages()