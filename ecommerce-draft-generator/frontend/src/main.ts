import { createApp } from 'vue'
import { createPinia } from 'pinia'
import naive from 'naive-ui'
import SimpleApp from './SimpleApp.vue'
import "/src/styles/global.css"

const app = createApp(SimpleApp)
app.use(createPinia())
app.use(naive)
app.mount("#app")