<template>
  <n-card class="analysis-results-card" hoverable>
    <template #header>
      <div class="card-header">
        <n-space align="center" :size="12">
          <n-icon size="24" color="#18a058">
            <analytics-icon />
          </n-icon>
          <n-text class="card-title">AI 图片分析结果</n-text>
        </n-space>
        <n-tag type="success" size="small" round>
          智能识别
        </n-tag>
      </div>
    </template>

    <div v-if="loading" class="loading-container">
      <n-spin size="large" />
      <n-text class="loading-text">AI 正在分析图片，请稍候...</n-text>
    </div>

    <div v-else-if="error" class="error-container">
      <n-alert type="error" :show-icon="false">
        <template #default>
          <n-text>{{ error }}</n-text>
        </template>
      </n-alert>
    </div>

    <div v-else-if="analysisResult" class="results-container">
      <!-- 商品图片展示 -->
      <div class="image-section">
        <n-image
          :src="analysisResult.data.product_info.imageUrl"
          :preview-src="analysisResult.data.product_info.imageUrl"
          class="product-image"
          alt="商品图片"
        />
      </div>

      <!-- 生成的商品信息 -->
      <n-divider />
      
      <n-space vertical :size="16">
        <!-- 商品标题 -->
        <div class="info-section">
          <n-text class="section-label">商品标题</n-text>
          <n-input
            v-model:value="analysisResult.data.generated_content.title"
            type="textarea"
            :autosize="{ minRows: 1, maxRows: 2 }"
            readonly
            class="generated-input"
          />
        </div>

        <!-- 卖点文案 -->
        <div class="info-section">
          <n-text class="section-label">卖点文案</n-text>
          <n-input
            v-model:value="analysisResult.data.generated_content.selling_points"
            type="textarea"
            :autosize="{ minRows: 2, maxRows: 4 }"
            readonly
            class="generated-input"
          />
        </div>

        <!-- 商品属性 -->
        <n-grid :cols="2" :x-gap="16" :y-gap="16">
          <n-gi>
            <div class="info-section">
              <n-text class="section-label">品牌</n-text>
              <n-input
                v-model:value="analysisResult.data.generated_content.brand"
                readonly
                class="generated-input"
              />
            </div>
          </n-gi>
          <n-gi>
            <div class="info-section">
              <n-text class="section-label">材质</n-text>
              <n-input
                v-model:value="analysisResult.data.generated_content.material"
                readonly
                class="generated-input"
              />
            </div>
          </n-gi>
          <n-gi>
            <div class="info-section">
              <n-text class="section-label">尺寸</n-text>
              <n-input
                v-model:value="analysisResult.data.generated_content.size"
                readonly
                class="generated-input"
              />
            </div>
          </n-gi>
          <n-gi>
            <div class="info-section">
              <n-text class="section-label">颜色</n-text>
              <n-input
                v-model:value="analysisResult.data.generated_content.color"
                readonly
                class="generated-input"
              />
            </div>
          </n-gi>
        </n-grid>

        <!-- 目标人群 -->
        <div class="info-section">
          <n-text class="section-label">目标人群</n-text>
          <n-input
            v-model:value="analysisResult.data.generated_content.target_group"
            readonly
            class="generated-input"
          />
        </div>

        <!-- AI分析详情 -->
        <n-collapse class="analysis-details">
          <n-collapse-item title="AI 分析详情" name="details">
            <n-space vertical :size="12">
              <!-- 商品类型和类别 -->
              <div class="detail-section">
                <n-text class="detail-label">商品类型</n-text>
                <n-text>{{ analysisResult.data.product_info.name }}</n-text>
              </div>
              <div class="detail-section">
                <n-text class="detail-label">商品类别</n-text>
                <n-text>{{ analysisResult.data.product_info.category }}</n-text>
              </div>

              <!-- 识别出的卖点 -->
              <div class="detail-section">
                <n-text class="detail-label">识别卖点</n-text>
                <n-space>
                  <n-tag
                    v-for="(point, index) in analysisResult.data.analysis.selling_points"
                    :key="index"
                    type="info"
                    size="small"
                    round
                  >
                    {{ point }}
                  </n-tag>
                </n-space>
              </div>

              <!-- 关键词 -->
              <div class="detail-section">
                <n-text class="detail-label">关键词</n-text>
                <n-space>
                  <n-tag
                    v-for="(keyword, index) in analysisResult.data.analysis.keywords"
                    :key="index"
                    type="warning"
                    size="small"
                    round
                  >
                    {{ keyword }}
                  </n-tag>
                </n-space>
              </div>

              <!-- 商品描述 -->
              <div class="detail-section">
                <n-text class="detail-label">商品描述</n-text>
                <n-text>{{ analysisResult.data.analysis.description }}</n-text>
              </div>
            </n-space>
          </n-collapse-item>
        </n-collapse>

        <!-- 操作按钮 -->
        <n-space justify="space-between" align="center">
          <n-space>
            <n-button @click="copyToClipboard" type="primary" ghost>
              <template #icon>
                <n-icon><copy-icon /></n-icon>
              </template>
              复制内容
            </n-button>
            <n-button @click="useAsProduct" type="success">
              <template #icon>
                <n-icon><checkmark-icon /></n-icon>
              </template>
              使用此商品
            </n-button>
          </n-space>
          <n-text depth="3" class="confidence-text">
            AI 智能分析，置信度: 高
          </n-text>
        </n-space>
      </n-space>
    </div>

    <div v-else class="empty-container">
      <n-empty description="上传图片开始AI分析">
        <template #extra>
          <n-text depth="3">支持 JPG、PNG、WebP 格式</n-text>
        </template>
      </n-empty>
    </div>
  </n-card>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useMessage } from 'naive-ui'
import { uploadApi, ImageAnalysisResult } from '@/api'
import { 
  Analytics as AnalyticsIcon,
  Copy as CopyIcon,
  Checkmark as CheckmarkIcon
} from '@vicons/ionicons5'

const props = defineProps<{
  analysisResult?: ImageAnalysisResult | null
  loading?: boolean
  error?: string | null
}>()

const emit = defineEmits<{
  useAsProduct: [productInfo: any]
}>()

const message = useMessage()

const copyToClipboard = async () => {
  if (!props.analysisResult) return
  
  const content = `
商品标题：${props.analysisResult.data.generated_content.title}
卖点文案：${props.analysisResult.data.generated_content.selling_points}
品牌：${props.analysisResult.data.generated_content.brand}
材质：${props.analysisResult.data.generated_content.material}
尺寸：${props.analysisResult.data.generated_content.size}
颜色：${props.analysisResult.data.generated_content.color}
目标人群：${props.analysisResult.data.generated_content.target_group}
  `.trim()
  
  try {
    await navigator.clipboard.writeText(content)
    message.success('内容已复制到剪贴板')
  } catch (error) {
    message.error('复制失败，请手动复制')
  }
}

const useAsProduct = () => {
  if (!props.analysisResult) return
  
  emit('useAsProduct', props.analysisResult.data.product_info)
  message.success('商品信息已添加到列表')
}
</script>

<style scoped>
.analysis-results-card {
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

.loading-container {
  text-align: center;
  padding: 48px 24px;
}

.loading-text {
  display: block;
  margin-top: 16px;
  font-size: 16px;
  color: #666;
}

.error-container {
  padding: 24px;
}

.empty-container {
  text-align: center;
  padding: 48px 24px;
}

.results-container {
  padding: 8px;
}

.image-section {
  text-align: center;
  margin-bottom: 24px;
}

.product-image {
  max-width: 300px;
  max-height: 300px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.info-section {
  margin-bottom: 16px;
}

.section-label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #666;
  margin-bottom: 8px;
}

.generated-input {
  background: rgba(248, 249, 250, 0.8);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 6px;
}

.analysis-details {
  margin-top: 24px;
  background: rgba(248, 249, 250, 0.6);
  border-radius: 8px;
}

.detail-section {
  margin-bottom: 16px;
}

.detail-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #888;
  margin-bottom: 6px;
}

.confidence-text {
  font-size: 12px;
  font-style: italic;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .product-image {
    max-width: 200px;
    max-height: 200px;
  }
  
  .card-title {
    font-size: 18px;
  }
}
</style>