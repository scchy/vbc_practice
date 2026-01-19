from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

Base = declarative_base()

# 数据库模型
class Asset(Base):
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    brand = Column(String(100), nullable=False)
    material = Column(String(100), nullable=False)
    size = Column(String(50), nullable=False)
    color = Column(String(50), nullable=False)
    target_group = Column(String(100), nullable=False)
    image_url = Column(String(500))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Draft(Base):
    __tablename__ = "drafts"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(100), nullable=False, index=True)
    product_id = Column(String(100), nullable=False)
    title = Column(String(200), nullable=False)
    selling_points = Column(Text, nullable=False)
    image_url = Column(String(500), nullable=False)
    status = Column(String(20), default='pending')  # pending, processing, completed, failed
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

# Pydantic 模型
class Product(BaseModel):
    name: str = Field(..., description="商品名称")
    category: str = Field(..., description="商品分类")
    brand: str = Field(..., description="品牌")
    material: str = Field(..., description="材质")
    size: str = Field(..., description="尺寸")
    color: str = Field(..., description="颜色")
    targetGroup: str = Field(..., description="目标人群")
    imageUrl: Optional[str] = Field(None, description="图片URL")

class DraftRequest(BaseModel):
    products: List[Product] = Field(..., description="商品列表")
    saveToAsset: bool = Field(False, description="是否保存到素材库")

class DraftResponse(BaseModel):
    jobId: str = Field(..., description="任务ID")

class JobStatusResponse(BaseModel):
    total: int = Field(..., description="总任务数")
    finished: int = Field(..., description="已完成数")
    status: str = Field(..., description="任务状态")
    results: List[dict] = Field(default_factory=list, description="结果列表")

class ErrorResponse(BaseModel):
    detail: List[dict] = Field(..., description="错误详情")

# 素材库相关模型
class AssetCreate(BaseModel):
    name: str
    category: str
    brand: str
    material: str
    size: str
    color: str
    target_group: str
    image_url: Optional[str] = None

class AssetResponse(BaseModel):
    id: int
    name: str
    category: str
    brand: str
    material: str
    size: str
    color: str
    target_group: str
    image_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True