from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import httpx
import zipfile
import io
import csv
from typing import List
from datetime import datetime

router = APIRouter(prefix="/api", tags=["download"])

@router.post("/download-zip")
async def download_zip(image_urls: List[str]):
    """
    下载 ZIP 包，包含：
    1. 所有主图图片（文件名：商品名_主图.png）
    2. CSV 文件包含 title/sellingPoints
    """
    try:
        # 创建内存中的 ZIP 文件
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            csv_data = []
            
            # 下载并添加图片到 ZIP
            for idx, image_url in enumerate(image_urls):
                try:
                    # 下载图片
                    async with httpx.AsyncClient() as client:
                        response = await client.get(image_url, timeout=30)
                        response.raise_for_status()
                    
                    # 生成文件名
                    file_name = f"商品{idx+1}_主图.png"
                    
                    # 添加到 ZIP
                    zip_file.writestr(file_name, response.content)
                    
                    # 这里需要从数据库获取对应的标题和卖点
                    # 由于前端只传了 image_urls，我们需要根据 URL 找到对应的数据
                    # 在实际应用中，这里应该查询数据库获取对应的商品信息
                    csv_data.append({
                        '商品名称': f'商品{idx+1}',
                        '标题': f'标题{idx+1}',
                        '卖点': f'卖点{idx+1}'
                    })
                    
                except Exception as e:
                    print(f"下载图片失败 {image_url}: {e}")
                    continue
            
            # 创建 CSV 文件
            csv_buffer = io.StringIO()
            if csv_data:
                fieldnames = ['商品名称', '标题', '卖点']
                writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_data)
                
                # 添加 CSV 到 ZIP
                zip_file.writestr('商品信息.csv', csv_buffer.getvalue())
        
        # 准备 ZIP 文件用于下载
        zip_buffer.seek(0)
        
        return StreamingResponse(
            io.BytesIO(zip_buffer.getvalue()),
            media_type="application/zip",
            headers={
                "Content-Disposition": f"attachment; filename=商品草稿_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            }
        )
        
    except Exception as e:
        print(f"创建 ZIP 文件失败: {e}")
        raise HTTPException(status_code=500, detail="创建下载文件失败")