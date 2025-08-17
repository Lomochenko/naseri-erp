<template>
  <div class="rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark">
    <!-- Header -->
    <div class="px-4 py-6 md:px-6 xl:px-7.5 flex items-center justify-between">
      <h4 class="text-xl font-semibold text-black dark:text-white">
        مشتریان
      </h4>
      <div class="flex gap-2">
        <button @click="showCreateModal = true"
          class="inline-flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-opacity-90 transition-colors">
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          مشتری جدید
        </button>
        <button @click="refreshData"
          class="inline-flex items-center gap-2 rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors">
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          بروزرسانی
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="border-b border-stroke px-4 py-4 dark:border-strokedark">
      <div class="flex flex-col gap-4 md:flex-row md:items-center md:gap-6">
        <!-- Search -->
        <div class="flex-1">
          <input v-model="searchQuery" type="text" placeholder="جستجو در مشتریان..."
            class="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white" />
        </div>

        <!-- Type Filter -->
        <select v-model="typeFilter"
          class="rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white">
          <option value="">همه انواع</option>
          <option value="individual">شخص حقیقی</option>
          <option value="business">شخص حقوقی</option>
        </select>

        <!-- Category Filter -->
        <select v-model="categoryFilter"
          class="rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white">
          <option value="">همه دسته‌ها</option>
          <option value="retail">خرده‌فروش</option>
          <option value="wholesale">عمده‌فروش</option>
          <option value="contractor">پیمانکار</option>
          <option value="other">سایر</option>
        </select>

        <!-- Status Filter -->
        <select v-model="statusFilter"
          class="rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white">
          <option value="">همه وضعیت‌ها</option>
          <option value="active">فعال</option>
          <option value="inactive">غیرفعال</option>
        </select>
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
    <div v-else class="overflow-x-auto">
      <table class="w-full table-auto">
        <thead>
          <tr class="bg-gray-2 text-right dark:bg-meta-4">
            <th class="px-4 py-4 font-medium text-black dark:text-white xl:pl-11">نام مشتری</th>
            <th class="px-4 py-4 font-medium text-black dark:text-white">تلفن</th>
            <th class="px-4 py-4 font-medium text-black dark:text-white">نوع</th>
            <th class="px-4 py-4 font-medium text-black dark:text-white">دسته‌بندی</th>
            <th class="px-4 py-4 font-medium text-black dark:text-white">سقف اعتبار</th>
            <th class="px-4 py-4 font-medium text-black dark:text-white">بدهی فعلی</th>
            <th class="px-4 py-4 font-medium text-black dark:text-white">وضعیت</th>
            <th class="px-4 py-4 font-medium text-black dark:text-white">عملیات</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="customer in paginatedCustomers" :key="customer.id"
            class="border-b border-stroke dark:border-strokedark hover:bg-gray-50 dark:hover:bg-gray-800">
            <td class="px-4 py-5 pl-9 xl:pl-11">
              <div>
                <h5 class="font-medium text-black dark:text-white">{{ customer.name }}</h5>
                <p v-if="customer.email" class="text-sm text-gray-500">{{ customer.email }}</p>
              </div>
            </td>
            <td class="px-4 py-5">
              <p class="text-black dark:text-white">{{ customer.phone }}</p>
            </td>
            <td class="px-4 py-5">
              <span class="text-sm">{{ getCustomerTypeText(customer.customer_type) }}</span>
            </td>
            <td class="px-4 py-5">
              <span class="text-sm">{{ getCategoryText(customer.business_category) }}</span>
            </td>
            <td class="px-4 py-5">
              <p class="text-black dark:text-white">{{ formatPrice(customer.credit_limit) }}</p>
            </td>
            <td class="px-4 py-5">
              <p :class="customer.current_debt > 0 ? 'text-red-600' : 'text-green-600'">
                {{ formatPrice(customer.current_debt || 0) }}
              </p>
            </td>
            <td class="px-4 py-5">
              <span :class="customer.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                class="inline-flex rounded-full px-3 py-1 text-xs font-medium">
                {{ customer.is_active ? 'فعال' : 'غیرفعال' }}
              </span>
            </td>
            <td class="px-4 py-5">
              <div class="flex items-center space-x-3.5 space-x-reverse">
                <!-- View -->
                <button @click="viewCustomer(customer)" class="hover:text-primary" title="مشاهده">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </button>

                <!-- Edit -->
                <button @click="editCustomer(customer)" class="hover:text-primary" title="ویرایش">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>

                <!-- Toggle Status -->
                <button @click="toggleCustomerStatus(customer)"
                  :class="customer.is_active ? 'hover:text-red-600' : 'hover:text-green-600'"
                  :title="customer.is_active ? 'غیرفعال کردن' : 'فعال کردن'">
                  <svg v-if="customer.is_active" class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728L5.636 5.636m12.728 12.728L18.364 5.636M5.636 18.364l12.728-12.728" />
                  </svg>
                  <svg v-else class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </button>

                <!-- Delete -->
                <button @click="deleteCustomer(customer)" class="hover:text-danger" title="حذف">
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
    <CustomerForm v-if="showCreateModal" @close="showCreateModal = false" @saved="handleCustomerSaved" />
    <CustomerForm v-if="showEditModal" :customer="editingCustomer" @close="showEditModal = false" @saved="handleCustomerSaved" />
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
    'individual': 'شخص حقیقی',
    'business': 'شخص حقوقی'
  }
  return typeMap[type] || type
}

const getCategoryText = (category) => {
  const categoryMap = {
    'retail': 'خرده‌فروش',
    'wholesale': 'عمده‌فروش',
    'contractor': 'پیمانکار',
    'other': 'سایر'
  }
  return categoryMap[category] || category || '-'
}

const viewCustomer = (customer) => {
  // TODO: Implement customer view modal
  alert('نمایش جزئیات مشتری به‌زودی اضافه خواهد شد')
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
  const result = await salesStore.updateCustomer(customer.id, { is_active: newStatus })
  if (!result.success) {
    alert('خطا در تغییر وضعیت: ' + result.error)
  }
}

const refreshData = async () => {
  await salesStore.fetchCustomers()
}

const handleCustomerSaved = () => {
  showCreateModal.value = false
  showEditModal.value = false
  editingCustomer.value = null
  refreshData()
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
