<template>
  <div>
    <div class="d-flex justify-space-between align-center mb-6">
      <h1 class="text-h4">مدیریت محصولات</h1>
      <v-btn color="primary" prepend-icon="mdi-plus" @click="openAddProductDialog">
        افزودن محصول جدید
      </v-btn>
    </div>

    <!-- Filters -->
    <v-card class="mb-6">
      <v-card-text>
        <v-row>
          <v-col cols="12" md="3">
            <v-text-field
              v-model="search"
              label="جستجو"
              variant="outlined"
              density="compact"
              prepend-inner-icon="mdi-magnify"
              clearable
              @update:model-value="updateFilters({ search: $event })"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="3">
            <v-select
              v-model="selectedCategory"
              label="دسته‌بندی"
              variant="outlined"
              density="compact"
              :items="categories"
              item-title="name"
              item-value="id"
              clearable
              return-object
              @update:model-value="updateFilters({ category: $event })"
            ></v-select>
          </v-col>
          <v-col cols="12" md="3">
            <v-select
              v-model="sortBy"
              label="مرتب‌سازی بر اساس"
              variant="outlined"
              density="compact"
              :items="sortOptions"
              @update:model-value="updateFilters({ sortBy: $event })"
            ></v-select>
          </v-col>
          <v-col cols="12" md="3" class="d-flex align-center">
            <v-btn color="primary" variant="tonal" @click="loadProducts">
              اعمال فیلتر
            </v-btn>
            <v-btn color="error" variant="text" class="ms-2" @click="resetFilters">
              حذف فیلتر‌ها
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Products Table -->
    <v-card>
      <v-data-table
        :headers="headers"
        :items="products"
        :loading="loading"
        :items-per-page="pagination.itemsPerPage"
        :items-per-page-options="[10, 20, 50]"
        density="compact"
        class="elevation-1"
        @update:options="handleTableOptionsChange"
      >
        <!-- Code column -->
        <template v-slot:item.code="{ item }">
          <div class="font-weight-bold">{{ item.code }}</div>
        </template>

        <!-- Image column -->
        <template v-slot:item.image="{ item }">
          <v-avatar size="40">
            <v-img :src="item.image || 'https://via.placeholder.com/40'" cover></v-img>
          </v-avatar>
        </template>

        <!-- Price column -->
        <template v-slot:item.price="{ item }">
          {{ item.price.toLocaleString() }} تومان
        </template>

        <!-- Status column -->
        <template v-slot:item.stock="{ item }">
          <v-chip
            :color="getStockColor(item.stock)"
            size="small"
          >
            {{ getStockLabel(item.stock) }}
          </v-chip>
        </template>

        <!-- Actions column -->
        <template v-slot:item.actions="{ item }">
          <v-icon 
            size="small" 
            class="me-2"
            @click="editProduct(item)"
          >
            mdi-pencil
          </v-icon>
          <v-icon 
            size="small" 
            color="error"
            @click="confirmDelete(item)"
          >
            mdi-delete
          </v-icon>
        </template>
      </v-data-table>
      
      <!-- Pagination -->
      <v-pagination
        v-if="pagination.totalPages > 1"
        v-model="pagination.page"
        :length="pagination.totalPages"
        @update:model-value="handlePageChange"
        class="pt-4 pb-2"
      ></v-pagination>
    </v-card>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">حذف محصول</v-card-title>
        <v-card-text>
          آیا از حذف محصول "{{ selectedProduct?.name }}" اطمینان دارید؟ این عمل قابل بازگشت نیست.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="text" @click="deleteDialog = false">انصراف</v-btn>
          <v-btn color="error" variant="elevated" @click="deleteProduct" :loading="loading">حذف</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useProductsStore } from '../../store/products';

// استفاده از استور محصولات
const productsStore = useProductsStore();

// Table headers
const headers = [
  { title: 'تصویر', key: 'image', sortable: false, align: 'center' },
  { title: 'کد محصول', key: 'code', sortable: true, align: 'start' },
  { title: 'نام محصول', key: 'name', sortable: true, align: 'start' },
  { title: 'دسته‌بندی', key: 'category.name', sortable: true, align: 'start' },
  { title: 'واحد', key: 'unit.name', sortable: true, align: 'start' },
  { title: 'قیمت', key: 'price', sortable: true, align: 'end' },
  { title: 'موجودی', key: 'stock', sortable: true, align: 'center' },
  { title: 'عملیات', key: 'actions', sortable: false, align: 'center' }
];

// Reactive data
const deleteDialog = ref(false);
const selectedProduct = ref(null);

// استفاده از داده‌های استور
const products = computed(() => productsStore.products);
const categories = computed(() => productsStore.categories);
const loading = computed(() => productsStore.loading);
const error = computed(() => productsStore.error);
const pagination = computed(() => productsStore.pagination);

// متغیرهای محلی برای فیلترها
const search = ref('');
const selectedCategory = ref(null);
const sortBy = ref('name');

// Sort options
const sortOptions = [
  { title: 'نام (صعودی)', value: 'name' },
  { title: 'نام (نزولی)', value: '-name' },
  { title: 'قیمت (صعودی)', value: 'price' },
  { title: 'قیمت (نزولی)', value: '-price' },
  { title: 'موجودی (صعودی)', value: 'stock' },
  { title: 'موجودی (نزولی)', value: '-stock' }
];

// Methods
const loadProducts = async () => {
  await productsStore.fetchProducts();
};

const loadCategories = async () => {
  await productsStore.fetchCategories();
};

const updateFilters = (newFilters) => {
  productsStore.updateFilters(newFilters);
};

const resetFilters = () => {
  productsStore.resetFilters();
  search.value = '';
  selectedCategory.value = null;
  sortBy.value = 'name';
};

const handlePageChange = (newPage) => {
  productsStore.setPage(newPage);
  loadProducts();
};

const handleTableOptionsChange = (options) => {
  const { itemsPerPage } = options;
  if (itemsPerPage !== pagination.value.itemsPerPage) {
    productsStore.setItemsPerPage(itemsPerPage);
    loadProducts();
  }
};

const openAddProductDialog = () => {
  // TODO: اینجا بایستی دیالوگ افزودن محصول جدید باز شود
  console.log('Open add product dialog');
};

const editProduct = (product) => {
  // TODO: اینجا بایستی دیالوگ ویرایش محصول باز شود
  console.log('Edit product:', product);
};

const confirmDelete = (product) => {
  selectedProduct.value = product;
  deleteDialog.value = true;
};

const deleteProduct = async () => {
  if (selectedProduct.value) {
    const success = await productsStore.deleteProduct(selectedProduct.value.id);
    if (success) {
      deleteDialog.value = false;
      // نمایش پیام موفقیت‌آمیز
      // TODO: اضافه کردن سیستم نمایش پیام با Snackbar
    }
  }
};

const getStockColor = (stock) => {
  if (stock <= 5) return 'error';
  if (stock <= 10) return 'warning';
  return 'success';
};

const getStockLabel = (stock) => {
  if (stock <= 5) return 'بحرانی';
  if (stock <= 10) return 'کم';
  return 'موجود';
};

// Lifecycle hooks
onMounted(async () => {
  await loadCategories();
  await loadProducts();
});
</script> 