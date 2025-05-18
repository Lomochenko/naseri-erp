<template>
  <v-dialog v-model="dialogVisible" max-width="500px" persistent>
    <v-card>
      <v-card-title class="text-h5">
        {{ isEdit ? 'ویرایش واحد' : 'افزودن واحد جدید' }}
      </v-card-title>

      <v-card-text>
        <v-form ref="form" @submit.prevent="saveUnit">
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="unit.name"
                  label="نام واحد"
                  variant="outlined"
                  density="compact"
                  :rules="[v => !!v || 'نام واحد الزامی است']"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-text-field
                  v-model="unit.symbol"
                  label="نماد واحد"
                  variant="outlined"
                  density="compact"
                  :rules="[v => !!v || 'نماد واحد الزامی است']"
                  required
                ></v-text-field>
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
          @click="saveUnit"
          :loading="loading"
        >
          {{ isEdit ? 'ویرایش' : 'افزودن' }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useProductsStore } from '../../store/products';

// تعریف پراپس
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  editedUnit: {
    type: Object,
    default: () => null
  }
});

// تعریف ایونت‌ها
const emit = defineEmits(['update:modelValue', 'unit-saved']);

// استور محصولات
const productsStore = useProductsStore();

// متغیرهای واکنش‌پذیر
const form = ref(null);
const unit = ref({
  name: '',
  symbol: ''
});

// وضعیت دیالوگ و ویرایش
const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

const isEdit = computed(() => !!props.editedUnit);
const loading = computed(() => productsStore.loading);

// ذخیره واحد
const saveUnit = async () => {
  const { valid } = await form.value.validate();
  
  if (!valid) return;
  
  let result;
  if (isEdit.value) {
    // ویرایش واحد موجود
    result = await productsStore.updateUnit(props.editedUnit.id, unit.value);
  } else {
    // افزودن واحد جدید
    result = await productsStore.addUnit(unit.value);
  }
  
  if (result) {
    emit('unit-saved', result);
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
  unit.value = {
    name: '',
    symbol: ''
  };
  if (form.value) {
    form.value.resetValidation();
  }
};

// پر کردن فرم در حالت ویرایش
watch(() => props.editedUnit, (newUnit) => {
  if (newUnit) {
    unit.value = { ...newUnit };
  } else {
    resetForm();
  }
}, { immediate: true });
</script>

<style scoped>
.v-card-title {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  padding-bottom: 16px;
}
</style> 
 