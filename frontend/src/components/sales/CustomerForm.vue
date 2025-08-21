<template>
  <div v-if="show" class="fixed inset-0 flex items-center justify-center overflow-y-auto z-99999">
    <div class="fixed inset-0 h-full w-full bg-gray-400/50 backdrop-blur-[32px]" aria-hidden="true"
      @click="$emit('close')"></div>

    <!-- Modal Body -->
    <div
      class="relative w-full max-w-4xl mx-4 bg-white rounded-xl shadow-2xl dark:bg-gray-900 max-h-[90vh] overflow-y-auto">
      <!-- Modal Header -->
      <div
        class="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 rounded-t-xl">
        <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
          {{ isEditing ? 'ویرایش مشتری' : 'مشتری جدید' }}
        </h3>
        <button @click="$emit('close')"
          class="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Modal Content -->
      <div class="p-6">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Basic Information -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <!-- Customer Code -->
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">کد مشتری</label>
              <input v-model="form.customer_code" type="text" disabled
                class="h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800 disabled:bg-gray-100 disabled:text-gray-500 dark:disabled:bg-gray-800"
                placeholder="خودکار تولید می‌شود" />
              <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">کد مشتری به صورت خودکار تولید می‌شود</p>
            </div>

            <!-- Name -->
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">نام مشتری/شرکت *</label>
              <input v-model="form.name" type="text" required
                class="h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
                placeholder="نام کامل مشتری/شرکت" />
            </div>

            <!-- Phone -->
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">شماره تلفن *</label>
              <input v-model="form.phone" type="tel" required
                class="h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
                placeholder="09123456789" />
            </div>

            <!-- Customer Type -->
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">نوع مشتری *</label>
              <div class="relative z-20 bg-transparent">
                <select v-model="form.customer_type" required
                  class="h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 pr-11 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
                  :class="{ 'text-gray-800 dark:text-white/90': form.customer_type }">
                  <option value="individual">شخص حقیقی</option>
                  <option value="business">شخص حقوقی</option>
                </select>
                <span
                  class="absolute z-30 text-gray-500 -translate-y-1/2 pointer-events-none right-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M7.5 7.5L10 10L12.5 7.5" stroke-width="1.5" stroke-linecap="round"
                      stroke-linejoin="round" />
                  </svg>
                </span>
              </div>
            </div>

            <!-- Business Category -->
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">دسته‌بندی
                کسب‌وکار</label>
              <div class="relative z-20 bg-transparent">
                <select v-model="form.business_category"
                  class="h-11 w-full appearance-none rounded-lg border border-gray-300 bg-transparent bg-none px-4 py-2.5 pr-11 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
                  :class="{ 'text-gray-800 dark:text-white/90': form.business_category }">
                  <option value="">انتخاب کنید</option>
                  <option value="retail">خرده‌فروش</option>
                  <option value="wholesale">عمده‌فروش</option>
                  <option value="contractor">پیمانکار</option>
                  <option value="other">سایر</option>
                </select>
                <span
                  class="absolute z-30 text-gray-500 -translate-y-1/2 pointer-events-none right-4 top-1/2 dark:text-gray-400">
                  <svg class="stroke-current" width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M7.5 7.5L10 10L12.5 7.5" stroke-width="1.5" stroke-linecap="round"
                      stroke-linejoin="round" />
                  </svg>
                </span>
              </div>
            </div>
            <!-- Credit Limit -->
            <div>
              <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">سقف اعتبار (تومان)</label>
              <input v-model.number="form.credit_limit" type="number" min="0" step="10000"
                class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                placeholder="0" />
              <p class="mt-1 text-xs text-gray-500">حداکثر مبلغ بدهی مجاز برای این مشتری</p>
            </div>

            <!-- Address -->
            <div>
              <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">آدرس</label>
              <textarea v-model="form.address" rows="3"
                class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                placeholder="آدرس کامل مشتری + کد پستی"></textarea>
            </div>
            <!-- Account Balance -->
            <div>
              <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">موجودی حساب (تومان)</label>
              <input :value="formatCurrency(form.account_balance || 0)" type="text" disabled
                class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white disabled:bg-gray-100 disabled:text-gray-500 dark:disabled:bg-gray-800"
                :class="(form.account_balance || 0) < 0 ? 'text-red-600' : 'text-green-600'" />
              <p class="mt-1 text-xs text-gray-500">
                {{ (form.account_balance || 0) < 0 ? 'بدهی مشتری' : 'اعتبار مشتری' }} - محاسبه خودکار </p>
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

        </form>
      </div>

      <!-- Modal Footer -->
      <div
        class="flex items-center justify-start gap-3 px-6 py-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 rounded-b-xl">
        <button type="submit" @click="handleSubmit" :disabled="loading || !isFormValid"
          class="inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary dark:bg-gray-700 dark:text-gray-300 dark:border-gray-600 dark:hover:bg-gray-600">
          <svg v-if="loading" class="w-4 h-4 mr-2 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
            </path>
          </svg>
          {{ loading ? 'در حال ذخیره...' : (isEditing ? 'به‌روزرسانی' : 'ایجاد مشتری') }}
        </button>
         <button type="button" @click="$emit('close')"
          class="inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary dark:bg-gray-700 dark:text-gray-300 dark:border-gray-600 dark:hover:bg-gray-600">
          انصراف
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useSalesStore } from '@/stores/sales'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  customer: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'saved'])



// Store
const salesStore = useSalesStore()

// State
const loading = ref(false)
const isEditing = computed(() => !!props.customer)

const form = ref({
  customer_code: '',
  name: '',
  phone: '',
  email: '',
  customer_type: 'individual',
  business_category: '',
  address: '',
  tax_number: '',
  credit_limit: 0,
  account_balance: 0,
  is_active: true,
  notes: ''
})

// Methods
const formatCurrency = (amount) => {
  return new Intl.NumberFormat('fa-IR').format(amount)
}

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
      customer_code: newCustomer.customer_code || '',
      name: newCustomer.name || '',
      phone: newCustomer.phone || '',
      email: newCustomer.email || '',
      customer_type: newCustomer.customer_type || 'individual',
      business_category: newCustomer.business_category || '',
      address: newCustomer.address || '',
      tax_number: newCustomer.tax_number || '',
      credit_limit: newCustomer.credit_limit || 0,
      account_balance: newCustomer.account_balance || 0,
      is_active: newCustomer.is_active !== false,
      notes: newCustomer.notes || ''
    }
  }
}, { immediate: true })
</script>
