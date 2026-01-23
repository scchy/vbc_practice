#!/bin/bash

# AI电商卖点生成器启动脚本

echo "🚀 启动AI电商卖点生成器..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

# 检查依赖
if [ ! -f "backend/requirements.txt" ]; then
    echo "❌ 依赖文件不存在: backend/requirements.txt"
    exit 1
fi

# 安装依赖
echo "📦 安装Python依赖..."
cd backend
pip install -r requirements.txt

# 检查环境变量
if [ ! -f "../.env" ]; then
    echo "⚠️  环境变量文件不存在，创建默认配置..."
    echo "ALI_API_KEY=your_api_key_here" > ../.env
    echo "❗ 请编辑 .env 文件，设置你的阿里云API密钥"
fi

# 创建上传目录
mkdir -p uploads

# 启动服务
echo "🌟 启动FastAPI服务..."
echo "📍 服务地址: http://localhost:8000"
echo "📝 API文档: http://localhost:8000/docs"
echo ""
echo "✨ 应用已启动！请打开浏览器访问 http://localhost:8000"
echo ""

python main.py