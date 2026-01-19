<template>
  <div id="app">
    <div class="simple-app">
      <header class="app-header">
        <h1>🚀 电商草稿生成器</h1>
        <p>AI驱动的批量商品主图 + 标题 + 卖点生成工具</p>
      </header>
      
      <main class="app-main">
        <div class="upload-section">
          <h2>📊 上传Excel文件</h2>
          <div class="upload-area" @click="handleExcelUpload">
            <p>📁 点击上传Excel文件</p>
            <small>支持 .xlsx 格式，需包含：name, category, brand, material, size, color, targetGroup</small>
          </div>
        </div>
        
        <div class="upload-section">
          <h2>🖼️ 上传商品图片</h2>
          <div class="upload-area" @click="handleImageUpload">
            <p>📸 点击上传商品图片</p>
            <small>支持 JPG/PNG 格式，自动压缩到800px宽，<200KB</small>
          </div>
        </div>
        
        <div class="action-section">
          <button class="btn-primary" @click="generateDrafts">🚀 生成草稿</button>
          <button class="btn-secondary" @click="downloadResults">📦 打包下载</button>
        </div>
        
        <div class="results-section" v-if="showResults">
          <h3>🎯 生成结果</h3>
          <div class="result-grid">
            <div class="result-card" v-for="(result, index) in mockResults" :key="index">
              <div class="product-image">{{ result.name }}主图</div>
              <h4>{{ result.title }}</h4>
              <p>{{ result.sellingPoints }}</p>
            </div>
          </div>
        </div>
      </main>
      
      <footer class="app-footer">
        <p>© 2024 电商草稿生成器 - Powered by AI</p>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const showResults = ref(false)

const mockResults = ref([
  {
    name: '纯棉T恤',
    title: '纯棉T恤 - 舒适透气，时尚百搭',
    sellingPoints: '100%纯棉材质，亲肤透气；经典版型，适合各种身材；多色可选，百搭时尚'
  },
  {
    name: '运动鞋',
    title: '耐克运动鞋 - 专业运动，舒适体验',
    sellingPoints: '专业运动科技，缓震出色；透气网面，保持干爽；耐磨大底，持久耐用'
  }
])

const handleExcelUpload = () => {
  alert('📊 Excel上传功能\n\n在实际应用中，这里会：\n- 打开文件选择器\n- 解析Excel文件\n- 验证必填字段\n- 显示数据预览')
}

const handleImageUpload = () => {
  alert('🖼️ 图片上传功能\n\n在实际应用中，这里会：\n- 打开图片选择器\n- 自动压缩图片\n- 格式转换优化\n- 显示上传进度')
}

const generateDrafts = () => {
  showResults.value = true
  alert('🚀 草稿生成功能\n\n在实际应用中，这里会：\n- 调用AI生成标题\n- 创建卖点文案\n- 生成主图草稿\n- 显示实时进度')
}

const downloadResults = () => {
  alert('📦 打包下载功能\n\n在实际应用中，这里会：\n- 生成ZIP文件\n- 包含所有主图\n- 附加CSV数据\n- 自动下载到本地')
}
</script>

<style scoped>
.simple-app {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.app-header {
  text-align: center;
  padding: 40px 20px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.app-header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.app-header p {
  font-size: 1.2rem;
  opacity: 0.9;
}

.app-main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.upload-section {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 30px;
  margin-bottom: 30px;
  backdrop-filter: blur(10px);
}

.upload-section h2 {
  margin-bottom: 20px;
  color: #fff;
}

.upload-area {
  border: 2px dashed rgba(255, 255, 255, 0.5);
  border-radius: 10px;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.05);
}

.upload-area:hover {
  border-color: rgba(255, 255, 255, 0.8);
  background: rgba(255, 255, 255, 0.1);
}

.upload-area p {
  font-size: 1.2rem;
  margin-bottom: 10px;
}

.upload-area small {
  opacity: 0.8;
  font-size: 0.9rem;
}

.action-section {
  text-align: center;
  margin: 40px 0;
}

.btn-primary {
  background: linear-gradient(45deg, #4CAF50, #45a049);
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 25px;
  font-size: 1.1rem;
  cursor: pointer;
  margin: 0 10px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
}

.btn-secondary {
  background: linear-gradient(45deg, #2196F3, #1976D2);
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 25px;
  font-size: 1.1rem;
  cursor: pointer;
  margin: 0 10px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(33, 150, 243, 0.3);
}

.btn-secondary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(33, 150, 243, 0.4);
}

.results-section {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 30px;
  margin-top: 30px;
  backdrop-filter: blur(10px);
}

.results-section h3 {
  margin-bottom: 20px;
  color: #fff;
}

.result-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.result-card {
  background: rgba(255, 255, 255, 0.9);
  color: #333;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.product-image {
  width: 100%;
  height: 150px;
  background: linear-gradient(45deg, #f0f0f0, #e0e0e0);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
  font-size: 14px;
  color: #666;
}

.result-card h4 {
  color: #333;
  margin-bottom: 10px;
  font-size: 1.1rem;
}

.result-card p {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.5;
}

.app-footer {
  text-align: center;
  padding: 20px;
  background: rgba(0, 0, 0, 0.1);
}
</style>