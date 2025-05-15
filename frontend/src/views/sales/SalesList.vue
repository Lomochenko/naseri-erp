<template>
  <div>
    <v-card class="mb-6">
      <v-card-title class="d-flex align-center justify-space-between flex-wrap">
        <span class="text-h5">مدیریت فروش</span>
        <v-btn 
          color="primary" 
          prepend-icon="mdi-cart-plus" 
          variant="elevated"
          to="/sales/new"
        >
          فروش جدید
        </v-btn>
      </v-card-title>

      <v-card-text>
        <v-row>
          <!-- فیلترهای جستجو -->
          <v-col cols="12" md="3">
            <v-text-field
              v-model="filters.search"
              label="جستجو در فاکتورها"
              variant="outlined"
              density="compact"
              prepend-inner-icon="mdi-magnify"
              hide-details
              @update:model-value="applyFilters"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="3">
            <v-select
              v-model="filters.status"
              :items="statusOptions"
              item-title="title"
              item-value="value"
              label="وضعیت فاکتور"
              variant="outlined"
              density="compact"
              hide-details
              clearable
              @update:model-value="applyFilters"
            ></v-select>
          </v-col>

          <v-col cols="12" md="3">
            <v-menu
              ref="menuFrom"
              v-model="dateMenuFrom"
              :close-on-content-click="false"
              location="bottom"
              min-width="auto"
              transition="scale-transition"
            >
              <template v-slot:activator="{ props }">
                <v-text-field
                  v-model="filters.date_from"
                  label="از تاریخ"
                  variant="outlined"
                  density="compact"
                  hide-details
                  readonly
                  prepend-inner-icon="mdi-calendar"
                  v-bind="props"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="filters.date_from"
                @update:model-value="dateMenuFrom = false; applyFilters()"
              ></v-date-picker>
            </v-menu>
          </v-col>

          <v-col cols="12" md="3">
            <v-menu
              ref="menuTo"
              v-model="dateMenuTo"
              :close-on-content-click="false"
              location="bottom"
              min-width="auto"
              transition="scale-transition"
            >
              <template v-slot:activator="{ props }">
                <v-text-field
                  v-model="filters.date_to"
                  label="تا تاریخ"
                  variant="outlined"
                  density="compact"
                  hide-details
                  readonly
                  prepend-inner-icon="mdi-calendar"
                  v-bind="props"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="filters.date_to"
                @update:model-value="dateMenuTo = false; applyFilters()"
              ></v-date-picker>
            </v-menu>
          </v-col>
        </v-row>

        <v-row class="mt-2">
          <v-col cols="12" md="3">
            <v-select
              v-model="filters.customer"
              :items="customers"
              item-title="name"
              item-value="id"
              label="مشتری"
              variant="outlined"
              density="compact"
              hide-details
              clearable
              return-object
              @update:model-value="applyFilters"
            ></v-select>
          </v-col>

          <v-col cols="12" md="6">
            <v-slider
              v-model="filters.amount_range"
              label="محدوده مبلغ (تومان)"
              min="0"
              max="50000000"
              step="1000000"
              hide-details
              density="compact"
              thumb-label="always"
              :format-value="formatPrice"
            >
              <template v-slot:prepend>
                <v-text-field
                  v-model="filters.amount_range[0]"
                  type="number"
                  style="width: 100px"
                  variant="outlined"
                  density="compact"
                  hide-details
                  @update:model-value="applyFilters"
                ></v-text-field>
              </template>
              <template v-slot:append>
                <v-text-field
                  v-model="filters.amount_range[1]"
                  type="number"
                  style="width: 100px"
                  variant="outlined"
                  density="compact"
                  hide-details
                  @update:model-value="applyFilters"
                ></v-text-field>
              </template>
            </v-slider>
          </v-col>

          <v-col cols="12" md="3" class="d-flex justify-end align-center">
            <v-btn 
              color="secondary" 
              variant="text" 
              prepend-icon="mdi-refresh"
              @click="resetFilters"
            >
              بازنشانی فیلترها
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- جدول نمایش فروش‌ها -->
    <v-card variant="outlined">
      <v-data-table
        :headers="headers"
        :items="sales"
        :loading="loading"
        :items-per-page="itemsPerPage"
        :page="page"
        :server-items-length="totalItems"
        class="elevation-0 rtl-table"
        hover
        @update:options="handleOptions"
      >
        <!-- لودینگ -->
        <template v-slot:loader>
          <v-progress-linear indeterminate color="primary"></v-progress-linear>
        </template>

        <!-- شماره فاکتور -->
        <template v-slot:item.invoice_number="{ item }">
          <div class="font-weight-medium">{{ item.invoice_number }}</div>
          <div class="text-caption text-medium-emphasis">{{ formatDate(item.created_at) }}</div>
        </template>

        <!-- مشتری -->
        <template v-slot:item.customer="{ item }">
          <div>{{ item.customer?.name || 'فروش متفرقه' }}</div>
          <div v-if="item.customer?.phone" class="text-caption text-medium-emphasis">{{ item.customer.phone }}</div>
        </template>

        <!-- تعداد اقلام -->
        <template v-slot:item.items_count="{ item }">
          <v-chip size="small" color="info" variant="flat">{{ item.items.length }} قلم</v-chip>
        </template>

        <!-- مبلغ کل -->
        <template v-slot:item.total_amount="{ item }">
          <div class="font-weight-medium">{{ formatPrice(item.total_amount) }}</div>
          <div class="text-caption" :class="getPaymentClass(item)">
            {{ getPaymentStatus(item) }}
          </div>
        </template>

        <!-- وضعیت -->
        <template v-slot:item.status="{ item }">
          <v-chip :color="getStatusColor(item.status)" size="small" variant="flat">
            {{ getStatusText(item.status) }}
          </v-chip>
        </template>

        <!-- نمایش دکمه‌های عملیات -->
        <template v-slot:item.actions="{ item }">
          <div class="d-flex justify-end">
            <v-btn
              icon="mdi-eye"
              size="small"
              variant="text"
              color="info"
              class="ml-1"
              @click="viewSale(item)"
            ></v-btn>
            <v-btn
              icon="mdi-receipt"
              size="small"
              variant="text"
              color="primary"
              class="ml-1"
              @click="printInvoice(item)"
            ></v-btn>
            <v-btn
              icon="mdi-delete"
              size="small"
              variant="text"
              color="error"
              @click="confirmDelete(item)"
              v-if="canDelete(item)"
            ></v-btn>
          </div>
        </template>

        <!-- نمایش در حالت خالی بودن لیست -->
        <template v-slot:no-data>
          <div class="text-center pa-5">
            <v-icon size="large" icon="mdi-cart-off" color="secondary" class="mb-3"></v-icon>
            <div>فاکتور فروشی یافت نشد</div>
            <v-btn 
              variant="text" 
              color="primary" 
              class="mt-3" 
              @click="loadSales"
            >
              تلاش مجدد
            </v-btn>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <!-- دیالوگ جزئیات فروش -->
    <v-dialog v-model="detailDialog" max-width="800px">
      <v-card v-if="selectedSale">
        <v-card-title class="text-h5 d-flex justify-space-between">
          <span>جزئیات فاکتور {{ selectedSale.invoice_number }}</span>
          <v-chip :color="getStatusColor(selectedSale.status)" size="small">
            {{ getStatusText(selectedSale.status) }}
          </v-chip>
        </v-card-title>

        <v-card-text>
          <v-row>
            <v-col cols="12" sm="6">
              <v-list density="compact">
                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-account"></v-icon>
                  </template>
                  <v-list-item-title>نام مشتری:</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedSale.customer?.name || 'فروش متفرقه' }}</v-list-item-subtitle>
                </v-list-item>

                <v-list-item v-if="selectedSale.customer?.phone">
                  <template v-slot:prepend>
                    <v-icon icon="mdi-phone"></v-icon>
                  </template>
                  <v-list-item-title>شماره تماس:</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedSale.customer.phone }}</v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-calendar"></v-icon>
                  </template>
                  <v-list-item-title>تاریخ فاکتور:</v-list-item-title>
                  <v-list-item-subtitle>{{ formatDate(selectedSale.created_at) }}</v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-col>

            <v-col cols="12" sm="6">
              <v-list density="compact">
                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-cash-multiple"></v-icon>
                  </template>
                  <v-list-item-title>مبلغ کل:</v-list-item-title>
                  <v-list-item-subtitle>{{ formatPrice(selectedSale.total_amount) }}</v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-cash-check"></v-icon>
                  </template>
                  <v-list-item-title>مبلغ پرداخت شده:</v-list-item-title>
                  <v-list-item-subtitle>{{ formatPrice(selectedSale.paid_amount || 0) }}</v-list-item-subtitle>
                </v-list-item>

                <v-list-item v-if="selectedSale.total_amount > (selectedSale.paid_amount || 0)">
                  <template v-slot:prepend>
                    <v-icon icon="mdi-cash-remove"></v-icon>
                  </template>
                  <v-list-item-title>مانده حساب:</v-list-item-title>
                  <v-list-item-subtitle class="text-error">
                    {{ formatPrice(selectedSale.total_amount - (selectedSale.paid_amount || 0)) }}
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-col>
          </v-row>

          <v-divider class="my-3"></v-divider>

          <h3 class="text-h6 mb-3">اقلام فاکتور</h3>
          <v-table>
            <thead>
              <tr>
                <th>ردیف</th>
                <th>نام محصول</th>
                <th>تعداد</th>
                <th>قیمت واحد</th>
                <th>مبلغ کل</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in selectedSale.items" :key="index">
                <td>{{ index + 1 }}</td>
                <td>
                  <div>{{ item.product.name }}</div>
                  <div class="text-caption">کد: {{ item.product.code }}</div>
                </td>
                <td>{{ item.quantity }} {{ item.product.unit_symbol }}</td>
                <td>{{ formatPrice(item.unit_price) }}</td>
                <td>{{ formatPrice(item.total_price) }}</td>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                <td colspan="4" class="text-right font-weight-bold">جمع کل:</td>
                <td class="font-weight-bold">{{ formatPrice(selectedSale.total_amount) }}</td>
              </tr>
            </tfoot>
          </v-table>

          <v-divider class="my-3"></v-divider>

          <h3 class="text-h6 mb-3">توضیحات</h3>
          <p v-if="selectedSale.notes">{{ selectedSale.notes }}</p>
          <p v-else class="text-medium-emphasis">بدون توضیحات</p>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="text" @click="detailDialog = false">
            بستن
          </v-btn>
          <v-btn
            color="info"
            variant="elevated"
            prepend-icon="mdi-receipt"
            @click="printInvoice(selectedSale)"
          >
            چاپ فاکتور
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- دیالوگ حذف فاکتور -->
    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title class="text-h5">حذف فاکتور</v-card-title>
        <v-card-text>
          آیا از حذف فاکتور <strong>{{ deleteItem?.invoice_number }}</strong> اطمینان دارید؟
          <div class="text-caption text-medium-emphasis mt-2">
            این عملیات غیرقابل بازگشت است و تمام اطلاعات مربوط به این فاکتور حذف خواهد شد.
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" variant="text" @click="deleteDialog = false">انصراف</v-btn>
          <v-btn 
            color="error" 
            variant="elevated" 
            @click="deleteSale" 
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
import { useSalesStore } from '../../store/sales';
import { useCustomersStore } from '../../store/customers';

// استورها
const salesStore = useSalesStore();
const customersStore = useCustomersStore();

// ثابت‌های نمایش
const headers = [
  { title: 'شماره فاکتور', key: 'invoice_number', align: 'start', sortable: true },
  { title: 'مشتری', key: 'customer', align: 'start', sortable: false },
  { title: 'تعداد اقلام', key: 'items_count', align: 'center', sortable: false },
  { title: 'مبلغ کل (تومان)', key: 'total_amount', align: 'center', sortable: true },
  { title: 'وضعیت', key: 'status', align: 'center', sortable: true },
  { title: 'عملیات', key: 'actions', align: 'center', sortable: false },
];

const statusOptions = [
  { title: 'همه', value: null },
  { title: 'در انتظار پرداخت', value: 'pending' },
  { title: 'پرداخت شده', value: 'paid' },
  { title: 'نیمه پرداخت', value: 'partially_paid' },
  { title: 'تحویل شده', value: 'delivered' },
  { title: 'لغو شده', value: 'cancelled' }
];

// متغیرهای واکنش‌پذیر
const detailDialog = ref(false);
const deleteDialog = ref(false);
const selectedSale = ref(null);
const deleteItem = ref(null);
const dateMenuFrom = ref(false);
const dateMenuTo = ref(false);
const page = ref(1);
const itemsPerPage = ref(10);

// فیلترها
const filters = ref({
  search: '',
  status: null,
  customer: null,
  date_from: '',
  date_to: '',
  amount_range: [0, 50000000]
});

// دریافت داده‌ها از استور
const loading = computed(() => salesStore.loading);
const sales = computed(() => salesStore.sales);
const customers = computed(() => customersStore.customers);
const totalItems = computed(() => salesStore.totalItems);

// فرمت‌کننده قیمت
const formatPrice = (price) => {
  return new Intl.NumberFormat('fa-IR').format(price);
};

// فرمت‌کننده تاریخ
const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(date);
};

// وضعیت فاکتور
const getStatusText = (status) => {
  switch (status) {
    case 'pending': return 'در انتظار پرداخت';
    case 'paid': return 'پرداخت شده';
    case 'partially_paid': return 'نیمه پرداخت';
    case 'delivered': return 'تحویل شده';
    case 'cancelled': return 'لغو شده';
    default: return 'نامشخص';
  }
};

const getStatusColor = (status) => {
  switch (status) {
    case 'pending': return 'warning';
    case 'paid': return 'success';
    case 'partially_paid': return 'info';
    case 'delivered': return 'primary';
    case 'cancelled': return 'error';
    default: return 'grey';
  }
};

// وضعیت پرداخت
const getPaymentStatus = (sale) => {
  if (!sale.paid_amount) return 'پرداخت نشده';
  if (sale.paid_amount >= sale.total_amount) return 'پرداخت کامل';
  return `پرداخت ${Math.round((sale.paid_amount / sale.total_amount) * 100)}%`;
};

const getPaymentClass = (sale) => {
  if (!sale.paid_amount) return 'text-error';
  if (sale.paid_amount >= sale.total_amount) return 'text-success';
  return 'text-warning';
};

// آیا این فاکتور قابل حذف است؟
const canDelete = (sale) => {
  // فقط فاکتورهای در انتظار پرداخت یا لغو شده قابل حذف هستند
  return ['pending', 'cancelled'].includes(sale.status);
};

// مدیریت فیلترها
const applyFilters = () => {
  page.value = 1;
  loadSales();
};

const resetFilters = () => {
  filters.value = {
    search: '',
    status: null,
    customer: null,
    date_from: '',
    date_to: '',
    amount_range: [0, 50000000]
  };
  page.value = 1;
  loadSales();
};

// بارگذاری فروش‌ها
const loadSales = async () => {
  // تبدیل فیلترها به پارامترهای API
  const apiParams = {
    search: filters.value.search,
    status: filters.value.status,
    customer_id: filters.value.customer?.id,
    date_from: filters.value.date_from,
    date_to: filters.value.date_to,
    amount_min: filters.value.amount_range[0],
    amount_max: filters.value.amount_range[1],
    page: page.value,
    page_size: itemsPerPage.value
  };
  
  await salesStore.fetchSales(apiParams);
};

// مدیریت گزینه‌های جدول
const handleOptions = (options) => {
  page.value = options.page;
  itemsPerPage.value = options.itemsPerPage;
  
  // تنظیم مرتب‌سازی
  const sortBy = options.sortBy.length > 0 ? options.sortBy[0] : null;
  
  if (sortBy) {
    const ordering = sortBy.order === 'desc' ? `-${sortBy.key}` : sortBy.key;
    salesStore.setSorting(ordering);
  }
  
  loadSales();
};

// مدیریت فروش‌ها
const viewSale = (sale) => {
  selectedSale.value = { ...sale };
  detailDialog.value = true;
};

const printInvoice = (sale) => {
  // در نسخه واقعی، اینجا کد پرینت فاکتور قرار می‌گیرد
  console.log('Printing invoice for sale:', sale.invoice_number);
  
  // نمونه ساده: ایجاد صفحه چاپ
  const printWindow = window.open('', '_blank');
  printWindow.document.write(`
    <html dir="rtl">
      <head>
        <title>فاکتور فروش ${sale.invoice_number}</title>
        <style>
          body { font-family: 'Vazirmatn', Tahoma, sans-serif; }
          .invoice-header { text-align: center; margin-bottom: 20px; }
          .invoice-title { font-size: 24px; }
          .invoice-meta { display: flex; justify-content: space-between; margin-bottom: 20px; }
          table { width: 100%; border-collapse: collapse; }
          th, td { border: 1px solid #ddd; padding: 8px; text-align: right; }
          th { background-color: #f2f2f2; }
          .total-row { font-weight: bold; }
          .footer { margin-top: 40px; text-align: center; color: #666; }
        </style>
      </head>
      <body>
        <div class="invoice-header">
          <h1 class="invoice-title">فاکتور فروش</h1>
          <p>فروشگاه سخت‌افزار ناصری</p>
        </div>
        
        <div class="invoice-meta">
          <div>
            <p><strong>شماره فاکتور:</strong> ${sale.invoice_number}</p>
            <p><strong>تاریخ:</strong> ${formatDate(sale.created_at)}</p>
          </div>
          <div>
            <p><strong>مشتری:</strong> ${sale.customer?.name || 'فروش متفرقه'}</p>
            <p><strong>شماره تماس:</strong> ${sale.customer?.phone || '-'}</p>
          </div>
        </div>
        
        <table>
          <thead>
            <tr>
              <th>ردیف</th>
              <th>کد محصول</th>
              <th>نام محصول</th>
              <th>تعداد</th>
              <th>قیمت واحد (تومان)</th>
              <th>جمع (تومان)</th>
            </tr>
          </thead>
          <tbody>
            ${sale.items.map((item, index) => `
              <tr>
                <td>${index + 1}</td>
                <td>${item.product.code}</td>
                <td>${item.product.name}</td>
                <td>${item.quantity} ${item.product.unit_symbol}</td>
                <td>${formatPrice(item.unit_price)}</td>
                <td>${formatPrice(item.total_price)}</td>
              </tr>
            `).join('')}
          </tbody>
          <tfoot>
            <tr class="total-row">
              <td colspan="5">مبلغ کل:</td>
              <td>${formatPrice(sale.total_amount)}</td>
            </tr>
            <tr>
              <td colspan="5">مبلغ پرداخت شده:</td>
              <td>${formatPrice(sale.paid_amount || 0)}</td>
            </tr>
            <tr>
              <td colspan="5">مانده:</td>
              <td>${formatPrice(sale.total_amount - (sale.paid_amount || 0))}</td>
            </tr>
          </tfoot>
        </table>
        
        <div class="footer">
          <p>با تشکر از خرید شما</p>
          <p>آدرس: تهران، خیابان حافظ، پلاک 123</p>
          <p>تلفن: 021-12345678</p>
        </div>
        
        <script>
          window.onload = function() { window.print(); }
        </script>
      </body>
    </html>
  `);
  printWindow.document.close();
};

const confirmDelete = (sale) => {
  deleteItem.value = sale;
  deleteDialog.value = true;
};

const deleteSale = async () => {
  if (await salesStore.deleteSale(deleteItem.value.id)) {
    deleteDialog.value = false;
    deleteItem.value = null;
  }
};

// دریافت داده‌ها در زمان بارگذاری
onMounted(async () => {
  // دریافت لیست مشتریان برای فیلتر
  if (customers.value.length === 0) {
    await customersStore.fetchCustomers();
  }
  
  await loadSales();
});
</script>

<style scoped>
.rtl-table :deep(th) {
  text-align: right;
}
</style> 