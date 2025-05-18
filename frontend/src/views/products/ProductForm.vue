<template>
  <v-dialog v-model="dialogVisible" max-width="800px" persistent>
    <v-card>
      <v-card-title class="text-h5">
        {{ isEdit ? 'ویرایش محصول' : 'افزودن محصول جدید' }}
      </v-card-title>

      <v-card-text>
        <v-form ref="form" @submit.prevent="saveProduct">
          <v-container>
            <v-row>
              <!-- اطلاعات پایه محصول -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="product.code"
                  label="کد محصول"
                  variant="outlined"
                  density="compact"
                  :rules="[v => !!v || 'کد محصول الزامی است']"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-select
                  v-model="product.category"
                  :items="categories"
                  item-title="name"
                  item-value="id"
                  return-object
                  label="دسته‌بندی"
                  variant="outlined"
                  density="compact"
                >
                  <template v-slot:append>
                    <v-btn
                      icon="mdi-plus"
                      size="small"
                      variant="text"
                      class="mr-n2"
                      @click.stop="openCategoryDialog"
                    ></v-btn>
                  </template>
                </v-select>
              </v-col>

              <v-col cols="12">
                <v-text-field
                  v-model="product.name"
                  label="نام محصول"
                  variant="outlined"
                  density="compact"
                  :rules="[v => !!v || 'نام محصول الزامی است']"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-select
                  v-model="product.unit"
                  :items="units"
                  item-title="name"
                  item-value="id"
                  return-object
                  label="واحد اندازه‌گیری"
                  variant="outlined"
                  density="compact"
                ></v-select>
              </v-col>

              <!-- اطلاعات قیمت و موجودی -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model.number="product.purchase_price"
                  label="قیمت خرید (تومان)"
                  variant="outlined"
                  density="compact"
                  type="number"
                  :rules="[
                    v => !!v || 'قیمت خرید الزامی است',
                    v => v >= 0 || 'قیمت باید بزرگتر یا مساوی صفر باشد'
                  ]"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model.number="product.selling_price"
                  label="قیمت فروش (تومان)"
                  variant="outlined"
                  density="compact"
                  type="number"
                  :rules="[
                    v => !!v || 'قیمت فروش الزامی است',
                    v => v >= 0 || 'قیمت باید بزرگتر یا مساوی صفر باشد'
                  ]"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model.number="product.min_stock"
                  label="حداقل موجودی"
                  variant="outlined"
                  density="compact"
                  type="number"
                  :rules="[v => v >= 0 || 'حداقل موجودی باید بزرگتر یا مساوی صفر باشد']"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-switch
                  v-model="product.is_active"
                  label="وضعیت فعال"
                  color="success"
                  inset
                ></v-switch>
              </v-col>

              <!-- توضیحات محصول -->
              <v-col cols="12">
                <v-textarea
                  v-model="product.description"
                  label="توضیحات محصول"
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
          @click="saveProduct" 
          :loading="loading"
        >
          {{ isEdit ? 'ویرایش' : 'افزودن' }}
        </v-btn>
      </v-card-actions>
    </v-card>

    <!-- دیالوگ افزودن دسته‌بندی جدید -->
    <category-form
      v-model="categoryDialog"
      @category-added="onCategoryAdded"
    />
  </v-dialog>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useProductsStore } from '../../store/products';
import CategoryForm from './CategoryForm.vue';

// تعریف پراپس
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  editedProduct: {
    type: Object,
    default: () => null
  }
});

// تعریف ایونت‌ها
const emit = defineEmits(['update:modelValue', 'product-saved']);

// استور محصولات
const productsStore = useProductsStore();

// متغیرهای واکنش‌پذیر
const form = ref(null);
const product = ref({
  code: '',
  name: '',
  description: '',
  category: null,
  unit: null,
  purchase_price: 0,
  selling_price: 0,
  min_stock: 0,
  is_active: true
});
const categoryDialog = ref(false);

// وضعیت دیالوگ و ویرایش
const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

const isEdit = computed(() => !!props.editedProduct);
const loading = computed(() => productsStore.loading);
const categories = computed(() => productsStore.categories);
const units = computed(() => productsStore.units);

// ایجاد دسته‌بندی جدید
const openCategoryDialog = () => {
  categoryDialog.value = true;
};

const onCategoryAdded = (newCategory) => {
  product.value.category = newCategory;
};

// ذخیره محصول
const saveProduct = async () => {
  try {
    const { valid } = await form.value.validate();
    
    if (!valid) return;
    
    // تبدیل داده‌های محصول به فرمت مناسب برای API
    const productData = { ...product.value };
    
    // تبدیل آبجکت دسته‌بندی به ID
    if (productData.category) {
      productData.category = productData.category.id;
    }
    
    // تبدیل آبجکت واحد به ID
    if (productData.unit) {
      productData.unit = productData.unit.id;
    }
    
    console.log('Saving product data:', productData);
    
    // ذخیره محصول
    let result;
    if (isEdit.value) {
      result = await productsStore.updateProduct(props.editedProduct.id, productData);
      console.log('Product updated, result:', result);
    } else {
      result = await productsStore.addProduct(productData);
      console.log('Product added, result:', result);
    }
    
    // حتی اگر result تعریف نشده یا null باشد، دیالوگ را ببند
    console.log('Closing product dialog directly...');
    
    // بستن دیالوگ به طور مستقیم
    emit('update:modelValue', false);
    // بستن دیالوگ از طریق computed property
    dialogVisible.value = false;
    
    // اگر عملیات موفقیت آمیز بود، رویداد product-saved را ارسال کن
    if (result) {
      emit('product-saved', result);
    }
    
    // ریست کردن فرم
    resetForm();
  } catch (error) {
    console.error('Error in saveProduct:', error);
  }
};

// بستن دیالوگ
const close = () => {
  console.log('Closing product dialog through close()...');
  // بستن دیالوگ به طور مستقیم
  emit('update:modelValue', false);
  dialogVisible.value = false;
  // ریست کردن فرم
  resetForm();
};

// بازنشانی فرم
const resetForm = () => {
  product.value = {
    code: '',
    name: '',
    description: '',
    category: null,
    unit: null,
    purchase_price: 0,
    selling_price: 0,
    min_stock: 0,
    is_active: true
  };
  
  if (form.value) {
    form.value.resetValidation();
  }
};

// پر کردن فرم در حالت ویرایش
watch(() => props.editedProduct, (newProduct) => {
  if (newProduct) {
    product.value = { ...newProduct };
  }
}, { immediate: true });

// دریافت لیست واحدها در زمان نمایش
onMounted(async () => {
  if (categories.value.length === 0) {
    await productsStore.fetchCategories();
  }
  
  if (units.value.length === 0) {
    await productsStore.fetchUnits();
  }
});
</script>

<style scoped>
.v-card-title {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  padding-bottom: 16px;
}
</style> 