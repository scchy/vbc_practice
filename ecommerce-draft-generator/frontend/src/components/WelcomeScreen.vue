<template>
  <div class="welcome-screen" v-if="showWelcome">
    <div class="welcome-content">
      <div class="logo-animation">
        <div class="logo-circle">
          <n-icon size="64" color="white">
            <sparkles-icon />
          </n-icon>
        </div>
        <div class="logo-ring"></div>
        <div class="logo-ring"></div>
      </div>
      
      <div class="text-animation">
        <h1 class="welcome-title">AI 商品草稿生成器</h1>
        <p class="welcome-subtitle">智能生成 · 高效创作 · 一键完成</p>
      </div>
      
      <div class="features-animation">
        <div class="feature-item" v-for="(feature, index) in features" :key="index"
             :style="{ animationDelay: `${index * 0.2}s` }">
          <div class="feature-icon">
            <n-icon size="24" color="#18a058">
              <component :is="feature.icon" />
            </n-icon>
          </div>
          <div class="feature-text">
            <div class="feature-title">{{ feature.title }}</div>
            <div class="feature-desc">{{ feature.desc }}</div>
          </div>
        </div>
      </div>
      
      <n-button 
        type="primary" 
        size="large" 
        @click="enterApp"
        class="enter-btn"
        :loading="entering"
      >
        <template #icon>
          <n-icon><arrow-forward-icon /></n-icon>
        </template>
        开始体验
      </n-button>
    </div>
    
    <!-- 背景动画 -->
    <div class="background-animation">
      <div class="floating-shape" v-for="i in 6" :key="i"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { 
  NButton, 
  NIcon,
  NText
} from 'naive-ui'
import { 
  Sparkles as SparklesIcon,
  ArrowForward as ArrowForwardIcon,
  Speedometer as SpeedIcon,
  ColorPalette as PaletteIcon,
  Rocket as RocketIcon,
  Heart as HeartIcon
} from '@vicons/ionicons5'

const emit = defineEmits(['enter'])

const showWelcome = ref(true)
const entering = ref(false)

const features = [
  {
    icon: SpeedIcon,
    title: '极速生成',
    desc: '3秒内看到首条结果'
  },
  {
    icon: PaletteIcon,
    title: '智能设计',
    desc: 'AI自动生成主图和文案'
  },
  {
    icon: RocketIcon,
    title: '批量处理',
    desc: '支持Excel批量导入'
  },
  {
    icon: HeartIcon,
    title: '简单易用',
    desc: '拖拽上传，一键完成'
  }
]

const enterApp = () => {
  entering.value = true
  setTimeout(() => {
    showWelcome.value = false
    emit('enter')
  }, 800)
}

onMounted(() => {
  // 3秒后自动进入
  setTimeout(() => {
    if (showWelcome.value) {
      enterApp()
    }
  }, 3000)
})
</script>

<style scoped>
.welcome-screen {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  overflow: hidden;
}

.welcome-content {
  text-align: center;
  z-index: 10;
  position: relative;
  max-width: 600px;
  padding: 40px;
}

.logo-animation {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto 40px;
}

.logo-circle {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #18a058 0%, #36ad6a 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 20px auto;
  box-shadow: 0 8px 32px rgba(24, 160, 88, 0.4);
  animation: logoFloat 3s ease-in-out infinite;
}

.logo-ring {
  position: absolute;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.logo-ring:nth-child(2) {
  width: 100px;
  height: 100px;
  animation: ringPulse 2s ease-in-out infinite;
}

.logo-ring:nth-child(3) {
  width: 120px;
  height: 120px;
  animation: ringPulse 2s ease-in-out infinite 0.5s;
}

.text-animation {
  margin-bottom: 40px;
  animation: textFadeIn 1s ease-out;
}

.welcome-title {
  font-size: 36px;
  font-weight: 700;
  color: white;
  margin-bottom: 12px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.welcome-subtitle {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.features-animation {
  margin-bottom: 48px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  animation: featuresSlideUp 1s ease-out 0.5s both;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  animation: featureItemSlide 0.6s ease-out both;
}

.feature-icon {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.feature-title {
  font-size: 14px;
  font-weight: 600;
  color: white;
  display: block;
  margin-bottom: 2px;
}

.feature-desc {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.8);
}

.enter-btn {
  background: linear-gradient(135deg, #18a058 0%, #36ad6a 100%);
  border: none;
  box-shadow: 0 8px 32px rgba(24, 160, 88, 0.4);
  font-size: 16px;
  font-weight: 600;
  padding: 16px 32px;
  animation: buttonPulse 2s ease-in-out infinite;
  transition: all 0.3s ease;
}

.enter-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(24, 160, 88, 0.5);
}

.background-animation {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}

.floating-shape {
  position: absolute;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  animation: float 6s ease-in-out infinite;
}

.floating-shape:nth-child(1) {
  width: 80px;
  height: 80px;
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.floating-shape:nth-child(2) {
  width: 60px;
  height: 60px;
  top: 60%;
  left: 80%;
  animation-delay: 1s;
}

.floating-shape:nth-child(3) {
  width: 40px;
  height: 40px;
  top: 80%;
  left: 20%;
  animation-delay: 2s;
}

.floating-shape:nth-child(4) {
  width: 100px;
  height: 100px;
  top: 10%;
  right: 10%;
  animation-delay: 3s;
}

.floating-shape:nth-child(5) {
  width: 50px;
  height: 50px;
  bottom: 20%;
  right: 30%;
  animation-delay: 4s;
}

.floating-shape:nth-child(6) {
  width: 70px;
  height: 70px;
  bottom: 10%;
  left: 60%;
  animation-delay: 5s;
}

/* 动画定义 */
@keyframes logoFloat {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

@keyframes ringPulse {
  0%, 100% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.1);
    opacity: 0.7;
  }
}

@keyframes textFadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes featuresSlideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes featureItemSlide {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes buttonPulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  33% {
    transform: translateY(-20px) rotate(120deg);
  }
  66% {
    transform: translateY(-10px) rotate(240deg);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .welcome-content {
    padding: 20px;
  }
  
  .welcome-title {
    font-size: 28px;
  }
  
  .welcome-subtitle {
    font-size: 16px;
  }
  
  .features-animation {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .feature-item {
    padding: 12px;
  }
}
</style>