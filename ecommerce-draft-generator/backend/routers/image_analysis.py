"""
图片分析路由 - 处理商品图片分析和内容生成
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Optional, Dict, Any
import uuid
from pydantic import BaseModel

from services.image_analyzer import image_analyzer
from services.image import image_processor

router = APIRouter(prefix="/api/image-analysis", tags=["image-analysis"])

# 请求和响应模型
class ImageAnalysisRequest(BaseModel):
    image_url: Optional[str] = None
    
class ImageAnalysisResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    job_id: Optional[str] = None

class ImageUploadResponse(BaseModel):
    success: bool
    message: str
    image_url: Optional[str] = None

@router.post("/analyze-from-url", response_model=ImageAnalysisResponse)
async def analyze_image_from_url(request: ImageAnalysisRequest):
    """从URL分析商品图片"""
    if not request.image_url:
        raise HTTPException(status_code=400, detail="图片URL不能为空")
    
    job_id = str(uuid.uuid4())
    
    try:
        # 分析图片
        result = await image_analyzer.analyze_product_from_url(request.image_url)
        
        # 格式化结果
        formatted_result = image_analyzer.format_analysis_result(result)
        
        return ImageAnalysisResponse(
            success=formatted_result["status"] == "success",
            message=formatted_result["message"],
            data=formatted_result["data"],
            job_id=job_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"图片分析失败: {str(e)}")

@router.post("/analyze-from-upload", response_model=ImageAnalysisResponse)
async def analyze_image_from_upload(file: UploadFile = File(...)):
    """从上传文件分析商品图片"""
    if not file:
        raise HTTPException(status_code=400, detail="未上传图片文件")
    
    # 验证文件类型
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp", "image/bmp"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"不支持的图片格式: {file.content_type}")
    
    job_id = str(uuid.uuid4())
    
    try:
        # 读取文件内容
        content = await file.read()
        
        # 验证文件大小（最大10MB）
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="图片文件过大，请上传小于10MB的图片")
        
        # 分析图片
        result = await image_analyzer.analyze_product_from_file(content, file.filename)
        
        # 格式化结果
        formatted_result = image_analyzer.format_analysis_result(result)
        
        return ImageAnalysisResponse(
            success=formatted_result["status"] == "success",
            message=formatted_result["message"],
            data=formatted_result["data"],
            job_id=job_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"图片分析失败: {str(e)}")

@router.post("/upload-image", response_model=ImageUploadResponse)
async def upload_image(file: UploadFile = File(...)):
    """上传图片到图床"""
    if not file:
        raise HTTPException(status_code=400, detail="未上传图片文件")
    
    # 验证文件类型
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp", "image/bmp"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"不支持的图片格式: {file.content_type}")
    
    try:
        # 读取文件内容
        content = await file.read()
        
        # 验证文件大小（最大10MB）
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="图片文件过大，请上传小于10MB的图片")
        
        # 上传到Cloudinary
        image_url = await image_processor.upload_to_cloudinary(content, file.filename)
        
        if not image_url:
            raise HTTPException(status_code=500, detail="图片上传失败")
        
        return ImageUploadResponse(
            success=True,
            message="图片上传成功",
            image_url=image_url
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"图片上传失败: {str(e)}")

@router.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "image-analysis"}