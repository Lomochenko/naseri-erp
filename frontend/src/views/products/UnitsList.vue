<template>
  <div>
    <v-card class="mb-6">
      <v-card-title class="d-flex align-center justify-space-between">
        <span class="text-h5">مدیریت واحدهای اندازه‌گیری</span>
        <v-btn 
          color="primary" 
          prepend-icon="mdi-plus" 
          variant="elevated"
          @click="addNewUnit"
        >
          واحد جدید
        </v-btn>
      </v-card-title>

      <v-card-text>
        <v-row>
          <!-- فیلترهای جستجو -->
          <v-col cols="12" md="6">
            <v-text-field
              v-model="search"
              label="جستجو در واحدها"
              variant="outlined"
              density="compact"
              prepend-inner-icon="mdi-magnify"
              hide-details
              @update:model-value="fetchUnits"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="6" class="d-flex justify-end align-center">
            <v-btn 
              color="secondary" 
              variant="text" 
              prepend-icon="mdi-refresh"
              @click="fetchUnits"
            >
              بازنشانی
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- جدول نمایش واحدها -->
    <v-card>
      <v-data-table
        :headers="headers"
        :items="units"
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

        <!-- نمایش نام واحد -->
        <template v-slot:item.name="{ item }">
          <div class="font-weight-medium">{{ item.name }}</div>
        </template>

        <!-- نمایش نماد واحد -->
        <template v-slot:item.symbol="{ item }">
          <v-chip
            size="small"
            color="primary"
            variant="flat"
          >
            {{ item.symbol }}
          </v-chip>
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
              @click="editUnit(item)"
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
            <v-icon size="large" icon="mdi-scale" color="secondary" class="mb-3"></v-icon>
            <div>واحدی یافت نشد</div>
            <v-btn 
              variant="text" 
              color="primary" 
              class="mt-3" 
              @click="fetchUnits"
            >
              تلاش مجدد
            </v-btn>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <!-- دیالوگ فرم واحد -->
    <unit-form
      v-model="unitDialog"
      :edited-unit="editedUnit"
      @unit-saved="onUnitSaved"
    />

    <!-- دیالوگ حذف واحد -->
    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title class="text-h5">حذف واحد</v-card-title>
        <v-card-text>
          آیا از حذف واحد <strong>{{ deleteItem?.name }}</strong> اطمینان دارید؟
          <div class="text-caption text-medium-emphasis mt-2">
            این عملیات غیرقابل بازگشت است و ممکن است بر محصولاتی که به این واحد متصل هستند تأثیر بگذارد.
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" variant="text" @click="deleteDialog = false">انصراف</v-btn>
          <v-btn 
            color="error" 
            variant="elevated" 
            @click="deleteUnit" 
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
import UnitForm from './UnitForm.vue';

// استور محصولات
const productsStore = useProductsStore();

// ثابت‌های نمایش
const headers = [
  { title: 'نام واحد', key: 'name', align: 'start', sortable: true },
  { title: 'نماد', key: 'symbol', align: 'center', sortable: true },
  { title: 'عملیات', key: 'actions', align: 'center', sortable: false },
];

// متغیرهای واکنش‌پذیر
const unitDialog = ref(false);
const deleteDialog = ref(false);
const editedUnit = ref(null);
const deleteItem = ref(null);
const page = ref(1);
const itemsPerPage = ref(10);
const search = ref('');
const totalItems = ref(0);

// دریافت داده‌ها از استور
const loading = computed(() => productsStore.loading);
const units = computed(() => productsStore.units);

// بارگذاری واحدها
const fetchUnits = async () => {
  try {
    await productsStore.fetchUnits({
      search: search.value,
      page: page.value,
      page_size: itemsPerPage.value
    });
    totalItems.value = productsStore.units.length;
  } catch (error) {
    console.error('خطا در بارگذاری واحدها:', error);
  }
};

// مدیریت گزینه‌های جدول
const handleOptions = (options) => {
  page.value = options.page;
  itemsPerPage.value = options.itemsPerPage;
  
  fetchUnits();
};

// مدیریت واحدها
const addNewUnit = () => {
  editedUnit.value = null;
  unitDialog.value = true;
};

const editUnit = (item) => {
  editedUnit.value = { ...item };
  unitDialog.value = true;
};

const confirmDelete = (item) => {
  deleteItem.value = item;
  deleteDialog.value = true;
};

const deleteUnit = async () => {
  try {
    await productsStore.deleteUnit(deleteItem.value.id);
    deleteDialog.value = false;
    deleteItem.value = null;
    fetchUnits();
  } catch (error) {
    console.error('خطا در حذف واحد:', error);
  }
};

const onUnitSaved = () => {
  fetchUnits();
};

// دریافت داده‌ها در زمان بارگذاری
onMounted(() => {
  fetchUnits();
});
</script>

<style scoped>
.rtl-table :deep(th) {
  text-align: right;
}
</style> 
 