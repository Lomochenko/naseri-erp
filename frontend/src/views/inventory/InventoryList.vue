<template>
  <div>
    <div class="d-flex justify-space-between align-center mb-6">
      <h1 class="text-h4">مدیریت موجودی</h1>
      <v-btn color="primary" prepend-icon="mdi-plus">
        ثبت تراکنش جدید
      </v-btn>
    </div>

    <!-- Warehouse Selection -->
    <v-card class="mb-6">
      <v-card-text>
        <v-row>
          <v-col cols="12" md="4">
            <v-select
              v-model="selectedWarehouse"
              label="انبار"
              variant="outlined"
              density="compact"
              :items="warehouses"
              item-title="name"
              item-value="id"
              @update:model-value="getInventory"
            ></v-select>
          </v-col>
          <v-col cols="12" md="8" class="d-flex align-center">
            <v-text-field
              v-model="searchQuery"
              label="جستجوی محصول"
              variant="outlined"
              density="compact"
              prepend-inner-icon="mdi-magnify"
              clearable
              @input="getInventory"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Inventory Table -->
    <v-card>
      <v-data-table
        :headers="headers"
        :items="inventory"
        :loading="loading"
        :items-per-page="10"
        :items-per-page-options="[10, 20, 50]"
        density="compact"
        class="elevation-1"
      >
        <!-- Product name column -->
        <template v-slot:item.product.name="{ item }">
          <div class="d-flex align-center">
            <v-avatar size="30" class="me-2">
              <v-img :src="item.product.image || 'https://via.placeholder.com/30'" cover></v-img>
            </v-avatar>
            <span>{{ item.product.name }}</span>
          </div>
        </template>

        <!-- Quantity column -->
        <template v-slot:item.quantity="{ item }">
          <span class="font-weight-bold">{{ item.quantity }}</span> {{ item.product.unit.name }}
        </template>

        <!-- Status column -->
        <template v-slot:item.status="{ item }">
          <v-chip
            :color="getStatusColor(item.quantity)"
            size="small"
          >
            {{ getStatusLabel(item.quantity) }}
          </v-chip>
        </template>

        <!-- Actions column -->
        <template v-slot:item.actions="{ item }">
          <v-tooltip text="تاریخچه تراکنش‌ها">
            <template v-slot:activator="{ props }">
              <v-icon 
                size="small" 
                class="me-2"
                v-bind="props"
                @click="showHistory(item)"
              >
                mdi-history
              </v-icon>
            </template>
          </v-tooltip>
          <v-tooltip text="تنظیم موجودی">
            <template v-slot:activator="{ props }">
              <v-icon 
                size="small" 
                class="me-2"
                v-bind="props"
                @click="adjustInventory(item)"
              >
                mdi-tune
              </v-icon>
            </template>
          </v-tooltip>
        </template>
      </v-data-table>
    </v-card>

    <!-- Adjust Inventory Dialog -->
    <v-dialog v-model="adjustDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">تنظیم موجودی</v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-model="adjustForm.product_name"
                label="نام محصول"
                readonly
                variant="outlined"
                density="compact"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="adjustForm.current_quantity"
                label="موجودی فعلی"
                readonly
                variant="outlined"
                density="compact"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="adjustForm.new_quantity"
                label="موجودی جدید"
                type="number"
                variant="outlined"
                density="compact"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-select
                v-model="adjustForm.reason"
                label="دلیل تغییر"
                :items="adjustReasons"
                variant="outlined"
                density="compact"
              ></v-select>
            </v-col>
            <v-col cols="12">
              <v-textarea
                v-model="adjustForm.notes"
                label="توضیحات"
                variant="outlined"
                density="compact"
                rows="3"
              ></v-textarea>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="text" @click="adjustDialog = false">انصراف</v-btn>
          <v-btn color="success" variant="elevated" @click="saveAdjustment">ذخیره</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Transaction History Dialog -->
    <v-dialog v-model="historyDialog" max-width="800px">
      <v-card>
        <v-card-title class="text-h5">تاریخچه تراکنش‌های {{ selectedProduct?.product?.name }}</v-card-title>
        <v-card-text>
          <v-table>
            <thead>
              <tr>
                <th>تاریخ</th>
                <th>نوع تراکنش</th>
                <th>مقدار</th>
                <th>توضیحات</th>
                <th>کاربر</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in transactionHistory" :key="item.id">
                <td>{{ item.created_at }}</td>
                <td>
                  <v-chip
                    :color="getTransactionTypeColor(item.transaction_type)"
                    size="small"
                  >
                    {{ getTransactionTypeLabel(item.transaction_type) }}
                  </v-chip>
                </td>
                <td>{{ item.quantity }} {{ selectedProduct?.product?.unit?.name }}</td>
                <td>{{ item.notes }}</td>
                <td>{{ item.created_by }}</td>
              </tr>
            </tbody>
          </v-table>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="historyDialog = false">بستن</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// Table headers
const headers = [
  { title: 'کد محصول', key: 'product.code', sortable: true, align: 'start' },
  { title: 'نام محصول', key: 'product.name', sortable: true, align: 'start' },
  { title: 'دسته‌بندی', key: 'product.category.name', sortable: true, align: 'start' },
  { title: 'موجودی', key: 'quantity', sortable: true, align: 'center' },
  { title: 'قیمت واحد', key: 'product.price', sortable: true, align: 'end' },
  { title: 'وضعیت', key: 'status', sortable: false, align: 'center' },
  { title: 'عملیات', key: 'actions', sortable: false, align: 'center' }
];

// Data
const inventory = ref([]);
const warehouses = ref([]);
const loading = ref(false);
const selectedWarehouse = ref(null);
const searchQuery = ref('');
const adjustDialog = ref(false);
const historyDialog = ref(false);
const selectedProduct = ref(null);
const transactionHistory = ref([]);

// Adjust inventory form
const adjustForm = ref({
  product_id: null,
  product_name: '',
  current_quantity: 0,
  new_quantity: 0,
  reason: '',
  notes: ''
});

// Adjust reasons
const adjustReasons = [
  'اصلاح خطای موجودی',
  'شمارش انبار',
  'ضایعات',
  'مرجوعی',
  'سایر'
];

// Mock data - Replace with API call
const mockWarehouses = [
  { id: 1, name: 'انبار مرکزی' },
  { id: 2, name: 'انبار شعبه 1' },
  { id: 3, name: 'انبار شعبه 2' }
];

const mockInventory = [
  { 
    id: 1, 
    product: { 
      id: 1, 
      code: 'HDL-G102', 
      name: 'دستگیره کابینت مدل G102', 
      category: { id: 1, name: 'دستگیره' },
      unit: { id: 1, name: 'عدد' },
      price: 125000,
      image: 'https://via.placeholder.com/30'
    }, 
    warehouse_id: 1, 
    quantity: 24 
  },
  { 
    id: 2, 
    product: { 
      id: 2, 
      code: 'HNG-S220', 
      name: 'لولا آرام بند', 
      category: { id: 2, name: 'لولا' },
      unit: { id: 1, name: 'عدد' },
      price: 85000,
      image: 'https://via.placeholder.com/30'
    }, 
    warehouse_id: 1, 
    quantity: 7 
  },
  { 
    id: 3, 
    product: { 
      id: 3, 
      code: 'RIL-T050', 
      name: 'ریل کشو تاندم ۵۰ سانتی', 
      category: { id: 3, name: 'ریل' },
      unit: { id: 3, name: 'جفت' },
      price: 320000,
      image: 'https://via.placeholder.com/30'
    }, 
    warehouse_id: 1, 
    quantity: 4 
  },
  { 
    id: 4, 
    product: { 
      id: 4, 
      code: 'LEG-S120', 
      name: 'پایه کابینت استیل', 
      category: { id: 4, name: 'پایه و اتصالات' },
      unit: { id: 1, name: 'عدد' },
      price: 45000,
      image: 'https://via.placeholder.com/30'
    }, 
    warehouse_id: 1, 
    quantity: 8 
  },
  { 
    id: 5, 
    product: { 
      id: 5, 
      code: 'LCK-K85', 
      name: 'قفل درب سوئیچی', 
      category: { id: 5, name: 'قفل' },
      unit: { id: 1, name: 'عدد' },
      price: 165000,
      image: 'https://via.placeholder.com/30'
    }, 
    warehouse_id: 1, 
    quantity: 2 
  },
];

const mockTransactionHistory = [
  { 
    id: 1, 
    product_id: 1, 
    warehouse_id: 1, 
    transaction_type: 'IN', 
    quantity: 10, 
    created_at: '۱۴۰۳/۰۲/۲۰', 
    notes: 'خرید از تامین‌کننده', 
    created_by: 'علی محمدی' 
  },
  { 
    id: 2, 
    product_id: 1, 
    warehouse_id: 1, 
    transaction_type: 'OUT', 
    quantity: 2, 
    created_at: '۱۴۰۳/۰۲/۲۲', 
    notes: 'فروش به مشتری', 
    created_by: 'رضا رضایی' 
  },
  { 
    id: 3, 
    product_id: 1, 
    warehouse_id: 1, 
    transaction_type: 'ADJUST', 
    quantity: 1, 
    created_at: '۱۴۰۳/۰۲/۲۳', 
    notes: 'اصلاح موجودی - شمارش انبار', 
    created_by: 'علی محمدی' 
  },
  { 
    id: 4, 
    product_id: 1, 
    warehouse_id: 1, 
    transaction_type: 'IN', 
    quantity: 15, 
    created_at: '۱۴۰۳/۰۲/۲۴', 
    notes: 'خرید از تامین‌کننده', 
    created_by: 'علی محمدی' 
  },
  { 
    id: 5, 
    product_id: 1, 
    warehouse_id: 1, 
    transaction_type: 'OUT', 
    quantity: 4, 
    created_at: '۱۴۰۳/۰۲/۲۵', 
    notes: 'فروش به مشتری', 
    created_by: 'رضا رضایی' 
  },
];

// Methods
const getInventory = async () => {
  loading.value = true;
  
  try {
    // Replace with actual API call
    // const response = await axios.get('http://localhost:8000/api/inventory/inventory/', { 
    //   params: {
    //     search: searchQuery.value,
    //     warehouse: selectedWarehouse.value
    //   }
    // });
    // inventory.value = response.data.results;
    
    // Using mock data for now
    setTimeout(() => {
      // Filter by warehouse if selected
      let result = [...mockInventory];
      if (selectedWarehouse.value) {
        result = result.filter(item => item.warehouse_id === selectedWarehouse.value);
      }
      
      // Filter by search query if provided
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase();
        result = result.filter(item => 
          item.product.name.toLowerCase().includes(query) || 
          item.product.code.toLowerCase().includes(query)
        );
      }
      
      inventory.value = result;
      loading.value = false;
    }, 500);
  } catch (error) {
    console.error('Error fetching inventory:', error);
  }
};

const getWarehouses = async () => {
  try {
    // Replace with actual API call
    // const response = await axios.get('http://localhost:8000/api/inventory/warehouses/');
    // warehouses.value = response.data.results;
    
    // Using mock data for now
    warehouses.value = mockWarehouses;
    if (warehouses.value.length > 0) {
      selectedWarehouse.value = warehouses.value[0].id;
    }
  } catch (error) {
    console.error('Error fetching warehouses:', error);
  }
};

const getStatusColor = (quantity) => {
  if (quantity <= 5) return 'error';
  if (quantity <= 10) return 'warning';
  return 'success';
};

const getStatusLabel = (quantity) => {
  if (quantity <= 5) return 'بحرانی';
  if (quantity <= 10) return 'کم';
  return 'موجود';
};

const getTransactionTypeColor = (type) => {
  switch(type) {
    case 'IN': return 'success';
    case 'OUT': return 'error';
    case 'ADJUST': return 'warning';
    case 'TRANSFER': return 'info';
    default: return 'grey';
  }
};

const getTransactionTypeLabel = (type) => {
  switch(type) {
    case 'IN': return 'ورود به انبار';
    case 'OUT': return 'خروج از انبار';
    case 'ADJUST': return 'تنظیم موجودی';
    case 'TRANSFER': return 'انتقال بین انبارها';
    default: return 'نامشخص';
  }
};

const adjustInventory = (item) => {
  selectedProduct.value = item;
  adjustForm.value = {
    product_id: item.product.id,
    product_name: item.product.name,
    current_quantity: item.quantity,
    new_quantity: item.quantity,
    reason: '',
    notes: ''
  };
  adjustDialog.value = true;
};

const saveAdjustment = async () => {
  try {
    // Replace with actual API call
    // await axios.post('http://localhost:8000/api/inventory/adjustments/', {
    //   product: adjustForm.value.product_id,
    //   warehouse: selectedWarehouse.value,
    //   quantity: adjustForm.value.new_quantity,
    //   reason: adjustForm.value.reason,
    //   notes: adjustForm.value.notes
    // });
    
    // Using mock update for now
    const index = inventory.value.findIndex(i => i.id === selectedProduct.value.id);
    if (index !== -1) {
      inventory.value[index].quantity = adjustForm.value.new_quantity;
    }
    
    // Close dialog and reset form
    adjustDialog.value = false;
    
    // Show success message
  } catch (error) {
    console.error('Error saving adjustment:', error);
    // Show error message
  }
};

const showHistory = (item) => {
  selectedProduct.value = item;
  // Replace with actual API call
  // const response = await axios.get(`http://localhost:8000/api/inventory/transactions/`, {
  //   params: {
  //     product: item.product.id,
  //     warehouse: selectedWarehouse.value
  //   }
  // });
  // transactionHistory.value = response.data.results;
  
  // Using mock data for now
  transactionHistory.value = mockTransactionHistory;
  historyDialog.value = true;
};

// Lifecycle hooks
onMounted(async () => {
  await getWarehouses();
  await getInventory();
});
</script> 