<template>
  <div>
    <div class="d-flex justify-space-between align-center mb-6">
      <h1 class="text-h4">مدیریت خرید</h1>
      <v-btn color="primary" prepend-icon="mdi-plus">
        ثبت خرید جدید
      </v-btn>
    </div>

    <!-- Filters -->
    <v-card class="mb-6">
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="6" md="3">
            <v-text-field
              v-model="filters.search"
              label="جستجو"
              variant="outlined"
              density="compact"
              prepend-inner-icon="mdi-magnify"
              clearable
              @input="getPurchases"
              hint="شماره سند، نام تامین‌کننده یا شماره تلفن"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-select
              v-model="filters.status"
              label="وضعیت"
              variant="outlined"
              density="compact"
              :items="statusOptions"
              clearable
              @update:model-value="getPurchases"
            ></v-select>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-menu
              v-model="menu1"
              :close-on-content-click="false"
              location="bottom"
            >
              <template v-slot:activator="{ props }">
                <v-text-field
                  v-model="filters.date_from_display"
                  label="از تاریخ"
                  variant="outlined"
                  density="compact"
                  readonly
                  v-bind="props"
                  prepend-inner-icon="mdi-calendar"
                  clearable
                  @click:clear="filters.date_from = null; filters.date_from_display = ''"
                ></v-text-field>
              </template>
              <!-- Replace with a Persian date picker component -->
              <v-date-picker
                v-model="filters.date_from"
                @update:model-value="updateDateFromDisplay"
                @cancel="menu1 = false"
              ></v-date-picker>
            </v-menu>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-menu
              v-model="menu2"
              :close-on-content-click="false"
              location="bottom"
            >
              <template v-slot:activator="{ props }">
                <v-text-field
                  v-model="filters.date_to_display"
                  label="تا تاریخ"
                  variant="outlined"
                  density="compact"
                  readonly
                  v-bind="props"
                  prepend-inner-icon="mdi-calendar"
                  clearable
                  @click:clear="filters.date_to = null; filters.date_to_display = ''"
                ></v-text-field>
              </template>
              <!-- Replace with a Persian date picker component -->
              <v-date-picker
                v-model="filters.date_to"
                @update:model-value="updateDateToDisplay"
                @cancel="menu2 = false"
              ></v-date-picker>
            </v-menu>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" class="text-center">
            <v-btn color="primary" variant="tonal" @click="getPurchases" class="mx-2">
              اعمال فیلتر
            </v-btn>
            <v-btn color="error" variant="text" @click="resetFilters" class="mx-2">
              حذف فیلتر‌ها
            </v-btn>
            <v-btn color="success" prepend-icon="mdi-file-excel" variant="text" class="mx-2">
              خروجی اکسل
            </v-btn>
            <v-btn color="info" prepend-icon="mdi-printer" variant="text" class="mx-2">
              چاپ لیست
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Purchases Table -->
    <v-card>
      <v-data-table
        :headers="headers"
        :items="purchases"
        :loading="loading"
        :items-per-page="10"
        :items-per-page-options="[10, 20, 50]"
        density="compact"
        class="elevation-1"
      >
        <!-- Reference number column -->
        <template v-slot:item.reference_number="{ item }">
          <div class="font-weight-bold">
            <v-btn variant="text" color="primary" @click="viewPurchaseDetails(item)">
              {{ item.reference_number }}
            </v-btn>
          </div>
        </template>

        <!-- Supplier column -->
        <template v-slot:item.supplier.name="{ item }">
          <div>{{ item.supplier.name }}</div>
          <div class="text-caption">{{ item.supplier.phone_number }}</div>
        </template>

        <!-- Total amount column -->
        <template v-slot:item.total_amount="{ item }">
          <div class="font-weight-bold">{{ item.total_amount.toLocaleString() }} تومان</div>
        </template>

        <!-- Status column -->
        <template v-slot:item.status="{ item }">
          <v-chip
            :color="getStatusColor(item.status)"
            size="small"
          >
            {{ getStatusLabel(item.status) }}
          </v-chip>
        </template>

        <!-- Actions column -->
        <template v-slot:item.actions="{ item }">
          <v-tooltip text="مشاهده جزئیات">
            <template v-slot:activator="{ props }">
              <v-icon 
                size="small" 
                class="me-2"
                v-bind="props"
                @click="viewPurchaseDetails(item)"
              >
                mdi-eye
              </v-icon>
            </template>
          </v-tooltip>
          <v-tooltip text="چاپ سند">
            <template v-slot:activator="{ props }">
              <v-icon 
                size="small" 
                class="me-2"
                v-bind="props"
                @click="printDocument(item)"
              >
                mdi-printer
              </v-icon>
            </template>
          </v-tooltip>
          <v-tooltip text="ویرایش">
            <template v-slot:activator="{ props }">
              <v-icon 
                size="small" 
                class="me-2"
                v-bind="props"
                @click="editPurchase(item)"
              >
                mdi-pencil
              </v-icon>
            </template>
          </v-tooltip>
          <v-tooltip text="حذف سند">
            <template v-slot:activator="{ props }">
              <v-icon 
                size="small" 
                color="error"
                v-bind="props"
                @click="confirmDelete(item)"
              >
                mdi-delete
              </v-icon>
            </template>
          </v-tooltip>
        </template>
      </v-data-table>
    </v-card>

    <!-- Purchase Details Dialog -->
    <v-dialog v-model="detailsDialog" max-width="900px">
      <v-card>
        <v-card-title class="text-h5">
          جزئیات خرید {{ selectedPurchase?.reference_number }}
          <v-spacer></v-spacer>
          <v-chip :color="getStatusColor(selectedPurchase?.status)" class="ma-2">
            {{ getStatusLabel(selectedPurchase?.status) }}
          </v-chip>
        </v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12" md="6">
              <p><strong>تامین‌کننده:</strong> {{ selectedPurchase?.supplier?.name }}</p>
              <p><strong>شماره تماس:</strong> {{ selectedPurchase?.supplier?.phone_number }}</p>
              <p><strong>تاریخ:</strong> {{ selectedPurchase?.date }}</p>
            </v-col>
            <v-col cols="12" md="6">
              <p><strong>ثبت‌کننده:</strong> {{ selectedPurchase?.created_by }}</p>
              <p><strong>روش پرداخت:</strong> {{ getPaymentMethodLabel(selectedPurchase?.payment_method) }}</p>
              <p><strong>توضیحات:</strong> {{ selectedPurchase?.notes || 'بدون توضیحات' }}</p>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>
          
          <h3 class="text-subtitle-1 mb-2">اقلام خرید</h3>
          <v-table>
            <thead>
              <tr>
                <th>کد محصول</th>
                <th>نام محصول</th>
                <th>تعداد</th>
                <th>قیمت واحد</th>
                <th>تخفیف</th>
                <th>قیمت کل</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in selectedPurchase?.items" :key="item.id">
                <td>{{ item.product.code }}</td>
                <td>{{ item.product.name }}</td>
                <td>{{ item.quantity }} {{ item.product.unit.name }}</td>
                <td>{{ item.unit_price.toLocaleString() }}</td>
                <td>{{ item.discount || 0 }}%</td>
                <td>{{ item.total_price.toLocaleString() }}</td>
              </tr>
            </tbody>
          </v-table>

          <v-divider class="my-4"></v-divider>

          <v-row class="text-right">
            <v-col cols="12" md="6" offset-md="6">
              <div class="d-flex justify-space-between mb-2">
                <span>جمع کل:</span>
                <span>{{ selectedPurchase?.subtotal.toLocaleString() }} تومان</span>
              </div>
              <div class="d-flex justify-space-between mb-2">
                <span>تخفیف:</span>
                <span>{{ selectedPurchase?.discount.toLocaleString() }} تومان</span>
              </div>
              <div class="d-flex justify-space-between mb-2">
                <span>مالیات ({{ selectedPurchase?.tax_percent }}%):</span>
                <span>{{ selectedPurchase?.tax_amount.toLocaleString() }} تومان</span>
              </div>
              <v-divider class="my-2"></v-divider>
              <div class="d-flex justify-space-between text-h6">
                <span>مبلغ قابل پرداخت:</span>
                <span>{{ selectedPurchase?.total_amount.toLocaleString() }} تومان</span>
              </div>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-btn color="info" prepend-icon="mdi-printer" @click="printDocument(selectedPurchase)">
            چاپ سند
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="detailsDialog = false">بستن</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">حذف سند خرید</v-card-title>
        <v-card-text>
          آیا از حذف این سند خرید اطمینان دارید؟ این عمل قابل بازگشت نیست.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="text" @click="deleteDialog = false">انصراف</v-btn>
          <v-btn color="error" variant="elevated" @click="deletePurchase">حذف</v-btn>
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
  { title: 'شماره سند', key: 'reference_number', sortable: true, align: 'start' },
  { title: 'تامین‌کننده', key: 'supplier.name', sortable: true, align: 'start' },
  { title: 'تاریخ', key: 'date', sortable: true, align: 'center' },
  { title: 'مبلغ کل', key: 'total_amount', sortable: true, align: 'end' },
  { title: 'روش پرداخت', key: 'payment_method', sortable: true, align: 'center' },
  { title: 'وضعیت', key: 'status', sortable: true, align: 'center' },
  { title: 'عملیات', key: 'actions', sortable: false, align: 'center' }
];

// Data
const purchases = ref([]);
const loading = ref(false);
const detailsDialog = ref(false);
const deleteDialog = ref(false);
const selectedPurchase = ref(null);
const menu1 = ref(false);
const menu2 = ref(false);

// Filters
const filters = ref({
  search: '',
  status: null,
  date_from: null,
  date_to: null,
  date_from_display: '',
  date_to_display: ''
});

// Status options
const statusOptions = [
  { title: 'پرداخت شده', value: 'PAID' },
  { title: 'در انتظار پرداخت', value: 'PENDING' },
  { title: 'لغو شده', value: 'CANCELLED' }
];

// Mock data - Replace with API call
const mockPurchases = [
  { 
    id: 1, 
    reference_number: 'PO-1001', 
    supplier: { 
      id: 1, 
      name: 'شرکت فروش یراق میلاد', 
      phone_number: '09121234567' 
    }, 
    date: '۱۴۰۳/۰۲/۱۵', 
    subtotal: 3200000,
    discount: 200000,
    tax_percent: 9,
    tax_amount: 270000,
    total_amount: 3270000, 
    payment_method: 'TRANSFER', 
    status: 'PAID',
    notes: 'تحویل در محل انبار',
    created_by: 'علی محمدی',
    items: [
      {
        id: 1,
        product: {
          id: 1,
          code: 'HDL-G102',
          name: 'دستگیره کابینت مدل G102',
          unit: { id: 1, name: 'عدد' }
        },
        quantity: 20,
        unit_price: 100000,
        discount: 10,
        total_price: 1800000
      },
      {
        id: 2,
        product: {
          id: 2,
          code: 'HNG-S220',
          name: 'لولا آرام بند',
          unit: { id: 1, name: 'عدد' }
        },
        quantity: 20,
        unit_price: 70000,
        discount: 5,
        total_price: 1330000
      }
    ]
  },
  { 
    id: 2, 
    reference_number: 'PO-1002', 
    supplier: { 
      id: 2, 
      name: 'شرکت یراق آلات تهران', 
      phone_number: '09131234567' 
    }, 
    date: '۱۴۰۳/۰۲/۱۸', 
    subtotal: 4500000,
    discount: 300000,
    tax_percent: 9,
    tax_amount: 378000,
    total_amount: 4578000, 
    payment_method: 'CHEQUE', 
    status: 'PENDING',
    notes: 'چک به تاریخ ۱۴۰۳/۰۳/۲۵',
    created_by: 'رضا رضایی',
    items: [
      {
        id: 3,
        product: {
          id: 3,
          code: 'RIL-T050',
          name: 'ریل کشو تاندم ۵۰ سانتی',
          unit: { id: 3, name: 'جفت' }
        },
        quantity: 15,
        unit_price: 300000,
        discount: 10,
        total_price: 4050000
      }
    ]
  },
  { 
    id: 3, 
    reference_number: 'PO-1003', 
    supplier: { 
      id: 3, 
      name: 'فروشگاه لوازم ساختمانی مجتبی', 
      phone_number: '09141234567' 
    }, 
    date: '۱۴۰۳/۰۲/۲۰', 
    subtotal: 1800000,
    discount: 0,
    tax_percent: 9,
    tax_amount: 162000,
    total_amount: 1962000, 
    payment_method: 'CASH', 
    status: 'PAID',
    notes: '',
    created_by: 'علی محمدی',
    items: [
      {
        id: 4,
        product: {
          id: 4,
          code: 'LEG-S120',
          name: 'پایه کابینت استیل',
          unit: { id: 1, name: 'عدد' }
        },
        quantity: 40,
        unit_price: 45000,
        discount: 0,
        total_price: 1800000
      }
    ]
  },
  { 
    id: 4, 
    reference_number: 'PO-1004', 
    supplier: { 
      id: 4, 
      name: 'شرکت بازرگانی آراد', 
      phone_number: '09151234567' 
    }, 
    date: '۱۴۰۳/۰۲/۲۲', 
    subtotal: 5400000,
    discount: 400000,
    tax_percent: 9,
    tax_amount: 450000,
    total_amount: 5450000, 
    payment_method: 'TRANSFER', 
    status: 'PAID',
    notes: 'تحویل محموله طی سه روز آینده',
    created_by: 'رضا رضایی',
    items: [
      {
        id: 5,
        product: {
          id: 5,
          code: 'LCK-K85',
          name: 'قفل درب سوئیچی',
          unit: { id: 1, name: 'عدد' }
        },
        quantity: 30,
        unit_price: 150000,
        discount: 10,
        total_price: 4050000
      },
      {
        id: 6,
        product: {
          id: 1,
          code: 'HDL-G102',
          name: 'دستگیره کابینت مدل G102',
          unit: { id: 1, name: 'عدد' }
        },
        quantity: 15,
        unit_price: 100000,
        discount: 5,
        total_price: 1425000
      }
    ]
  },
  { 
    id: 5, 
    reference_number: 'PO-1005', 
    supplier: { 
      id: 1, 
      name: 'شرکت فروش یراق میلاد', 
      phone_number: '09121234567' 
    }, 
    date: '۱۴۰۳/۰۲/۲۳', 
    subtotal: 2600000,
    discount: 100000,
    tax_percent: 9,
    tax_amount: 225000,
    total_amount: 2725000, 
    payment_method: 'CASH', 
    status: 'CANCELLED',
    notes: 'لغو به دلیل مشکل در تامین محصول',
    created_by: 'علی محمدی',
    items: [
      {
        id: 7,
        product: {
          id: 2,
          code: 'HNG-S220',
          name: 'لولا آرام بند',
          unit: { id: 1, name: 'عدد' }
        },
        quantity: 30,
        unit_price: 70000,
        discount: 5,
        total_price: 1995000
      },
      {
        id: 8,
        product: {
          id: 4,
          code: 'LEG-S120',
          name: 'پایه کابینت استیل',
          unit: { id: 1, name: 'عدد' }
        },
        quantity: 15,
        unit_price: 40000,
        discount: 0,
        total_price: 600000
      }
    ]
  }
];

// Methods
const getPurchases = async () => {
  loading.value = true;
  
  try {
    // Replace with actual API call
    // const response = await axios.get('http://localhost:8000/api/purchases/purchases/', { 
    //   params: {
    //     search: filters.value.search,
    //     status: filters.value.status,
    //     date_from: filters.value.date_from,
    //     date_to: filters.value.date_to
    //   }
    // });
    // purchases.value = response.data.results;
    
    // Using mock data for now
    setTimeout(() => {
      // Filter by search query if provided
      let result = [...mockPurchases];
      
      if (filters.value.search) {
        const query = filters.value.search.toLowerCase();
        result = result.filter(item => 
          item.reference_number.toLowerCase().includes(query) || 
          item.supplier.name.toLowerCase().includes(query) ||
          item.supplier.phone_number.includes(query)
        );
      }
      
      // Filter by status if selected
      if (filters.value.status) {
        result = result.filter(item => item.status === filters.value.status);
      }
      
      // Date filters would be handled on the server side in a real implementation
      
      purchases.value = result;
      loading.value = false;
    }, 500);
  } catch (error) {
    console.error('Error fetching purchases:', error);
  }
};

const resetFilters = () => {
  filters.value = {
    search: '',
    status: null,
    date_from: null,
    date_to: null,
    date_from_display: '',
    date_to_display: ''
  };
  getPurchases();
};

const updateDateFromDisplay = (date) => {
  // Convert Gregorian date to Persian date (in a real app you would use a Persian calendar library)
  filters.value.date_from_display = date; // This would be converted to Persian format
  menu1.value = false;
};

const updateDateToDisplay = (date) => {
  // Convert Gregorian date to Persian date (in a real app you would use a Persian calendar library)
  filters.value.date_to_display = date; // This would be converted to Persian format
  menu2.value = false;
};

const getStatusColor = (status) => {
  switch(status) {
    case 'PAID': return 'success';
    case 'PENDING': return 'warning';
    case 'CANCELLED': return 'error';
    default: return 'grey';
  }
};

const getStatusLabel = (status) => {
  switch(status) {
    case 'PAID': return 'پرداخت شده';
    case 'PENDING': return 'در انتظار پرداخت';
    case 'CANCELLED': return 'لغو شده';
    default: return 'نامشخص';
  }
};

const getPaymentMethodLabel = (method) => {
  switch(method) {
    case 'CASH': return 'نقدی';
    case 'CARD': return 'کارت بانکی';
    case 'TRANSFER': return 'انتقال بانکی';
    case 'CHEQUE': return 'چک';
    default: return 'نامشخص';
  }
};

const viewPurchaseDetails = (purchase) => {
  selectedPurchase.value = purchase;
  detailsDialog.value = true;
};

const editPurchase = (purchase) => {
  // Navigate to edit purchase page or open edit dialog
  console.log('Edit purchase:', purchase);
};

const confirmDelete = (purchase) => {
  selectedPurchase.value = purchase;
  deleteDialog.value = true;
};

const deletePurchase = async () => {
  try {
    // Replace with actual API call
    // await axios.delete(`http://localhost:8000/api/purchases/purchases/${selectedPurchase.value.id}/`);
    
    // Using mock deletion for now
    purchases.value = purchases.value.filter(p => p.id !== selectedPurchase.value.id);
    deleteDialog.value = false;
    // Show success message
  } catch (error) {
    console.error('Error deleting purchase:', error);
    // Show error message
  }
};

const printDocument = (purchase) => {
  // In a real application, this would open a print dialog or generate a PDF
  console.log('Print document for purchase:', purchase);
  alert('چاپ سند خرید: ' + purchase.reference_number);
};

// Lifecycle hooks
onMounted(() => {
  getPurchases();
});
</script> 