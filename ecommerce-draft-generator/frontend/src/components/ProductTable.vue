<template>
  <div class="product-table-container">
    <div v-if="products.length === 0" class="empty-state">
      <div class="empty-icon">
        <n-icon size="64" color="#e0e0e0">
          <document-text-icon />
        </n-icon>
      </div>
      <n-text class="empty-title">暂无商品数据</n-text>
      <n-text depth="3" class="empty-desc">
        请先上传包含商品信息的 Excel 文件
      </n-text>
      <n-button type="primary" dashed @click="emit('upload-excel')">
        <template #icon>
          <n-icon><upload-icon /></n-icon>
        </template>
        上传 Excel 文件
      </n-button>
    </div>
    
    <div v-else class="table-wrapper">
      <div class="table-header">
        <n-space align="center" justify="space-between">
          <n-space align="center">
            <n-icon size="20" color="#18a058">
              <list-icon />
            </n-icon>
            <n-text class="table-title">商品信息列表</n-text>
            <n-tag type="success" round size="small">
              共 {{ products.length }} 件商品
            </n-tag>
          </n-space>
          <n-space>
            <n-button quaternary circle @click="emit('refresh')">
              <template #icon>
                <n-icon><refresh-icon /></n-icon>
              </template>
            </n-button>
          </n-space>
        </n-space>
      </div>
      
      <div class="table-content">
        <n-data-table
          :columns="columns"
          :data="products"
          :pagination="pagination"
          :scroll-x="800"
          size="small"
          class="modern-table"
          :row-class-name="rowClassName"
        />
      </div>
      
      <div class="table-footer">
        <n-space align="center" justify="space-between">
          <n-text depth="3" class="footer-text">
            提示：点击单元格可直接编辑商品信息
          </n-text>
          <n-space>
            <n-button size="small" quaternary @click="exportData">
              <template #icon>
                <n-icon><download-icon /></n-icon>
              </template>
              导出数据
            </n-button>
          </n-space>
        </n-space>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { h, computed } from 'vue'
import { useUploadStore } from '@/stores/upload'
import {
  NDataTable,
  NEmpty,
  NIcon,
  NInput,
  NTag,
  NSpace,
  NText,
  NButton,
  NTooltip,
  useMessage
} from 'naive-ui'
import { 
  DocumentText as DocumentTextIcon,
  List as ListIcon,
  Refresh as RefreshIcon,
  Upload as UploadIcon,
  Download as DownloadIcon,
  Image as ImageIcon,
  CheckmarkCircle as CheckIcon,
  Warning as WarningIcon
} from '@vicons/ionicons5'

const emit = defineEmits(['upload-excel', 'refresh'])

const message = useMessage()
const uploadStore = useUploadStore()
const { products } = uploadStore

// 表格列定义
const columns = computed(() => [
  {
    title: '商品信息',
    key: 'product-info',
    width: 200,
    fixed: 'left',
    render: (row: any) => {
      return h('div', { class: 'product-cell' }, [
        h('div', { class: 'product-name' }, row.name),
        h('div', { class: 'product-brand' }, row.brand)
      ])
    }
  },
  {
    title: '分类',
    key: 'category',
    width: 100,
    render: (row: any, index: number) => {
      return h(NInput, {
        value: row.category,
        onUpdateValue: (value: string) => {
          products[index].category = value
        },
        placeholder: '商品分类',
        size: 'small'
      })
    }
  },
  {
    title: '材质',
    key: 'material',
    width: 80,
    render: (row: any, index: number) => {
      return h(NInput, {
        value: row.material,
        onUpdateValue: (value: string) => {
          products[index].material = value
        },
        placeholder: '材质',
        size: 'small'
      })
    }
  },
  {
    title: '规格',
    key: 'size',
    width: 80,
    render: (row: any, index: number) => {
      return h(NInput, {
        value: row.size,
        onUpdateValue: (value: string) => {
          products[index].size = value
        },
        placeholder: '尺寸',
        size: 'small'
      })
    }
  },
  {
    title: '颜色',
    key: 'color',
    width: 80,
    render: (row: any, index: number) => {
      return h(NInput, {
        value: row.color,
        onUpdateValue: (value: string) => {
          products[index].color = value
        },
        placeholder: '颜色',
        size: 'small'
      })
    }
  },
  {
    title: '目标人群',
    key: 'targetGroup',
    width: 120,
    render: (row: any, index: number) => {
      return h(NInput, {
        value: row.targetGroup,
        onUpdateValue: (value: string) => {
          products[index].targetGroup = value
        },
        placeholder: '目标人群',
        size: 'small'
      })
    }
  },
  {
    title: '图片状态',
    key: 'imageUrl',
    width: 100,
    align: 'center',
    render: (row: any) => {
      const hasImage = !!row.imageUrl
      return h(NTag, {
        type: hasImage ? 'success' : 'warning',
        size: 'small',
        round: true
      }, {
        icon: () => h(NIcon, { size: 14 }, h(hasImage ? CheckIcon : WarningIcon)),
        default: () => hasImage ? '已上传' : '待上传'
      })
    }
  }
])

const pagination = {
  pageSize: 10,
  showSizePicker: true,
  pageSizes: [10, 20, 50],
  showQuickJumper: true
}

const rowClassName = (row: any, index: number) => {
  return index % 2 === 0 ? 'even-row' : 'odd-row'
}

const exportData = () => {
  // 导出数据功能
  const dataStr = JSON.stringify(products, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  const link = document.createElement('a')
  link.href = url
  link.download = `商品信息_${new Date().toISOString().slice(0, 10)}.json`
  link.click()
  URL.revokeObjectURL(url)
  message.success('数据导出成功！')
}
</script>

<style scoped>
.product-table-container {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  overflow: hidden;
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

.table-wrapper {
  background: #ffffff;
}

.table-header {
  padding: 20px 24px;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.table-title {
  font-size: 18px;
  font-weight: 600;
  background: linear-gradient(135deg, #18a058 0%, #36ad6a 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.table-content {
  padding: 0;
}

.table-footer {
  padding: 16px 24px;
  background: #f8f9fa;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
}

.footer-text {
  font-size: 12px;
}

/* 商品单元格样式 */
.product-cell {
  padding: 8px 0;
}

.product-name {
  font-weight: 600;
  font-size: 14px;
  color: #2c3e50;
  margin-bottom: 4px;
}

.product-brand {
  font-size: 12px;
  color: #7f8c8d;
  background: rgba(24, 160, 88, 0.1);
  padding: 2px 8px;
  border-radius: 12px;
  display: inline-block;
}

/* 表格行样式 */
:deep(.modern-table) {
  border-radius: 0;
}

:deep(.even-row) {
  background: rgba(248, 249, 250, 0.5);
}

:deep(.odd-row) {
  background: #ffffff;
}

:deep(.even-row:hover),
:deep(.odd-row:hover) {
  background: rgba(24, 160, 88, 0.05) !important;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .table-header,
  .table-footer {
    padding: 16px;
  }
  
  .empty-state {
    padding: 60px 16px;
  }
}
</style>