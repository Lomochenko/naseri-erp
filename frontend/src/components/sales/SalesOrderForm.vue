<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center lg:justify-start bg-black bg-opacity-50 p-0 lg:p-4" @click.self="handleOverlayClick">
    <!-- Modal container - full screen on mobile, centered on desktop -->
    <div class="w-full h-full lg:w-auto lg:max-w-4xl lg:h-[85vh] rounded-lg bg-white shadow-xl flex flex-col overflow-visible relative">

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
            {{ isEditing ? 'ویرایش سفارش فروش' : 'سفارش فروش جدید' }}
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
        <!-- Customer & Basic Info -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <!-- Customer Selection -->
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">مشتری *</label>
            <select v-model="form.customer" required
              class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white">
              <option value="">انتخاب مشتری</option>
              <option v-for="customer in customers" :key="customer.id" :value="customer.id">
                {{ customer.name }} - {{ customer.phone }}
              </option>
            </select>
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
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">تاریخ فروش *</label>
            <DatePicker v-model="form.sale_date" format="YYYY/MM/DD" display-format="jYYYY/jMM/jDD"
              :editable="false" :clearable="false" required
              class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white" />
          </div>

          <!-- Warehouse -->
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">انبار *</label>
            <select v-model="form.warehouse" required
              class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white">
              <option value="">انتخاب انبار</option>
              <option v-for="warehouse in warehouses" :key="warehouse.id" :value="warehouse.id">
                {{ warehouse.name }}
              </option>
            </select>
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
                <div class="md:col-span-2">
                  <label class="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">محصول</label>
                  <select v-model="item.product" @change="updateProductInfo(index)" required
                    class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white">
                    <option value="">انتخاب محصول</option>
                    <option v-for="product in availableProducts" :key="product.id" :value="product.id">
                      {{ product.name }} ({{ product.code }}) - موجودی: {{ product.current_stock }}
                    </option>
                  </select>
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

            <div>
              <label class="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">تخفیف (تومان)</label>
              <input v-model.number="form.discount_amount" type="number" min="0" step="1000"
                class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white" />
            </div>

            <div class="flex justify-between border-t pt-2">
              <span class="font-medium text-gray-900 dark:text-white">مبلغ نهایی:</span>
              <span class="font-bold text-lg text-primary">{{ formatPrice(total) }}</span>
            </div>
          </div>
        </div>

          <!-- Actions -->
          <div class="flex gap-3 justify-end">
            <button type="button" @click="$emit('close')"
              class="rounded-lg border border-gray-300 px-6 py-2 text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700">
              انصراف
            </button>
            <button type="submit" :disabled="loading || !isFormValid"
              class="rounded-lg bg-primary px-6 py-2 text-white hover:bg-opacity-90 disabled:opacity-50 transition-colors">
              {{ loading ? 'در حال ذخیره...' : (isEditing ? 'به‌روزرسانی' : 'ایجاد سفارش') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useSalesStore } from '@/stores/sales'
import { useProductsStore } from '@/stores/products'
import { useInventoryStore } from '@/stores/inventory'
import DatePicker from 'vue3-persian-datetime-picker'

const props = defineProps({
  salesOrder: {
    type: Object,
    default: null
  }
})

// Handle overlay click
const handleOverlayClick = () => {
  emit('close')
}

const emit = defineEmits(['close', 'saved'])

// Stores
const salesStore = useSalesStore()
const productsStore = useProductsStore()
const inventoryStore = useInventoryStore()

// State
const loading = ref(false)
const isEditing = computed(() => !!props.salesOrder)

const form = ref({
  customer: '',
  sale_type: 'retail',
  sale_date: new Date().toISOString().split('T')[0],
  warehouse: '',
  notes: '',
  discount_amount: 0,
  items: []
})

// Computed
const customers = computed(() => salesStore.customers)
const warehouses = computed(() => inventoryStore.warehouses)
const availableProducts = computed(() => productsStore.products.filter(p => p.is_active))

const subtotal = computed(() => {
  return form.value.items.reduce((sum, item) => sum + (item.quantity * item.unit_price), 0)
})

const total = computed(() => {
  return Math.max(0, subtotal.value - (form.value.discount_amount || 0))
})

const isFormValid = computed(() => {
  const hasCustomer = form.value.customer && form.value.customer !== ''
  const hasWarehouse = form.value.warehouse && form.value.warehouse !== ''
  const hasItems = form.value.items.length > 0
  const itemsValid = form.value.items.every(item =>
    item.product && item.product !== '' &&
    item.quantity > 0 &&
    item.unit_price >= 0
  )

  console.log('Form validation details:', {
    hasCustomer,
    hasWarehouse,
    hasItems,
    itemsValid,
    customer: form.value.customer,
    warehouse: form.value.warehouse,
    items: form.value.items
  })

  return hasCustomer && hasWarehouse && hasItems && itemsValid
})

// Methods
const formatPrice = (price) => {
  if (!price) return '0 تومان'
  return new Intl.NumberFormat('fa-IR').format(price) + ' تومان'
}

const addProduct = () => {
  form.value.items.push({
    product: '',
    quantity: 1,
    unit_price: 0
  })
}

const removeProduct = (index) => {
  form.value.items.splice(index, 1)
}

const updateProductInfo = (index) => {
  const item = form.value.items[index]
  const productId = parseInt(item.product)
  const product = availableProducts.value.find(p => p.id === productId)
  if (product) {
    item.unit_price = form.value.sale_type === 'wholesale' ?
      Math.round(product.selling_price * 0.9) : // 10% wholesale discount
      product.selling_price
  }
}

const calculateItemTotal = (index) => {
  // Auto-calculate if needed
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
    const orderData = {
      customer: parseInt(form.value.customer),
      warehouse: parseInt(form.value.warehouse),
      sale_type: form.value.sale_type,
      sale_date: form.value.sale_date,
      notes: form.value.notes || '',
      discount_amount: parseFloat(form.value.discount_amount) || 0,
      tax_amount: 0,
      status: 'draft',
      items: form.value.items.map(item => ({
        product: parseInt(item.product),
        quantity: parseFloat(item.quantity),
        unit_price: parseFloat(item.unit_price),
        discount: parseFloat(item.discount) || 0,
        notes: item.notes || ''
      }))
    }

    console.log('Sending order data:', orderData)

    let result
    if (isEditing.value) {
      result = await salesStore.updateSalesOrder(props.salesOrder.id, orderData)
    } else {
      result = await salesStore.createSalesOrder(orderData)
    }

    if (result.success) {
      emit('saved', result.data)
      emit('close')
    } else {
      alert('خطا در ذخیره سفارش: ' + result.error)
    }
  } catch (error) {
    console.error('Error saving sales order:', error)
    alert('خطا در ذخیره سفارش: ' + (error.response?.data?.message || error.message))
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
      warehouse: newOrder.warehouse,
      notes: newOrder.notes || '',
      discount_amount: newOrder.discount_amount || 0,
      items: newOrder.items?.map(item => ({
        product: item.product,
        quantity: item.quantity,
        unit_price: item.unit_price
      })) || []
    }
  }
}, { immediate: true })

// Load data on mount
onMounted(async () => {
  await Promise.all([
    salesStore.fetchCustomers(),
    productsStore.fetchProducts(),
    inventoryStore.fetchWarehouses()
  ])

  // Auto-select warehouse if only one exists
  if (!isEditing.value && warehouses.value.length === 1) {
    form.value.warehouse = warehouses.value[0].id
  }

  // Add first product row if creating new order
  if (!isEditing.value && form.value.items.length === 0) {
    addProduct()
  }
})
</script>
