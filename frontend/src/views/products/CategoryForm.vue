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
        // اطمینان از بسته شدن پنجره
        setTimeout(() => {
          close();
        }, 100);
      }
    } else {
      // افزودن دسته‌بندی جدید
      result = await productsStore.addCategory(categoryData);
      console.log('Category added:', result);
      if (result) {
        emit('category-added', result);
        // اطمینان از بسته شدن پنجره (افزودن تأخیر برای اطمینان از بسته شدن)
        setTimeout(() => {
          close();
        }, 100);
      }
    }
  } catch (err) {
    console.error('خطا در ذخیره دسته‌بندی:', err);
    error.value = err.message || 'خطا در ذخیره اطلاعات دسته‌بندی';
  }
};

const resetForm = () => {
  if (form.value) {
    form.value.reset();
  }
  
  formData.value = {
    name: '',
    description: ''
  };
  
  editedId.value = null;
  error.value = '';
};

const close = () => {
  console.log('Closing dialog...');
  // تنظیم مستقیم دیالوگ
  dialog.value = false;
  // فراخوانی resetForm برای پاکسازی فرم
  resetForm();
  // اطمینان از اعمال تغییرات
  setTimeout(() => {
    emit('update:modelValue', false);
    console.log('Dialog closed');
  }, 50);
};

const loadCategoryData = () => {
  if (props.editedCategory) {
    editedId.value = props.editedCategory.id;
    formData.value = {
      name: props.editedCategory.name || '',
      description: props.editedCategory.description || ''
    };
  } else {
    resetForm();
  }
};

// Watchers
watch(() => dialog.value, (val) => {
  if (val) {
    loadCategoryData();
  }
});

watch(() => props.editedCategory, (val) => {
  if (val && dialog.value) {
    loadCategoryData();
  }
}, { deep: true });

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