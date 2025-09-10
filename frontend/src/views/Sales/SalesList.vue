<template>
  <AdminLayout>
    <div>
      <!-- Breadcrumb -->
      <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <!-- Modern Tabs -->
      <div class="mb-6">
        <div class="bg-gray-100 dark:bg-gray-800 p-1 rounded-xl inline-flex">
          <button @click="activeTab = 'orders'" :class="[
            'px-4 py-2 text-sm font-medium rounded-lg transition-all duration-300 flex items-center',
            activeTab === 'orders'
              ? 'bg-white dark:bg-gray-700 dark:text-white shadow-md'
              : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
          ]">
            <BarChartIcon class="ml-1"/>
            سفارشات فروش
          </button>
          <button @click="activeTab = 'customers'" :class="[
            'px-4 py-2 text-sm font-medium rounded-lg transition-all duration-300 flex items-center',
            activeTab === 'customers'
              ? 'bg-white dark:bg-gray-700 dark:text-white shadow-md'
              : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
          ]">
           <UserCircleIcon class="ml-1"/>
            مشتریان
          </button>
        </div>
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


      <!-- Tab Content -->
      <div v-if="activeTab === 'orders'">
        <SalesOrderList />
      </div>

      <div v-if="activeTab === 'customers'">
        <CustomerList />
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useSalesStore } from '@/stores/sales'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import SalesOrderList from '@/components/sales/SalesOrderList.vue'
import CustomerList from '@/components/sales/CustomerList.vue'
import UserCircleIcon from '../../icons/UserCircleIcon.vue'
import BarChartIcon from '../../icons/BarChartIcon.vue'

// Store
const salesStore = useSalesStore()

// State
const activeTab = ref('orders')

// Computed
const salesStats = computed(() => salesStore.stats || {
  todaySales: 0,
  monthSales: 0,
  totalCustomers: 0,
  pendingOrders: 0
})

// Methods
const formatPrice = (price) => {
  if (!price) return '0 تومان'
  return new Intl.NumberFormat('fa-IR').format(price) + ' تومان'
}

// Lifecycle
onMounted(async () => {
  await salesStore.fetchStats()
})
</script>
