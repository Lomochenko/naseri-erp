<template>
  <v-dialog v-model="dialogVisible" max-width="500px" persistent>
    <v-card>
      <v-card-title class="text-h5">
        {{ isEdit ? 'ویرایش دسته‌بندی' : 'افزودن دسته‌بندی جدید' }}
      </v-card-title>

      <v-card-text>
        <v-form ref="form" @submit.prevent="saveCategory">
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="category.name"
                  label="نام دسته‌بندی"
                  variant="outlined"
                  density="compact"
                  :rules="[v => !!v || 'نام دسته‌بندی الزامی است']"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-select
                  v-model="category.parent"
                  :items="categories"
                  item-title="name"
                  item-value="id"
                  label="دسته‌بندی والد (اختیاری)"
                  variant="outlined"
                  density="compact"
                  return-object
                  clearable
                  :disabled="categories.length === 0"
                ></v-select>
              </v-col>

              <v-col cols="12">
                <v-textarea
                  v-model="category.description"
                  label="توضیحات دسته‌بندی"
                  variant="outlined"
                  density="compact"
                  auto-grow
                  rows="3"
                ></v-textarea>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="error" variant="text" @click="close">انصراف</v-btn>
        <v-btn 
          color="primary" 
          variant="elevated" 
          @click="saveCategory"
          :loading="loading"
        >
          {{ isEdit ? 'ویرایش' : 'افزودن' }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useProductsStore } from '../../store/products';

// تعریف پراپس
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  editedCategory: {
    type: Object,
    default: () => null
  }
});

// تعریف ایونت‌ها
const emit = defineEmits(['update:modelValue', 'category-added', 'category-updated']);

// استور محصولات
const productsStore = useProductsStore();

// متغیرهای واکنش‌پذیر
const form = ref(null);
const category = ref({
  name: '',
  parent: null,
  description: ''
});

// وضعیت دیالوگ و ویرایش
const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

const isEdit = computed(() => !!props.editedCategory);
const loading = computed(() => productsStore.loading);
const categories = computed(() => {
  // فیلتر کردن دسته‌بندی فعلی (در صورت ویرایش) از لیست
  if (isEdit.value) {
    return productsStore.categories.filter(cat => cat.id !== props.editedCategory.id);
  }
  return productsStore.categories;
});

// ذخیره دسته‌بندی
const saveCategory = async () => {
  const { valid } = await form.value.validate();
  
  if (!valid) return;
  
  const categoryData = {
    name: category.value.name,
    description: category.value.description || '',
    parent: category.value.parent ? category.value.parent.id : null
  };
  
  let result;
  if (isEdit.value) {
    result = await productsStore.updateCategory(props.editedCategory.id, categoryData);
    if (result) {
      emit('category-updated', result);
    }
  } else {
    result = await productsStore.addCategory(categoryData);
    if (result) {
      emit('category-added', result);
    }
  }
  
  if (result) {
    close();
  }
};

// بستن دیالوگ
const close = () => {
  dialogVisible.value = false;
  resetForm();
};

// بازنشانی فرم
const resetForm = () => {
  category.value = {
    name: '',
    parent: null,
    description: ''
  };
  if (form.value) {
    form.value.resetValidation();
  }
};

// پر کردن فرم در حالت ویرایش
const loadCategory = () => {
  if (props.editedCategory) {
    category.value = { ...props.editedCategory };
  } else {
    resetForm();
  }
};

// دریافت لیست دسته‌بندی‌ها در زمان نمایش
onMounted(async () => {
  if (categories.value.length === 0) {
    await productsStore.fetchCategories();
  }
  loadCategory();
});
</script>

<style scoped>
.v-card-title {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  padding-bottom: 16px;
}
</style> 