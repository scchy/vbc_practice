import os
from typing import Optional
import openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
    
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
                model="gpt-3.5-turbo",
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
                model="gpt-3.5-turbo",
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

# 全局客户端实例
openai_client = OpenAIClient()