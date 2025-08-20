<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center lg:justify-start bg-black bg-opacity-50 p-0 lg:p-4" @click.self="handleOverlayClick">
    <!-- Modal container - full screen on mobile, centered on desktop -->
    <div class="w-full h-full lg:w-auto lg:max-w-2xl lg:h-[85vh] rounded-lg bg-white shadow-xl flex flex-col overflow-visible relative">

      <!-- Close button for large screens (top-left corner with blinking effect) -->
      <button @click="$emit('close')"
        class="hidden lg:block absolute -top-2 -left-2 z-50 rounded-full p-2 bg-red-500 text-white shadow-lg animate-pulse">
        <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <!-- Header with mobile close button -->
      <div class="sticky top-0 z-20 bg-white border-b border-gray-200 px-4 py-3 lg:px-6 lg:py-4">
        <div class="flex items-center justify-between">
          <h3 class="text-lg lg:text-xl font-semibold text-gray-900">
            {{ isEditing ? 'ویرایش مشتری' : 'مشتری جدید' }}
          </h3>
          <!-- Mobile close button -->
          <button @click="$emit('close')" class="lg:hidden rounded-lg p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-600">
            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Form Content -->
      <div class="flex-1 overflow-y-auto">
        <form @submit.prevent="handleSubmit" class="p-4 lg:p-6">
        <!-- Basic Information -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <!-- Name -->
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">نام مشتری *</label>
            <input v-model="form.name" type="text" required
              class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white"
              placeholder="نام کامل مشتری" />
          </div>

          <!-- Phone -->
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">شماره تلفن *</label>
            <input v-model="form.phone" type="tel" required
              class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white"
              placeholder="09123456789" />
          </div>

          <!-- Email -->
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">ایمیل</label>
            <input v-model="form.email" type="email"
              class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white"
              placeholder="customer@example.com" />
          </div>

          <!-- Customer Type -->
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">نوع مشتری *</label>
            <select v-model="form.customer_type" required
              class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white">
              <option value="individual">شخص حقیقی</option>
              <option value="business">شخص حقوقی</option>
            </select>
          </div>

          <!-- Business Category -->
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">دسته‌بندی کسب‌وکار</label>
            <select v-model="form.business_category"
              class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white">
              <option value="">انتخاب کنید</option>
              <option value="retail">خرده‌فروش</option>
              <option value="wholesale">عمده‌فروش</option>
              <option value="contractor">پیمانکار</option>
              <option value="other">سایر</option>
            </select>
          </div>

          <!-- Tax Number -->
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">شماره مالیاتی</label>
            <input v-model="form.tax_number" type="text"
              class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white"
              placeholder="شماره مالیاتی" />
          </div>
        </div>

        <!-- Address -->
        <div class="mb-6">
          <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">آدرس</label>
          <textarea v-model="form.address" rows="3"
            class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white"
            placeholder="آدرس کامل مشتری..."></textarea>
        </div>

        <!-- Financial Settings -->
        <div class="mb-6">
          <!-- Credit Limit -->
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">سقف اعتبار (تومان)</label>
            <input v-model.number="form.credit_limit" type="number" min="0" step="10000"
              class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white"
              placeholder="0" />
            <p class="mt-1 text-xs text-gray-500">حداکثر مبلغ بدهی مجاز برای این مشتری</p>
          </div>
        </div>

        <!-- Status -->
        <div class="mb-6">
          <div class="flex items-center">
            <input v-model="form.is_active" type="checkbox" id="is_active"
              class="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary" />
            <label for="is_active" class="mr-2 text-sm font-medium text-gray-700 dark:text-gray-300">
              مشتری فعال
            </label>
          </div>
        </div>

        <!-- Notes -->
        <div class="mb-6">
          <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">یادداشت</label>
          <textarea v-model="form.notes" rows="3"
            class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white"
            placeholder="یادداشت اختیاری در مورد مشتری..."></textarea>
        </div>

          <!-- Actions -->
          <div class="flex gap-3 justify-end">
            <button type="button" @click="$emit('close')"
              class="rounded-lg border border-gray-300 px-6 py-2 text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700">
              انصراف
            </button>
            <button type="submit" :disabled="loading || !isFormValid"
              class="rounded-lg bg-primary px-6 py-2 text-white hover:bg-opacity-90 disabled:opacity-50 transition-colors">
              {{ loading ? 'در حال ذخیره...' : (isEditing ? 'به‌روزرسانی' : 'ایجاد مشتری') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useSalesStore } from '@/stores/sales'

const props = defineProps({
  customer: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'saved'])

// Handle overlay click
const handleOverlayClick = () => {
  emit('close')
}

// Store
const salesStore = useSalesStore()

// State
const loading = ref(false)
const isEditing = computed(() => !!props.customer)

const form = ref({
  name: '',
  phone: '',
  email: '',
  customer_type: 'individual',
  business_category: '',
  address: '',
  tax_number: '',
  credit_limit: 0,
  is_active: true,
  notes: ''
})

// Computed
const isFormValid = computed(() => {
  return form.value.name.trim() &&
         form.value.phone.trim() &&
         form.value.customer_type
})

// Methods
const handleSubmit = async () => {
  if (!isFormValid.value) return

  loading.value = true
  try {
    let result
    if (isEditing.value) {
      result = await salesStore.updateCustomer(props.customer.id, form.value)
    } else {
      result = await salesStore.createCustomer(form.value)
    }

    if (result.success) {
      emit('saved', result.data)
      emit('close')
    } else {
      alert('خطا در ذخیره مشتری: ' + result.error)
    }
  } catch (error) {
    console.error('Error saving customer:', error)
    alert('خطا در ذخیره مشتری')
  } finally {
    loading.value = false
  }
}

// Initialize form if editing
watch(() => props.customer, (newCustomer) => {
  if (newCustomer) {
    form.value = {
      name: newCustomer.name || '',
      phone: newCustomer.phone || '',
      email: newCustomer.email || '',
      customer_type: newCustomer.customer_type || 'individual',
      business_category: newCustomer.business_category || '',
      address: newCustomer.address || '',
      tax_number: newCustomer.tax_number || '',
      credit_limit: newCustomer.credit_limit || 0,
      is_active: newCustomer.is_active !== false,
      notes: newCustomer.notes || ''
    }
  }
}, { immediate: true })
</script>
