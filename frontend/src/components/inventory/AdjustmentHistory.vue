<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="w-full max-w-4xl rounded-lg bg-white p-6 dark:bg-boxdark max-h-[80vh] overflow-y-auto">
      <div class="mb-4 flex items-center justify-between">
        <h3 class="text-lg font-medium text-black dark:text-white">
          تاریخچه تعدیلات موجودی - {{ product.name }}
        </h3>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-600 dark:text-gray-300 dark:hover:text-gray-100"
        >
          <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-8">
        <LoadingSpinner text="در حال بارگذاری تاریخچه..." />
      </div>

      <!-- Empty State -->
      <div v-else-if="adjustments.length === 0" class="text-center py-8">
        <div class="text-gray-500 dark:text-gray-400">
          <svg class="mx-auto h-16 w-16 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 5H7a2 2 0 00-2 2v11a2 2 0 002 2h9.586a1 1 0 00.707-.293L20 14.414V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"/>
          </svg>
          <p>هیچ تعدیل موجودی ثبت نشده است</p>
        </div>
      </div>

      <!-- Adjustments List -->
      <div v-else class="space-y-4">
        <div
          v-for="adjustment in adjustments"
          :key="adjustment.id"
          class="border rounded-lg p-4 dark:border-strokedark"
        >
          <div class="flex justify-between items-start mb-3">
            <div class="flex items-center gap-3">
              <!-- Type Icon -->
              <div
                class="flex h-10 w-10 items-center justify-center rounded-full"
                :class="adjustment.adjustment_type === 'add' ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'"
              >
                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    v-if="adjustment.adjustment_type === 'add'"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                  />
                  <path
                    v-else
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M20 12H4"
                  />
                </svg>
              </div>

              <!-- Adjustment Info -->
              <div>
                <h4 class="font-medium text-black dark:text-white">
                  {{ adjustment.adjustment_type === 'add' ? 'افزایش موجودی' : 'کاهش موجودی' }}
                </h4>
                <p class="text-sm text-gray-500 dark:text-gray-400">
                  {{ formatDate(adjustment.created_at) }}
                </p>
              </div>
            </div>

            <!-- Quantity Badge -->
            <span
              class="px-3 py-1 text-sm font-medium rounded-full"
              :class="adjustment.adjustment_type === 'add' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
            >
              {{ adjustment.adjustment_type === 'add' ? '+' : '-' }}{{ adjustment.total_quantity }}
            </span>
          </div>

          <!-- Reason/Description -->
          <div v-if="adjustment.reason" class="mb-3">
            <h5 class="text-sm font-medium text-gray-900 dark:text-white mb-1">دلیل تعدیل:</h5>
            <p class="text-sm text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 p-3 rounded">
              {{ adjustment.reason }}
            </p>
          </div>

          <!-- Items List -->
          <div v-if="adjustment.items && adjustment.items.length > 0" class="space-y-2">
            <h5 class="text-sm font-medium text-gray-900 dark:text-white">جزئیات:</h5>
            <div class="space-y-1">
              <div
                v-for="item in adjustment.items"
                :key="item.id"
                class="flex justify-between items-center text-sm bg-gray-50 dark:bg-gray-800 p-2 rounded"
              >
                <span class="text-gray-900 dark:text-white">{{ item.product_name }}</span>
                <span class="font-medium">مقدار: {{ item.quantity }}</span>
              </div>
            </div>
          </div>

          <!-- User Info -->
          <div class="mt-3 pt-3 border-t dark:border-gray-700">
            <p class="text-xs text-gray-500 dark:text-gray-400">
              ثبت شده توسط: {{ adjustment.created_by_name || 'نامشخص' }}
            </p>
          </div>
        </div>
      </div>

      <!-- Close Button -->
      <div class="mt-6 flex justify-end">
        <button
          @click="$emit('close')"
          class="px-6 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
        >
          بستن
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { inventoryAPI } from '@/services/api'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})

const adjustments = ref([])
const loading = ref(true)

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const fetchAdjustments = async () => {
  try {
    loading.value = true
    const response = await inventoryAPI.getAdjustments()

    // Filter adjustments for this product and calculate quantities
    const productAdjustments = response.data.results?.filter(adj =>
      adj.items?.some(item => item.product === props.product.id)
    ) || []

    // Add total quantity for display
    adjustments.value = productAdjustments.map(adj => ({
      ...adj,
      total_quantity: adj.items?.reduce((sum, item) =>
        item.product === props.product.id ? sum + parseFloat(item.quantity) : sum, 0
      ) || 0
    }))
  } catch (error) {
    console.error('Error fetching adjustments:', error)
    adjustments.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchAdjustments()
})
</script>

<style scoped>
/* Custom scrollbar */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
