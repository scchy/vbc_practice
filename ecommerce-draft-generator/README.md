# 电商草稿生成器

批量生成商品主图草稿 + 标题 + 卖点，支持 Excel 导入和图片上传。

## 功能特性

- 📊 **Excel 批量导入**：支持 xlsx 文件，自动解析商品信息
- 🖼️ **图片批量上传**：拖拽上传，自动压缩到 800px 宽，< 200KB
- 🤖 **AI 智能生成**：调用 OpenAI GPT-3.5 生成标题和卖点
- 🎨 **主图草稿生成**：使用 Pillow 在白色画布上生成带文字的主图
- 📦 **一键打包下载**：支持 ZIP 格式下载所有主图和商品信息 CSV
- 🔄 **异步处理**：FastAPI BackgroundTasks 异步处理，前端轮询进度
- 💾 **素材库管理**：可选保存商品信息到素材库，支持复用

## 技术栈

### 前端
- Vue 3 + `<script setup>`
- Naive UI 组件库
- Pinia 状态管理
- Vite 构建工具

### 后端
- FastAPI
- SQLAlchemy + SQLite
- OpenAI API
- Pillow 图像处理
- Cloudinary 图床

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd ecommerce-draft-generator

# 安装前端依赖
cd frontend
pnpm install

# 安装后端依赖
cd ../backend
pip install -r requirements.txt
```

### 2. 环境变量配置

复制环境变量模板：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入必要的 API 密钥：

```env
# OpenAI API 密钥
OPENAI_API_KEY=your_openai_api_key_here

# Cloudinary 配置
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### 3. 启动服务

```bash
# 启动后端（端口 8000）
cd backend
python -m uvicorn main:app --reload

# 启动前端（端口 3060）
cd frontend
pnpm dev
```

访问 http://localhost:3060 查看应用。

## API 文档

后端 API 文档：http://localhost:8000/docs

## 使用说明

### 1. 上传 Excel 文件

Excel 文件必须包含以下列头：
- `name`: 商品名称
- `category`: 商品分类
- `brand`: 品牌
- `material`: 材质
- `size`: 尺寸
- `color`: 颜色
- `targetGroup`: 目标人群

其他列将被忽略。

### 2. 上传商品图片

- 支持批量拖拽上传
- 自动压缩到 800px 宽，< 200KB
- 格式转换为 WebP
- 上传到 Cloudinary 图床

### 3. 生成草稿

点击"生成草稿"按钮，系统将：
1. 验证数据完整性
2. 异步调用 OpenAI 生成标题和卖点
3. 使用 Pillow 生成主图草稿
4. 保存结果到数据库

### 4. 下载结果

生成完成后，可以：
- 在线预览主图
- 复制标题和卖点
- 一键打包下载 ZIP 文件

## 项目结构

```
ecommerce-draft-generator/
├─ frontend/                    # Vue3 前端
│  ├─ src/
│  │  ├─ components/           # Vue 组件
│  │  │  ├─ UploadCard.vue     # 上传组件
│  │  │  ├─ ProductTable.vue   # 商品表格
│  │  │  └─ DraftResults.vue   # 结果展示
│  │  ├─ pages/
│  │  │  └─ UploadPage.vue     # 主页面
│  │  ├─ stores/
│  │  │  └─ upload.ts          # 状态管理
│  │  ├─ api/
│  │  │  └─ index.ts           # API 接口
│  │  └─ main.ts               # 应用入口
│  ├─ package.json
│  └─ vite.config.ts
├─ backend/                     # FastAPI 后端
│  ├─ routers/
│  │  ├─ draft.py              # 草稿相关路由
│  │  └─ download.py           # 下载路由
│  ├─ services/
│  │  ├─ openai_client.py      # OpenAI 客户端
│  │  └─ image.py              # 图片处理服务
│  ├─ main.py                  # 应用主文件
│  ├─ models.py                # 数据模型
│  ├─ database.py              # 数据库连接
│  └─ requirements.txt         # Python 依赖
└─ README.md
```

## 性能指标

- **响应时间**: 3 秒内看到第一条草稿结果
- **处理速度**: 15 秒内完成 10 个商品的批量处理
- **图片压缩**: 自动压缩到 < 200KB，保持高质量
- **并发处理**: 支持异步批量处理

## 注意事项

1. **API 配额**: OpenAI API 有调用频率限制，大量处理时请注意配额
2. **图片大小**: 上传图片会自动压缩，但建议原始图片不要超过 2MB
3. **Excel 格式**: 确保 Excel 文件格式正确，列头必须完全匹配
4. **网络环境**: 需要稳定的网络连接以访问 OpenAI 和 Cloudinary 服务

## 开发计划

### Phase-1 MVP ✅
- [x] Excel 批量导入
- [x] 图片批量上传和压缩
- [x] AI 标题和卖点生成
- [x] 主图草稿生成
- [x] 异步任务处理
- [x] 结果打包下载

### Phase-2 增强功能
- [ ] 素材库管理界面
- [ ] 模板库功能
- [ ] 批量编辑功能
- [ ] 更多图片样式模板
- [ ] 用户权限管理

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License