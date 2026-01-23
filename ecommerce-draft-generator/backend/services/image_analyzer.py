"""
图片分析服务 - 基于阿里云视觉模型分析商品图片并生成电商内容
"""
import os
from typing import Dict, Any, Optional
from PIL import Image
import requests
from io import BytesIO
from services.openai_client import openai_client

class ImageAnalyzer:
    def __init__(self):
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
    
    def validate_image_url(self, image_url: str) -> bool:
        """验证图片URL是否有效"""
        try:
            response = requests.head(image_url, timeout=10)
            content_type = response.headers.get('content-type', '')
            return content_type.startswith('image/')
        except Exception:
            return False
    
    def validate_image_file(self, file_path: str) -> bool:
        """验证本地图片文件是否有效"""
        try:
            with Image.open(file_path) as img:
                # 检查图片格式
                if img.format.lower() not in ['jpeg', 'jpg', 'png', 'webp', 'bmp']:
                    return False
                
                # 检查图片尺寸（最小50x50，最大5000x5000）
                width, height = img.size
                if width < 50 or height < 50 or width > 5000 or height > 5000:
                    return False
                
                return True
        except Exception:
            return False
    
    async def analyze_product_from_url(self, image_url: str) -> Dict[str, Any]:
        """从URL分析商品图片"""
        if not self.validate_image_url(image_url):
            raise ValueError("无效的图片URL或图片格式不支持")
        
        try:
            # 使用阿里云视觉模型分析图片
            analysis_result = await openai_client.analyze_product_image(image_url)
            
            # 基于分析结果生成电商内容
            ecommerce_content = await openai_client.generate_ecommerce_content_from_image(analysis_result)
            
            # 合并结果
            return {
                "success": True,
                "image_analysis": analysis_result,
                "ecommerce_content": ecommerce_content,
                "image_url": image_url
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "fallback": {
                    "image_analysis": {
                        "product_type": "商品",
                        "category": "其他",
                        "selling_points": ["优质材质", "精工制作"],
                        "target_audience": "广大消费者",
                        "keywords": ["商品", "优质"],
                        "description": "这是一款优质的商品"
                    },
                    "ecommerce_content": {
                        "title": "优质商品推荐",
                        "selling_points": "优质材质，精工制作，品质保证",
                        "brand": "优质品牌",
                        "material": "优质材质",
                        "size": "标准尺寸",
                        "color": "经典颜色",
                        "target_group": "广大消费者"
                    }
                }
            }
    
    async def analyze_product_from_file(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """从文件内容分析商品图片"""
        try:
            # 先上传到图床获取URL
            from services.image import image_processor
            
            image_url = await image_processor.upload_to_cloudinary(file_content, filename)
            
            if not image_url:
                raise Exception("图片上传失败")
            
            # 分析图片
            return await self.analyze_product_from_url(image_url)
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "fallback": {
                    "image_analysis": {
                        "product_type": "商品",
                        "category": "其他",
                        "selling_points": ["优质材质", "精工制作"],
                        "target_audience": "广大消费者",
                        "keywords": ["商品", "优质"],
                        "description": "这是一款优质的商品"
                    },
                    "ecommerce_content": {
                        "title": "优质商品推荐",
                        "selling_points": "优质材质，精工制作，品质保证",
                        "brand": "优质品牌",
                        "material": "优质材质",
                        "size": "标准尺寸",
                        "color": "经典颜色",
                        "target_group": "广大消费者"
                    }
                }
            }
    
    def format_analysis_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """格式化分析结果，便于前端展示"""
        if not result.get("success"):
            return {
                "status": "error",
                "message": result.get("error", "分析失败"),
                "data": result.get("fallback", {})
            }
        
        data = result.get("image_analysis", {})
        content = result.get("ecommerce_content", {})
        
        return {
            "status": "success",
            "message": "分析成功",
            "data": {
                "product_info": {
                    "name": data.get("product_type", "商品"),
                    "category": data.get("category", "其他"),
                    "brand": content.get("brand", "优质品牌"),
                    "material": content.get("material", "优质材质"),
                    "size": content.get("size", "标准尺寸"),
                    "color": content.get("color", "经典颜色"),
                    "targetGroup": content.get("target_group", "广大消费者"),
                    "imageUrl": result.get("image_url", "")
                },
                "analysis": {
                    "selling_points": data.get("selling_points", []),
                    "keywords": data.get("keywords", []),
                    "description": data.get("description", ""),
                    "target_audience": data.get("target_audience", "广大消费者")
                },
                "generated_content": {
                    "title": content.get("title", ""),
                    "selling_points": content.get("selling_points", ""),
                    "brand": content.get("brand", ""),
                    "material": content.get("material", ""),
                    "size": content.get("size", ""),
                    "color": content.get("color", ""),
                    "target_group": content.get("target_group", "")
                }
            }
        }

# 全局图片分析器实例
image_analyzer = ImageAnalyzer()