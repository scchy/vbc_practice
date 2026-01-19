<template>
  <n-config-provider :theme="theme" :theme-overrides="themeOverrides">
    <n-global-style />
    <n-message-provider>
      <n-dialog-provider>
        <!-- 欢迎屏幕 -->
        <welcome-screen v-if="showWelcome" @enter="handleWelcomeEnter" />
        
        <!-- 主应用 -->
        <div class="app-container" v-else>
          <!-- 头部导航 -->
          <n-layout-header class="app-header" bordered>
            <div class="header-content">
              <n-space align="center" justify="space-between">
                <n-space align="center" :size="12">
                  <div class="logo">
                    <n-icon size="32" color="#18a058">
                      <sparkles-icon />
                    </n-icon>
                  </div>
                  <div>
                    <n-text class="app-title">电商草稿生成器</n-text>
                    <n-text depth="3" style="font-size: 12px;">AI 智能生成 · 高效创作</n-text>
                  </div>
                </n-space>
                <n-space>
                  <n-button 
                    quaternary 
                    circle
                    @click="showHelp = true"
                  >
                    <template #icon>
                      <n-icon><help-icon /></n-icon>
                    </template>
                  </n-button>
                  <n-button 
                    quaternary 
                    circle
                    @click="toggleTheme"
                  >
                    <template #icon>
                      <n-icon>
                        <component :is="themeIcon" />
                      </n-icon>
                    </template>
                  </n-button>
                </n-space>
              </n-space>
            </div>
          </n-layout-header>

          <!-- 主内容区 -->
          <n-layout-content class="app-content">
            <router-view />
          </n-layout-content>

          <!-- 底部 -->
          <n-layout-footer class="app-footer" bordered>
            <n-text depth="3">© 2024 电商草稿生成器 - Powered by AI</n-text>
          </n-layout-footer>
        </div>

        <!-- 帮助对话框 -->
        <n-modal v-model:show="showHelp" preset="card" title="使用帮助" style="width: 600px">
          <div class="help-content">
            <n-steps :current="5" vertical>
              <n-step title="上传 Excel 文件" description="准备包含商品信息的 Excel 文件，确保包含必要的列：name, category, brand, material, size, color, targetGroup" />
              <n-step title="上传商品图片" description="可选步骤，上传商品图片以获得更好的主图生成效果" />
              <n-step title="配置生成选项" description="选择是否保存到素材库，设置生成参数" />
              <n-step title="开始智能生成" description="点击生成按钮，AI 将自动创建标题、卖点和主图" />
              <n-step title="下载和使用" description="生成完成后，可以预览、复制或打包下载所有内容" />
            </n-steps>
          </div>
        </n-modal>
      </n-dialog-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { darkTheme, type GlobalTheme, type GlobalThemeOverrides } from 'naive-ui'
import { 
  Sparkles as SparklesIcon, 
  Help as HelpIcon,
  Sunny as SunIcon,
  Moon as MoonIcon
} from '@vicons/ionicons5'
import WelcomeScreen from '@/components/WelcomeScreen.vue'

const showWelcome = ref(true)
const showHelp = ref(false)
const isDark = ref(false)

const theme = computed<GlobalTheme | null>(() => 
  isDark.value ? darkTheme : null
)

const themeIcon = computed(() => 
  isDark.value ? MoonIcon : SunIcon
)

// 自定义主题配置
const themeOverrides: GlobalThemeOverrides = {
  common: {
    primaryColor: '#18a058',
    primaryColorHover: '#36ad6a',
    primaryColorPressed: '#0c7a43',
    primaryColorSuppl: '#18a058',
  },
  Card: {
    borderRadius: '12px',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)',
  },
  Button: {
    borderRadius: '8px',
  },
  Input: {
    borderRadius: '8px',
  }
}

const handleWelcomeEnter = () => {
  showWelcome.value = false
}

const toggleTheme = () => {
  isDark.value = !isDark.value
  // 保存主题偏好
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

// 恢复主题偏好
const savedTheme = localStorage.getItem('theme')
if (savedTheme) {
  isDark.value = savedTheme === 'dark'
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  transition: background 0.3s ease;
}

.app-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  padding: 16px 0;
  position: sticky;
  top: 0;
  z-index: 100;
  transition: all 0.3s ease;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #18a058 0%, #36ad6a 100%);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(24, 160, 88, 0.3);
  animation: logoGlow 3s ease-in-out infinite;
}

.app-title {
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(135deg, #18a058 0%, #36ad6a 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.app-content {
  flex: 1;
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.app-footer {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  text-align: center;
  padding: 20px;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
}

.help-content {
  padding: 20px 0;
}

.help-title {
  font-size: 16px;
  font-weight: 600;
  display: block;
  margin-bottom: 12px;
}

.help-content {
  font-size: 14px;
}

/* 暗色主题适配 */
:deep(.n-layout-header) {
  background: rgba(255, 255, 255, 0.95);
}

:deep(.dark .n-layout-header) {
  background: rgba(16, 16, 16, 0.95);
}

:deep(.dark .app-container) {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
}

:deep(.dark .app-footer) {
  background: rgba(16, 16, 16, 0.8);
}

/* 动画 */
@keyframes logoGlow {
  0%, 100% {
    box-shadow: 0 4px 12px rgba(24, 160, 88, 0.3);
  }
  50% {
    box-shadow: 0 8px 24px rgba(24, 160, 88, 0.5);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    padding: 0 16px;
  }
  
  .app-content {
    padding: 16px;
  }
  
  .app-title {
    font-size: 20px;
  }
  
  .page-header {
    padding: 32px 16px 24px;
  }
  
  .page-title {
    font-size: 24px;
  }
}
</style>