<template>
  <AdminLayout>
    <div class="mx-auto max-w-screen-2xl p-4 md:p-6 2xl:p-10">
    <!-- Breadcrumb -->
    <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <h2 class="text-title-md2 font-bold text-black dark:text-white">
        مدیریت مشتریان
      </h2>
      <nav>
        <ol class="flex items-center gap-2">
          <li>
            <router-link class="font-medium" to="/">داشبورد /</router-link>
          </li>
          <li class="font-medium text-primary">مشتریان</li>
        </ol>
      </nav>
    </div>

    <!-- Search and Actions -->
    <div class="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div class="flex items-center gap-4">
        <!-- Search Input -->
        <div class="relative">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="جستجو در مشتریان..."
            class="w-64 rounded-lg border border-gray-200 bg-white py-2.5 pl-10 pr-4 text-sm text-gray-800 shadow-sm placeholder:text-gray-400 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:placeholder:text-gray-500"
            @input="handleSearch"
          />
          <div class="absolute left-3 top-1/2 -translate-y-1/2">
            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>

        <!-- Filter Dropdown -->
        <select
          v-model="selectedFilter"
          class="rounded-lg border border-gray-200 bg-white py-2.5 px-4 text-sm text-gray-800 shadow-sm focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 dark:border-gray-700 dark:bg-gray-800 dark:text-white"
          @change="handleSearch"
        >
          <option value="all">همه مشتریان</option>
          <option value="active">مشتریان فعال</option>
          <option value="inactive">مشتریان غیرفعال</option>
        </select>
      </div>

      <!-- Add Customer Button -->
      <button
        @click="showCreateModal = true"
        class="inline-flex items-center justify-center rounded-lg bg-primary px-6 py-2.5 text-center font-medium text-white hover:bg-opacity-90 transition-colors"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        افزودن مشتری جدید
      </button>
    </div>

    <!-- Statistics Cards -->
    <div class="mb-6 grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
      <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">کل مشتریان</p>
            <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ totalCustomers }}</p>
          </div>
          <div class="flex h-12 w-12 items-center justify-center rounded-lg bg-blue-100 dark:bg-blue-900/20">
            <svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
        </div>
      </div>

      <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">مشتریان فعال</p>
            <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ activeCustomers }}</p>
          </div>
          <div class="flex h-12 w-12 items-center justify-center rounded-lg bg-green-100 dark:bg-green-900/20">
            <svg class="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
      </div>

      <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">مشتریان جدید (ماه)</p>
            <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ newCustomersThisMonth }}</p>
          </div>
          <div class="flex h-12 w-12 items-center justify-center rounded-lg bg-purple-100 dark:bg-purple-900/20">
            <svg class="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
            </svg>
          </div>
        </div>
      </div>

      <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">کل خرید</p>
            <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ formatPrice(totalPurchases) }}</p>
          </div>
          <div class="flex h-12 w-12 items-center justify-center rounded-lg bg-yellow-100 dark:bg-yellow-900/20">
            <svg class="w-6 h-6 text-yellow-600 dark:text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Customers Table -->
    <div class="rounded-lg border border-gray-200 bg-white shadow-sm dark:border-gray-700 dark:bg-gray-800">
      <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
          لیست مشتریان
          <span class="text-sm font-normal text-gray-500 dark:text-gray-400">
            ({{ filteredCustomers.length }} مشتری)
          </span>
        </h3>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-sm text-right text-gray-500 dark:text-gray-400">
          <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
            <tr>
              <th scope="col" class="px-6 py-3">نام مشتری</th>
              <th scope="col" class="px-6 py-3">کد مشتری</th>
              <th scope="col" class="px-6 py-3">شماره تماس</th>
              <th scope="col" class="px-6 py-3">آدرس</th>
              <th scope="col" class="px-6 py-3">تاریخ عضویت</th>
              <th scope="col" class="px-6 py-3">وضعیت</th>
              <th scope="col" class="px-6 py-3">عملیات</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="customer in paginatedCustomers"
              :key="customer.id"
              class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
            >
              <td class="px-6 py-4 font-medium text-gray-900 dark:text-white">
                {{ customer.name }}
              </td>
              <td class="px-6 py-4">
                {{ customer.customer_code || 'نامشخص' }}
              </td>
              <td class="px-6 py-4">
                {{ customer.phone_number || customer.phone || 'نامشخص' }}
              </td>
              <td class="px-6 py-4">
                <span class="max-w-xs truncate block" :title="customer.address">
                  {{ customer.address || 'نامشخص' }}
                </span>
              </td>
              <td class="px-6 py-4">
                {{ formatDate(customer.created_at) }}
              </td>
              <td class="px-6 py-4">
                <span
                  :class="{
                    'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300': customer.is_active,
                    'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300': !customer.is_active
                  }"
                  class="text-xs font-medium px-2.5 py-0.5 rounded-full"
                >
                  {{ customer.is_active ? 'فعال' : 'غیرفعال' }}
                </span>
              </td>
              <td class="px-6 py-4">
                <div class="flex items-center gap-2">
                  <button
                    @click="editCustomer(customer)"
                    class="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300"
                    title="ویرایش"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button
                    @click="viewCustomerSales(customer)"
                    class="text-green-600 hover:text-green-900 dark:text-green-400 dark:hover:text-green-300"
                    title="مشاهده خریدها"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                    </svg>
                  </button>
                  <button
                    @click="deleteCustomer(customer)"
                    class="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300"
                    title="حذف"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
      <div class="px-6 py-4 border-t border-gray-200 dark:border-gray-700">
        <div class="flex items-center justify-between">
          <div class="text-sm text-gray-700 dark:text-gray-300">
            نمایش {{ (currentPage - 1) * itemsPerPage + 1 }} تا {{ Math.min(currentPage * itemsPerPage, filteredCustomers.length) }} از {{ filteredCustomers.length }} مشتری
          </div>
          <div class="flex items-center gap-2">
            <button
              @click="currentPage--"
              :disabled="currentPage === 1"
              class="px-3 py-1 text-sm bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed dark:bg-gray-800 dark:border-gray-600 dark:hover:bg-gray-700"
            >
              قبلی
            </button>
            <span class="px-3 py-1 text-sm text-gray-700 dark:text-gray-300">
              صفحه {{ currentPage }} از {{ totalPages }}
            </span>
            <button
              @click="currentPage++"
              :disabled="currentPage === totalPages"
              class="px-3 py-1 text-sm bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed dark:bg-gray-800 dark:border-gray-600 dark:hover:bg-gray-700"
            >
              بعدی
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Customer Modal -->
    <CustomerForm
      v-if="showCreateModal || showEditModal"
      :show="showCreateModal || showEditModal"
      :customer="selectedCustomer"
      @close="closeModals"
      @saved="handleCustomerSaved"
    />
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useSalesStore } from '@/stores/sales'
import CustomerForm from '@/components/sales/CustomerForm.vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'

const router = useRouter()
const route = useRoute()
const salesStore = useSalesStore()

// State
const searchQuery = ref('')
const selectedFilter = ref('all')
const showCreateModal = ref(false)
const showEditModal = ref(false)
const selectedCustomer = ref(null)
const currentPage = ref(1)
const itemsPerPage = ref(20)

// Computed
const totalCustomers = computed(() => salesStore.customers.length)
const activeCustomers = computed(() => salesStore.customers.filter(c => c.is_active).length)
const newCustomersThisMonth = computed(() => {
  const now = new Date()
  const thisMonth = new Date(now.getFullYear(), now.getMonth(), 1)
  return salesStore.customers.filter(c => new Date(c.created_at) >= thisMonth).length
})
const totalPurchases = ref(0)

const filteredCustomers = computed(() => {
  let customers = salesStore.customers

  // Apply search filter
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    customers = customers.filter(customer =>
      customer.name.toLowerCase().includes(query) ||
      (customer.phone_number && customer.phone_number.includes(query)) ||
      (customer.phone && customer.phone.includes(query)) ||
      (customer.customer_code && customer.customer_code.toLowerCase().includes(query)) ||
      (customer.address && customer.address.toLowerCase().includes(query))
    )
  }

  // Apply status filter
  if (selectedFilter.value === 'active') {
    customers = customers.filter(c => c.is_active)
  } else if (selectedFilter.value === 'inactive') {
    customers = customers.filter(c => !c.is_active)
  }

  return customers
})

const totalPages = computed(() => Math.ceil(filteredCustomers.value.length / itemsPerPage.value))

const paginatedCustomers = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredCustomers.value.slice(start, end)
})

// Methods
const formatPrice = (price) => {
  if (!price) return '0 تومان'
  return new Intl.NumberFormat('fa-IR').format(price) + ' تومان'
}

const formatDate = (dateString) => {
  if (!dateString) return 'نامشخص'
  try {
    const date = new Date(dateString)
    return new Intl.DateTimeFormat('fa-IR').format(date)
  } catch (error) {
    return 'نامشخص'
  }
}

const handleSearch = () => {
  currentPage.value = 1 // Reset to first page when searching
}

const editCustomer = (customer) => {
  selectedCustomer.value = customer
  showEditModal.value = true
}

const viewCustomerSales = (customer) => {
  router.push({
    path: '/sales',
    query: { customer: customer.id, search: customer.name }
  })
}

const deleteCustomer = async (customer) => {
  if (confirm(`آیا از حذف مشتری "${customer.name}" اطمینان دارید؟`)) {
    try {
      const result = await salesStore.deleteCustomer(customer.id)
      if (result.success) {
        // Success message
        alert(`مشتری "${customer.name}" با موفقیت حذف شد`)
        // Refresh customers list to ensure UI is updated
        await salesStore.fetchCustomers()
      } else {
        // Show error from store
        alert(result.error || 'خطا در حذف مشتری')
      }
    } catch (error) {
      console.error('Error deleting customer:', error)
      alert('خطا در حذف مشتری: ' + (error.message || 'خطای نامشخص'))
    }
  }
}

const closeModals = () => {
  showCreateModal.value = false
  showEditModal.value = false
  selectedCustomer.value = null
}

const handleCustomerSaved = async () => {
  closeModals()
  // Refresh customers list
  await salesStore.fetchCustomers()
}

const fetchTotalPurchases = async () => {
  try {
    totalPurchases.value = await salesStore.getTotalPurchases()
  } catch (error) {
    console.error('Error fetching total purchases:', error)
  }
}

// Watch for route query changes (from search bar)
watch(() => route.query, (newQuery) => {
  if (newQuery.search) {
    searchQuery.value = newQuery.search
  }
  if (newQuery.customer) {
    // Highlight specific customer if needed
    const customer = salesStore.customers.find(c => c.id == newQuery.customer)
    if (customer) {
      selectedCustomer.value = customer
    }
  }
}, { immediate: true })

// Lifecycle
onMounted(async () => {
  // Fetch customers if not already loaded
  if (salesStore.customers.length === 0) {
    await salesStore.fetchCustomers()
  }
  // Fetch total purchases data
  await fetchTotalPurchases()
})
</script>

<style scoped>
/* Add any custom styles here */
</style>
