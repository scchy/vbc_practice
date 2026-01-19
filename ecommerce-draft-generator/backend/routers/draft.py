from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict
import uuid
import asyncio
from datetime import datetime

from models import DraftRequest, DraftResponse, JobStatusResponse, ErrorResponse, Draft, Asset
from services.openai_client import openai_client
from services.image import image_processor
from database import get_db_session

router = APIRouter(prefix="/api/draft", tags=["draft"])

# 任务状态存储（实际项目中应该使用 Redis）
job_status_store: Dict[str, Dict] = {}

@router.post("/batch", response_model=DraftResponse)
async def create_draft_batch(
    request: DraftRequest,
    background_tasks: BackgroundTasks
):
    """批量创建草稿任务"""
    # 验证必填字段
    errors = []
    for idx, product in enumerate(request.products):
        required_fields = ['name', 'category', 'brand', 'material', 'size', 'color', 'targetGroup']
        for field in required_fields:
            if not getattr(product, field):
                errors.append({
                    "loc": ["products", idx, field],
                    "msg": f"字段 {field} 不能为空",
                    "type": "value_error"
                })
    
    if errors:
        raise HTTPException(status_code=422, detail=errors)
    
    # 生成任务ID
    job_id = str(uuid.uuid4())
    
    # 初始化任务状态
    job_status_store[job_id] = {
        "total": len(request.products),
        "finished": 0,
        "status": "PENDING",
        "results": [],
        "created_at": datetime.now()
    }
    
    # 如果 saveToAsset 为 true，先保存到素材库
    if request.saveToAsset:
        await save_to_assets(request.products)
    
    # 添加后台任务
    background_tasks.add_task(
        process_draft_batch,
        job_id,
        request.products
    )
    
    return DraftResponse(jobId=job_id)

@router.get("/status/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """获取任务状态"""
    if job_id not in job_status_store:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    job_data = job_status_store[job_id]
    return JobStatusResponse(
        total=job_data["total"],
        finished=job_data["finished"],
        status=job_data["status"],
        results=job_data["results"]
    )

async def save_to_assets(products: List):
    """保存到素材库"""
    async with get_db_session() as session:
        for product in products:
            # 检查是否已存在相同的 name + brand
            existing = await session.execute(
                select(Asset).where(
                    Asset.name == product.name,
                    Asset.brand == product.brand
                )
            )
            existing_asset = existing.scalar_one_or_none()
            
            if existing_asset:
                # 更新图片URL
                if product.imageUrl:
                    existing_asset.image_url = product.imageUrl
                    existing_asset.updated_at = datetime.now()
            else:
                # 创建新素材
                new_asset = Asset(
                    name=product.name,
                    category=product.category,
                    brand=product.brand,
                    material=product.material,
                    size=product.size,
                    color=product.color,
                    target_group=product.targetGroup,
                    image_url=product.imageUrl
                )
                session.add(new_asset)
        
        await session.commit()

async def process_draft_batch(job_id: str, products: List):
    """处理草稿批量生成"""
    job_status_store[job_id]["status"] = "PROCESSING"
    
    try:
        # 逐个处理商品
        for idx, product in enumerate(products):
            try:
                # 生成标题
                title = await openai_client.generate_title(product.dict())
                
                # 生成卖点
                selling_points = await openai_client.generate_selling_points(product.dict())
                
                # 生成主图草稿
                image_url = product.imageUrl
                if image_url:
                    image_url = await image_processor.create_product_image(image_url, title)
                
                # 保存到数据库
                async with get_db_session() as session:
                    draft = Draft(
                        job_id=job_id,
                        product_id=f"{job_id}_{idx}",
                        title=title,
                        selling_points=selling_points,
                        image_url=image_url or "",
                        status="completed"
                    )
                    session.add(draft)
                    await session.commit()
                
                # 更新任务状态
                job_status_store[job_id]["finished"] += 1
                job_status_store[job_id]["results"].append({
                    "productId": f"{job_id}_{idx}",
                    "title": title,
                    "sellingPoints": selling_points,
                    "imageUrl": image_url
                })
                
                # 短暂延迟，避免 API 调用过快
                await asyncio.sleep(0.5)
                
            except Exception as e:
                print(f"处理商品 {idx} 失败: {e}")
                # 记录失败状态
                async with get_db_session() as session:
                    draft = Draft(
                        job_id=job_id,
                        product_id=f"{job_id}_{idx}",
                        title="",
                        selling_points="",
                        image_url="",
                        status="failed"
                    )
                    session.add(draft)
                    await session.commit()
                
                # 仍然增加完成计数
                job_status_store[job_id]["finished"] += 1
        
        # 更新任务状态为完成
        job_status_store[job_id]["status"] = "DONE"
        
    except Exception as e:
        print(f"批处理任务失败: {e}")
        job_status_store[job_id]["status"] = "FAILED"

# 导入需要在函数中使用的模块
from sqlalchemy import select