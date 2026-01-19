<template>
  <n-card class="upload-card" hoverable>
    <template #header>
      <div class="card-header">
        <n-space align="center" :size="12">
          <n-icon size="24" color="#18a058">
            <cloud-upload-icon />
          </n-icon>
          <n-text class="card-title">上传商品素材</n-text>
        </n-space>
        <n-tag type="success" size="small" round>
          AI 智能处理
        </n-tag>
      </div>
    </template>

    <n-space vertical :size="24">
      <!-- Excel 上传区域 -->
      <div class="upload-section">
        <div class="section-header">
          <n-text class="section-title">📊 商品信息导入</n-text>
          <n-text depth="3" class="section-subtitle">支持 Excel 批量导入</n-text>
        </div>
        
        <n-upload
          :file-list="excelFileList"
          :max="1"
          accept=".xlsx,.xls"
          :custom-request="handleExcelUpload"
          @remove="handleExcelRemove"
          class="excel-upload"
        >
          <n-upload-dragger class="custom-dragger">
            <div class="dragger-content">
              <n-icon size="48" color="#18a058" class="dragger-icon">
                <document-text-icon />
              </n-icon>
              <n-text class="dragger-title">点击或拖拽 Excel 文件到此处</n-text>
              <n-text depth="3" class="dragger-desc">
                支持 .xlsx, .xls 格式，文件大小不超过 10MB
              </n-text>
              <n-button type="primary" dashed class="dragger-btn">
                选择 Excel 文件
              </n-button>
            </div>
          </n-upload-dragger>
        </n-upload>
        
        <n-alert type="info" :show-icon="false" class="field-hint">
          <template #default>
            <n-text depth="3" style="font-size: 12px;">
              必填列：name, category, brand, material, size, color, targetGroup
            </n-text>
          </template>
        </n-alert>
      </div>

      <!-- 图片上传区域 -->
      <div class="upload-section">
        <div class="section-header">
          <n-text class="section-title">🖼️ 商品图片上传</n-text>
          <n-text depth="3" class="section-subtitle">支持批量上传，自动优化处理</n-text>
        </div>
        
        <n-upload
          multiple
          :file-list="imageFileList"
          accept="image/*"
          :custom-request="handleImageUpload"
          @remove="handleImageRemove"
          class="image-upload"
        >
          <n-upload-dragger class="custom-dragger image-dragger">
            <div class="dragger-content">
              <n-icon size="48" color="#2080f0" class="dragger-icon">
                <images-icon />
              </n-icon>
              <n-text class="dragger-title">点击或拖拽图片到此处上传</n-text>
              <n-text depth="3" class="dragger-desc">
                支持批量上传，自动压缩到 800px 宽，< 200KB，格式 WebP
              </n-text>
              <div class="image-features">
                <n-space>
                  <n-tag size="small" type="success" round>自动压缩</n-tag>
                  <n-tag size="small" type="info" round>格式优化</n-tag>
                  <n-tag size="small" type="warning" round>智能裁剪</n-tag>
                </n-space>
              </div>
            </div>
          </n-upload-dragger>
        </n-upload>
        
        <!-- 上传进度 -->
        <div v-if="uploadingImages" class="progress-container">
          <div class="progress-header">
            <n-text class="progress-title">正在上传和优化图片...</n-text>
            <n-text depth="3" class="progress-percent">{{ Math.round(uploadProgress) }}%</n-text>
          </div>
          <n-progress 
            type="line" 
            :percentage="uploadProgress" 
            :indicator-placement="'inside'"
            :color="themeOverrides.common?.primaryColor"
            :rail-color="'#f0f0f0'"
            :height="8"
            processing
          />
        </div>
      </div>

      <!-- 高级选项 -->
      <n-collapse class="advanced-options">
        <n-collapse-item title="高级选项" name="advanced">
          <n-space vertical :size="16">
            <n-space align="center" justify="space-between">
              <div>
                <n-text class="option-title">保存到素材库</n-text>
                <n-text depth="3" class="option-desc">将商品信息保存到素材库，方便下次复用</n-text>
              </div>
              <n-switch v-model:value="saveToAsset" size="large">
                <template #checked>
                  已开启
                </template>
                <template #unchecked>
                  已关闭
                </template>
              </n-switch>
            </n-space>
          </n-space>
        </n-collapse-item>
      </n-collapse>

      <!-- 生成按钮 -->
      <div class="action-section">
        <n-button
          type="primary"
          size="large"
          :disabled="!hasProducts || uploadingImages"
          :loading="isProcessing"
          @click="handleGenerate"
          block
          class="generate-btn"
        >
          <template #icon>
            <n-icon><magic-icon /></n-icon>
          </template>
          {{ isProcessing ? '正在生成草稿...' : '✨ 开始智能生成' }}
        </n-button>
        
        <div v-if="isProcessing" class="processing-hint">
          <n-spin size="small" />
          <n-text depth="3">AI 正在为您生成高质量的商品草稿，请稍候...</n-text>
        </div>
      </div>
    </n-space>
  </n-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useUploadStore } from '@/stores/upload'
import {
  NCard,
  NSpace,
  NUpload,
  NUploadDragger,
  NButton,
  NIcon,
  NText,
  NTag,
  NProgress,
  NSwitch,
  NCollapse,
  NCollapseItem,
  NAlert,
  NSpin,
  useMessage
} from 'naive-ui'
import { 
  DocumentText as DocumentTextIcon,
  Images as ImagesIcon,
  CloudUpload as CloudUploadIcon,
  Magic as MagicIcon
} from '@vicons/ionicons5'

const message = useMessage()
const uploadStore = useUploadStore()

const excelFileList = ref([])
const imageFileList = ref([])

const {
  products: hasProducts,
  uploadingImages,
  uploadProgress,
  saveToAsset,
  isProcessing
} = uploadStore

// 主题配置
const themeOverrides = {
  common: {
    primaryColor: '#18a058'
  }
}

// Excel 上传处理
const handleExcelUpload = async ({ file }: { file: File }) => {
  try {
    await uploadStore.parseExcel(file)
    excelFileList.value = [file]
    message.success('🎉 Excel 解析成功！已导入商品信息')
  } catch (error) {
    message.error('❌ Excel 解析失败，请检查文件格式')
    console.error(error)
  }
}

const handleExcelRemove = () => {
  excelFileList.value = []
  uploadStore.products = []
  message.info('商品信息已清空')
}

// 图片上传处理
const handleImageUpload = async ({ file }: { file: File }) => {
  const files = Array.isArray(file) ? file : [file]
  
  try {
    await uploadStore.uploadImages(files)
    imageFileList.value = [...imageFileList.value, ...files]
    message.success('🎉 图片上传完成！已自动优化处理')
  } catch (error) {
    message.error('❌ 图片上传失败')
    console.error(error)
  }
}

const handleImageRemove = ({ file }: { file: File }) => {
  const index = imageFileList.value.indexOf(file)
  if (index > -1) {
    imageFileList.value.splice(index, 1)
  }
}

// 生成草稿
const handleGenerate = async () => {
  try {
    await uploadStore.generateDraft()
    message.success('🚀 开始生成草稿，AI 正在努力创作中...')
  } catch (error) {
    message.error('❌ 生成草稿失败')
    console.error(error)
  }
}
</script>

<style scoped>
.upload-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
}

.card-title {
  font-size: 20px;
  font-weight: 600;
  background: linear-gradient(135deg, #18a058 0%, #36ad6a 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.upload-section {
  background: rgba(248, 249, 250, 0.6);
  border-radius: 12px;
  padding: 24px;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.section-header {
  margin-bottom: 16px;
  text-align: center;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  display: block;
  margin-bottom: 4px;
}

.section-subtitle {
  font-size: 14px;
  display: block;
}

.custom-dragger {
  background: rgba(255, 255, 255, 0.8);
  border: 2px dashed rgba(24, 160, 88, 0.3);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.custom-dragger:hover {
  border-color: #18a058;
  background: rgba(24, 160, 88, 0.05);
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(24, 160, 88, 0.2);
}

.image-dragger {
  border-color: rgba(32, 128, 240, 0.3);
}

.image-dragger:hover {
  border-color: #2080f0;
  background: rgba(32, 128, 240, 0.05);
  box-shadow: 0 4px 16px rgba(32, 128, 240, 0.2);
}

.dragger-content {
  text-align: center;
  padding: 40px 20px;
}

.dragger-icon {
  margin-bottom: 16px;
  animation: pulse 2s infinite;
}

.dragger-title {
  font-size: 18px;
  font-weight: 600;
  display: block;
  margin-bottom: 8px;
}

.dragger-desc {
  font-size: 14px;
  display: block;
  margin-bottom: 20px;
}

.dragger-btn {
  margin-top: 8px;
}

.image-features {
  margin-top: 16px;
}

.field-hint {
  margin-top: 12px;
  background: rgba(24, 160, 88, 0.1);
  border: none;
}

.progress-container {
  margin-top: 16px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  padding: 16px;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.progress-title {
  font-size: 14px;
  font-weight: 500;
}

.progress-percent {
  font-size: 12px;
  font-weight: 600;
}

.advanced-options {
  background: rgba(255, 255, 255, 0.6);
  border-radius: 8px;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.option-title {
  font-size: 16px;
  font-weight: 600;
  display: block;
  margin-bottom: 4px;
}

.option-desc {
  font-size: 13px;
  display: block;
}

.action-section {
  text-align: center;
}

.generate-btn {
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, #18a058 0%, #36ad6a 100%);
  border: none;
  box-shadow: 0 4px 16px rgba(24, 160, 88, 0.3);
  transition: all 0.3s ease;
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(24, 160, 88, 0.4);
}

.generate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.processing-hint {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 12px;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.05);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .upload-section {
    padding: 16px;
  }
  
  .dragger-content {
    padding: 24px 16px;
  }
  
  .card-title {
    font-size: 18px;
  }
}
</style>