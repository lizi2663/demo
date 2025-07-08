#!/usr/bin/env python3
import requests
import threading
import json
from concurrent.futures import ThreadPoolExecutor
import time

class LoginTester:
    def __init__(self, url, username, password, thread_count=5):
        self.url = url
        self.login_data = {
            "username": username,
            "password": password
        }
        self.thread_count = thread_count
        self.success_count = 0
        self.fail_count = 0
        self.lock = threading.Lock()
        
    def single_login_request(self, thread_id):
        """单次登录请求"""
        try:
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.post(
                self.url,
                json=self.login_data,
                headers=headers,
                timeout=10
            )
            
            result = response.json()
            
            with self.lock:
                if result.get("code") == 200:
                    self.success_count += 1
                    print(f"Thread {thread_id}: 登录成功 - {result}")
                else:
                    self.fail_count += 1
                    print(f"Thread {thread_id}: 登录失败 - {result}")
                    
        except requests.exceptions.RequestException as e:
            with self.lock:
                self.fail_count += 1
                print(f"Thread {thread_id}: 请求异常 - {e}")
        except json.JSONDecodeError as e:
            with self.lock:
                self.fail_count += 1
                print(f"Thread {thread_id}: JSON解析错误 - {e}")
    
    def run_test(self, request_count=10):
        """运行多线程登录测试"""
        print(f"开始测试: {request_count} 个请求, {self.thread_count} 个线程")
        print(f"目标URL: {self.url}")
        print(f"登录数据: {self.login_data}")
        print("-" * 50)
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.thread_count) as executor:
            futures = []
            for i in range(request_count):
                future = executor.submit(self.single_login_request, i+1)
                futures.append(future)
            
            # 等待所有请求完成
            for future in futures:
                future.result()
        
        end_time = time.time()
        
        print("-" * 50)
        print(f"测试完成!")
        print(f"总请求数: {request_count}")
        print(f"成功次数: {self.success_count}")
        print(f"失败次数: {self.fail_count}")
        print(f"总耗时: {end_time - start_time:.2f} 秒")
        print(f"平均响应时间: {(end_time - start_time) / request_count:.2f} 秒/请求")

def main():
    # 配置参数
    url = "https://web.demo.com/admin/system/index/login"
    username = "admin"
    password = "XYD1"
    
    # 创建测试实例
    tester = LoginTester(url, username, password, thread_count=5)
    
    # 运行测试 (10个请求)
    tester.run_test(request_count=10)

if __name__ == "__main__":
    main()