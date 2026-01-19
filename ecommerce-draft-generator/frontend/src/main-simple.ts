import { createApp, ref, computed } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import naive from 'naive-ui'
import SimpleApp from './SimpleApp.vue'
import SimpleUploadPage from './pages/SimpleUploadPage.vue'
import "/src/styles/global.css"

const routes = [
  { path: "/", redirect: "/upload" },
  { path: "/upload", component: SimpleUploadPage }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(SimpleApp)
app.use(createPinia())
app.use(router)
app.use(naive)
app.mount("#app")