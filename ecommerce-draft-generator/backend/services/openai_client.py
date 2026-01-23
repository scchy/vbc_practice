import os
from typing import Optional, Dict, Any
import openai
from openai import OpenAI
from dotenv import load_dotenv
import base64
import requests

load_dotenv()

class OpenAIClient:
    def __init__(self):
        # 原有 DeepSeek 客户端
        self.deepseek_client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY")
        )
        
        # 阿里云视觉模型配置
        self.ali_api_key = os.getenv("ALI_API_KEY")
        self.ali_base_url = os.getenv("ALI_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
        self.model_name = os.getenv("MODEL_NAME", "qwen3-vl-flash")
        
        # 阿里云客户端
        if self.ali_api_key:
            self.ali_client = OpenAI(
                api_key=self.ali_api_key,
                base_url=self.ali_base_url
            )
        else:
            self.ali_client = None
    
    async def generate_title(self, product_data: dict) -> str:
        """生成商品标题"""
        prompt = f"""
You are an e-commerce copywriter.
Create a 30-character-max Chinese title that includes the core keyword and selling point.
Product: {product_data['name']}, Category: {product_data['category']}, Brand: {product_data['brand']}, Material: {product_data['material']}, Size: {product_data['size']}, Color: {product_data['color']}, Target: {product_data['targetGroup']}
Only return the title, no quotes.
"""
        
        try:
            response = await self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a professional e-commerce copywriter."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=80
            )
            
            title = response.choices[0].message.content.strip()
            # 确保标题不超过30个字符
            if len(title) > 30:
                title = title[:30]
            return title
        except Exception as e:
            print(f"生成标题失败: {e}")
            #  fallback: 使用商品名称作为标题
            return product_data['name'][:30]
    
    async def generate_selling_points(self, product_data: dict) -> str:
        """生成商品卖点"""
        prompt = f"""
Write 1-2 short Chinese sentences (≤60 characters total) highlighting the biggest benefit.
Product: {product_data['name']}, Category: {product_data['category']}, Brand: {product_data['brand']}, Material: {product_data['material']}, Size: {product_data['size']}, Color: {product_data['color']}, Target: {product_data['targetGroup']}
Only return the sentences.
"""
        
        try:
            response = await self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a professional e-commerce copywriter."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=120
            )
            
            selling_points = response.choices[0].message.content.strip()
            # 确保不超过60个字符
            if len(selling_points) > 60:
                selling_points = selling_points[:60]
            return selling_points
        except Exception as e:
            print(f"生成卖点失败: {e}")
            # fallback: 使用简单的卖点
            return f"{product_data['brand']}品牌，{product_data['material']}材质，品质保证"[:60]

    async def analyze_product_image(self, image_url: str) -> Dict[str, Any]:
        """分析商品图片，提取卖点和关键词"""
        if not self.ali_client:
            raise Exception("阿里云视觉模型未配置")
        
        try:
            # 构建视觉理解请求
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        },
                        {
                            "type": "text",
                            "text": """请详细分析这张商品图片，提供以下信息：

1. 商品类型和类别
2. 主要特征和卖点（3-5个）
3. 目标用户群体
4. 关键词（5-8个）
5. 商品描述（50-100字）

请以JSON格式返回，结构如下：
{
    "product_type": "商品类型",
    "category": "商品类别",
    "selling_points": ["卖点1", "卖点2", "卖点3"],
    "target_audience": "目标用户群体",
    "keywords": ["关键词1", "关键词2", "关键词3"],
    "description": "商品描述"
}"""
                        }
                    ]
                }
            ]
            
            response = await self.ali_client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.3,
                max_tokens=1000
            )
            
            # 解析返回的JSON
            content = response.choices[0].message.content
            import json
            
            # 清理可能的markdown格式
            content = content.strip()
            if content.startswith('```json'):
                content = content[7:-3].strip()
            elif content.startswith('```'):
                content = content[3:-3].strip()
            
            result = json.loads(content)
            return result
            
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}")
            # Fallback: 返回基础信息
            return {
                "product_type": "未知商品",
                "category": "其他",
                "selling_points": ["优质材质", "精工制作", "实用性强"],
                "target_audience": "广大消费者",
                "keywords": ["商品", "优质", "实用"],
                "description": "这是一款优质的商品，具有良好的品质和实用性。"
            }
        except Exception as e:
            print(f"图片分析失败: {e}")
            # Fallback: 返回基础信息
            return {
                "product_type": "未知商品",
                "category": "其他",
                "selling_points": ["优质材质", "精工制作", "实用性强"],
                "target_audience": "广大消费者",
                "keywords": ["商品", "优质", "实用"],
                "description": "这是一款优质的商品，具有良好的品质和实用性。"
            }
    
    async def generate_ecommerce_content_from_image(self, image_analysis: Dict[str, Any]) -> Dict[str, str]:
        """基于图片分析结果生成电商内容"""
        try:
            # 使用 DeepSeek 生成电商内容
            prompt = f"""
基于以下商品信息，生成电商卖点文本：

商品类型：{image_analysis['product_type']}
商品类别：{image_analysis['category']}
主要卖点：{', '.join(image_analysis['selling_points'])}
目标用户：{image_analysis['target_audience']}
关键词：{', '.join(image_analysis['keywords'])}
商品描述：{image_analysis['description']}

请生成以下内容：
1. 商品标题（不超过30字，包含核心关键词）
2. 卖点文案（1-2句话，不超过60字）
3. 商品属性（品牌、材质、尺寸、颜色、适用人群）

以JSON格式返回：
{{
    "title": "商品标题",
    "selling_points": "卖点文案",
    "brand": "品牌名称",
    "material": "材质",
    "size": "尺寸",
    "color": "颜色",
    "target_group": "适用人群"
}}
"""
            
            response = await self.deepseek_client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个专业的电商文案策划师，擅长创作吸引人的商品标题和卖点文案。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            import json
            
            # 清理可能的markdown格式
            if content.startswith('```json'):
                content = content[7:-3].strip()
            elif content.startswith('```'):
                content = content[3:-3].strip()
            
            result = json.loads(content)
            return result
            
        except Exception as e:
            print(f"电商内容生成失败: {e}")
            # Fallback: 基于分析结果生成基础内容
            return {
                "title": f"{image_analysis['product_type']} - {image_analysis['selling_points'][0] if image_analysis['selling_points'] else '优质商品'}",
                "selling_points": image_analysis['description'][:60],
                "brand": "优质品牌",
                "material": "优质材质",
                "size": "标准尺寸",
                "color": "经典颜色",
                "target_group": image_analysis['target_audience']
            }

# 全局客户端实例
openai_client = OpenAIClient()