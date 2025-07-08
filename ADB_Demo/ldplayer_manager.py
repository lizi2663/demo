#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
雷电模拟器自动化管理脚本
用于连接雷电模拟器并管理应用程序
"""

import subprocess
import json
import time
from typing import List, Dict, Optional


def check_adb_available() -> bool:
    """
    检查adb命令是否可用
    
    Returns:
        bool: adb是否可用
    """
    try:
        subprocess.run(['adb', 'version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_connected_devices() -> List[str]:
    """
    获取已连接的设备列表
    
    Returns:
        List[str]: 设备ID列表
    """
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')[1:]  # 跳过标题行
        devices = []
        for line in lines:
            if '\tdevice' in line:
                device_id = line.split('\t')[0]
                devices.append(device_id)
        return devices
    except subprocess.CalledProcessError:
        return []


def connect_ldplayer(port: int = 5555) -> bool:
    """
    连接雷电模拟器
    
    Args:
        port (int): 连接端口，默认5555
        
    Returns:
        bool: 连接是否成功
    """
    try:
        # 连接本地雷电模拟器
        result = subprocess.run(
            ['adb', 'connect', f'127.0.0.1:{port}'],
            capture_output=True,
            text=True,
            check=True
        )
        
        if 'connected' in result.stdout or 'already connected' in result.stdout:
            print(f"✓ 成功连接雷电模拟器 (端口: {port})")
            return True
        else:
            print(f"✗ 连接失败: {result.stdout}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"✗ 连接异常: {e}")
        return False


def get_installed_apps(device_id: Optional[str] = None) -> List[Dict[str, str]]:
    """
    获取已安装应用列表
    
    Args:
        device_id (str, optional): 设备ID，如果为None则使用默认设备
        
    Returns:
        List[Dict[str, str]]: 应用信息列表，包含包名和应用名
    """
    try:
        cmd = ['adb']
        if device_id:
            cmd.extend(['-s', device_id])
        cmd.extend(['shell', 'pm', 'list', 'packages', '-3'])  # -3只显示第三方应用
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        packages = []
        
        for line in result.stdout.strip().split('\n'):
            if line.startswith('package:'):
                package_name = line.replace('package:', '')
                app_name = get_app_name(package_name, device_id)
                packages.append({
                    'package_name': package_name,
                    'app_name': app_name
                })
        
        return packages
        
    except subprocess.CalledProcessError as e:
        print(f"✗ 获取应用列表失败: {e}")
        return []


def get_app_name(package_name: str, device_id: Optional[str] = None) -> str:
    """
    获取应用的显示名称
    
    Args:
        package_name (str): 包名
        device_id (str, optional): 设备ID
        
    Returns:
        str: 应用显示名称
    """
    try:
        cmd = ['adb']
        if device_id:
            cmd.extend(['-s', device_id])
        cmd.extend(['shell', 'dumpsys', 'package', package_name, '|', 'grep', '-A', '1', 'applicationInfo'])
        
        # 由于grep命令在某些系统上可能不可用，我们简化处理
        cmd = ['adb']
        if device_id:
            cmd.extend(['-s', device_id])
        cmd.extend(['shell', 'pm', 'dump', package_name])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # 简单提取应用名，如果失败则返回包名
        lines = result.stdout.split('\n')
        for line in lines:
            if 'versionName=' in line:
                # 这里可以添加更复杂的解析逻辑
                break
                
        return package_name  # 简化处理，直接返回包名
        
    except:
        return package_name


def print_apps_list(apps: List[Dict[str, str]]) -> None:
    """
    格式化打印应用列表
    
    Args:
        apps (List[Dict[str, str]]): 应用列表
    """
    if not apps:
        print("📱 未找到已安装的第三方应用")
        return
    
    print(f"\n📱 已安装应用列表 (共 {len(apps)} 个):")
    print("-" * 80)
    print(f"{'序号':<4} {'包名':<40} {'应用名'}")
    print("-" * 80)
    
    for i, app in enumerate(apps, 1):
        print(f"{i:<4} {app['package_name']:<40} {app['app_name']}")


def main():
    """
    主函数
    """
    print("🚀 雷电模拟器自动化管理工具")
    print("=" * 50)
    
    # 检查adb是否可用
    if not check_adb_available():
        print("✗ 错误: 未找到adb命令，请确保已安装Android SDK")
        return
    
    print("✓ ADB工具检查通过")
    
    # 连接雷电模拟器
    if not connect_ldplayer():
        print("✗ 无法连接雷电模拟器，请确保模拟器已启动")
        return
    
    # 等待连接稳定
    time.sleep(1)
    
    # 获取连接的设备
    devices = get_connected_devices()
    if not devices:
        print("✗ 未找到已连接的设备")
        return
    
    print(f"✓ 找到设备: {', '.join(devices)}")
    
    # 获取应用列表
    device_id = devices[0] if len(devices) == 1 else None
    apps = get_installed_apps(device_id)
    
    # 显示应用列表
    print_apps_list(apps)


if __name__ == "__main__":
    main()