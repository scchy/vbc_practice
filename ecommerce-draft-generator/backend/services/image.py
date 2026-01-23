import os
import io
from PIL import Image, ImageDraw, ImageFont
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

# 配置 Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

class ImageProcessor:
    def __init__(self):
        self.canvas_size = (800, 800)
        self.text_area_height = 180
        self.bg_color = (255, 255, 255)  # 白色背景
        self.text_color = (0, 0, 0)      # 黑色文字
        
    def create_product_image(self, product_image_url: str, title: str) -> str:
        """
        创建商品主图草稿
        - 800x800 白色画布
        - 商品图片居中放置
        - 底部 180px 区域显示标题
        """
        try:
            # 创建白色画布
            canvas = Image.new('RGB', self.canvas_size, self.bg_color)
            draw = ImageDraw.Draw(canvas)
            
            # 下载并处理商品图片
            product_image = self._download_and_process_image(product_image_url)
            if product_image:
                # 计算图片放置位置（居中）
                img_width, img_height = product_image.size
                x = (self.canvas_size[0] - img_width) // 2
                y = (self.canvas_size[1] - self.text_area_height - img_height) // 2
                
                # 粘贴商品图片
                canvas.paste(product_image, (x, y))
            
            # 添加标题文字
            self._add_title_text(draw, title)
            
            # 保存到内存
            img_buffer = io.BytesIO()
            canvas.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            # 上传到 Cloudinary
            upload_result = cloudinary.uploader.upload(
                img_buffer,
                folder="ecommerce-drafts",
                format="png"
            )
            
            return upload_result['secure_url']
            
        except Exception as e:
            print(f"创建商品图片失败: {e}")
            # fallback: 返回原图片URL
            return product_image_url
    
    def _download_and_process_image(self, image_url: str) -> Optional[Image.Image]:
        """下载并处理图片"""
        try:
            # 下载图片
            import httpx
            response = httpx.get(image_url, timeout=30)
            response.raise_for_status()
            
            # 打开图片
            image = Image.open(io.BytesIO(response.content))
            
            # 转换为 RGB 模式（处理 PNG 透明背景）
            if image.mode in ('RGBA', 'LA'):
                bg = Image.new('RGB', image.size, (255, 255, 255))
                bg.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = bg
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            # 计算缩放比例，确保图片适合画布（留出文字区域）
            max_width = self.canvas_size[0] - 40  # 左右各留 20px 边距
            max_height = self.canvas_size[1] - self.text_area_height - 40  # 上下各留 20px 边距
            
            width_ratio = max_width / image.width
            height_ratio = max_height / image.height
            scale_ratio = min(width_ratio, height_ratio, 1.0)  # 不超过原图大小
            
            new_width = int(image.width * scale_ratio)
            new_height = int(image.height * scale_ratio)
            
            # 缩放图片
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            return image
            
        except Exception as e:
            print(f"处理图片失败: {e}")
            return None
    
    def _add_title_text(self, draw: ImageDraw.Draw, title: str):
        """添加标题文字"""
        try:
            # 限制标题长度（前18个字）
            display_title = title[:18]
            
            # 计算字体大小（自适应）
            max_font_size = 48
            min_font_size = 24
            
            # 根据标题长度调整字体大小
            if len(display_title) <= 10:
                font_size = max_font_size
            elif len(display_title) <= 15:
                font_size = 36
            else:
                font_size = min_font_size
            
            # 尝试使用思源黑体，如果不可用则使用默认字体
            try:
                font = ImageFont.truetype("SourceHanSansSC-Regular.otf", font_size)
            except:
                try:
                    font = ImageFont.truetype("SimHei.ttf", font_size)
                except:
                    font = ImageFont.load_default()
            
            # 文字区域
            text_area_top = self.canvas_size[1] - self.text_area_height
            
            # 计算文字位置（居中）
            bbox = draw.textbbox((0, 0), display_title, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (self.canvas_size[0] - text_width) // 2
            y = text_area_top + (self.text_area_height - text_height) // 2
            
            # 绘制文字
            draw.text((x, y), display_title, font=font, fill=self.text_color)
            
        except Exception as e:
            print(f"添加文字失败: {e}")

    async def upload_to_cloudinary(self, file_content: bytes, filename: str) -> Optional[str]:
        """上传图片到Cloudinary"""
        try:
            # 上传到 Cloudinary
            upload_result = cloudinary.uploader.upload(
                file_content,
                folder="ecommerce-analysis",
                format="webp",
                quality="auto:good",
                width=800,
                height=800,
                crop="limit"
            )
            
            return upload_result['secure_url']
            
        except Exception as e:
            print(f"上传到Cloudinary失败: {e}")
            return None

# 全局图片处理器实例
image_processor = ImageProcessor()