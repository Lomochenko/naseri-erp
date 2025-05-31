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
              @click="resetFilters"
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
        :server-items-length="totalItems || 0"
        :items-per-page-options="[5, 10, 15, 20]"
        class="elevation-1 rtl-table"
        hover
        show-select
        fixed-footer
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

        <!-- تنظیم نمایش فوتر -->
        <template v-slot:bottom>
          <div class="d-flex align-center justify-center pt-3 pb-3">
            <v-pagination
              v-model="page"
              :length="Math.ceil(totalItems / itemsPerPage) || 1"
              :total-visible="5"
              show-first-last-page
              prev-icon="mdi-chevron-right"
              next-icon="mdi-chevron-left"
              first-icon="mdi-page-first"
              last-icon="mdi-page-last"
              rounded="circle"
              @click:prev="onPrevPage"
              @click:next="onNextPage"
              @update:model-value="pageChange"
            ></v-pagination>
            <div class="ml-4 text-body-2">
              نمایش {{ totalItems ? (page - 1) * itemsPerPage + 1 : 0 }} تا {{ Math.min(page * itemsPerPage, totalItems) }} از {{ totalItems }} مورد
            </div>
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
import moment from 'jalali-moment';

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
    if (!cat) return { id: 'unknown', name: 'دسته‌بندی نامشخص', description: '', created_at: new Date().toISOString() };
    
    // اطمینان از اینکه created_at در فرمت ISO باشد یا به فرمت معتبر تبدیل شود
    let safeCreatedAt = cat.created_at;
    if (safeCreatedAt) {
      try {
        // بررسی کنیم که آیا تاریخ معتبر است
        const testDate = new Date(safeCreatedAt);
        if (isNaN(testDate.getTime())) {
          // اگر معتبر نیست، از تاریخ فعلی استفاده می‌کنیم
          safeCreatedAt = new Date().toISOString();
        }
      } catch (e) {
        safeCreatedAt = new Date().toISOString();
      }
    } else {
      safeCreatedAt = new Date().toISOString();
    }
    
    return {
      id: cat.id || 'unknown',
      name: cat.name || 'بدون نام',
      description: cat.description || '',
      created_at: safeCreatedAt
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
    
    // استفاده از تایید اعتبار تاریخ
    const m = moment(String(dateStr));
    if (!m.isValid()) {
      console.log('تاریخ نامعتبر است:', dateStr);
      return 'تاریخ نامعتبر';
    }
    
    // تبدیل به تاریخ شمسی
    return m.locale('fa').format('jYYYY/jMM/jDD HH:mm');
  } catch (error) {
    console.error('خطا در تبدیل تاریخ:', error, 'مقدار:', dateStr);
    return 'تاریخ نامعتبر';
  }
};

// مدیریت گزینه‌های جدول
const handleOptions = (options) => {
  console.log('Table options changed:', options);
  
  // بررسی تغییر در تعداد آیتم در هر صفحه
  const perPageChanged = itemsPerPage.value !== options.itemsPerPage;
  
  // به‌روزرسانی مقادیر صفحه‌بندی
  itemsPerPage.value = options.itemsPerPage;
  
  // اگر تعداد آیتم در هر صفحه تغییر کرده، برگشت به صفحه اول
  if (perPageChanged) {
    page.value = 1;
  } else {
    page.value = options.page;
  }
  
  // تنظیم مرتب‌سازی
  const sortBy = options.sortBy.length > 0 ? options.sortBy[0] : null;
  
  // آماده‌سازی پارامترهای درخواست
  let params = {
    page: page.value,
    per_page: itemsPerPage.value,
    search: search.value || ''
  };
  
  // اضافه کردن مرتب‌سازی
  if (sortBy) {
    params.sort_by = sortBy.key;
    params.sort_desc = sortBy.order === 'desc' ? '1' : '0';
  }
  
  console.log('Fetching categories with params:', params);
  
  // فراخوانی API با پارامترهای جدید
  fetchCategoriesWithParams(params);
};

// تابع جدید برای فراخوانی API با پارامترهای پیجینگ و فیلترینگ
const fetchCategoriesWithParams = async (params) => {
  try {
    console.log('Fetching categories with params:', params);
    
    // تاخیر کوتاه برای اطمینان از اینکه کامپوننت کاملاً mount شده است
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // استفاده از متغیر موقت برای ذخیره نتیجه درخواست
    const result = await productsStore.fetchCategories(
      params.search, 
      params.page, 
      params.per_page,
      params.sort_by,
      params.sort_desc === '1'
    );
    
    console.log('Categories fetched with result:', result);
    
    // اطمینان از اینکه مقدار totalItems معتبر است
    if (result && result.totalItems !== undefined) {
      // استفاده از مقدار بازگشتی از تابع
      totalItems.value = result.totalItems;
      console.log('Setting totalItems from API result:', totalItems.value);
    } else if (productsStore.categories && Array.isArray(productsStore.categories)) {
      // استفاده از مقدار دریافت‌شده از استور
      totalItems.value = productsStore.totalItems || productsStore.categories.length;
      console.log('Setting totalItems from store:', totalItems.value);
    } else {
      totalItems.value = 0;
      console.log('Reset totalItems to 0 (no valid data)');
    }
  } catch (error) {
    console.error('خطا در بارگذاری دسته‌بندی‌ها با پارامترها:', error);
    totalItems.value = 0;
  }
};

// اصلاح تابع اصلی fetchCategories که با search فراخوانی می‌شود
const fetchCategories = async () => {
  const params = {
    page: page.value,
    per_page: itemsPerPage.value,
    search: search.value || ''
  };
  
  await fetchCategoriesWithParams(params);
};

// تابع بازنشانی فیلترها
const resetFilters = async () => {
  console.log('Resetting category filters');
  
  // بازنشانی متغیرهای محلی
  search.value = '';
  page.value = 1;
  itemsPerPage.value = 10;
  
  // بارگذاری مجدد دسته‌بندی‌ها بدون فیلتر
  await fetchCategories();
};

// تابع تغییر صفحه در پیجینیشن
const pageChange = (newPage) => {
  console.log('Page changed to:', newPage);
  
  if (newPage !== page.value) {
    page.value = newPage;
    
    // بارگذاری داده‌ها با صفحه جدید
    const params = {
      page: page.value,
      per_page: itemsPerPage.value,
      search: search.value || ''
    };
    
    fetchCategoriesWithParams(params);
  }
};

// تابع برای رفتن به صفحه قبلی
const onPrevPage = () => {
  console.log('Go to previous page, current page:', page.value);
  if (page.value > 1) {
    page.value -= 1;
    
    // بارگذاری داده‌ها با صفحه جدید
    const params = {
      page: page.value,
      per_page: itemsPerPage.value,
      search: search.value || ''
    };
    
    fetchCategoriesWithParams(params);
  }
};

// تابع برای رفتن به صفحه بعدی
const onNextPage = () => {
  console.log('Go to next page, current page:', page.value);
  const maxPage = Math.ceil(totalItems.value / itemsPerPage.value) || 1;
  if (page.value < maxPage) {
    page.value += 1;
    
    // بارگذاری داده‌ها با صفحه جدید
    const params = {
      page: page.value,
      per_page: itemsPerPage.value,
      search: search.value || ''
    };
    
    fetchCategoriesWithParams(params);
  }
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
  setTimeout(async () => {
    console.log('Loading categories after mount delay');
    
    try {
      // بازنشانی متغیرهای صفحه‌بندی
      page.value = 1;
      itemsPerPage.value = 10;
      
      // بارگذاری اولیه دسته‌بندی‌ها
      await fetchCategories();
      
      console.log('Initial categories loaded successfully');
    } catch (error) {
      console.error('Error during initial categories load:', error);
    }
  }, 500);
});
</script>

<style scoped>
.rtl-table :deep(th) {
  text-align: right;
}
</style> 