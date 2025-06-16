// This file is used as the main entry point for the app build (was previously index.js)
import { createApp } from 'vue'
import { FrappeUI } from 'frappe-ui'
import MermaidEditor from './pages/MermaidEditor.vue'

// Create Vue app
const app = createApp(MermaidEditor)

// Use plugins
app.use(FrappeUI)

// Mount app
app.mount('#app')
