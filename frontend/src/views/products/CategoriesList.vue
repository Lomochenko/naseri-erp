<template>
  <div>
    <v-card class="mb-6">
      <v-card-title class="d-flex align-center justify-space-between">
        <span class="text-h5">مدیریت دسته‌بندی‌های محصول</span>
        <v-btn 
          color="primary" 
          prepend-icon="mdi-plus" 
          variant="elevated"
          @click="addNewCategory"
        >
          دسته‌بندی جدید
        </v-btn>
      </v-card-title>

      <v-card-text>
        <v-row>
          <!-- فیلترهای جستجو -->
          <v-col cols="12" md="6">
            <v-text-field
              v-model="search"
              label="جستجو در دسته‌بندی‌ها"
              variant="outlined"
              density="compact"
              prepend-inner-icon="mdi-magnify"
              hide-details
              @update:model-value="fetchCategories"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="6" class="d-flex justify-end align-center">
            <v-btn 
              color="secondary" 
              variant="text" 
              prepend-icon="mdi-refresh"
              @click="fetchCategories"
            >
              بازنشانی
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- جدول نمایش دسته‌بندی‌ها -->
    <v-card>
      <v-data-table
        :headers="headers"
        :items="categories"
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

        <!-- نمایش نام دسته‌بندی -->
        <template v-slot:item.name="{ item }">
          <div class="font-weight-medium">{{ item.name }}</div>
        </template>

        <!-- نمایش توضیحات -->
        <template v-slot:item.description="{ item }">
          <div class="text-truncate" style="max-width: 300px;">
            {{ item.description || 'بدون توضیحات' }}
          </div>
        </template>

        <!-- نمایش تاریخ ایجاد -->
        <template v-slot:item.created_at="{ item }">
          <div>{{ formatDate(item.created_at) }}</div>
        </template>

        <!-- نمایش دکمه‌های عملیات -->
        <template v-slot:item.actions="{ item }">
          <div class="d-flex justify-end">
            <v-btn
              icon="mdi-pencil"
              size="small"
              variant="text"
              color="warning"
              class="ml-1"
              @click="editCategory(item)"
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
            <v-icon size="large" icon="mdi-tag-multiple" color="secondary" class="mb-3"></v-icon>
            <div>دسته‌بندی‌ای یافت نشد</div>
            <v-btn 
              variant="text" 
              color="primary" 
              class="mt-3" 
              @click="fetchCategories"
            >
              تلاش مجدد
            </v-btn>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <!-- دیالوگ فرم دسته‌بندی -->
    <category-form
      v-model="categoryDialog"
      :edited-category="editedCategory"
      @category-added="onCategorySaved"
      @category-updated="onCategorySaved"
    />

    <!-- دیالوگ حذف دسته‌بندی -->
    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title class="text-h5">حذف دسته‌بندی</v-card-title>
        <v-card-text>
          آیا از حذف دسته‌بندی <strong>{{ deleteItem?.name }}</strong> اطمینان دارید؟
          <div class="text-caption text-medium-emphasis mt-2">
            این عملیات غیرقابل بازگشت است و ممکن است بر محصولاتی که به این دسته‌بندی متصل هستند تأثیر بگذارد.
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" variant="text" @click="deleteDialog = false">انصراف</v-btn>
          <v-btn 
            color="error" 
            variant="elevated" 
            @click="deleteCategory" 
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
import CategoryForm from './CategoryForm.vue';

// استور محصولات
const productsStore = useProductsStore();

// ثابت‌های نمایش
const headers = [
  { title: 'نام دسته‌بندی', key: 'name', align: 'start', sortable: true },
  { title: 'توضیحات', key: 'description', align: 'start', sortable: false },
  { title: 'تاریخ ایجاد', key: 'created_at', align: 'center', sortable: true },
  { title: 'عملیات', key: 'actions', align: 'center', sortable: false },
];

// متغیرهای واکنش‌پذیر
const categoryDialog = ref(false);
const deleteDialog = ref(false);
const editedCategory = ref(null);
const deleteItem = ref(null);
const page = ref(1);
const itemsPerPage = ref(10);
const search = ref('');
const totalItems = ref(0);

// دریافت داده‌ها از استور
const loading = computed(() => productsStore.loading);
const categories = computed(() => productsStore.categories);

// فرمت‌کننده تاریخ
const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return new Intl.DateTimeFormat('fa-IR').format(date);
};

// بارگذاری دسته‌بندی‌ها
const fetchCategories = async () => {
  try {
    console.log('Trying to fetch categories...');
    await productsStore.fetchCategories();
    console.log('Categories fetched:', productsStore.categories);
    totalItems.value = productsStore.categories.length;
  } catch (error) {
    console.error('خطا در بارگذاری دسته‌بندی‌ها:', error);
  }
};

// مدیریت گزینه‌های جدول
const handleOptions = (options) => {
  page.value = options.page;
  itemsPerPage.value = options.itemsPerPage;
  
  fetchCategories();
};

// مدیریت دسته‌بندی‌ها
const addNewCategory = () => {
  editedCategory.value = null;
  categoryDialog.value = true;
};

const editCategory = (item) => {
  editedCategory.value = { ...item };
  categoryDialog.value = true;
};

const confirmDelete = (item) => {
  deleteItem.value = item;
  deleteDialog.value = true;
};

const deleteCategory = async () => {
  if (await productsStore.deleteCategory(deleteItem.value.id)) {
    deleteDialog.value = false;
    deleteItem.value = null;
    fetchCategories();
  }
};

const onCategorySaved = () => {
  fetchCategories();
};

// دریافت داده‌ها در زمان بارگذاری
onMounted(() => {
  fetchCategories();
});
</script>

<style scoped>
.rtl-table :deep(th) {
  text-align: right;
}
</style> 