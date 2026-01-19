#!/bin/bash

echo "启动电商草稿生成器..."

# 启动后端服务
echo "启动后端服务..."
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 检查后端是否成功启动
if curl -s http://localhost:8000/health > /dev/null; then
    echo "后端服务启动成功！"
else
    echo "后端服务启动失败！"
    exit 1
fi

# 启动前端服务
echo "启动前端服务..."
cd ../frontend

# 检查是否有 node 或 pnpm
if command -v pnpm &> /dev/null; then
    pnpm dev &
    FRONTEND_PID=$!
elif command -v npm &> /dev/null; then
    npm run dev &
    FRONTEND_PID=$!
elif command -v yarn &> /dev/null; then
    yarn dev &
    FRONTEND_PID=$!
else
    echo "警告：未找到 Node.js 包管理器，前端服务无法启动"
    echo "请手动安装 Node.js 和 pnpm，然后运行：pnpm dev"
fi

echo "=================================="
echo "服务启动完成！"
echo "后端 API: http://localhost:8000"
echo "API 文档: http://localhost:8000/docs"
if [ ! -z "$FRONTEND_PID" ]; then
    echo "前端应用: http://localhost:3060"
fi
echo "=================================="
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
wait