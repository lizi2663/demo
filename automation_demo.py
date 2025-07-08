#!/usr/bin/env python3
"""
桌面自动化使用示例
演示如何使用desktop_automation.py中的各种功能
"""

from desktop_automation import DesktopAutomation
import time
import cv2

def demo_basic_operations():
    """基本操作演示"""
    print("=== 基本操作演示 ===")
    automation = DesktopAutomation()
    
    # 获取屏幕信息
    width, height = automation.get_screen_size()
    print(f"屏幕尺寸: {width}x{height}")
    
    # 截图演示
    screenshot = automation.take_screenshot()
    cv2.imwrite("full_screenshot.png", screenshot)
    print("全屏截图已保存到 full_screenshot.png")
    
    # 区域截图
    region_screenshot = automation.take_screenshot((0, 0, 500, 400))
    cv2.imwrite("region_screenshot.png", region_screenshot)
    print("区域截图已保存到 region_screenshot.png")

def demo_window_operations():
    """窗口操作演示"""
    print("\n=== 窗口操作演示 ===")
    automation = DesktopAutomation()
    
    # 查找记事本窗口
    notepad_hwnd = automation.find_window_by_title("记事本")
    if notepad_hwnd:
        print(f"找到记事本窗口句柄: {notepad_hwnd}")
        
        # 获取窗口信息
        title = automation.get_window_title(notepad_hwnd)
        rect = automation.get_window_rect(notepad_hwnd)
        pid = automation.get_window_process_id(notepad_hwnd)
        
        print(f"窗口标题: {title}")
        print(f"窗口位置: {rect}")
        print(f"进程ID: {pid}")
        
        # 激活窗口
        automation.activate_window(notepad_hwnd)
        time.sleep(1)
        
        # 在记事本中输入文本
        automation.type_text("这是自动化输入的文本\\n")
        automation.type_text("当前时间: " + time.strftime("%Y-%m-%d %H:%M:%S"))
        
        # 窗口操作
        print("移动窗口到 (100, 100)")
        automation.move_window(notepad_hwnd, 100, 100, 600, 400)
        time.sleep(2)
        
        print("最大化窗口")
        automation.maximize_window(notepad_hwnd)
        time.sleep(2)
        
        print("恢复窗口")
        automation.activate_window(notepad_hwnd)
        
    else:
        print("未找到记事本窗口，请先打开记事本")

def demo_keyboard_mouse():
    """键盘鼠标操作演示"""
    print("\n=== 键盘鼠标操作演示 ===")
    automation = DesktopAutomation()
    
    print("3秒后开始演示，请将鼠标移动到安全位置")
    time.sleep(3)
    
    # 获取当前鼠标位置附近进行操作
    center_x, center_y = automation.get_screen_size()
    center_x //= 2
    center_y //= 2
    
    # 点击操作
    print("执行点击操作")
    automation.click_at(center_x, center_y)
    
    # 拖拽操作
    print("执行拖拽操作")
    automation.drag_to(center_x, center_y, center_x + 100, center_y + 100)
    
    # 键盘操作
    print("执行键盘操作")
    automation.press_key('ctrl')
    automation.key_combination('ctrl', 'a')  # 全选
    automation.type_text("Hello from automation!")
    
    # 滚动操作
    print("执行滚动操作")
    automation.scroll(3)  # 向上滚动
    time.sleep(1)
    automation.scroll(-3)  # 向下滚动

def demo_image_recognition():
    """图像识别演示"""
    print("\n=== 图像识别演示 ===")
    automation = DesktopAutomation()
    
    # 创建一个简单的模板图像用于测试
    import numpy as np
    
    # 创建一个简单的红色方块作为模板
    template = np.zeros((50, 50, 3), dtype=np.uint8)
    template[:, :] = [0, 0, 255]  # 红色
    cv2.imwrite("test_template.png", template)
    print("创建测试模板图像: test_template.png")
    
    # 查找图像（这个例子可能找不到，因为屏幕上没有红色方块）
    result = automation.find_image_on_screen("test_template.png", confidence=0.8)
    if result:
        x, y, w, h = result
        print(f"找到图像位置: ({x}, {y}), 尺寸: {w}x{h}")
        
        # 点击找到的图像
        automation.click_image("test_template.png")
        print("点击了找到的图像")
    else:
        print("未找到模板图像（这是正常的，因为屏幕上没有红色方块）")
    
    # 等待图像出现的演示
    print("等待图像出现演示（5秒超时）")
    result = automation.wait_for_image("test_template.png", timeout=5, confidence=0.8)
    if result:
        print("图像出现了！")
    else:
        print("等待超时，未找到图像")

def demo_advanced_features():
    """高级功能演示"""
    print("\n=== 高级功能演示 ===")
    automation = DesktopAutomation()
    
    # 查找计算器窗口
    calc_hwnd = automation.find_window_by_title("计算器")
    if calc_hwnd:
        print("找到计算器窗口")
        
        # 截取计算器窗口截图
        calc_screenshot = automation.capture_window_screenshot(calc_hwnd)
        cv2.imwrite("calculator_screenshot.png", calc_screenshot)
        print("计算器窗口截图已保存")
        
        # 激活计算器并进行操作
        automation.activate_window(calc_hwnd)
        time.sleep(1)
        
        # 在计算器中输入计算
        automation.type_text("123+456=")
        print("在计算器中输入了 123+456=")
        
    else:
        print("未找到计算器窗口，请先打开计算器")

def main():
    """主函数 - 运行所有演示"""
    print("桌面自动化演示程序")
    print("=" * 40)
    
    try:
        # 基本操作演示
        demo_basic_operations()
        
        # 窗口操作演示
        demo_window_operations()
        
        # 键盘鼠标操作演示
        demo_keyboard_mouse()
        
        # 图像识别演示
        demo_image_recognition()
        
        # 高级功能演示
        demo_advanced_features()
        
    except Exception as e:
        print(f"演示过程中发生错误: {e}")
    
    print("\n演示完成！")

if __name__ == "__main__":
    main()