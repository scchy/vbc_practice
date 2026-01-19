<template>
  <div class="results-container">
    <!-- 任务状态头部 -->
    <div class="results-header">
      <n-space align="center" justify="space-between">
        <n-space align="center">
          <n-icon size="24" :color="statusColor">
            <component :is="statusIcon" />
          </n-icon>
          <div>
            <n-text class="status-title">{{ statusTitle }}</n-text>
            <n-text depth="3" class="status-desc">{{ statusDesc }}</n-text>
          </div>
        </n-space>
        
        <n-space>
          <n-statistic label="总任务" :value="total" />
          <n-statistic label="已完成" :value="finished" />
          <n-progress 
            type="circle"
            :percentage="completionRate"
            :color="statusColor"
            :stroke-width="6"
            :show-indicator="false"
            style="width: 60px; height: 60px;"
          />
          
          <n-button
            v-if="isDone"
            type="primary"
            @click="handleDownload"
            :loading="downloading"
            class="download-btn"
          >
            <template #icon>
              <n-icon><download-icon /></n-icon>
            </template>
            打包下载
          </n-button>
        </n-space>
      </n-space>
    </div>

    <!-- 进度条 -->
    <div v-if="isProcessing" class="progress-section">
      <n-progress 
        type="line"
        :percentage="completionRate"
        :indicator-placement="'inside'"
        :color="statusColor"
        :rail-color="'#f0f0f0'"
        :height="8"
        processing
      />
      <div class="progress-info">
        <n-space align="center">
          <n-spin size="small" />
          <n-text depth="3">AI 正在为您生成高质量的商品草稿，请稍候...</n-text>
        </n-space>
      </div>
    </div>

    <!-- 结果卡片网格 -->
    <div v-if="results.length > 0" class="results-grid">
      <n-grid :cols="getGridCols" :x-gap="20" :y-gap="20">
        <n-gi v-for="(result, index) in results" :key="index">
          <n-card 
            hoverable 
            class="result-card"
            :class="{ 'processing': result.status === 'processing' }"
          >
            <template #cover v-if="result.imageUrl">
              <div class="image-container" @click="showImageModal(result.imageUrl)">
                <img :src="result.imageUrl" :alt="result.title" class="product-image" />
                <div class="image-overlay">
                  <n-icon size="32" color="white">
                    <eye-icon />
                  </n-icon>
                  <n-text class="overlay-text">点击查看大图</n-text>
                </div>
              </div>
            </template>
            
            <n-space vertical :size="12">
              <!-- 标题 -->
              <div class="title-section">
                <n-text class="result-title">{{ result.title }}</n-text>
                <n-button 
                  size="tiny" 
                  quaternary 
                  circle
                  @click="copyText(result.title)"
                  class="copy-btn"
                >
                  <template #icon>
                    <n-icon><copy-icon /></n-icon>
                  </template>
                </n-button>
              </div>
              
              <!-- 卖点 -->
              <div class="selling-points-section">
                <n-text depth="3" class="selling-points">
                  {{ result.sellingPoints }}
                </n-text>
                <n-button 
                  size="tiny" 
                  quaternary 
                  circle
                  @click="copyText(result.sellingPoints)"
                  class="copy-btn"
                >
                  <template #icon>
                    <n-icon><copy-icon /></n-icon>
                  </template>
                </n-button>
              </div>
              
              <!-- 操作按钮 -->
              <div class="actions-section">
                <n-space>
                  <n-button 
                    size="small" 
                    type="primary" 
                    ghost
                    @click="copyText(result.title)"
                  >
                    <template #icon>
                      <n-icon><copy-icon /></n-icon>
                    </template>
                    复制标题
                  </n-button>
                  <n-button 
                    size="small" 
                    @click="copyText(result.sellingPoints)"
                  >
                    <template #icon>
                      <n-icon><copy-icon /></n-icon>
                    </template>
                    复制卖点
                  </n-button>
                </n-space>
              </div>
            </n-space>
          </n-card>
        </n-gi>
      </n-grid>
    </div>

    <!-- 空状态 -->
    <div v-else-if="jobId && !isProcessing" class="empty-state">
      <div class="empty-icon">
        <n-icon size="64" color="#e0e0e0">
          <magic-icon />
        </n-icon>
      </div>
      <n-text class="empty-title">准备生成草稿</n-text>
      <n-text depth="3" class="empty-desc">
        点击"开始智能生成"按钮，AI 将为您创建高质量的商品草稿
      </n-text>
    </div>

    <!-- 图片预览模态框 -->
    <n-modal
      v-model:show="showModal"
      preset="card"
      :style="{ width: '80vw', maxWidth: '800px' }"
      title="商品主图预览"
      :bordered="false"
    >
      <div class="modal-image-container">
        <img :src="modalImageUrl" class="modal-image" alt="商品主图" />
      </div>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useUploadStore } from '@/stores/upload'
import {
  NGrid,
  NGi,
  NCard,
  NSpace,
  NText,
  NButton,
  NIcon,
  NProgress,
  NSpin,
  NModal,
  NStatistic,
  NTag,
  NTooltip,
  useMessage
} from 'naive-ui'
import {
  CheckmarkCircle as CheckIcon,
  Time as TimeIcon,
  CloseCircle as ErrorIcon,
  Sparkles as MagicIcon,
  Eye as EyeIcon,
  Copy as CopyIcon,
  Download as DownloadIcon
} from '@vicons/ionicons5'

const message = useMessage()
const uploadStore = useUploadStore()
const { jobStatus, isProcessing, isDone } = storeToRefs(uploadStore)

const showModal = ref(false)
const modalImageUrl = ref('')
const downloading = ref(false)

const total = computed(() => jobStatus.value?.total || 0)
const finished = computed(() => jobStatus.value?.finished || 0)
const results = computed(() => jobStatus.value?.results || [])
const jobId = computed(() => uploadStore.jobId)

const completionRate = computed(() => {
  return total.value > 0 ? Math.round((finished.value / total.value) * 100) : 0
})

const statusColor = computed(() => {
  if (isProcessing.value) return '#2080f0'
  if (isDone.value) return '#18a058'
  return '#e0e0e0'
})

const statusIcon = computed(() => {
  if (isProcessing.value) return TimeIcon
  if (isDone.value) return CheckIcon
  return MagicIcon
})

const statusTitle = computed(() => {
  if (isProcessing.value) return '正在生成中...'
  if (isDone.value) return '生成完成！'
  return '准备就绪'
})

const statusDesc = computed(() => {
  if (isProcessing.value) return `${finished.value}/${total.value} 个商品已处理完成`
  if (isDone.value) return `所有商品草稿已生成完毕，可以下载使用`
  return '等待开始生成'
})

const getGridCols = computed(() => {
  const width = window.innerWidth
  if (width < 768) return 1
  if (width < 1024) return 2
  return 3
})

// 显示图片模态框
const showImageModal = (imageUrl: string) => {
  modalImageUrl.value = imageUrl
  showModal.value = true
}

// 复制文本
const copyText = async (text: string) => {
  try {
    await navigator.clipboard.writeText(text)
    message.success('📋 已复制到剪贴板')
  } catch (error) {
    message.error('❌ 复制失败')
  }
}

// 下载 ZIP
const handleDownload = async () => {
  try {
    downloading.value = true
    await uploadStore.downloadZip()
    message.success('📦 下载开始，请查看下载文件夹')
  } catch (error) {
    message.error('❌ 下载失败')
  } finally {
    downloading.value = false
  }
}
</script>

<style scoped>
.results-container {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.results-header {
  padding: 24px;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.status-title {
  font-size: 18px;
  font-weight: 600;
  display: block;
  margin-bottom: 4px;
}

.status-desc {
  font-size: 14px;
  display: block;
}

.download-btn {
  background: linear-gradient(135deg, #18a058 0%, #36ad6a 100%);
  border: none;
  box-shadow: 0 4px 16px rgba(24, 160, 88, 0.3);
}

.progress-section {
  padding: 20px 24px;
  background: rgba(255, 255, 255, 0.8);
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.progress-info {
  margin-top: 12px;
  text-align: center;
}

.results-grid {
  padding: 24px;
}

.result-card {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.05);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.result-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
}

.result-card.processing {
  opacity: 0.7;
}

.image-container {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  cursor: pointer;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.image-container:hover .product-image {
  transform: scale(1.05);
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.image-container:hover .image-overlay {
  opacity: 1;
}

.overlay-text {
  color: white;
  font-size: 12px;
  margin-top: 8px;
}

.title-section {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
}

.result-title {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  line-height: 1.4;
  flex: 1;
}

.selling-points-section {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
  padding: 12px;
  background: rgba(248, 249, 250, 0.8);
  border-radius: 8px;
}

.selling-points {
  font-size: 13px;
  line-height: 1.5;
  color: #5a6c7d;
  flex: 1;
}

.copy-btn {
  opacity: 0.6;
  transition: opacity 0.2s ease;
}

.copy-btn:hover {
  opacity: 1;
}

.actions-section {
  padding-top: 12px;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.empty-state {
  text-align: center;
  padding: 80px 24px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.empty-icon {
  margin-bottom: 24px;
}

.empty-title {
  font-size: 20px;
  font-weight: 600;
  display: block;
  margin-bottom: 8px;
  color: #495057;
}

.empty-desc {
  font-size: 14px;
  display: block;
  margin-bottom: 24px;
}

.modal-image-container {
  text-align: center;
  padding: 20px;
}

.modal-image {
  max-width: 100%;
  max-height: 70vh;
  border-radius: 8px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .results-header {
    padding: 16px;
  }
  
  .results-grid {
    padding: 16px;
  }
  
  .progress-section {
    padding: 16px;
  }
}
</style>