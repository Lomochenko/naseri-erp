<template>
  <AdminLayout>
    <div>
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

    <!-- Action Buttons -->
    <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div class="flex gap-3">
        <button
          @click="showCreateModal = true"
          class="inline-flex items-center justify-center rounded-md bg-primary px-6 py-3 text-center font-medium text-white hover:bg-opacity-90"
        >
          <svg class="mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          افزودن مشتری جدید
        </button>
      </div>

      <!-- Search -->
      <div class="relative">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="جستجو در مشتریان..."
          class="w-full rounded-lg border border-stroke bg-transparent py-3 pl-12 pr-4 text-black focus:border-primary focus-visible:outline-none dark:border-strokedark dark:bg-meta-4 dark:text-white dark:focus:border-primary"
        />
        <svg
          class="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-body"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>
    </div>

    <!-- Customers Table -->
    <div class="rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark">
      <div class="px-4 py-6 md:px-6 xl:px-7.5">
        <h4 class="text-xl font-semibold text-black dark:text-white">
          لیست مشتریان
        </h4>
      </div>

      <div class="grid grid-cols-6 border-t border-stroke px-4 py-4.5 dark:border-strokedark sm:grid-cols-8 md:px-6 2xl:px-7.5">
        <div class="col-span-2 flex items-center">
          <p class="font-medium">نام مشتری</p>
        </div>
        <div class="col-span-2 hidden items-center sm:flex">
          <p class="font-medium">شماره تلفن</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="font-medium">شهر</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="font-medium">کل خرید</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="font-medium">وضعیت</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="font-medium">عملیات</p>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="salesStore.isLoading" class="flex justify-center py-8">
        <div class="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
      </div>

      <!-- Error Message -->
      <div v-if="salesStore.error" class="mx-4 my-4 rounded-lg bg-red-100 p-4 text-red-700">
        {{ salesStore.error }}
      </div>

      <!-- Customer Data -->
      <div v-for="customer in filteredCustomers" :key="customer.id" class="grid grid-cols-6 border-t border-stroke px-4 py-4.5 dark:border-strokedark sm:grid-cols-8 md:px-6 2xl:px-7.5">
        <div class="col-span-2 flex items-center">
          <div class="flex flex-col gap-1 sm:flex-row sm:items-center">
            <div class="h-12.5 w-15 rounded-md">
              <div class="h-12.5 w-12.5 rounded-full bg-primary/10 flex items-center justify-center">
                <span class="text-primary font-medium">{{ getInitials(customer.name) }}</span>
              </div>
            </div>
            <p class="text-sm text-black dark:text-white">{{ customer.name }}</p>
          </div>
        </div>
        <div class="col-span-2 hidden items-center sm:flex">
          <p class="text-sm text-black dark:text-white">{{ customer.phone }}</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="text-sm text-black dark:text-white">{{ customer.city }}</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="text-sm text-black dark:text-white">{{ formatPrice(customer.total_purchase || 0) }}</p>
        </div>
        <div class="col-span-1 flex items-center">
          <span
            :class="customer.is_active ? 'bg-success text-success' : 'bg-danger text-danger'"
            class="inline-flex rounded-full bg-opacity-10 px-3 py-1 text-sm font-medium"
          >
            {{ customer.is_active ? 'فعال' : 'غیرفعال' }}
          </span>
        </div>
        <div class="col-span-1 flex items-center space-x-2">
          <button
            @click="editCustomer(customer)"
            class="hover:text-primary"
            title="ویرایش"
          >
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>
          <button
            @click="deleteCustomer(customer.id)"
            class="hover:text-danger ml-2"
            title="حذف"
          >
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Create/Edit Customer Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="w-full max-w-md rounded-lg bg-white p-6 dark:bg-boxdark">
        <div class="mb-4 flex items-center justify-between">
          <h3 class="text-lg font-medium text-black dark:text-white">
            {{ editingCustomer ? 'ویرایش مشتری' : 'افزودن مشتری جدید' }}
          </h3>
          <button
            @click="closeModal"
            class="text-gray-400 hover:text-gray-600"
          >
            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="handleSubmit">
          <div class="mb-4">
            <label class="mb-2 block text-sm font-medium text-black dark:text-white">
              نام مشتری <span class="text-red-500">*</span>
            </label>
            <input
              v-model="customerForm.name"
              type="text"
              required
              class="w-full rounded border border-stroke bg-transparent px-3 py-2 text-black outline-none focus:border-primary dark:border-strokedark dark:bg-meta-4 dark:text-white dark:focus:border-primary"
              placeholder="نام کامل مشتری"
            />
          </div>

          <div class="mb-4">
            <label class="mb-2 block text-sm font-medium text-black dark:text-white">
              شماره تلفن <span class="text-red-500">*</span>
            </label>
            <input
              v-model="customerForm.phone"
              type="tel"
              required
              class="w-full rounded border border-stroke bg-transparent px-3 py-2 text-black outline-none focus:border-primary dark:border-strokedark dark:bg-meta-4 dark:text-white dark:focus:border-primary"
              placeholder="09123456789"
            />
          </div>

          <div class="mb-4">
            <label class="mb-2 block text-sm font-medium text-black dark:text-white">
              آدرس
            </label>
            <textarea
              v-model="customerForm.address"
              rows="3"
              class="w-full rounded border border-stroke bg-transparent px-3 py-2 text-black outline-none focus:border-primary dark:border-strokedark dark:bg-meta-4 dark:text-white dark:focus:border-primary"
              placeholder="آدرس کامل مشتری"
            ></textarea>
          </div>

          <div class="mb-6">
            <label class="mb-2 block text-sm font-medium text-black dark:text-white">
              شهر
            </label>
            <input
              v-model="customerForm.city"
              type="text"
              class="w-full rounded border border-stroke bg-transparent px-3 py-2 text-black outline-none focus:border-primary dark:border-strokedark dark:bg-meta-4 dark:text-white dark:focus:border-primary"
              placeholder="نام شهر"
            />
          </div>

          <div class="flex gap-3">
            <button
              type="submit"
              class="flex-1 rounded bg-primary px-4 py-2 text-white hover:bg-opacity-90"
            >
              {{ editingCustomer ? 'به‌روزرسانی' : 'ذخیره' }}
            </button>
            <button
              type="button"
              @click="closeModal"
              class="flex-1 rounded border border-stroke px-4 py-2 text-black hover:bg-gray-50 dark:border-strokedark dark:text-white dark:hover:bg-meta-4"
            >
              انصراف
            </button>
          </div>
        </form>
      </div>
    </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useSalesStore } from '@/stores/sales'
import AdminLayout from '@/components/layout/AdminLayout.vue'

const salesStore = useSalesStore()

// Reactive data
const searchQuery = ref('')
const showCreateModal = ref(false)
const editingCustomer = ref(null)

const customerForm = ref({
  name: '',
  phone: '',
  address: '',
  city: ''
})

// Computed
const filteredCustomers = computed(() => {
  if (!searchQuery.value) return salesStore.customers

  return salesStore.customers.filter(customer =>
    customer.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    customer.phone.includes(searchQuery.value) ||
    customer.city?.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// Methods
const formatPrice = (price) => {
  return new Intl.NumberFormat('fa-IR').format(price) + ' تومان'
}

const getInitials = (name) => {
  return name.split(' ').map(n => n[0]).join('').toUpperCase()
}

const editCustomer = (customer) => {
  editingCustomer.value = customer
  customerForm.value = { ...customer }
  showCreateModal.value = true
}

const deleteCustomer = async (id) => {
  if (confirm('آیا از حذف این مشتری اطمینان دارید؟')) {
    const result = await salesStore.deleteCustomer(id)
    if (!result.success) {
      alert('خطا در حذف مشتری: ' + result.error)
    }
  }
}

const closeModal = () => {
  showCreateModal.value = false
  editingCustomer.value = null
  customerForm.value = {
    name: '',
    phone: '',
    address: '',
    city: ''
  }
}

const handleSubmit = async () => {
  let result

  if (editingCustomer.value) {
    // Update existing customer
    result = await salesStore.updateCustomer(editingCustomer.value.id, customerForm.value)
  } else {
    // Create new customer
    result = await salesStore.createCustomer(customerForm.value)
  }

  if (result.success) {
    closeModal()
  } else {
    alert('خطا: ' + result.error)
  }
}

// Lifecycle
onMounted(async () => {
  await salesStore.fetchCustomers()
})
</script>
