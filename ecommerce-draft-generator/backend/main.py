from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
from contextlib import asynccontextmanager

from database import init_db
from routers import draft, download, image_analysis

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化数据库
    await init_db()
    yield
    # 关闭时清理资源

# 创建 FastAPI 应用
app = FastAPI(
    title="电商草稿生成器 API",
    description="批量生成商品主图草稿 + 标题 + 卖点",
    version="1.0.0",
    lifespan=lifespan
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3060"],  # 前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(draft.router)
app.include_router(download.router)
app.include_router(image_analysis.router)

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"服务器内部错误: {str(exc)}"}
    )

# 健康检查接口
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ecommerce-draft-generator"}

# 根路径
@app.get("/")
async def root():
    return {
        "message": "电商草稿生成器 API",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)