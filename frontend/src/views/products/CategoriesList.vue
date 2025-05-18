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
        :items="safeCategories"
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
          <div class="font-weight-medium">{{ item.raw ? item.raw.name : item.name }}</div>
        </template>

        <!-- نمایش توضیحات -->
        <template v-slot:item.description="{ item }">
          <div class="text-truncate" style="max-width: 300px;">
            {{ (item.raw ? item.raw.description : item.description) || 'بدون توضیحات' }}
          </div>
        </template>

        <!-- نمایش تاریخ ایجاد -->
        <template v-slot:item.created_at="{ item }">
          <div>{{ formatDate(item.raw ? item.raw.created_at : item.created_at) }}</div>
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
              @click="editCategory(item.raw || item)"
            ></v-btn>
            <v-btn
              icon="mdi-delete"
              size="small"
              variant="text"
              color="error"
              @click="confirmDelete(item.raw || item)"
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
const categories = computed(() => productsStore.categories || []);

// ایجاد آرایه ایمن از دسته‌بندی‌ها برای استفاده در جدول
const safeCategories = computed(() => {
  const cats = categories.value;
  // اطمینان از اینکه آرایه معتبر داریم
  if (!Array.isArray(cats)) {
    console.warn('Categories is not an array, returning empty array');
    return [];
  }
  
  // اطمینان از اینکه هر آیتم حداقل دارای id و name است
  return cats.map(cat => {
    if (!cat) return { id: 'unknown', name: 'دسته‌بندی نامشخص', description: '', created_at: new Date() };
    
    return {
      id: cat.id || 'unknown',
      name: cat.name || 'بدون نام',
      description: cat.description || '',
      created_at: cat.created_at || new Date()
    };
  });
});

// فرمت‌کننده تاریخ
const formatDate = (dateStr) => {
  if (!dateStr) return 'بدون تاریخ';
  try {
    // بررسی اولیه مقدار تاریخ
    if (dateStr === 'Invalid Date' || dateStr === 'undefined' || dateStr === 'null') {
      return 'تاریخ نامعتبر';
    }
    
    // تبدیل به تاریخ
    const date = new Date(dateStr);
    
    // بررسی معتبر بودن تاریخ
    if (isNaN(date.getTime())) {
      return 'تاریخ نامعتبر';
    }
    
    // فرمت کردن تاریخ
    return new Intl.DateTimeFormat('fa-IR').format(date);
  } catch (error) {
    console.error('خطا در تبدیل تاریخ:', error, 'مقدار:', dateStr);
    return 'تاریخ نامعتبر';
  }
};

// بارگذاری دسته‌بندی‌ها
const fetchCategories = async () => {
  try {
    console.log('Trying to fetch categories...');
    // تاخیر کوتاه برای اطمینان از اینکه کامپوننت کاملاً mount شده است
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // ارسال مقدار جستجو به تابع fetchCategories در استور
    await productsStore.fetchCategories(search.value);
    
    console.log('Categories fetched:', productsStore.categories);
    
    // اطمینان از اینکه مقدار totalItems معتبر است
    if (productsStore.categories && Array.isArray(productsStore.categories)) {
      totalItems.value = productsStore.categories.length;
    } else {
      totalItems.value = 0;
    }
  } catch (error) {
    console.error('خطا در بارگذاری دسته‌بندی‌ها:', error);
    totalItems.value = 0;
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
  try {
    if (deleteItem.value && deleteItem.value.id) {
      await productsStore.deleteCategory(deleteItem.value.id);
      deleteDialog.value = false;
      deleteItem.value = null;
      await fetchCategories();
    }
  } catch (error) {
    console.error('خطا در حذف دسته‌بندی:', error);
  }
};

const onCategorySaved = () => {
  fetchCategories();
};

// دریافت داده‌ها در زمان بارگذاری
onMounted(() => {
  console.log('CategoriesList component mounted');
  // تاخیر بیشتر برای اطمینان از اینکه کامپوننت کاملاً آماده است
  setTimeout(() => {
    fetchCategories();
  }, 500);
});
</script>

<style scoped>
.rtl-table :deep(th) {
  text-align: right;
}
</style> 