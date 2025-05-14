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
        dark: false,
        colors: {
          primary: '#9155FD',
          secondary: '#8A8D93',
          success: '#56CA00',
          info: '#16B1FF',
          warning: '#FFB400',
          error: '#FF4C51',
          'on-primary': '#FFFFFF',
          'on-secondary': '#FFFFFF',
          'on-success': '#FFFFFF',
          'on-info': '#FFFFFF',
          'on-warning': '#FFFFFF',
          'on-error': '#FFFFFF',
          background: '#F4F5FA',
          'on-background': '#3A3541',
          surface: '#FFFFFF',
          'on-surface': '#3A3541',
        },
      },
      dark: {
        dark: true,
        colors: {
          primary: '#9155FD',
          secondary: '#8A8D93',
          success: '#56CA00',
          info: '#16B1FF',
          warning: '#FFB400',
          error: '#FF4C51',
          background: '#28243D',
          'on-background': '#E7E3FC',
          surface: '#312D4B',
          'on-surface': '#E7E3FC',
        },
      },
    },
  },
  locale: {
    locale: 'fa',
    fallback: 'fa',
    messages: { fa },
  },
  rtl: true, // فعال‌سازی پشتیبانی از RTL
})

const pinia = createPinia()

const app = createApp(App)
  .use(vuetify)
  .use(router)
  .use(pinia);

// راه‌اندازی احراز هویت
const authStore = useAuthStore();
authStore.initAuth().finally(() => {
  // اجرای برنامه
  app.mount('#app');
});
