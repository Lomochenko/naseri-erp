<template>
  <div class="overflow-hidden rounded-xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]">
    <!-- Header -->
    <div class="border-b border-gray-200 bg-gray-50 px-6 py-4 dark:border-gray-700 dark:bg-gray-800/50">
      <div class="flex items-center justify-between">
        <h4 class="text-xl font-semibold text-gray-900 dark:text-white">
          مشتریان
        </h4>
        <button @click="showCreateModal = true"
          class="inline-flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-medium text-black dark:text-white border-2 border-black dark:border-white hover:bg-opacity-90 transition-colors">
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          مشتری جدید
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="border-b border-gray-200 bg-gray-50 px-6 py-4 dark:border-gray-700 dark:bg-gray-800/50">
      <div class="grid grid-cols-1 gap-4 md:grid-cols-4">
        <div>
          <input v-model="searchQuery" type="text" placeholder="جستجو در مشتریان..."
            class="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white" />
        </div>
        <div>
          <select v-model="typeFilter"
            class="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white">
            <option value="">همه انواع</option>
            <option value="individual">شخص حقیقی</option>
            <option value="business">شخص حقوقی</option>
          </select>
        </div>
        <div>
          <select v-model="categoryFilter"
            class="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white">
            <option value="">همه دسته‌ها</option>
            <option value="retail">خرده‌فروش</option>
            <option value="wholesale">عمده‌فروش</option>
            <option value="contractor">پیمانکار</option>
            <option value="other">سایر</option>
          </select>
        </div>
        <div>
          <select v-model="statusFilter"
            class="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white">
            <option value="">همه وضعیت‌ها</option>
            <option value="active">فعال</option>
            <option value="inactive">غیرفعال</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center p-8">
      <LoadingSpinner text="در حال بارگذاری مشتریان..." />
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredCustomers.length === 0 && !loading" class="flex flex-col items-center justify-center p-12">
      <svg class="h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
      </svg>
      <h3 class="text-lg font-medium text-gray-900 mb-2">هیچ مشتری‌ای یافت نشد</h3>
      <p class="text-gray-500 mb-4">برای شروع، اولین مشتری خود را اضافه کنید</p>
      <button @click="showCreateModal = true"
        class="inline-flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-opacity-90 transition-colors">
        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        ایجاد مشتری جدید
      </button>
    </div>

    <!-- Customers Table -->
    <div v-else class="max-w-full overflow-x-auto custom-scrollbar">
      <table class="min-w-full">
        <thead>
          <tr class="border-b border-gray-200 dark:border-gray-700">
            <th class="px-5 py-3 text-right w-3/12 sm:px-6">
              <p class="font-medium text-gray-500 text-sm dark:text-gray-400">مشتری</p>
            </th>
            <th class="px-5 py-3 text-right w-2/12 sm:px-6">
              <p class="font-medium text-gray-500 text-sm dark:text-gray-400">تلفن</p>
            </th>
            <th class="px-5 py-3 text-center w-1/12 sm:px-6">
              <p class="font-medium text-gray-500 text-sm dark:text-gray-400">نوع</p>
            </th>
            <th class="px-5 py-3 text-right w-2/12 sm:px-6">
              <p class="font-medium text-gray-500 text-sm dark:text-gray-400">سقف اعتبار</p>
            </th>
            <th class="px-5 py-3 text-right w-2/12 sm:px-6">
              <p class="font-medium text-gray-500 text-sm dark:text-gray-400">موجودی</p>
            </th>
            <th class="px-5 py-3 text-right w-1/12 sm:px-6">
              <p class="font-medium text-gray-500 text-sm dark:text-gray-400">وضعیت</p>
            </th>
            <th class="px-5 py-3 text-center w-1/12 sm:px-6">
              <p class="font-medium text-gray-500 text-sm dark:text-gray-400">عملیات</p>
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
          <tr v-for="customer in paginatedCustomers" :key="customer.id"
            class="border-t border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50">
            <td class="px-5 py-4 sm:px-6">
              <div class="flex items-center gap-3">
                <div>
                  <span class="block font-medium text-gray-800 text-sm dark:text-white/90">
                    {{ customer.name }}
                  </span>
                  <span v-if="customer.customer_code" class="block text-gray-500 text-xs dark:text-gray-400">
                    {{ customer.customer_code }}
                  </span>
                </div>
              </div>
            </td>
            <td class="px-5 py-4 sm:px-6">
              <p class="text-gray-500 text-sm dark:text-gray-400">{{ customer.phone }}</p>
            </td>
            <td class="px-5 py-4 sm:px-6">
              <span class="rounded-full px-2 py-0.5 text-xs font-medium bg-blue-50 text-blue-700 dark:bg-blue-500/15 dark:text-blue-500">
                {{ getCustomerTypeText(customer.customer_type) }}
              </span>
            </td>
            <td class="px-5 py-4 sm:px-6">
              <p class="text-gray-500 text-sm dark:text-gray-400">{{ formatPrice(customer.credit_limit) }}</p>
            </td>
            <td class="px-5 py-4 sm:px-6">
              <p :class="(customer.account_balance || 0) < 0 ? 'text-red-600' : 'text-green-600'" class="text-sm font-medium">
                {{ formatPrice(customer.account_balance || 0) }}
              </p>
            </td>
            <td class="px-5 py-4 sm:px-6">
              <span :class="[
                'rounded-full px-2 py-0.5 text-xs font-medium',
                customer.is_active
                  ? 'bg-success-50 text-success-700 dark:bg-success-500/15 dark:text-success-500'
                  : 'bg-error-50 text-error-700 dark:bg-error-500/15 dark:text-error-500'
              ]">
                {{ customer.is_active ? 'فعال' : 'غیرفعال' }}
              </span>
            </td>
            <td class="px-5 py-4 sm:px-6">
              <div class="flex items-center gap-2">
                <!-- Edit -->
                <button @click="editCustomer(customer)"
                  class="p-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-600 hover:text-primary transition-colors"
                  title="ویرایش">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>

                <!-- Toggle Status -->
                <button @click="toggleCustomerStatus(customer)"
                  :class="customer.is_active ? 'text-green-600 hover:text-red-600' : 'text-red-600 hover:text-green-600'"
                  :title="customer.is_active ? 'غیرفعال کردن' : 'فعال کردن'"
                  class="p-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-all duration-300 transform hover:scale-110">
                  <!-- Active Icon (Green with pulse) -->
                  <svg v-if="customer.is_active" class="h-4 w-4 text-green-600 animate-pulse" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  <!-- Inactive Icon (Red with pulse) -->
                  <svg v-else class="h-4 w-4 text-red-600 animate-pulse" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                  </svg>
                </button>

                <!-- Delete -->
                <button @click="deleteCustomer(customer)"
                  class="p-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-600 hover:text-red-600 transition-colors"
                  title="حذف">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="flex items-center justify-between border-t border-stroke px-4 py-4 dark:border-strokedark">
      <div class="text-sm text-gray-700 dark:text-gray-300">
        نمایش {{ (currentPage - 1) * pageSize + 1 }} تا {{ Math.min(currentPage * pageSize, filteredCustomers.length) }} از {{ filteredCustomers.length }} مشتری
      </div>
      <div class="flex items-center gap-2">
        <button @click="currentPage--" :disabled="currentPage === 1"
          class="rounded-lg border border-gray-300 px-3 py-1 text-sm disabled:opacity-50 dark:border-gray-600">
          قبلی
        </button>
        <span class="px-3 py-1 text-sm">{{ currentPage }} از {{ totalPages }}</span>
        <button @click="currentPage++" :disabled="currentPage === totalPages"
          class="rounded-lg border border-gray-300 px-3 py-1 text-sm disabled:opacity-50 dark:border-gray-600">
          بعدی
        </button>
      </div>
    </div>

    <!-- Modals -->
    <CustomerForm :show="showCreateModal" @close="showCreateModal = false" @saved="handleCustomerSaved" />
    <CustomerForm :show="showEditModal" :customer="editingCustomer" @close="showEditModal = false" @saved="handleCustomerSaved" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useSalesStore } from '@/stores/sales'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import CustomerForm from './CustomerForm.vue'

// Store
const salesStore = useSalesStore()

// State
const searchQuery = ref('')
const typeFilter = ref('')
const categoryFilter = ref('')
const statusFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const editingCustomer = ref(null)
const loading = ref(false)

// Computed
const customers = computed(() => salesStore.customers)

const filteredCustomers = computed(() => {
  let filtered = customers.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(customer =>
      customer.name.toLowerCase().includes(query) ||
      customer.phone.toLowerCase().includes(query) ||
      customer.email?.toLowerCase().includes(query) ||
      customer.national_id?.toLowerCase().includes(query)
    )
  }

  if (typeFilter.value) {
    filtered = filtered.filter(customer => customer.customer_type === typeFilter.value)
  }

  if (categoryFilter.value) {
    filtered = filtered.filter(customer => customer.business_category === categoryFilter.value)
  }

  if (statusFilter.value) {
    const isActive = statusFilter.value === 'active'
    filtered = filtered.filter(customer => customer.is_active === isActive)
  }

  return filtered
})

const paginatedCustomers = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filteredCustomers.value.slice(start, start + pageSize.value)
})

const totalPages = computed(() => {
  return Math.ceil(filteredCustomers.value.length / pageSize.value)
})

// Methods
const formatPrice = (price) => {
  if (!price) return '0 تومان'
  return new Intl.NumberFormat('fa-IR').format(price) + ' تومان'
}

const getCustomerTypeText = (type) => {
  const typeMap = {
    'individual': 'حقیقی',
    'business': 'حقوقی'
  }
  return typeMap[type] || type
}





const editCustomer = (customer) => {
  editingCustomer.value = customer
  showEditModal.value = true
}

const deleteCustomer = async (customer) => {
  if (confirm(`آیا از حذف مشتری ${customer.name} اطمینان دارید؟`)) {
    const result = await salesStore.deleteCustomer(customer.id)
    if (!result.success) {
      alert('خطا در حذف مشتری: ' + result.error)
    }
  }
}

const toggleCustomerStatus = async (customer) => {
  const newStatus = !customer.is_active

  // Send complete customer data with updated status
  const customerData = {
    name: customer.name,
    phone: customer.phone,
    email: customer.email || '',
    customer_type: customer.customer_type || 'individual',
    business_category: customer.business_category || '',
    address: customer.address || '',
    tax_number: customer.tax_number || '',
    credit_limit: customer.credit_limit || 0,
    is_active: newStatus,
    notes: customer.notes || ''
  }

  const result = await salesStore.updateCustomer(customer.id, customerData)
  if (!result.success) {
    alert('خطا در تغییر وضعیت: ' + result.error)
  }
}

const handleCustomerSaved = () => {
  showCreateModal.value = false
  showEditModal.value = false
  editingCustomer.value = null
}

// Lifecycle
onMounted(async () => {
  loading.value = true
  try {
    await salesStore.fetchCustomers()
  } finally {
    loading.value = false
  }
})
</script>
