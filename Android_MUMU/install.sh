#!/bin/bash

echo "=== 雷电模拟器快手自动化脚本安装器 ==="

# 检查Python版本
python_version=$(python --version 2>&1)
if [[ $? -ne 0 ]]; then
    echo "❌ 未检测到Python，请先安装Python 3.7+"
    exit 1
else
    echo "✅ 检测到: $python_version"
fi

# 创建虚拟环境（可选）
read -p "是否创建虚拟环境? (y/n): " create_venv
if [[ $create_venv == "y" || $create_venv == "Y" ]]; then
    echo "创建虚拟环境..."
    python -m venv venv
    source venv/bin/activate
    echo "✅ 虚拟环境已激活"
fi

# 安装依赖
echo "安装Python依赖包..."
pip install -r requirements.txt

if [[ $? -eq 0 ]]; then
    echo "✅ 依赖安装成功"
else
    echo "❌ 依赖安装失败"
    exit 1
fi

# 检查templates目录
if [[ ! -d "templates" ]]; then
    mkdir templates
    echo "✅ 已创建templates目录"
fi

# 创建示例配置
if [[ ! -f "config.json" ]]; then
    echo "✅ config.json已存在"
else
    echo "⚠️  请配置config.json文件"
fi

echo ""
echo "🎉 安装完成！"
echo ""
echo "下一步："
echo "1. 将快手相关UI元素截图放入templates/目录"
echo "2. 根据需要修改config.json配置"
echo "3. 运行: python kuaishou_automation.py"
echo ""
echo "详细使用说明请查看: README.md"