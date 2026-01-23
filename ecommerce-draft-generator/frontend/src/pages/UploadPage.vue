<template>
  <div class="upload-page">
    <!-- 页面标题区域 -->
    <div class="page-header">
      <n-space vertical :size="8" align="center">
        <n-icon size="48" color="#18a058">
          <rocket-icon />
        </n-icon>
        <div class="page-title-group">
          <n-text class="page-title">AI 商品草稿生成器</n-text>
          <n-text depth="3" class="page-subtitle">
            上传商品信息，AI 智能生成主图、标题和卖点
          </n-text>
        </div>
      </n-space>
    </div>

    <!-- 主要内容区域 -->
    <n-grid :cols="24" :x-gap="32" :y-gap="24" class="main-content">
      <!-- 左侧上传区域 -->
      <n-gi :span="10">
        <div class="sticky-container">
          <upload-card
            @ai-analysis-complete="handleAIAnalysisComplete"
            @ai-analysis-clear="handleAIAnalysisClear"
          />
        </div>
      </n-gi>

      <!-- 右侧结果区域 -->
      <n-gi :span="14">
        <n-space vertical :size="24">
          <!-- AI图片分析结果 -->
          <n-card
            v-if="analysisResult"
            class="section-card"
            hoverable
            :class="{ 'processing': isAnalyzing }"
          >
            <template #header>
              <div class="section-header">
                <n-space align="center" :size="12">
                  <n-icon size="20" color="#f5222d">
                    <analytics-icon />
                  </n-icon>
                  <n-text class="section-title">AI 图片分析</n-text>
                  <n-tag
                    v-if="isAnalyzing"
                    type="warning"
                    round
                    size="small"
                    :loading="true"
                  >
                    分析中
                  </n-tag>
                  <n-tag
                    v-else-if="analysisResult"
                    type="success"
                    round
                    size="small"
                  >
                    分析完成
                  </n-tag>
                </n-space>
              </div>
            </template>
            <image-analysis-results
              :analysis-result="analysisResult"
              :loading="isAnalyzing"
              @use-as-product="handleUseAIProduct"
            />
          </n-card>

          <!-- 商品列表卡片 -->
          <n-card class="section-card" hoverable>
            <template #header>
              <div class="section-header">
                <n-space align="center" :size="12">
                  <n-icon size="20" color="#2080f0">
                    <list-icon />
                  </n-icon>
                  <n-text class="section-title">商品信息</n-text>
                  <n-tag type="info" round size="small">
                    可编辑
                  </n-tag>
                </n-space>
              </div>
            </template>
            <product-table @upload-excel="handleUploadExcel" @refresh="handleRefresh" />
          </n-card>

          <!-- 生成结果卡片 -->
          <n-card
            v-if="jobId"
            class="section-card"
            hoverable
            :class="{ 'processing': isProcessing }"
          >
            <template #header>
              <div class="section-header">
                <n-space align="center" :size="12">
                  <n-icon size="20" color="#18a058">
                    <magic-icon />
                  </n-icon>
                  <n-text class="section-title">AI 生成结果</n-text>
                  <n-tag
                    v-if="isProcessing"
                    type="warning"
                    round
                    size="small"
                    :loading="true"
                  >
                    生成中
                  </n-tag>
                  <n-tag
                    v-else-if="isDone"
                    type="success"
                    round
                    size="small"
                  >
                    已完成
                  </n-tag>
                </n-space>
              </div>
            </template>
            <draft-results />
          </n-card>
        </n-space>
      </n-gi>
    </n-grid>

    <!-- 浮动帮助按钮 -->
    <n-float-button :right="24" :bottom="24" :shape="'circle'" class="help-btn">
      <n-icon size="24">
        <help-icon />
      </n-icon>
      <template #tooltip>
        <div class="help-tooltip">
          <n-text class="help-title">使用帮助</n-text>
          <n-space vertical :size="8" class="help-content">
            <n-text depth="3">1. 上传 Excel 文件导入商品信息</n-text>
            <n-text depth="3">2. 上传商品图片（可选）</n-text>
            <n-text depth="3">3. 点击"开始智能生成"按钮</n-text>
            <n-text depth="3">4. 等待 AI 生成完成并下载</n-text>
          </n-space>
        </div>
      </template>
    </n-float-button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useUploadStore } from '@/stores/upload'
import UploadCard from '@/components/UploadCard.vue'
import ProductTable from '@/components/ProductTable.vue'
import DraftResults from '@/components/DraftResults.vue'
import ImageAnalysisResults from '@/components/ImageAnalysisResults.vue'
import { ImageAnalysisResult } from '@/api'
import {
  NGrid,
  NGi,
  NCard,
  NSpace,
  NText,
  NIcon,
  NTag,
  NFloatButton,
  NTooltip,
  useMessage
} from 'naive-ui'
import {
  Rocket as RocketIcon,
  List as ListIcon,
  Magic as MagicIcon,
  Help as HelpIcon,
  Analytics as AnalyticsIcon
} from '@vicons/ionicons5'

const message = useMessage()
const uploadStore = useUploadStore()
const { jobId, isProcessing, isDone } = storeToRefs(uploadStore)

// AI分析相关状态
const analysisResult = ref<ImageAnalysisResult | null>(null)
const isAnalyzing = ref(false)

const handleUploadExcel = () => {
  // 触发上传 Excel 的逻辑
  const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement
  if (fileInput) {
    fileInput.click()
  }
}

const handleRefresh = () => {
  // 刷新数据逻辑
  window.location.reload()
}

// 处理AI分析完成
const handleAIAnalysisComplete = (result: ImageAnalysisResult) => {
  analysisResult.value = result
  isAnalyzing.value = false
}

// 处理AI分析清除
const handleAIAnalysisClear = () => {
  analysisResult.value = null
  isAnalyzing.value = false
}

// 使用AI分析的商品
const handleUseAIProduct = (productInfo: any) => {
  // 将AI分析的商品添加到商品列表
  uploadStore.products = [productInfo]
  message.success('AI分析的商品已添加到商品列表')
}
</script>

<style scoped>
.upload-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 24px;
}

.page-header {
  text-align: center;
  padding: 48px 0 32px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 16px;
  margin-bottom: 32px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.page-title-group {
  margin-top: 16px;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  background: linear-gradient(135deg, #18a058 0%, #36ad6a 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: block;
  margin-bottom: 8px;
}

.page-subtitle {
  font-size: 16px;
  display: block;
  color: #5a6c7d;
}

.main-content {
  max-width: 1400px;
  margin: 0 auto;
}

.sticky-container {
  position: sticky;
  top: 100px;
}

.section-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.section-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.section-card.processing {
  border-color: #2080f0;
  box-shadow: 0 8px 32px rgba(32, 128, 240, 0.2);
}

.section-header {
  display: flex;
  align-items: center;
  padding: 4px 0;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  background: linear-gradient(135deg, #18a058 0%, #36ad6a 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.help-btn {
  background: linear-gradient(135deg, #18a058 0%, #36ad6a 100%);
  box-shadow: 0 4px 16px rgba(24, 160, 88, 0.3);
  transition: all 0.3s ease;
}

.help-btn:hover {
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 8px 24px rgba(24, 160, 88, 0.4);
}

.help-tooltip {
  padding: 12px;
  max-width: 200px;
}

.help-title {
  font-size: 14px;
  font-weight: 600;
  display: block;
  margin-bottom: 8px;
}

.help-content {
  font-size: 12px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .main-content {
    grid-template-columns: 1fr;
  }
  
  .sticky-container {
    position: static;
  }
}

@media (max-width: 768px) {
  .upload-page {
    padding: 16px;
  }
  
  .page-header {
    padding: 32px 16px 24px;
    margin-bottom: 24px;
  }
  
  .page-title {
    font-size: 24px;
  }
  
  .page-subtitle {
    font-size: 14px;
  }
}
</style>