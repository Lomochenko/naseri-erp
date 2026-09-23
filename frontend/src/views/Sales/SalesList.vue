<template>
  <AdminLayout>
    <div>
      <!-- Breadcrumb -->
      <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <!-- Page Title -->
      <div class="mb-6">
        <h2 class="text-title-md2 font-bold text-black dark:text-white">
          مدیریت فروش
        </h2>
      </div>
        <nav>
          <ol class="flex items-center gap-2">
            <li>
              <router-link class="font-medium text-black dark:text-white" to="/">داشبورد /</router-link>
            </li>
            <li class="font-medium text-black dark:text-white">فروش</li>
          </ol>
        </nav>
      </div>


      <!-- Sales Orders Content -->
      <SalesOrderList />
    </div>
  </AdminLayout>
</template>

<script setup>
import { onMounted } from 'vue'
import { useSalesStore } from '@/stores/sales'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import SalesOrderList from '@/components/sales/SalesOrderList.vue'

// Store
const salesStore = useSalesStore()

// Lifecycle
onMounted(async () => {
  await salesStore.fetchStats()
})
</script>
