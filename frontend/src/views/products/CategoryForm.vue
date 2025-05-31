<template>
  <v-dialog v-model="dialog" max-width="500px" persistent>
    <v-card>
      <v-card-title class="text-h5">
        {{ editedId ? 'ویرایش دسته‌بندی' : 'افزودن دسته‌بندی جدید' }}
      </v-card-title>

      <v-card-text>
        <v-container>
          <v-form ref="form" @submit.prevent="save">
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="formData.name"
                  label="نام دسته‌بندی *"
                  :rules="rules.name"
                  required
                  variant="outlined"
                  density="comfortable"
                  autofocus
                  dir="rtl"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-textarea
                  v-model="formData.description"
                  label="توضیحات"
                  variant="outlined"
                  rows="3"
                  auto-grow
                  density="comfortable"
                  dir="rtl"
                ></v-textarea>
              </v-col>
            </v-row>
          </v-form>
          <v-alert
            v-if="error"
            type="error"
            variant="tonal"
            closable
            class="mt-3"
            @click:close="error = ''"
          >
            {{ error }}
          </v-alert>
        </v-container>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="secondary"
          variant="text"
          @click="close"
        >
          انصراف
        </v-btn>
        <v-btn
          color="primary"
          variant="elevated"
          @click="save"
          :loading="loading"
          :disabled="!isFormValid"
        >
          {{ editedId ? 'ذخیره تغییرات' : 'افزودن' }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useProductsStore } from '../../store/products';

// Props و Emits
const props = defineProps({
  modelValue: Boolean,
  editedCategory: Object
});

const emit = defineEmits(['update:modelValue', 'category-added', 'category-updated']);

// دسترسی به فروشگاه
const productsStore = useProductsStore();

// داده‌های فرم
const form = ref(null);
const formData = ref({
  name: '',
  description: ''
});
const error = ref('');
const editedId = ref(null);

// قوانین اعتبارسنجی
const rules = {
  name: [
    v => !!v || 'نام دسته‌بندی الزامی است',
    v => (v && v.length >= 3) || 'نام دسته‌بندی باید حداقل 3 کاراکتر باشد',
  ]
};

// محاسبات
const dialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

const loading = computed(() => productsStore.loading);

const isFormValid = computed(() => {
  return formData.value.name && formData.value.name.length >= 3;
});

// توابع
const save = async () => {
  if (!isFormValid.value) {
    error.value = 'لطفاً همه فیلدها را به درستی پر کنید';
    return;
  }
  
  error.value = '';
  
  try {
    const categoryData = {
      name: formData.value.name,
      description: formData.value.description || ''
    };
    
    let result;
    
    if (editedId.value) {
      // ویرایش دسته‌بندی موجود
      result = await productsStore.updateCategory(editedId.value, categoryData);
      console.log('Category updated:', result);
      if (result) {
        emit('category-updated', result);
      }
    } else {
      // افزودن دسته‌بندی جدید
      result = await productsStore.addCategory(categoryData);
      console.log('Category added:', result);
      if (result) {
        emit('category-added', result);
      }
    }
    
    // بستن پنجره بعد از ذخیره، چه برای ویرایش و چه برای افزودن
    console.log('Directly closing category dialog...');
    
    // بستن دیالوگ به طور مستقیم
    emit('update:modelValue', false);
    dialog.value = false;
    resetForm();
    
  } catch (err) {
    console.error('خطا در ذخیره دسته‌بندی:', err);
    error.value = err.message || 'خطا در ذخیره اطلاعات دسته‌بندی';
  }
};

const resetForm = () => {
  // ریست کردن رفرنس فرم
  if (form.value) {
    try {
      form.value.reset();
    } catch (e) {
      console.error('خطا در ریست کردن فرم:', e);
    }
  }
  
  // بازنشانی مستقیم فیلدها
  formData.value = {
    name: '',
    description: ''
  };
  
  // بازنشانی آی‌دی دسته‌بندی ویرایش شده
  editedId.value = null;
  
  // بازنشانی پیام خطا
  error.value = '';
  
  console.log('Form reset completed');
};

const close = () => {
  console.log('Directly closing dialog via close button...');
  // بستن دیالوگ به طور مستقیم 
  emit('update:modelValue', false);
  dialog.value = false;
  resetForm();
};

const loadCategoryData = () => {
  if (!props.editedCategory) {
    console.warn('No category data to load');
    return;
  }
  
  console.log('Loading category data for editing:', props.editedCategory);
  
  // ذخیره آی‌دی برای استفاده در هنگام ذخیره تغییرات
  editedId.value = props.editedCategory.id;
  
  // پر کردن فرم با مقادیر دسته‌بندی
  formData.value = {
    name: props.editedCategory.name || '',
    description: props.editedCategory.description || ''
  };
  
  console.log('Category data loaded into form:', formData.value);
};

// Watchers
watch(() => props.modelValue, (newVal) => {
  console.log('Dialog modelValue changed:', newVal);
  dialog.value = newVal;
  
  if (!newVal) {
    // اگر دیالوگ بسته شده است، فرم را ریست کنیم
    console.log('Dialog closing via modelValue change, resetting form');
    resetForm();
  } else if (props.editedCategory) {
    // اگر در حالت ویرایش هستیم، داده‌های دسته‌بندی را لود کنیم
    loadCategoryData();
  }
});

// واچر برای ردیابی تغییرات دسته‌بندی ویرایش شده
watch(() => props.editedCategory, (newVal) => {
  console.log('Edited category changed:', newVal);
  if (newVal && dialog.value) {
    // فقط اگر دیالوگ باز است، داده‌ها را لود کنیم
    loadCategoryData();
  }
});

// واچر برای ردیابی تغییرات dialog و انتقال به modelValue
watch(() => dialog.value, (newVal) => {
  console.log('Dialog value changed internally:', newVal);
  if (newVal !== props.modelValue) {
    emit('update:modelValue', newVal);
  }
});

// Lifecycle hooks
onMounted(() => {
  if (dialog.value && props.editedCategory) {
    loadCategoryData();
  }
});
</script>

<style scoped>
.v-card-title {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  padding-bottom: 16px;
}
</style> 