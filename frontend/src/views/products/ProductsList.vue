<template>
  <div>
    <v-card class="mb-6">
      <v-card-title class="d-flex align-center justify-space-between">
        <span class="text-h5">مدیریت محصولات</span>
        <div>
          <v-btn
            color="secondary"
            variant="text"
            class="ml-2"
            prepend-icon="mdi-tag-multiple"
            :to="{ name: 'categories' }"
          >
            مدیریت دسته‌بندی‌ها
          </v-btn>
          <v-btn
            color="secondary"
            variant="text"
            class="ml-2"
            prepend-icon="mdi-scale"
            :to="{ name: 'units' }"
          >
            مدیریت واحدها
          </v-btn>
          <v-btn 
            color="primary" 
            prepend-icon="mdi-plus" 
            variant="elevated"
            @click="addNewProduct"
          >
            محصول جدید
          </v-btn>
        </div>
      </v-card-title>

      <v-card-text>
        <v-row>
          <!-- فیلترهای جستجو -->
          <v-col cols="12" md="3">
            <v-text-field
              v-model="filters.search"
              label="جستجو در محصولات"
              variant="outlined"
              density="compact"
              prepend-inner-icon="mdi-magnify"
              hide-details
              @update:model-value="updateFilters"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="3">
            <v-select
              v-model="filters.category"
              :items="categories"
              item-title="name"
              item-value="id"
              label="دسته‌بندی"
              variant="outlined"
              density="compact"
              hide-details
              clearable
              return-object
              @update:model-value="updateFilters"
            ></v-select>
          </v-col>

          <v-col cols="12" md="3">
            <v-select
              v-model="filters.status"
              :items="[
                { title: 'همه محصولات', value: null },
                { title: 'محصولات فعال', value: 'active' },
                { title: 'محصولات غیرفعال', value: 'inactive' },
                { title: 'موجودی کم', value: 'low_stock' },
                { title: 'اتمام موجودی', value: 'out_of_stock' }
              ]"
              item-title="title"
              item-value="value"
              label="وضعیت"
              variant="outlined"
              density="compact"
              hide-details
              @update:model-value="updateFilters"
            ></v-select>
          </v-col>

          <v-col cols="12" md="3" class="d-flex justify-end align-center">
            <v-btn 
              color="secondary" 
              variant="text" 
              prepend-icon="mdi-refresh"
              @click="resetFilters"
            >
              بازنشانی فیلترها
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- جدول نمایش محصولات -->
    <v-card>
      <v-data-table
        :headers="headers"
        :items="products"
        :loading="loading"
        :items-per-page="itemsPerPage"
        :page="page"
        :server-items-length="totalItems"
        class="elevation-1 rtl-table"
        hover
        @update:options="handleOptions"
      >
        <!-- لودینگ -->
        <template v-slot:loader>
          <v-progress-linear indeterminate color="primary"></v-progress-linear>
        </template>

        <!-- نمایش نام محصول و کد -->
        <template v-slot:item.name="{ item }">
          <div>
            <div class="text-subtitle-2 font-weight-bold">{{ item.name }}</div>
            <div class="text-body-2 text-medium-emphasis">کد: {{ item.code }}</div>
          </div>
        </template>

        <!-- نمایش دسته‌بندی -->
        <template v-slot:item.category="{ item }">
          <v-chip
            v-if="item.category_name"
            size="small"
            color="secondary"
            text-color="white"
            variant="flat"
          >
            {{ item.category_name }}
          </v-chip>
          <span v-else class="text-disabled">-</span>
        </template>

        <!-- نمایش قیمت فروش -->
        <template v-slot:item.selling_price="{ item }">
          <div class="text-right">
            <div class="font-weight-medium">{{ formatPrice(item.selling_price) }}</div>
            <div class="text-caption text-medium-emphasis">خرید: {{ formatPrice(item.purchase_price) }}</div>
          </div>
        </template>

        <!-- نمایش موجودی -->
        <template v-slot:item.stock="{ item }">
          <div class="d-flex align-center">
            <v-chip
              :color="getStockColor(item.current_stock, item.min_stock)"
              size="small"
              variant="flat"
            >
              {{ getStockLabel(item.current_stock, item.min_stock) }}
            </v-chip>
          </div>
        </template>

        <!-- نمایش وضعیت -->
        <template v-slot:item.is_active="{ item }">
          <v-chip
            :color="item.is_active ? 'success' : 'error'"
            size="small"
            variant="flat"
          >
            {{ item.is_active ? 'فعال' : 'غیرفعال' }}
          </v-chip>
        </template>

        <!-- نمایش دکمه‌های عملیات -->
        <template v-slot:item.actions="{ item }">
          <div class="d-flex justify-end">
            <v-btn
              icon="mdi-eye"
              size="small"
              variant="text"
              color="info"
              class="ml-1"
              @click="viewProduct(item)"
            ></v-btn>
            <v-btn
              icon="mdi-pencil"
              size="small"
              variant="text"
              color="warning"
              class="ml-1"
              @click="editProduct(item)"
            ></v-btn>
            <v-btn
              icon="mdi-delete"
              size="small"
              variant="text"
              color="error"
              @click="confirmDelete(item)"
            ></v-btn>
          </div>
        </template>

        <!-- نمایش در حالت خالی بودن لیست -->
        <template v-slot:no-data>
          <div class="text-center pa-5">
            <v-icon size="large" icon="mdi-package-variant" color="secondary" class="mb-3"></v-icon>
            <div>محصولی یافت نشد</div>
            <v-btn 
              variant="text" 
              color="primary" 
              class="mt-3" 
              @click="loadProducts"
            >
              تلاش مجدد
            </v-btn>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <!-- دیالوگ فرم محصول -->
    <product-form
      v-model="productDialog"
      :edited-product="editedProduct"
      @product-saved="onProductSaved"
    />

    <!-- دیالوگ نمایش جزئیات محصول -->
    <v-dialog v-model="detailDialog" max-width="500">
      <v-card v-if="selectedProduct">
        <v-card-title class="text-h5">{{ selectedProduct.name }}</v-card-title>

        <v-card-text>
          <v-list lines="two">
            <v-list-item>
              <template v-slot:prepend>
                <v-icon icon="mdi-barcode"></v-icon>
              </template>
              <v-list-item-title>کد محصول:</v-list-item-title>
              <v-list-item-subtitle>{{ selectedProduct.code }}</v-list-item-subtitle>
            </v-list-item>

            <v-list-item v-if="selectedProduct.category">
              <template v-slot:prepend>
                <v-icon icon="mdi-tag"></v-icon>
              </template>
              <v-list-item-title>دسته‌بندی:</v-list-item-title>
              <v-list-item-subtitle>{{ selectedProduct.category.name }}</v-list-item-subtitle>
            </v-list-item>

            <v-list-item v-if="selectedProduct.unit">
              <template v-slot:prepend>
                <v-icon icon="mdi-scale"></v-icon>
              </template>
              <v-list-item-title>واحد:</v-list-item-title>
              <v-list-item-subtitle>{{ selectedProduct.unit.name }} ({{ selectedProduct.unit.symbol }})</v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon icon="mdi-currency-usd"></v-icon>
              </template>
              <v-list-item-title>قیمت خرید:</v-list-item-title>
              <v-list-item-subtitle>{{ formatPrice(selectedProduct.purchase_price) }} تومان</v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon icon="mdi-sale"></v-icon>
              </template>
              <v-list-item-title>قیمت فروش:</v-list-item-title>
              <v-list-item-subtitle>{{ formatPrice(selectedProduct.selling_price) }} تومان</v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon :color="getStockColor(selectedProduct.current_stock, selectedProduct.min_stock)" icon="mdi-package-variant"></v-icon>
              </template>
              <v-list-item-title>موجودی:</v-list-item-title>
              <v-list-item-subtitle>
                {{ selectedProduct.current_stock }}
                <v-chip
                  v-if="selectedProduct.current_stock <= selectedProduct.min_stock"
                  :color="getStockColor(selectedProduct.current_stock, selectedProduct.min_stock)"
                  size="x-small"
                  class="mr-2"
                >
                  {{ selectedProduct.current_stock <= 0 ? 'اتمام موجودی' : 'موجودی کم' }}
                </v-chip>
              </v-list-item-subtitle>
            </v-list-item>

            <v-list-item v-if="selectedProduct.description">
              <template v-slot:prepend>
                <v-icon icon="mdi-text"></v-icon>
              </template>
              <v-list-item-title>توضیحات:</v-list-item-title>
              <v-list-item-subtitle>{{ selectedProduct.description }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="text" @click="detailDialog = false">بستن</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- دیالوگ حذف محصول -->
    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title class="text-h5">حذف محصول</v-card-title>
        <v-card-text>
          آیا از حذف محصول <strong>{{ deleteItem?.name }}</strong> اطمینان دارید؟
          <div class="text-caption text-medium-emphasis mt-2">
            این عملیات غیرقابل بازگشت است و تمام اطلاعات مربوط به این محصول حذف خواهد شد.
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" variant="text" @click="deleteDialog = false">انصراف</v-btn>
          <v-btn 
            color="error" 
            variant="elevated" 
            @click="deleteProduct" 
            :loading="loading"
          >
            حذف
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useProductsStore } from '../../store/products';
import ProductForm from './ProductForm.vue';

// استور محصولات
const productsStore = useProductsStore();

// ثابت‌های نمایش
const headers = [
  { title: 'نام محصول', key: 'name', align: 'start', sortable: true },
  { title: 'دسته‌بندی', key: 'category_name', align: 'center', sortable: true },
  { title: 'قیمت فروش (تومان)', key: 'selling_price', align: 'center', sortable: true },
  { title: 'موجودی', key: 'current_stock', align: 'center', sortable: true },
  { title: 'وضعیت', key: 'is_active', align: 'center', sortable: true },
  { title: 'عملیات', key: 'actions', align: 'center', sortable: false },
];

// متغیرهای واکنش‌پذیر
const productDialog = ref(false);
const detailDialog = ref(false);
const deleteDialog = ref(false);
const editedProduct = ref(null);
const selectedProduct = ref(null);
const deleteItem = ref(null);
const page = ref(1);
const itemsPerPage = ref(10);

// دریافت داده‌ها از استور
const loading = computed(() => productsStore.loading);
const products = computed(() => productsStore.products);
const categories = computed(() => productsStore.categories);
const totalItems = computed(() => productsStore.totalItems);
const filters = computed(() => productsStore.filters);

// فرمت‌کننده قیمت
const formatPrice = (price) => {
  return new Intl.NumberFormat('fa-IR').format(price);
};

// بررسی وضعیت موجودی
const getStockColor = (stock, minStock) => {
  if (stock <= 0) return 'error';
  if (stock <= minStock) return 'warning';
  return 'success';
};

const getStockLabel = (stock, minStock) => {
  if (stock <= 0) return 'اتمام موجودی';
  if (stock <= minStock) return 'موجودی کم';
  return `${stock} عدد`;
};

// مدیریت فیلترها
const updateFilters = () => {
  productsStore.updateFilters({
    search: filters.value.search,
    category: filters.value.category?.id,
    status: filters.value.status
  });
};

const resetFilters = () => {
  productsStore.resetFilters();
};

// بارگذاری محصولات
const loadProducts = async () => {
  console.log('نصب اولیه: بارگذاری محصولات');
  try {
    await productsStore.fetchProducts();
    console.log('نصب اولیه: محصولات با موفقیت بارگذاری شدند', products.value);
  } catch (error) {
    console.error('نصب اولیه: خطا در بارگذاری محصولات', error);
  }
};

// مدیریت گزینه‌های جدول
const handleOptions = (options) => {
  page.value = options.page;
  itemsPerPage.value = options.itemsPerPage;
  
  // تنظیم مرتب‌سازی
  const sortBy = options.sortBy.length > 0 ? options.sortBy[0] : null;
  
  if (sortBy) {
    productsStore.updateFilters({
      sortBy: sortBy.key,
      sortDesc: sortBy.order === 'desc'
    });
  }
  
  // بروزرسانی تنظیمات صفحه‌بندی
  productsStore.setPage(page.value);
  productsStore.setItemsPerPage(itemsPerPage.value);
};

// مدیریت محصولات
const addNewProduct = () => {
  editedProduct.value = null;
  productDialog.value = true;
};

const editProduct = (item) => {
  editedProduct.value = { ...item };
  productDialog.value = true;
};

const viewProduct = (item) => {
  selectedProduct.value = { ...item };
  detailDialog.value = true;
};

const editSelectedProduct = () => {
  editedProduct.value = { ...selectedProduct.value };
  detailDialog.value = false;
  productDialog.value = true;
};

const confirmDelete = (item) => {
  deleteItem.value = item;
  deleteDialog.value = true;
};

const deleteProduct = async () => {
  if (await productsStore.deleteProduct(deleteItem.value.id)) {
    deleteDialog.value = false;
    deleteItem.value = null;
  }
};

const onProductSaved = () => {
  loadProducts();
};

// دریافت داده‌ها در زمان بارگذاری
onMounted(async () => {
  console.log('نصب اولیه: کامپوننت محصولات نصب شد');
  
  try {
    if (categories.value.length === 0) {
      console.log('نصب اولیه: بارگذاری دسته‌بندی‌ها');
      await productsStore.fetchCategories();
      console.log('نصب اولیه: دسته‌بندی‌ها بارگذاری شدند', categories.value);
    }
    
    console.log('نصب اولیه: فراخوانی loadProducts');
    await loadProducts();
  } catch (error) {
    console.error('نصب اولیه: خطا در onMounted', error);
  }
});
</script>

<style scoped>
.rtl-table :deep(th) {
  text-align: right;
}
.v-chip {
  font-size: 0.8rem;
}
</style> 