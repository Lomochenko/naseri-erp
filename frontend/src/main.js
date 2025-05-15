import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'

// Vue Router
import router from './router'

// Pinia Store
import { createPinia } from 'pinia'
import { useAuthStore } from './store/auth'

// Theme and RTL setup
import { fa } from 'vuetify/locale'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

// تنظیمات Vuetify
const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#1976D2',
          secondary: '#424242',
          accent: '#82B1FF',
          error: '#FF5252',
          info: '#2196F3',
          success: '#4CAF50',
          warning: '#FB8C00',
        },
      },
    },
  },
  locale: {
    locale: 'fa',
    messages: { fa }
  },
  rtl: true, // فعال‌سازی پشتیبانی از RTL
})

const pinia = createPinia()

const app = createApp(App)
  .use(vuetify)
  .use(router)
  .use(pinia);

// ابتدا برنامه را اجرا کن
app.mount('#app');

// بررسی وضعیت احراز هویت بدون ایجاد تاخیر در اجرای برنامه
const authStore = useAuthStore()
authStore.initAuth().catch(error => {
  console.log('خطا در بارگذاری وضعیت احراز هویت:', error)
})
