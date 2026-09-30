<template>
  <div v-if="insideAdminLayout"><slot /></div>
  <div v-else class="min-h-screen text-gray-700 dark:text-gray-200 xl:flex">
    <app-sidebar />
    <Backdrop />
    <div
      class="flex-1 transition-all duration-300 ease-in-out"
      :class="[isExpanded || isHovered ? 'lg:ml-[290px]' : 'lg:ml-[90px]']"
    >
      <app-header />
      <div class="admin-content p-4 mx-auto max-w-(--breakpoint-2xl) md:p-6">
        <slot></slot>
      </div>
    </div>
    <MobileBottomNav />
  </div>
</template>

<script setup>
import { inject, provide } from 'vue'
import AppSidebar from './AppSidebar.vue'
import AppHeader from './AppHeader.vue'
import { useSidebar } from '@/composables/useSidebar'
import Backdrop from './Backdrop.vue'
import MobileBottomNav from './MobileBottomNav.vue'
const { isExpanded, isHovered } = useSidebar()
// Route views still use this wrapper; only the persistent outer layout owns the shell.
const insideAdminLayout = inject('erp-admin-layout', false)
provide('erp-admin-layout', true)
</script>
<style scoped>
@media(max-width:767px){.admin-content{padding-bottom:calc(108px + env(safe-area-inset-bottom,0px))}}
@media print{.admin-content{padding-bottom:0}}
</style>
