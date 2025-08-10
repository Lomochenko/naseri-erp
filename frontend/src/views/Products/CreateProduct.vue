<template>
  <AdminLayout>
    <div>
    <!-- Breadcrumb -->
    <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <h2 class="text-title-md2 font-bold text-black dark:text-white">
        افزودن محصول جدید
      </h2>
      <nav>
        <ol class="flex items-center gap-2">
          <li>
            <router-link class="font-medium text-black dark:text-white" to="/">داشبورد /</router-link>
          </li>
          <li>
            <router-link class="font-medium text-black dark:text-white" to="/products">محصولات /</router-link>
          </li>
          <li class="font-medium text-primary text-black dark:text-white">افزودن محصول</li>
        </ol>
      </nav>
    </div>

    <!-- Form -->
    <div class="rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark">
      <div class=" bg-slate-100 dark:bg-slate-300 border-b border-black rounded border-stroke px-6.5 py-4 dark:border-strokedark">
        <h3 class="font-medium text-black">
          اطلاعات محصول
        </h3>
      </div>

      <!-- Error Message -->
      <div v-if="productsStore.error" class="mx-6.5 mt-4 rounded-lg bg-red-100 p-4 text-red-700">
        {{ productsStore.error }}
      </div>

      <form @submit.prevent="handleSubmit" class="p-6.5  bg-slate-100 dark:bg-slate-300 dark:border-gray-800 border-r border-gray-200">
        <div class="mb-4.5 flex flex-col gap-6 xl:flex-row">
          <!-- Product Name -->
          <div class="w-full xl:w-1/2">
            <label class="mb-2.5 block text-black">
              نام محصول <span class="text-meta-1">*</span>
            </label>
            <input
              v-model="form.name"
              type="text"
              placeholder="نام محصول را وارد کنید"
              class="w-full placeholder-gray-500 rounded border-[1.5px] border-stroke bg-transparent px-5 py-3 text-black outline-none transition focus:border-primary  active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input border-slate-300 dark:border-slate-500 dark:focus:border-slate-800"
              required
            />
          </div>

          <!-- Product Code -->
          <div class="w-full xl:w-1/2">
            <label class="mb-2.5 block text-black">
              کد محصول <span class="text-meta-1">*</span>
            </label>
            <input
              v-model="form.code"
              type="text"
              placeholder="کد محصول"
              class="w-full placeholder-gray-500 rounded border-[1.5px] border-stroke bg-transparent px-5 py-3 text-black outline-none transition focus:border-slate-800 active:border-black disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input border-slate-300 dark:border-slate-500 dark:focus:border-slate-800"
              required
            />
          </div>
        </div>

        <div class="mb-4.5 flex flex-col gap-6 xl:flex-row">
          <!-- Category -->
          <div class="w-full xl:w-1/2">
            <label class="mb-2.5 block text-black">
              دسته‌بندی <span class="text-meta-1">*</span>
            </label>
            <div class="flex gap-2">
            <select
              v-model="form.category"
              class="w-full rounded border-[1.5px] border-stroke bg-transparent px-5 py-3 text-black outline-none transition focus:border-slate-800 active:border-black disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input border-slate-300 dark:border-slate-500 dark:focus:border-slate-800"
              required
            >
              <option value="">دسته‌بندی را انتخاب کنید</option>
              <option v-for="category in productsStore.categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
            <button @click="openModal('category')" type="button" class="hover:bg-slate-200 rounded border-[1.5px] outline-none transition dark:border-form-strokedark dark:bg-form-input border-slate-300 dark:border-slate-500 dark:focus:border-slate-800  hover:border-gray-400 px-4 py-2 font-medium text-black">
              جدید
            </button>
            </div>
          </div>

          <!-- Unit -->
          <div class="w-full xl:w-1/2">
            <label class="mb-2.5 block text-black">
              واحد <span class="text-meta-1">*</span>
            </label>
            <div class="flex gap-2">
            <select
              v-model="form.unit"
              class="w-full rounded border-[1.5px] border-stroke bg-transparent px-5 py-3 text-black outline-none transition focus:border-slate-800 active:border-black disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input border-slate-300 dark:border-slate-500 dark:focus:border-slate-800"
              required
            >
              <option value="">واحد را انتخاب کنید</option>
              <option v-for="unit in productsStore.units" :key="unit.id" :value="unit.id">
                {{ unit.name }}
              </option>
            </select>
            <button @click="openModal('unit')" type="button" class="hover:bg-slate-200 rounded border-[1.5px] outline-none transition dark:border-form-strokedark dark:bg-form-input border-slate-300 dark:border-slate-500 dark:focus:border-slate-800 hover:border-gray-400 px-4 py-2 font-medium text-black">
              جدید
            </button>
            </div>
          </div>
        </div>

        <div class="mb-4.5 flex flex-col gap-6 xl:flex-row">
          <!-- Purchase Price -->
          <div class="w-full xl:w-1/2">
            <label class="mb-2.5 block text-black">
              قیمت خرید (تومان) <span class="text-meta-1">*</span>
            </label>
            <input
              v-model="form.purchase_price"
              type="number"
              step="1"
              placeholder="قیمت خرید محصول"
              class="w-full placeholder-gray-500 rounded border-[1.5px] border-stroke bg-transparent px-5 py-3 text-black outline-none transition focus:border-slate-800 active:border-black disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input border-slate-300 dark:border-slate-500 dark:focus:border-slate-800"
              required
            />
          </div>

          <!-- Selling Price -->
          <div class="w-full xl:w-1/2">
            <label class="mb-2.5 block text-black">
              قیمت فروش (تومان) <span class="text-meta-1">*</span>
            </label>
            <input
              v-model="form.selling_price"
              type="number"
              step="1"
              placeholder="قیمت فروش محصول"
              class="w-full placeholder-gray-500 rounded border-[1.5px] border-stroke bg-transparent px-5 py-3 text-black outline-none transition focus:border-slate-800 active:border-black disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input border-slate-300 dark:border-slate-500 dark:focus:border-slate-800"
              required
            />
          </div>
        </div>

        <div class="mb-4.5 flex flex-col gap-6 xl:flex-row">
          <!-- Min Stock Level -->
          <div class="w-full xl:w-1/2">
            <label class="mb-2.5 block text-black">
              حداقل موجودی
            </label>
            <input
              v-model="form.min_stock"
              type="number"
              step="0.01"
              min="0"
              placeholder="حداقل موجودی"
              class="w-full placeholder-gray-500 rounded border-[1.5px] border-stroke bg-transparent px-5 py-3 text-black outline-none transition focus:border-slate-800 active:border-black disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input border-slate-300 dark:border-slate-500 dark:focus:border-slate-800"
            />
          </div>

          <!-- Max Stock Level -->
          <div class="w-full xl:w-1/2">
            <label class="mb-2.5 block text-black">
              حداکثر موجودی
            </label>
            <input
              v-model="form.max_stock"
              type="number"
              step="0.01"
              min="0"
              placeholder="حداکثر موجودی"
              class="w-full placeholder-gray-500 rounded border-[1.5px] border-stroke bg-transparent px-5 py-3 text-black outline-none transition focus:border-slate-800 active:border-black disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input border-slate-300 dark:border-slate-500 dark:focus:border-slate-800"
            />
          </div>
        </div>

        <div class="mb-4.5">
          <!-- Current Stock Level -->
          <div class="w-full xl:w-1/2">
            <label class="mb-2.5 block text-black">
              موجودی فعلی <span class="text-sm text-gray-500">(اختیاری - در صورت خالی بودن صفر خواهد بود)</span>
            </label>
            <input
              v-model="form.current_stock"
              type="number"
              step="0.01"
              min="0"
              placeholder="موجودی فعلی"
              class="w-full placeholder-gray-500 rounded border-[1.5px] border-stroke bg-transparent px-5 py-3 text-black outline-none transition focus:border-slate-800 active:border-black disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input border-slate-300 dark:border-slate-500 dark:focus:border-slate-800"
            />
          </div>
        </div>

        <!-- Description -->
        <div class="mb-6">
          <label class="mb-2.5 block text-black">
            توضیحات
          </label>
          <textarea
            v-model="form.description"
            rows="4"
            placeholder="توضیحات محصول"
            class="w-full placeholder-gray-500 rounded border-[1.5px] border-stroke bg-transparent px-5 py-3 text-black outline-none transition focus:border-slate-800 active:border-black disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input border-slate-300 dark:border-slate-500 dark:focus:border-slate-800"
          ></textarea>
        </div>

        <!-- Active Status -->
        <div class="mb-6">
          <label class="flex items-center cursor-pointer">
            <input
              v-model="form.is_active"
              type="checkbox"
              class="sr-only"
            />
            <span class="text-black">محصول فعال باشد؟</span>
            <div
              :class="form.is_active ? 'bg-gray-800 border-black text-white' : 'bg-transparent border-gray-800 border-stroke dark:border-form-strokedark'"
              class="mr-4 flex h-5 w-5 items-center justify-center rounded border"
            >
              <span :class="form.is_active ? 'opacity-100' : 'opacity-0'">
                <svg class="h-3.5 w-3.5 stroke-current text-white" fill="none" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </span>
            </div>
          </label>
        </div>

        <!-- Submit Buttons -->
        <div class="flex gap-4">
          <button
            type="submit"
            :disabled="productsStore.isLoading"
            class="flex justify-center border-slate-800 hover:bg-slate-200  rounded border border-stroke bg-primary px-6 py-2 font-medium text-black hover:bg-opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="productsStore.isLoading" class="mr-2">
              <svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            {{ productsStore.isLoading ? 'در حال ذخیره...' : 'ذخیره محصول' }}
          </button>

          <router-link
            to="/products"
            class="flex justify-center hover:bg-slate-200  rounded border border-slate-800 border-stroke px-6 py-2 font-medium text-black hover:shadow-1 dark:border-strokedark"
          >
            انصراف
          </router-link>
        </div>
      </form>
    </div>
    </div>

    <!-- Modal for creating new category/unit -->
    <div v-if="showModal" class="fixed inset-0 z-9999 flex items-center justify-center bg-black bg-opacity-50">
      <div class="w-full max-w-md rounded-lg bg-white p-6 dark:bg-boxdark">
        <h3 class="mb-4 text-lg font-medium text-black">
          افزودن {{ modalType === 'category' ? 'دسته‌بندی' : 'واحد' }} جدید
        </h3>
        <input
          v-model="newItemName"
          type="text"
          :placeholder="`نام ${modalType === 'category' ? 'دسته‌بندی' : 'واحد'} جدید`"
          class="w-full placeholder-gray-500 rounded border-[1.5px] border-stroke bg-transparent px-5 py-3 text-black outline-none transition focus:border-slate-800 active:border-black disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input border-slate-300 dark:border-slate-500 dark:focus:border-slate-800"
        />
        <div v-if="modalType === 'unit'" class="mt-4">
          <input
            v-model="newUnitSymbol"
            type="text"
            placeholder="نماد واحد (مثال: kg)"
            class="w-full placeholder-gray-500 rounded border-[1.5px] border-stroke bg-transparent px-5 py-3 text-black outline-none transition focus:border-slate-800 active:border-black disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input border-slate-300 dark:border-slate-500 dark:focus:border-slate-800"
          />
        </div>
        <div class="mt-6 flex justify-start gap-4">
          <button @click="handleCreateNewItem" class="rounded border border-stroke bg-primary px-6 py-2 font-medium text-black hover:bg-opacity-90">
            ایجاد
          </button>
          <button @click="showModal = false" class="rounded border border-stroke px-6 py-2 font-medium text-black hover:shadow-1 dark:border-strokedark dark:text-white">
            انصراف
          </button>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProductsStore } from '@/stores/products'
import AdminLayout from '@/components/layout/AdminLayout.vue'

const router = useRouter()
const productsStore = useProductsStore()

// Form data
const form = ref({
  name: '',
  code: '',
  description: '',
  category: '',
  unit: '',
  purchase_price: '',
  selling_price: '',
  min_stock: 0,
  max_stock: 0,
  current_stock: 0,
  is_active: true
})

// Modal state
const showModal = ref(false)
const modalType = ref('') // 'category' or 'unit'
const newItemName = ref('')
const newUnitSymbol = ref('')

// Methods
const openModal = (type) => {
  modalType.value = type
  newItemName.value = ''
  if(type == 'unit') newUnitSymbol.value = ''
  showModal.value = true
}

const handleCreateNewItem = async () => {
  let result;
  if (modalType.value === 'category') {
    result = await productsStore.createCategory({ name: newItemName.value })
    if (result.success) {
        form.value.category = result.data.id
    }
  } else {
    result = await productsStore.createUnit({ name: newItemName.value, symbol: newUnitSymbol.value })
    if(result.success) {
        form.value.unit = result.data.id
    }
  }

  if (result.success) {
    showModal.value = false
  } else {
    // Handle error display if necessary
    alert(result.error)
  }
}

const handleSubmit = async () => {
  const result = await productsStore.createProduct(form.value)

  if (result.success) {
    router.push('/products')
  }
}

// Lifecycle
onMounted(async () => {
  await Promise.all([
    productsStore.fetchCategories(),
    productsStore.fetchUnits()
  ])
})
</script>
