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
                <v-text-field
                  v-model="product.barcode"
                  label="بارکد محصول"
                  variant="outlined"
                  density="compact"
                ></v-text-field>
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
                  v-model="product.category"
                  :items="categories"
                  item-title="name"
                  item-value="id"
                  label="دسته‌بندی"
                  variant="outlined"
                  density="compact"
                  :rules="[v => !!v || 'انتخاب دسته‌بندی الزامی است']"
                  required
                  return-object
                >
                  <template v-slot:append>
                    <v-btn 
                      icon="mdi-plus" 
                      size="small" 
                      variant="text" 
                      color="primary"
                      @click.stop="openCategoryDialog"
                    ></v-btn>
                  </template>
                </v-select>
              </v-col>

              <v-col cols="12" md="6">
                <v-select
                  v-model="product.unit"
                  :items="units"
                  item-title="name"
                  item-value="id"
                  label="واحد اندازه‌گیری"
                  variant="outlined"
                  density="compact"
                  :rules="[v => !!v || 'انتخاب واحد الزامی است']"
                  required
                  return-object
                >
                  <template v-slot:item="{ item, props }">
                    <v-list-item v-bind="props" :title="`${item.name} (${item.symbol})`"></v-list-item>
                  </template>
                </v-select>
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

              <!-- آپلود تصویر محصول -->
              <v-col cols="12">
                <v-file-input
                  v-model="productImage"
                  label="تصویر محصول"
                  variant="outlined"
                  density="compact"
                  accept="image/*"
                  prepend-icon="mdi-camera"
                  truncate-length="20"
                  :show-size="1000"
                  @change="previewImage"
                >
                  <template v-slot:selection="{ fileNames }">
                    <template v-for="(fileName, index) in fileNames" :key="index">
                      <v-chip size="small" class="me-2" variant="outlined">
                        {{ fileName }}
                      </v-chip>
                    </template>
                  </template>
                </v-file-input>
              </v-col>

              <!-- پیش‌نمایش تصویر -->
              <v-col v-if="imageSrc || product.image" cols="12" class="text-center">
                <v-img 
                  :src="imageSrc || product.image" 
                  max-height="200" 
                  max-width="200"
                  class="mx-auto"
                ></v-img>
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
const productImage = ref(null);
const imageSrc = ref(null);
const product = ref({
  code: '',
  barcode: '',
  name: '',
  description: '',
  category: null,
  unit: null,
  purchase_price: 0,
  selling_price: 0,
  min_stock: 0,
  is_active: true,
  image: null
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

// پیش‌نمایش تصویر
const previewImage = (event) => {
  const file = event?.[0];
  if (file) {
    imageSrc.value = URL.createObjectURL(file);
  } else {
    imageSrc.value = null;
  }
};

// ایجاد دسته‌بندی جدید
const openCategoryDialog = () => {
  categoryDialog.value = true;
};

const onCategoryAdded = (newCategory) => {
  product.value.category = newCategory;
};

// ذخیره محصول
const saveProduct = async () => {
  const { valid } = await form.value.validate();
  
  if (!valid) return;
  
  // ایجاد FormData برای آپلود تصویر
  const formData = new FormData();
  
  // اضافه کردن فیلدهای محصول به FormData
  Object.keys(product.value).forEach(key => {
    if (key === 'category' && product.value.category) {
      formData.append('category', product.value.category.id);
    } else if (key === 'unit' && product.value.unit) {
      formData.append('unit', product.value.unit.id);
    } else if (product.value[key] !== null && product.value[key] !== undefined) {
      formData.append(key, product.value[key]);
    }
  });
  
  // اضافه کردن تصویر در صورت انتخاب
  if (productImage.value?.[0]) {
    formData.append('image', productImage.value[0]);
  }
  
  // ذخیره محصول
  let result;
  if (isEdit.value) {
    result = await productsStore.updateProduct(props.editedProduct.id, formData);
  } else {
    result = await productsStore.addProduct(formData);
  }
  
  if (result) {
    emit('product-saved', result);
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
  product.value = {
    code: '',
    barcode: '',
    name: '',
    description: '',
    category: null,
    unit: null,
    purchase_price: 0,
    selling_price: 0,
    min_stock: 0,
    is_active: true,
    image: null
  };
  productImage.value = null;
  imageSrc.value = null;
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