<template>
  <ThemeProvider>
    <SidebarProvider>
      <AdminLayout v-if="usesAdminLayout">
        <RouterView v-slot="{ Component, route }">
          <Transition name="page" mode="out-in">
            <component :is="Component" :key="route.fullPath" />
          </Transition>
        </RouterView>
      </AdminLayout>
      <RouterView v-else v-slot="{ Component, route }">
        <Transition name="page" mode="out-in">
          <component :is="Component" :key="route.fullPath" />
        </Transition>
      </RouterView>
    </SidebarProvider>
  </ThemeProvider>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AdminLayout from './components/layout/AdminLayout.vue'
import { useAuthStore } from './stores/auth'
import ThemeProvider from './components/layout/ThemeProvider.vue'
import SidebarProvider from './components/layout/SidebarProvider.vue'

const authStore = useAuthStore()
const route = useRoute()
const usesAdminLayout = computed(() => !['Signin', 'PublicInvoice', 'MobilePDFDownload', '404 Error'].includes(route.name))

onMounted(() => {
  // Initialize auth state from localStorage
  authStore.initializeAuth()
})
</script>
