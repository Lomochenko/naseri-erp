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
            <router-link class="font-medium" to="/">داشبورد /</router-link>
          </li>
          <li>
            <router-link class="font-medium" to="/products">محصولات /</router-link>
          </li>
          <li class="font-medium text-primary">افزودن محصول</li>
        </ol>
      </nav>
    </div>

    <!-- Form -->
    <div class="rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark">
      <div class="border-b border-stroke px-6.5 py-4 dark:border-strokedark">
        <h3 class="font-medium text-black dark:text-white">
          اطلاعات محصول
        </h3>
      </div>

      <!-- Error Message -->
      <div v-if="productsStore.error" class="mx-6.5 mt-4 rounded-lg bg-red-100 p-4 text-red-700">
        {{ productsStore.error }}
      </div>

      <form @submit.prevent="handleSubmit" class="p-6.5">
        <div class="mb-4.5 flex flex-col gap-6 xl:flex-row">
          <!-- Product Name -->
          <div class="w-full xl:w-1/2">
            <label class="mb-2.5 block text-black dark:text-white">
              نام محصول <span class="text-meta-1">*</span>
            </label>
            <input
              v-model="form.name"
              type="text"
              placeholder="نام محصول را وارد کنید"
              class="w-full rounded border-[1.5px] border-stroke bg-transparent px-5 py-3 text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
              required
            />
          </div>

          <!-- SKU -->
          <div class="w-full xl:w-1/2">
            <label class="mb-2.5 block text-black dark:text-white">
              کد محصول (SKU)
            </label>
            <input
              v-model="form.sku"
              type="text"
              placeholder="کد محصول"
              class="w-full rounded border-[1.5px] border-stroke bg-transparent px-5 py-3 text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
            />
          </div>
        </div>

        <div class="mb-4.5 flex flex-col gap-6 xl:flex-row">
          <!-- Category -->
          <div class="w-full xl:w-1/2">
            <label class="mb-2.5 block text-black dark:text-white">
              دسته‌بندی <span class="text-meta-1">*</span>
            </label>
            <select
              v-model="form.category"
              class="w-full rounded border-[1.5px] border-stroke bg-transparent px-5 py-3 text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
              required
            >
              <option value="">دسته‌بندی را انتخاب کنید</option>
              <option v-for="category in productsStore.categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
          </div>

          <!-- Unit -->
          <div class="w-full xl:w-1/2">
            <label class="mb-2.5 block text-black dark:text-white">
              واحد <span class="text-meta-1">*</span>
            </label>
            <select
              v-model="form.unit"
              class="w-full rounded border-[1.5px] border-stroke bg-transparent px-5 py-3 text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
              required
            >
              <option value="">واحد را انتخاب کنید</option>
              <option v-for="unit in productsStore.units" :key="unit.id" :value="unit.id">
                {{ unit.name }}
              </option>
            </select>
          </div>
        </div>

        <div class="mb-4.5 flex flex-col gap-6 xl:flex-row">
          <!-- Price -->
          <div class="w-full xl:w-1/2">
            <label class="mb-2.5 block text-black dark:text-white">
              قیمت (تومان) <span class="text-meta-1">*</span>
            </label>
            <input
              v-model="form.price"
              type="number"
              step="0.01"
              placeholder="قیمت محصول"
              class="w-full rounded border-[1.5px] border-stroke bg-transparent px-5 py-3 text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
              required
            />
          </div>

          <!-- Initial Stock -->
          <div class="w-full xl:w-1/2">
            <label class="mb-2.5 block text-black dark:text-white">
              موجودی اولیه
            </label>
            <input
              v-model="form.stock_quantity"
              type="number"
              placeholder="موجودی اولیه"
              class="w-full rounded border-[1.5px] border-stroke bg-transparent px-5 py-3 text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
            />
          </div>
        </div>

        <div class="mb-4.5 flex flex-col gap-6 xl:flex-row">
          <!-- Min Stock Level -->
          <div class="w-full xl:w-1/2">
            <label class="mb-2.5 block text-black dark:text-white">
              حداقل موجودی
            </label>
            <input
              v-model="form.min_stock_level"
              type="number"
              placeholder="حداقل موجودی"
              class="w-full rounded border-[1.5px] border-stroke bg-transparent px-5 py-3 text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
            />
          </div>

          <!-- Max Stock Level -->
          <div class="w-full xl:w-1/2">
            <label class="mb-2.5 block text-black dark:text-white">
              حداکثر موجودی
            </label>
            <input
              v-model="form.max_stock_level"
              type="number"
              placeholder="حداکثر موجودی"
              class="w-full rounded border-[1.5px] border-stroke bg-transparent px-5 py-3 text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
            />
          </div>
        </div>

        <!-- Description -->
        <div class="mb-6">
          <label class="mb-2.5 block text-black dark:text-white">
            توضیحات
          </label>
          <textarea
            v-model="form.description"
            rows="4"
            placeholder="توضیحات محصول"
            class="w-full rounded border-[1.5px] border-stroke bg-transparent px-5 py-3 text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
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
            <div
              :class="form.is_active ? 'bg-primary border-primary' : 'bg-transparent border-stroke dark:border-form-strokedark'"
              class="mr-4 flex h-5 w-5 items-center justify-center rounded border"
            >
              <span :class="form.is_active ? 'opacity-100' : 'opacity-0'">
                <svg class="h-3.5 w-3.5 stroke-current text-white" fill="none" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </span>
            </div>
            <span class="text-black dark:text-white">محصول فعال باشد</span>
          </label>
        </div>

        <!-- Submit Buttons -->
        <div class="flex gap-4">
          <button
            type="submit"
            :disabled="productsStore.isLoading"
            class="flex justify-center rounded bg-primary px-6 py-2 font-medium text-gray hover:bg-opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
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
            class="flex justify-center rounded border border-stroke px-6 py-2 font-medium text-black hover:shadow-1 dark:border-strokedark dark:text-white"
          >
            انصراف
          </router-link>
        </div>
      </form>
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
  sku: '',
  description: '',
  category: '',
  unit: '',
  price: '',
  stock_quantity: 0,
  min_stock_level: 0,
  max_stock_level: 0,
  is_active: true
})

// Methods
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
