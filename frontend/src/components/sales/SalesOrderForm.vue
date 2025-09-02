<template>
  <div v-if="show" class="fixed inset-0 flex items-center justify-center overflow-y-auto z-99999">
    <div
      class="fixed inset-0 h-full w-full bg-gray-400/50 backdrop-blur-[32px]"
      aria-hidden="true"
      @click="$emit('close')"
    ></div>

    <!-- Modal Body -->
    <div class="relative w-full max-w-6xl mx-4 bg-white rounded-xl shadow-2xl dark:bg-gray-900 max-h-[90vh] overflow-y-auto">
      <!-- Modal Header -->
      <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 rounded-t-xl">
        <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
          {{ isEditing ? 'ویرایش سفارش فروش' : 'سفارش فروش جدید' }}
        </h3>
        <button @click="$emit('close')" class="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Modal Content -->
      <div class="p-6">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Customer & Basic Info -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <!-- Customer Selection -->
            <div>
              <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">مشتری *</label>
              <div class="flex gap-2">
                <div class="flex-1 relative">
                  <input v-model="customerSearch" type="text" placeholder="جستجو مشتری..."
                    @input="filterCustomers"
                    @focus="showCustomerDropdown = true"
                    class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white" />

                  <!-- Customer Dropdown -->
                  <div v-if="showCustomerDropdown && filteredCustomers.length > 0"
                    class="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto dark:bg-gray-700 dark:border-gray-600">
                    <div v-for="customer in filteredCustomers" :key="customer.id"
                      @click="selectCustomer(customer)"
                      class="px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 cursor-pointer">
                      <div class="font-medium  dark:text-white">{{ customer.name }}</div>
                      <div class="text-sm text-gray-500 dark:tegray-300">{{ customer.phone }}</div>
                    </div>
                  </div>
                </div>
                <button type="button" @click="showNewCustomerModal = true"
                  class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Sale Type -->
            <div>
              <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">نوع فروش *</label>
              <select v-model="form.sale_type" required
                class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white">
                <option value="retail">خرده‌فروشی</option>
                <option value="wholesale">عمده‌فروشی</option>
              </select>
            </div>

            <!-- Sale Date -->
            <div class=" dark:bg-white">
              <label class="mb-2 block text-sm font-medium text-gray-700">تاریخ فروش *</label>
              <div class="w-48">
                <DatePicker v-model="form.sale_date" format="YYYY/MM/DD" display-format="jYYYY/jMM/jDD"
                  :editable="false" :clearable="false" required
                  class="w- px-3 py-2 text-sm focus:border-primary focus:outline-none text-black" />
              </div>
            </div>


          </div>

          <!-- Products Section -->
          <div class="mb-6">
            <div class="flex items-center justify-between mb-4">
              <h4 class="text-lg font-medium text-gray-900 dark:text-white">محصولات</h4>
              <button type="button" @click="addProduct"
                class="rounded-lg bg-primary px-4 py-2 text-white hover:bg-opacity-90 transition-colors">
                افزودن محصول
              </button>
            </div>

            <!-- Products List -->
            <div class="space-y-4">
              <div v-for="(item, index) in form.items" :key="index"
                class="border border-gray-200 rounded-lg p-4 dark:border-gray-700">
                <div class="grid grid-cols-1 md:grid-cols-5 gap-4 items-end">
                  <!-- Product -->
                  <div class="md:col-span-2 relative">
                    <label class="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">محصول</label>
                    <input v-model="item.productSearch" type="text" placeholder="جستجو محصول..."
                      @input="filterProducts(index)"
                      @focus="item.showProductDropdown = true"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white" />

                    <!-- Product Dropdown -->
                    <div v-if="item.showProductDropdown && item.filteredProducts?.length > 0"
                      class="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto dark:bg-gray-700 dark:border-gray-600">
                      <div v-for="product in item.filteredProducts" :key="product.id"
                        @click="selectProduct(index, product)"
                        class="px-3 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 cursor-pointer">
                        <div class="font-medium">{{ product.name }} ({{ product.code }})</div>
                        <div class="text-sm text-gray-500">موجودی: {{ product.current_stock }} - قیمت: {{ formatPrice(product.selling_price) }}</div>
                      </div>
                    </div>
                  </div>

                  <!-- Quantity -->
                  <div>
                    <label class="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">تعداد</label>
                    <input v-model.number="item.quantity" type="number" min="0.01" step="0.01" required
                      @input="calculateItemTotal(index)"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white" />
                  </div>

                  <!-- Unit Price -->
                  <div>
                    <label class="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">قیمت واحد</label>
                    <input v-model.number="item.unit_price" type="number" min="0" step="1000" required
                      @input="calculateItemTotal(index)"
                      class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white" />
                  </div>

                  <!-- Actions -->
                  <div class="flex items-center gap-2">
                    <span class="text-sm font-medium text-gray-700 dark:text-gray-300">
                      {{ formatPrice(item.quantity * item.unit_price) }}
                    </span>
                    <button type="button" @click="removeProduct(index)"
                      class="rounded-lg p-2 text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20">
                      <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Totals & Discount -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <!-- Notes -->
            <div>
              <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">یادداشت</label>
              <textarea v-model="form.notes" rows="3"
                class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                placeholder="یادداشت اختیاری..."></textarea>
            </div>

            <!-- Totals -->
            <div class="space-y-3">
              <div class="flex justify-between">
                <span class="text-sm font-medium text-gray-700 dark:text-gray-300">جمع کل:</span>
                <span class="text-sm font-bold text-gray-900 dark:text-white">{{ formatPrice(subtotal) }}</span>
              </div>

              <div class="grid grid-cols-2 gap-2">
                <div>
                  <label class="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">تخفیف (تومان)</label>
                  <input v-model.number="form.discount_amount" type="number" min="0" step="1000"
                    @input="form.discount_percent = 0"
                    class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white" />
                </div>
                <div>
                  <label class="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">تخفیف (%)</label>
                  <input v-model.number="form.discount_percent" type="number" min="0" max="100" step="1"
                    @input="form.discount_amount = 0"
                    class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white" />
                </div>
              </div>

              <div class="flex justify-between border-t pt-2">
                <span class="font-medium text-gray-900 dark:text-white">مبلغ نهایی:</span>
                <span class="font-bold text-lg text-gray-900 dark:text-white">{{ formatPrice(total) }}</span>
              </div>
            </div>
          </div>
        </form>
      </div>

      <!-- Modal Footer -->
      <div class="flex items-center justify-start gap-3 px-6 py-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 rounded-b-xl">
        <button type="submit" @click="handleSubmit" :disabled="loading || !isFormValid"
          class="inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary dark:bg-gray-700 dark:text-gray-300 dark:border-gray-600 dark:hover:bg-gray-600 disabled:cursor-not-allowed">
          <svg v-if="loading" class="w-4 h-4 mr-2 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ loading ? 'در حال ذخیره...' : (isEditing ? 'به‌روزرسانی' : 'ایجاد سفارش') }}
        </button>
        <button type="button" @click="$emit('close')"
          class="inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary dark:bg-gray-700 dark:text-gray-300 dark:border-gray-600 dark:hover:bg-gray-600">
          انصراف
        </button>
      </div>
    </div>
  </div>

  <!-- New Customer Modal -->
  <CustomerForm :show="showNewCustomerModal" @close="showNewCustomerModal = false" @saved="handleNewCustomerSaved" />
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useSalesStore } from '@/stores/sales'
import { useProductsStore } from '@/stores/products'
import DatePicker from 'vue3-persian-datetime-picker'
import CustomerForm from './CustomerForm.vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  salesOrder: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'saved'])

// Stores
const salesStore = useSalesStore()
const productsStore = useProductsStore()

// State
const loading = ref(false)
const isEditing = computed(() => !!props.salesOrder)
const customerSearch = ref('')
const showCustomerDropdown = ref(false)
const filteredCustomers = ref([])
const showNewCustomerModal = ref(false)

const form = ref({
  customer: '',
  sale_type: 'retail',
  sale_date: new Date().toISOString().split('T')[0],
  notes: '',
  discount_amount: 0,
  discount_percent: 0,
  items: []
})

// Computed
const customers = computed(() => salesStore.customers)
const availableProducts = computed(() => productsStore.products.filter(p => p.is_active))

const subtotal = computed(() => {
  return form.value.items.reduce((sum, item) => sum + (item.quantity * item.unit_price), 0)
})

const total = computed(() => {
  const discountAmount = form.value.discount_percent > 0
    ? (subtotal.value * form.value.discount_percent / 100)
    : (form.value.discount_amount || 0)
  return Math.max(0, subtotal.value - discountAmount)
})

const isFormValid = computed(() => {
  const hasCustomer = form.value.customer && form.value.customer !== ''
  const hasItems = form.value.items.length > 0
  const itemsValid = form.value.items.every(item => {
    const hasProduct = item.product && item.product !== ''
    const hasValidQuantity = item.quantity && parseFloat(item.quantity) > 0
    const hasValidPrice = item.unit_price !== undefined && parseFloat(item.unit_price) >= 0

    console.log('Item validation:', {
      product: item.product,
      hasProduct,
      quantity: item.quantity,
      hasValidQuantity,
      unit_price: item.unit_price,
      hasValidPrice
    })

    return hasProduct && hasValidQuantity && hasValidPrice
  })

  console.log('Form validation details:', {
    hasCustomer,
    hasItems,
    itemsValid,
    customer: form.value.customer,
    items: form.value.items
  })

  return hasCustomer && hasItems && itemsValid
})

// Methods
const formatPrice = (price) => {
  if (!price) return '0 تومان'
  return new Intl.NumberFormat('fa-IR').format(price) + ' تومان'
}

// Customer methods
const filterCustomers = () => {
  const search = customerSearch.value.toLowerCase()
  filteredCustomers.value = customers.value.filter(customer =>
    customer.name.toLowerCase().includes(search) ||
    customer.phone.includes(search)
  )
}

const selectCustomer = (customer) => {
  form.value.customer = customer.id
  customerSearch.value = `${customer.name}`
  showCustomerDropdown.value = false
}

// Product methods
const addProduct = () => {
  form.value.items.push({
    product: '',
    productSearch: '',
    quantity: 1,
    unit_price: 0,
    showProductDropdown: false,
    filteredProducts: []
  })
}

const removeProduct = (index) => {
  form.value.items.splice(index, 1)
}

const filterProducts = (index) => {
  const item = form.value.items[index]
  const search = item.productSearch.toLowerCase()
  item.filteredProducts = availableProducts.value.filter(product =>
    product.name.toLowerCase().includes(search) ||
    product.code.toLowerCase().includes(search)
  )
}

const selectProduct = (index, product) => {
  const item = form.value.items[index]
  item.product = product.id
  item.productSearch = `${product.name} (${product.code})`
  item.unit_price = product.selling_price
  item.showProductDropdown = false
}

const handleNewCustomerSaved = async () => {
  showNewCustomerModal.value = false
  await salesStore.fetchCustomers()
}





const handleSubmit = async () => {
  console.log('Form validation:', isFormValid.value)
  console.log('Form data:', form.value)

  if (!isFormValid.value) {
    alert('لطفاً تمام فیلدهای اجباری را پر کنید')
    return
  }

  loading.value = true
  try {
    const discountAmount = form.value.discount_percent > 0
      ? (subtotal.value * form.value.discount_percent / 100)
      : (form.value.discount_amount || 0)

    const orderData = {
      customer: parseInt(form.value.customer),
      sale_date: form.value.sale_date,
      notes: form.value.notes || '',
      discount_amount: parseFloat(discountAmount) || 0,
      tax_amount: 0,
      status: 'draft',
      items: form.value.items.map(item => ({
        product: parseInt(item.product),
        quantity: parseFloat(item.quantity) || 0,
        unit_price: parseFloat(item.unit_price) || 0,
        discount: 0,
        notes: ''
      })).filter(item => item.product && item.quantity > 0)
    }

    // Validate data before sending
    if (!orderData.customer) {
      alert('لطفاً مشتری را انتخاب کنید')
      return
    }

    if (!orderData.items || orderData.items.length === 0) {
      alert('لطفاً حداقل یک محصول اضافه کنید')
      return
    }

    console.log('Sending order data:', orderData)

    let result
    if (isEditing.value) {
      console.log('Updating existing order...')
      result = await salesStore.updateSalesOrder(props.salesOrder.id, orderData)
    } else {
      console.log('Creating new order...')
      result = await salesStore.createSalesOrder(orderData)
    }

    console.log('API Result:', result)

    if (result.success) {
      console.log('Order saved successfully:', result.data)
      alert('سفارش با موفقیت ذخیره شد!')
      emit('saved', result.data)
      emit('close')
    } else {
      console.error('Order save failed:', result.error)
      alert('خطا در ذخیره سفارش: ' + result.error)
    }
  } catch (error) {
    console.error('Error saving sales order:', error)
    console.error('Error details:', error.response?.data)

    let errorMessage = 'خطا در ذخیره سفارش'

    if (error.response?.data) {
      if (typeof error.response.data === 'string') {
        errorMessage += ': ' + error.response.data
      } else if (error.response.data.message) {
        errorMessage += ': ' + error.response.data.message
      } else if (error.response.data.non_field_errors) {
        errorMessage += ': ' + error.response.data.non_field_errors.join(', ')
      } else {
        errorMessage += ': ' + JSON.stringify(error.response.data)
      }
    } else if (error.message) {
      errorMessage += ': ' + error.message
    }

    alert(errorMessage)
  } finally {
    loading.value = false
  }
}

// Initialize form if editing
watch(() => props.salesOrder, (newOrder) => {
  if (newOrder) {
    form.value = {
      customer: newOrder.customer,
      sale_type: newOrder.sale_type || 'retail',
      sale_date: newOrder.sale_date,
      notes: newOrder.notes || '',
      discount_amount: newOrder.discount_amount || 0,
      discount_percent: 0,
      items: newOrder.items?.map(item => ({
        product: item.product,
        productSearch: '',
        quantity: item.quantity,
        unit_price: item.unit_price,
        showProductDropdown: false,
        filteredProducts: []
      })) || []
    }
  }
}, { immediate: true })

// Load data on mount
onMounted(async () => {
  await Promise.all([
    salesStore.fetchCustomers(),
    productsStore.fetchProducts()
  ])

  // Initialize customers for search
  filteredCustomers.value = customers.value

  // Add first product row if creating new order
  if (!isEditing.value && form.value.items.length === 0) {
    addProduct()
  }
})
</script>
