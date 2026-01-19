import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import naive from 'naive-ui'
import App from './App.vue'
import UploadPage from './pages/UploadPage.vue'

// 全局样式
import './styles/global.css'

const routes = [
  { path: '/', redirect: '/upload' },
  { path: '/upload', component: UploadPage }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(naive)
app.mount('#app')