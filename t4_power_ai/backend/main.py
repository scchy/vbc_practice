from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
import json
import base64
from io import BytesIO
from PIL import Image
import httpx
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI电商卖点生成器", description="基于图片自动生成电商卖点文本和关键词")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 阿里云API配置
ALI_API_KEY = os.getenv("ALI_API_KEY")
ALI_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL_NAME = "qwen3-vl-flash"

# 创建上传目录
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 挂载静态文件
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

async def analyze_image_with_ai(image_base64: str) -> dict:
    """使用阿里云大模型分析图片"""
    headers = {
        "Authorization": f"Bearer {ALI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "请分析这张商品图片，生成电商卖点文本和关键词。要求：1. 生成3-5个吸引人的卖点标题 2. 每个卖点配详细描述 3. 提取10个相关关键词 4. 输出格式为JSON，包含selling_points和keywords两个字段"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 2000
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{ALI_BASE_URL}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60.0
            )
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # 尝试解析JSON格式的响应
            try:
                # 清理可能的markdown格式
                if '```json' in content:
                    content = content.split('```json')[1].split('```')[0]
                elif '```' in content:
                    content = content.split('```')[1].split('```')[0]
                
                parsed_content = json.loads(content.strip())
                return parsed_content
            except json.JSONDecodeError:
                # 如果无法解析JSON，返回原始文本
                return {
                    "selling_points": [{"title": "AI分析结果", "description": content}],
                    "keywords": ["商品", "优质", "推荐"]
                }
                
        except Exception as e:
            print(f"AI分析失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"AI分析失败: {str(e)}")

@app.post("/api/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    """分析上传的图片并生成电商卖点"""
    try:
        # 验证文件类型
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="请上传图片文件")
        
        # 读取图片内容
        contents = await file.read()
        
        # 转换为base64
        image_base64 = base64.b64encode(contents).decode('utf-8')
        
        # 保存原图
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, 'wb') as f:
            f.write(contents)
        
        # AI分析图片
        analysis_result = await analyze_image_with_ai(image_base64)
        
        return {
            "success": True,
            "image_url": f"/uploads/{file.filename}",
            "analysis": analysis_result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")

@app.get("/")
async def read_root():
    """返回前端页面"""
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI电商卖点生成器</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }
            
            .header h1 {
                font-size: 2.5rem;
                margin-bottom: 10px;
                font-weight: 300;
            }
            
            .header p {
                font-size: 1.1rem;
                opacity: 0.9;
            }
            
            .content {
                padding: 40px;
            }
            
            .upload-section {
                text-align: center;
                margin-bottom: 30px;
            }
            
            .upload-area {
                border: 3px dashed #4facfe;
                border-radius: 15px;
                padding: 60px 40px;
                text-align: center;
                background: #f8fbff;
                transition: all 0.3s ease;
                cursor: pointer;
                margin-bottom: 20px;
                position: relative;
            }
            
            .upload-area:hover {
                border-color: #00f2fe;
                background: #f0f8ff;
                transform: translateY(-2px);
            }
            
            .upload-area.dragover {
                border-color: #00f2fe;
                background: #e6f3ff;
            }
            
            .upload-area.has-image {
                padding: 20px;
                border-style: solid;
            }
            
            .upload-icon {
                font-size: 4rem;
                color: #4facfe;
                margin-bottom: 20px;
            }
            
            .upload-text {
                font-size: 1.3rem;
                color: #333;
                margin-bottom: 10px;
            }
            
            .upload-hint {
                color: #666;
                font-size: 0.9rem;
            }
            
            #fileInput {
                display: none;
            }
            
            .image-preview-container {
                position: relative;
                display: inline-block;
                margin: 20px auto;
            }
            
            .preview-image {
                max-width: 300px;
                max-height: 300px;
                border-radius: 10px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                display: block;
            }
            
            .delete-image {
                position: absolute;
                top: -10px;
                right: -10px;
                background: #ff4757;
                color: white;
                border: none;
                border-radius: 50%;
                width: 30px;
                height: 30px;
                font-size: 18px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 2px 5px rgba(0,0,0,0.3);
            }
            
            .delete-image:hover {
                background: #ff3742;
            }
            
            .analyze-button {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                border: none;
                padding: 15px 40px;
                font-size: 1.1rem;
                border-radius: 25px;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 5px 15px rgba(79, 172, 254, 0.4);
                margin-top: 20px;
            }
            
            .analyze-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(79, 172, 254, 0.6);
            }
            
            .analyze-button:disabled {
                background: #ccc;
                cursor: not-allowed;
                transform: none;
                box-shadow: none;
            }
            
            .results-container {
                display: none;
                margin-top: 40px;
            }
            
            .results-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
                margin-top: 30px;
            }
            
            .result-card {
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                border-left: 5px solid #4facfe;
            }
            
            .result-title {
                font-size: 1.5rem;
                color: #333;
                margin-bottom: 20px;
                font-weight: 600;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .selling-points {
                margin-bottom: 0;
            }
            
            .selling-point {
                background: #f8fbff;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 15px;
                border-left: 4px solid #00f2fe;
            }
            
            .selling-point h4 {
                color: #333;
                margin-bottom: 10px;
                font-size: 1.1rem;
            }
            
            .selling-point p {
                color: #666;
                line-height: 1.6;
            }
            
            .keywords {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
            }
            
            .keyword {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 0.9rem;
                font-weight: 500;
            }
            
            .loading {
                display: none;
                text-align: center;
                padding: 40px;
            }
            
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #4facfe;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                animation: spin 1s linear infinite;
                margin: 0 auto 20px;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .error {
                background: #fee;
                color: #c33;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
                display: none;
            }
            
            @media (max-width: 768px) {
                .header h1 {
                    font-size: 2rem;
                }
                
                .content {
                    padding: 20px;
                }
                
                .results-grid {
                    grid-template-columns: 1fr;
                    gap: 20px;
                }
                
                .preview-image {
                    max-width: 100%;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>AI电商卖点生成器</h1>
                <p>上传商品图片，智能生成吸引人的卖点文案和关键词</p>
            </div>
            
            <div class="content">
                <div class="upload-section">
                    <div class="upload-area" id="uploadArea">
                        <div class="upload-icon">📸</div>
                        <div class="upload-text">点击或拖拽上传图片</div>
                        <div class="upload-hint">支持 JPG、PNG、GIF 格式</div>
                        <input type="file" id="fileInput" accept="image/*">
                        <div id="imagePreviewContainer" class="image-preview-container" style="display: none;">
                            <img id="previewImage" class="preview-image" alt="预览图片">
                            <button id="deleteImage" class="delete-image">×</button>
                        </div>
                    </div>
                    <button id="analyzeButton" class="analyze-button" disabled>开始分析</button>
                </div>
                
                <div class="error" id="errorMessage"></div>
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>AI正在分析图片，请稍候...</p>
                </div>
                
                <div class="results-container" id="resultsContainer">
                    <div class="results-grid">
                        <div class="result-card">
                            <h3 class="result-title">🎯 商品卖点</h3>
                            <div id="sellingPoints" class="selling-points"></div>
                        </div>
                        
                        <div class="result-card">
                            <h3 class="result-title">🏷️ 关键词</h3>
                            <div id="keywords" class="keywords"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            const uploadArea = document.getElementById('uploadArea');
            const fileInput = document.getElementById('fileInput');
            const analyzeButton = document.getElementById('analyzeButton');
            const loading = document.getElementById('loading');
            const resultsContainer = document.getElementById('resultsContainer');
            const errorMessage = document.getElementById('errorMessage');
            const previewImage = document.getElementById('previewImage');
            const deleteImage = document.getElementById('deleteImage');
            const imagePreviewContainer = document.getElementById('imagePreviewContainer');
            const sellingPoints = document.getElementById('sellingPoints');
            const keywords = document.getElementById('keywords');
            
            let currentFile = null;
            let uploadedImageUrl = null;
            
            // 点击上传
            uploadArea.addEventListener('click', (e) => {
                if (e.target.id !== 'deleteImage' && !imagePreviewContainer.contains(e.target)) {
                    fileInput.click();
                }
            });
            
            // 文件选择
            fileInput.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    handleFileSelect(file);
                }
            });
            
            // 拖拽上传
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });
            
            uploadArea.addEventListener('dragleave', () => {
                uploadArea.classList.remove('dragover');
            });
            
            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                const file = e.dataTransfer.files[0];
                if (file && file.type.startsWith('image/')) {
                    handleFileSelect(file);
                }
            });
            
            // 删除图片
            deleteImage.addEventListener('click', (e) => {
                e.stopPropagation();
                resetUploadArea();
            });
            
            // 开始分析按钮
            analyzeButton.addEventListener('click', () => {
                if (currentFile) {
                    analyzeImage();
                }
            });
            
            function handleFileSelect(file) {
                // 验证文件类型
                if (!file.type.startsWith('image/')) {
                    showError('请上传图片文件！');
                    return;
                }
                
                // 验证文件大小 (10MB)
                if (file.size > 10 * 1024 * 1024) {
                    showError('图片大小不能超过10MB！');
                    return;
                }
                
                currentFile = file;
                
                // 显示图片预览
                const reader = new FileReader();
                reader.onload = (e) => {
                    previewImage.src = e.target.result;
                    imagePreviewContainer.style.display = 'block';
                    uploadArea.classList.add('has-image');
                    
                    // 隐藏上传提示
                    document.querySelector('.upload-icon').style.display = 'none';
                    document.querySelector('.upload-text').style.display = 'none';
                    document.querySelector('.upload-hint').style.display = 'none';
                    
                    // 启用分析按钮
                    analyzeButton.disabled = false;
                    
                    // 隐藏之前的结果
                    resultsContainer.style.display = 'none';
                    hideError();
                };
                reader.readAsDataURL(file);
            }
            
            function resetUploadArea() {
                currentFile = null;
                uploadedImageUrl = null;
                
                // 重置上传区域
                imagePreviewContainer.style.display = 'none';
                uploadArea.classList.remove('has-image');
                
                // 显示上传提示
                document.querySelector('.upload-icon').style.display = 'block';
                document.querySelector('.upload-text').style.display = 'block';
                document.querySelector('.upload-hint').style.display = 'block';
                
                // 禁用分析按钮
                analyzeButton.disabled = true;
                
                // 清空文件输入
                fileInput.value = '';
                
                // 隐藏结果
                resultsContainer.style.display = 'none';
            }
            
            async function analyzeImage() {
                if (!currentFile) return;
                
                // 显示加载状态
                hideError();
                loading.style.display = 'block';
                
                const formData = new FormData();
                formData.append('file', currentFile);
                
                try {
                    const response = await fetch('/api/analyze-image', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (!response.ok) {
                        throw new Error('分析失败，请重试');
                    }
                    
                    const data = await response.json();
                    displayResults(data);
                    
                } catch (error) {
                    showError(error.message || '分析失败，请重试');
                } finally {
                    loading.style.display = 'none';
                }
            }
            
            function displayResults(data) {
                // 保存图片URL供后续使用
                uploadedImageUrl = data.image_url;
                
                // 显示卖点
                sellingPoints.innerHTML = '';
                if (data.analysis.selling_points) {
                    data.analysis.selling_points.forEach(point => {
                        const pointDiv = document.createElement('div');
                        pointDiv.className = 'selling-point';
                        pointDiv.innerHTML = `
                            <h4>${point.title}</h4>
                            <p>${point.description}</p>
                        `;
                        sellingPoints.appendChild(pointDiv);
                    });
                }
                
                // 显示关键词
                keywords.innerHTML = '';
                if (data.analysis.keywords) {
                    data.analysis.keywords.forEach(keyword => {
                        const keywordSpan = document.createElement('span');
                        keywordSpan.className = 'keyword';
                        keywordSpan.textContent = keyword;
                        keywords.appendChild(keywordSpan);
                    });
                }
                
                resultsContainer.style.display = 'block';
            }
            
            function showError(message) {
                errorMessage.textContent = message;
                errorMessage.style.display = 'block';
            }
            
            function hideError() {
                errorMessage.style.display = 'none';
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)