<template>
  <div>
    <!-- بخش بالایی - خوشامدگویی و کارت‌های آمار -->
    <v-row>
      <v-col cols="12">
        <v-card class="mb-4 pa-4" variant="flat" border>
          <div class="d-flex justify-space-between align-center flex-wrap">
            <div>
              <h1 class="text-h4 font-weight-bold">{{ userGreeting }}</h1>
              <p class="text-subtitle-1 text-medium-emphasis">خلاصه وضعیت فروشگاه سخت‌افزار ناصری در یک نگاه</p>
            </div>
            <div class="d-flex flex-wrap">
              <v-btn 
                prepend-icon="mdi-file-document-outline" 
                color="primary" 
                variant="tonal"
                class="ml-2 mt-2"
              >
                گزارش جدید
              </v-btn>
              <v-btn 
                prepend-icon="mdi-refresh" 
                variant="outlined" 
                class="mt-2" 
                :loading="loading"
                @click="refreshDashboard"
              >
                به‌روزرسانی
              </v-btn>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- آمارهای کلی -->
    <v-row>
      <v-col cols="12" sm="6" md="3">
        <v-card class="h-100" variant="elevated">
          <v-card-item>
            <template v-slot:prepend>
              <v-avatar color="primary" variant="flat" rounded="lg">
                <v-icon icon="mdi-cart-outline" color="white"></v-icon>
              </v-avatar>
            </template>
            <v-card-title>فروش امروز</v-card-title>
            <v-card-subtitle class="mt-2">
              <div class="text-h5 font-weight-bold">{{ formatPrice(summary.todaySales) }}</div>
              <div class="text-caption">
                <v-icon icon="mdi-arrow-up" color="success" v-if="summary.salesGrowth > 0"></v-icon>
                <v-icon icon="mdi-arrow-down" color="error" v-else-if="summary.salesGrowth < 0"></v-icon>
                <span :class="summary.salesGrowth > 0 ? 'text-success' : (summary.salesGrowth < 0 ? 'text-error' : '')">
                  {{ Math.abs(summary.salesGrowth) }}% نسبت به دیروز
                </span>
              </div>
            </v-card-subtitle>
          </v-card-item>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card class="h-100" variant="elevated">
          <v-card-item>
            <template v-slot:prepend>
              <v-avatar color="success" variant="flat" rounded="lg">
                <v-icon icon="mdi-package-variant-closed" color="white"></v-icon>
              </v-avatar>
            </template>
            <v-card-title>تعداد محصولات</v-card-title>
            <v-card-subtitle class="mt-2">
              <div class="text-h5 font-weight-bold">{{ summary.productsCount }}</div>
              <div class="text-caption">
                <span>{{ summary.lowStockCount }} محصول با موجودی کم</span>
              </div>
            </v-card-subtitle>
          </v-card-item>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card class="h-100" variant="elevated">
          <v-card-item>
            <template v-slot:prepend>
              <v-avatar color="warning" variant="flat" rounded="lg">
                <v-icon icon="mdi-account-group" color="white"></v-icon>
              </v-avatar>
            </template>
            <v-card-title>مشتریان</v-card-title>
            <v-card-subtitle class="mt-2">
              <div class="text-h5 font-weight-bold">{{ summary.customersCount }}</div>
              <div class="text-caption">
                <span>{{ summary.newCustomers }} مشتری جدید این هفته</span>
              </div>
            </v-card-subtitle>
          </v-card-item>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card class="h-100" variant="elevated">
          <v-card-item>
            <template v-slot:prepend>
              <v-avatar color="info" variant="flat" rounded="lg">
                <v-icon icon="mdi-cash-multiple" color="white"></v-icon>
              </v-avatar>
            </template>
            <v-card-title>درآمد ماهیانه</v-card-title>
            <v-card-subtitle class="mt-2">
              <div class="text-h5 font-weight-bold">{{ formatPrice(summary.monthlyRevenue) }}</div>
              <div class="text-caption">
                <v-icon icon="mdi-arrow-up" color="success" v-if="summary.revenueGrowth > 0"></v-icon>
                <v-icon icon="mdi-arrow-down" color="error" v-else-if="summary.revenueGrowth < 0"></v-icon>
                <span :class="summary.revenueGrowth > 0 ? 'text-success' : (summary.revenueGrowth < 0 ? 'text-error' : '')">
                  {{ Math.abs(summary.revenueGrowth) }}% نسبت به ماه گذشته
                </span>
              </div>
            </v-card-subtitle>
          </v-card-item>
        </v-card>
      </v-col>
    </v-row>

    <!-- نمودار فروش -->
    <v-row class="mt-4">
      <v-col cols="12" md="8">
        <v-card variant="outlined" class="h-100">
          <v-card-title class="d-flex align-center">
            <span>روند فروش</span>
            <v-spacer></v-spacer>
            <v-select
              v-model="chartPeriod"
              :items="periodOptions"
              variant="outlined"
              density="compact"
              hide-details
              class="mt-1"
              style="max-width: 150px"
            ></v-select>
          </v-card-title>
          <v-card-text class="d-flex justify-center align-center" style="height: 300px">
            <div v-if="loading">
              <v-progress-circular indeterminate color="primary"></v-progress-circular>
            </div>
            <div v-else-if="chartData.length === 0" class="text-center py-12">
              <v-icon size="64" icon="mdi-chart-line" color="grey-lighten-1" class="mb-4"></v-icon>
              <div class="text-h6 text-grey">داده‌ای برای نمایش وجود ندارد</div>
            </div>
            <div v-else style="width: 100%; height: 100%" id="sales-chart-container"></div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- فروش‌های اخیر -->
      <v-col cols="12" md="4">
        <v-card variant="outlined" class="h-100">
          <v-card-title class="d-flex align-center">
            <span>فروش‌های اخیر</span>
            <v-spacer></v-spacer>
            <v-btn 
              color="primary" 
              variant="text" 
              size="small" 
              to="/sales" 
              append-icon="mdi-arrow-left"
            >
              همه
            </v-btn>
          </v-card-title>
          <v-list v-if="!loading && recentSales.length > 0">
            <v-list-item
              v-for="sale in recentSales"
              :key="sale.id"
              :to="`/sales/${sale.id}`"
              class="mb-1"
            >
              <template v-slot:prepend>
                <v-avatar color="grey-lighten-3" size="36">
                  <v-icon :icon="getStatusIcon(sale.status)" :color="getStatusColor(sale.status)"></v-icon>
                </v-avatar>
              </template>
              <v-list-item-title>{{ sale.invoice_number }}</v-list-item-title>
              <v-list-item-subtitle>{{ formatDate(sale.date) }} - {{ sale.customer_name }}</v-list-item-subtitle>
              <template v-slot:append>
                <div class="text-right">
                  <div class="text-primary font-weight-bold">{{ formatPrice(sale.total_amount) }}</div>
                  <v-chip
                    size="x-small"
                    :color="getStatusColor(sale.status)"
                    class="mt-1"
                    variant="flat"
                  >
                    {{ getStatusText(sale.status) }}
                  </v-chip>
                </div>
              </template>
            </v-list-item>
          </v-list>

          <div v-else-if="loading" class="d-flex justify-center align-center" style="height: 300px">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
          </div>

          <div v-else class="text-center py-12">
            <v-icon size="64" icon="mdi-cart-outline" color="grey-lighten-1" class="mb-4"></v-icon>
            <div class="text-h6 text-grey">هیچ فروشی ثبت نشده است</div>
            <v-btn 
              color="primary" 
              variant="tonal" 
              class="mt-4"
              prepend-icon="mdi-plus"
              to="/sales/new"
            >
              ثبت فروش جدید
            </v-btn>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- محصولات پرفروش -->
    <v-row class="mt-4">
      <v-col cols="12" md="6">
        <v-card variant="outlined">
          <v-card-title class="d-flex align-center">
            <span>محصولات پرفروش</span>
            <v-spacer></v-spacer>
            <v-btn 
              color="primary" 
              variant="text" 
              size="small" 
              to="/products" 
              append-icon="mdi-arrow-left"
            >
              همه محصولات
            </v-btn>
          </v-card-title>
          <v-table v-if="!loading && topProducts.length > 0">
            <thead>
              <tr>
                <th>محصول</th>
                <th class="text-center">تعداد فروش</th>
                <th class="text-center">درآمد</th>
                <th class="text-center">موجودی</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="product in topProducts" :key="product.id">
                <td>
                  <div class="d-flex align-center">
                    <v-avatar size="32" rounded class="mr-2">
                      <v-img :src="product.image || '/images/no-image.png'" :alt="product.name"></v-img>
                    </v-avatar>
                    <div>
                      <div>{{ product.name }}</div>
                      <div class="text-caption text-grey">{{ product.code }}</div>
                    </div>
                  </div>
                </td>
                <td class="text-center">{{ product.sales_count }}</td>
                <td class="text-center">{{ formatPrice(product.sales_amount) }}</td>
                <td class="text-center">
                  <v-chip
                    :color="getStockColor(product.current_stock, product.min_stock)"
                    size="small"
                    variant="flat"
                  >
                    {{ product.current_stock }} {{ product.unit_symbol }}
                  </v-chip>
                </td>
              </tr>
            </tbody>
          </v-table>

          <div v-else-if="loading" class="d-flex justify-center align-center" style="height: 200px">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
          </div>

          <div v-else class="text-center py-6">
            <v-icon size="48" icon="mdi-package-variant-closed" color="grey-lighten-1" class="mb-2"></v-icon>
            <div class="text-subtitle-1 text-grey">اطلاعات محصولات پرفروش موجود نیست</div>
          </div>
        </v-card>
      </v-col>

      <!-- محصولات با موجودی کم -->
      <v-col cols="12" md="6">
        <v-card variant="outlined">
          <v-card-title class="d-flex align-center">
            <span>محصولات با موجودی کم</span>
            <v-spacer></v-spacer>
            <v-btn 
              color="primary" 
              variant="text" 
              size="small" 
              to="/inventory" 
              append-icon="mdi-arrow-left"
            >
              مدیریت موجودی
            </v-btn>
          </v-card-title>
          <v-table v-if="!loading && lowStockProducts.length > 0">
            <thead>
              <tr>
                <th>محصول</th>
                <th class="text-center">موجودی فعلی</th>
                <th class="text-center">حداقل موجودی</th>
                <th class="text-center">عملیات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="product in lowStockProducts" :key="product.id">
                <td>
                  <div class="d-flex align-center">
                    <v-avatar size="32" rounded class="mr-2">
                      <v-img :src="product.image || '/images/no-image.png'" :alt="product.name"></v-img>
                    </v-avatar>
                    <div>
                      <div>{{ product.name }}</div>
                      <div class="text-caption text-grey">{{ product.code }}</div>
                    </div>
                  </div>
                </td>
                <td class="text-center">
                  <v-chip
                    color="error"
                    size="small"
                    variant="flat"
                  >
                    {{ product.current_stock }} {{ product.unit_symbol }}
                  </v-chip>
                </td>
                <td class="text-center">{{ product.min_stock }} {{ product.unit_symbol }}</td>
                <td class="text-center">
                  <v-btn
                    icon="mdi-cart-plus"
                    size="small"
                    color="warning"
                    variant="flat"
                    to="/purchases/new"
                  ></v-btn>
                </td>
              </tr>
            </tbody>
          </v-table>

          <div v-else-if="loading" class="d-flex justify-center align-center" style="height: 200px">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
          </div>

          <div v-else class="text-center py-6">
            <v-icon size="48" icon="mdi-warehouse" color="grey-lighten-1" class="mb-2"></v-icon>
            <div class="text-subtitle-1 text-grey">تمام محصولات دارای موجودی کافی هستند</div>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useAuthStore } from '../store/auth';
import { useProductsStore } from '../store/products';
import { useSalesStore } from '../store/sales';
import { useInventoryStore } from '../store/inventory';

const authStore = useAuthStore();
const productsStore = useProductsStore();
const salesStore = useSalesStore();
const inventoryStore = useInventoryStore();
const loading = ref(true);
const lowStockProducts = ref([]);
const chartPeriod = ref('week');
const periodOptions = [
  { title: 'هفته‌ی جاری', value: 'week' },
  { title: 'ماه جاری', value: 'month' },
  { title: 'سه ماه اخیر', value: 'quarter' },
  { title: 'سال جاری', value: 'year' }
];

// دریافت داده‌های داشبورد
const refreshDashboard = async () => {
  loading.value = true;
  try {
    await productsStore.fetchProducts();
    await productsStore.fetchCategories();
    lowStockProducts.value = await productsStore.fetchLowStockProducts();
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
  } finally {
    loading.value = false;
  }
};

// اطلاعات داشبورد
const dashboardStats = computed(() => ({
  totalProducts: {
    value: productsStore.products.length > 0 ? productsStore.totalItems : 0,
    trend: '+5% از ماه گذشته',
    icon: 'mdi-package-variant-closed',
    color: 'info',
    title: 'محصولات'
  },
  totalCategories: {
    value: productsStore.categories.length,
    trend: '+2 دسته‌بندی جدید',
    icon: 'mdi-shape',
    color: 'success',
    title: 'دسته‌بندی‌ها'
  },
  lowStock: {
    value: lowStockProducts.value.length,
    trend: lowStockProducts.value.length > 0 ? 'نیاز به خرید' : 'موجودی کافی',
    icon: 'mdi-alert-circle',
    color: lowStockProducts.value.length > 0 ? 'warning' : 'success',
    title: 'کمبود موجودی'
  },
  totalSales: {
    value: 12580000,
    trend: '+12% از ماه گذشته',
    icon: 'mdi-cash-multiple',
    color: 'primary',
    title: 'فروش ماهانه'
  }
}));

// توابع کمکی برای نمایش روند
const getTrendClass = (trend) => {
  if (trend.includes('کافی') || trend.includes('+')) return 'text-success';
  if (trend.includes('نیاز') || trend.includes('-')) return 'text-warning';
  return 'text-medium-emphasis';
};

const getTrendColor = (trend) => {
  if (trend.includes('کافی') || trend.includes('+')) return 'success';
  if (trend.includes('نیاز') || trend.includes('-')) return 'warning';
  return 'medium-emphasis';
};

const getTrendIcon = (trend) => {
  if (trend.includes('کافی') || trend.includes('+')) return 'mdi-arrow-up';
  if (trend.includes('نیاز') || trend.includes('-')) return 'mdi-alert';
  return 'mdi-minus';
};

// فرمت‌کردن اعداد به فرمت پول ایران
const formatCurrency = (value) => {
  return new Intl.NumberFormat('fa-IR', {
    style: 'decimal',
    maximumFractionDigits: 0
  }).format(value) + ' تومان';
};

// محصولات پرفروش (در حالت واقعی از API دریافت می‌شود)
const topProducts = ref([
  { 
    id: 1, 
    name: 'قفل درب اصلی', 
    category: 'قفل و یراق‌آلات',
    sales: 182,
    stock: 42,
    price: 350000
  },
  { 
    id: 2, 
    name: 'دستگیره کابینت مدل گل', 
    category: 'دستگیره',
    sales: 145,
    stock: 67,
    price: 120000
  },
  { 
    id: 3, 
    name: 'لولا فنری درجه یک', 
    category: 'لولا',
    sales: 132,
    stock: 12,
    price: 85000
  },
  { 
    id: 4, 
    name: 'کلید و پریز دو خانه', 
    category: 'کلید و پریز',
    sales: 98,
    stock: 54,
    price: 65000
  }
]);

// فعالیت‌های اخیر
const recentActivities = ref([
  {
    type: 'sale',
    title: 'فروش جدید',
    description: 'سفارش جدید به مبلغ ۲,۵۰۰,۰۰۰ تومان ثبت شد',
    time: '۱۰ دقیقه پیش',
    icon: 'mdi-shopping-outline',
    color: 'success'
  },
  {
    type: 'product',
    title: 'محصول جدید',
    description: '۱۰ محصول جدید به انبار اضافه شد',
    time: '۱ ساعت پیش',
    icon: 'mdi-package-variant-plus',
    color: 'info'
  },
  {
    type: 'inventory',
    title: 'هشدار موجودی',
    description: 'موجودی "قفل سوئیچی" به حداقل رسیده است',
    time: '۳ ساعت پیش',
    icon: 'mdi-alert-circle-outline',
    color: 'warning'
  },
  {
    type: 'payment',
    title: 'پرداخت دریافت شد',
    description: 'مبلغ ۵,۸۰۰,۰۰۰ تومان از علی محمدی دریافت شد',
    time: 'دیروز',
    icon: 'mdi-bank-check',
    color: 'primary'
  }
]);

// تاریخچه فروش اخیر
const salesHistory = ref([
  { 
    id: '#INV-1001', 
    customer: 'علی محمدی',
    date: '۱۴۰۳/۰۴/۱۲',
    amount: 4850000,
    status: 'تکمیل شده',
    statusColor: 'success'
  },
  { 
    id: '#INV-1002', 
    customer: 'سارا احمدی',
    date: '۱۴۰۳/۰۴/۱۱',
    amount: 1250000,
    status: 'در انتظار پرداخت',
    statusColor: 'warning'
  },
  { 
    id: '#INV-1003', 
    customer: 'محمد رضایی',
    date: '۱۴۰۳/۰۴/۱۰',
    amount: 3640000,
    status: 'تکمیل شده',
    statusColor: 'success'
  },
  { 
    id: '#INV-1004', 
    customer: 'نازنین کریمی',
    date: '۱۴۰۳/۰۴/۱۰',
    amount: 750000,
    status: 'لغو شده',
    statusColor: 'error'
  }
]);

// اقدامات سریع
const quickActions = ref([
  { 
    title: 'ثبت فروش', 
    icon: 'mdi-shopping', 
    color: 'success',
    to: '/sales/new' 
  },
  { 
    title: 'افزودن محصول', 
    icon: 'mdi-package-variant-plus', 
    color: 'info',
    to: '/products' 
  },
  { 
    title: 'ثبت خرید', 
    icon: 'mdi-cart-plus', 
    color: 'primary',
    to: '/purchases/new' 
  },
  { 
    title: 'مشتری جدید', 
    icon: 'mdi-account-plus', 
    color: 'indigo',
    to: '/customers' 
  },
  { 
    title: 'گزارش موجودی', 
    icon: 'mdi-clipboard-list', 
    color: 'warning',
    to: '/inventory' 
  },
  { 
    title: 'گزارش مالی', 
    icon: 'mdi-chart-line', 
    color: 'deep-purple',
    to: '/reports' 
  }
]);

// نام کاربر
const userGreeting = computed(() => {
  if (authStore.user?.first_name) {
    return `سلام، ${authStore.user.first_name} عزیز!`;
  }
  return 'سلام، خوش آمدید!';
});

// داده‌های جدید
const summary = ref({
  todaySales: 1250000,
  salesGrowth: 12.5,
  productsCount: 0,
  lowStockCount: 0,
  customersCount: 45,
  newCustomers: 8,
  monthlyRevenue: 65450000,
  revenueGrowth: 8.3
});

const recentSales = ref([]);
const chartData = ref([]);

// فرمت‌کننده قیمت
const formatPrice = (price) => {
  return new Intl.NumberFormat('fa-IR').format(price);
};

// فرمت‌کننده تاریخ
const formatDate = (dateString) => {
  if (!dateString) return 'نامشخص';
  return new Date(dateString).toLocaleDateString('fa-IR');
};

// دریافت آیکون وضعیت
const getStatusIcon = (status) => {
  switch (status) {
    case 'PAID': return 'mdi-check-circle';
    case 'PENDING': return 'mdi-clock-outline';
    case 'CANCELLED': return 'mdi-cancel';
    default: return 'mdi-help-circle';
  }
};

// دریافت رنگ وضعیت
const getStatusColor = (status) => {
  switch (status) {
    case 'PAID': return 'success';
    case 'PENDING': return 'warning';
    case 'CANCELLED': return 'error';
    default: return 'grey';
  }
};

// دریافت متن وضعیت
const getStatusText = (status) => {
  switch (status) {
    case 'PAID': return 'پرداخت شده';
    case 'PENDING': return 'معلق';
    case 'CANCELLED': return 'لغو شده';
    default: return 'نامشخص';
  }
};

// تعیین رنگ برای موجودی
const getStockColor = (stock, minStock) => {
  if (stock <= 0) return 'error';
  if (stock <= minStock) return 'warning';
  return 'success';
};

// دریافت اطلاعات داشبورد
const fetchDashboardData = async () => {
  loading.value = true;
  
  try {
    // دریافت آمار فروش
    const salesData = await salesStore.fetchSaleReport({ period: chartPeriod.value });
    
    // دریافت فروش‌های اخیر
    const salesList = await salesStore.fetchSales({ 
      limit: 5, 
      sortBy: 'date',
      sortDesc: true
    });
    
    recentSales.value = salesList.results || [];
    
    // دریافت محصولات
    const productsData = await productsStore.fetchProducts();
    const products = productsData.results || [];
    
    summary.value.productsCount = products.length;
    
    // محصولات با موجودی کم
    lowStockProducts.value = products.filter(product => 
      product.current_stock <= product.min_stock
    ).slice(0, 5);
    
    summary.value.lowStockCount = products.filter(product => 
      product.current_stock <= product.min_stock
    ).length;
    
    // محصولات پرفروش (این داده‌ها باید از API دریافت شوند)
    // در اینجا برای نمونه، داده‌های جعلی استفاده می‌شوند
    topProducts.value = products.slice(0, 5).map(product => ({
      ...product,
      sales_count: Math.floor(Math.random() * 100) + 1,
      sales_amount: Math.floor(Math.random() * 10000000) + 500000
    }));
    
    // داده‌های نمودار (این داده‌ها باید از API دریافت شوند)
    chartData.value = [
      { date: '1402/01/01', sales: 1500000 },
      { date: '1402/01/02', sales: 1200000 },
      { date: '1402/01/03', sales: 1800000 },
      { date: '1402/01/04', sales: 2200000 },
      { date: '1402/01/05', sales: 1900000 },
      { date: '1402/01/06', sales: 2500000 },
      { date: '1402/01/07', sales: 3000000 }
    ];
    
    // نمایش نمودار
    setTimeout(() => {
      renderChart();
    }, 100);
    
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
  } finally {
    loading.value = false;
  }
};

// رسم نمودار (با Chart.js یا کتابخانه دیگر)
const renderChart = () => {
  // در یک پروژه واقعی، اینجا باید از یک کتابخانه نمودار مانند Chart.js استفاده شود
  // این تابع فقط یک نمونه است و در این مثال واقعاً نموداری رسم نمی‌کند
  console.log('Rendering chart with data:', chartData.value);
};

// نظارت بر تغییر دوره نمودار
watch(chartPeriod, () => {
  fetchDashboardData();
});

// هنگام نمایش صفحه، داده‌ها را دریافت کن
onMounted(() => {
  fetchDashboardData();
});
</script>

<style scoped>
.dashboard-card {
  height: 100%;
  transition: all 0.3s ease;
}
.dashboard-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}
</style> 