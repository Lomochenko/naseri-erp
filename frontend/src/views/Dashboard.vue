<template>
  <div>
    <!-- بخش بالایی - خوشامدگویی و کارت‌های آمار -->
    <v-row>
      <v-col cols="12">
        <v-card class="mb-4 pa-4">
          <div class="d-flex justify-space-between align-center">
            <div>
              <h1 class="text-h4 font-weight-bold">{{ userGreeting }}</h1>
              <p class="text-subtitle">خلاصه وضعیت کسب و کار شما در یک نگاه</p>
            </div>
            <div>
              <v-btn 
                prepend-icon="mdi-file-document-outline" 
                color="primary" 
                variant="tonal"
                class="ml-2"
              >
                گزارش جدید
              </v-btn>
              <v-btn prepend-icon="mdi-refresh" variant="outlined">به‌روزرسانی</v-btn>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- کارت‌های آمار -->
    <v-row>
      <v-col v-for="(stat, key) in dashboardStats" :key="key" cols="12" sm="6" md="3">
        <v-card class="dashboard-card">
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <p class="text-subtitle mb-1">{{ stat.title }}</p>
                <h3 class="text-h4 font-weight-bold mb-1">
                  {{ key === 'totalSales' ? formatCurrency(stat.value) : stat.value.toLocaleString('fa-IR') }}
                </h3>
                <p class="text-caption" :class="stat.trend.startsWith('+') ? 'text-success' : 'text-error'">
                  {{ stat.trend }}
                  <v-icon small :color="stat.trend.startsWith('+') ? 'success' : 'error'">
                    {{ stat.trend.startsWith('+') ? 'mdi-arrow-up' : 'mdi-arrow-down' }}
                  </v-icon>
                  نسبت به ماه قبل
                </p>
              </div>
              <v-avatar :color="stat.color" size="50" class="elevation-1">
                <v-icon size="28" color="white">{{ stat.icon }}</v-icon>
              </v-avatar>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- نمودار و جدول محصولات پرفروش -->
    <v-row class="mt-4">
      <v-col cols="12" md="8">
        <v-card class="dashboard-card">
          <v-card-title class="d-flex justify-space-between align-center">
            <div>نمودار فروش سالانه</div>
            <div>
              <v-btn-toggle v-model="selectedPeriod" color="primary" variant="outlined" density="comfortable">
                <v-btn value="month">ماهانه</v-btn>
                <v-btn value="year">سالانه</v-btn>
              </v-btn-toggle>
            </div>
          </v-card-title>
          <v-card-text>
            <!-- در نسخه واقعی از کتابخانه chart.js استفاده می‌شود -->
            <v-sheet height="400" class="d-flex justify-center align-center">
              <span class="text-caption">نمودار فروش اینجا نمایش داده می‌شود</span>
            </v-sheet>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card class="dashboard-card">
          <v-card-title>محصولات پرفروش</v-card-title>
          <v-divider></v-divider>
          <v-list class="py-0">
            <v-list-item v-for="product in topProducts" :key="product.id">
              <template v-slot:prepend>
                <v-avatar color="primary" class="mr-3" variant="tonal" size="36">
                  <span class="text-primary">{{ product.name.charAt(0) }}</span>
                </v-avatar>
              </template>
              <v-list-item-title>{{ product.name }}</v-list-item-title>
              <v-list-item-subtitle>{{ product.category }}</v-list-item-subtitle>
              <template v-slot:append>
                <div class="text-right">
                  <div>{{ formatCurrency(product.price) }}</div>
                  <div class="text-caption text-success">{{ product.sales }} فروش</div>
                </div>
              </template>
            </v-list-item>
          </v-list>
          <v-divider></v-divider>
          <v-card-actions>
            <v-btn color="primary" variant="text" block to="/products">
              مشاهده همه محصولات
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- فعالیت‌های اخیر و تاریخچه فروش -->
    <v-row class="mt-4">
      <v-col cols="12" md="4">
        <v-card class="dashboard-card">
          <v-card-title>فعالیت‌های اخیر</v-card-title>
          <v-divider></v-divider>
          <v-list>
            <v-list-item v-for="(activity, index) in recentActivities" :key="index">
              <template v-slot:prepend>
                <v-avatar :color="activity.color" size="36" class="mr-3">
                  <v-icon color="white">{{ activity.icon }}</v-icon>
                </v-avatar>
              </template>
              <v-list-item-title>{{ activity.title }}</v-list-item-title>
              <v-list-item-subtitle>{{ activity.description }}</v-list-item-subtitle>
              <template v-slot:append>
                <span class="text-caption">{{ activity.time }}</span>
              </template>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>

      <v-col cols="12" md="8">
        <v-card class="dashboard-card">
          <v-card-title>تاریخچه فروش اخیر</v-card-title>
          <v-divider></v-divider>
          <v-table>
            <thead>
              <tr>
                <th>شماره فاکتور</th>
                <th>مشتری</th>
                <th>تاریخ</th>
                <th>مبلغ</th>
                <th>وضعیت</th>
                <th>عملیات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="sale in salesHistory" :key="sale.id">
                <td>{{ sale.id }}</td>
                <td>{{ sale.customer }}</td>
                <td>{{ sale.date }}</td>
                <td>{{ formatCurrency(sale.amount) }}</td>
                <td>
                  <v-chip :color="sale.statusColor" size="small" label>
                    {{ sale.status }}
                  </v-chip>
                </td>
                <td>
                  <v-btn icon="mdi-eye-outline" size="small" variant="text" density="comfortable"></v-btn>
                  <v-btn icon="mdi-pencil-outline" size="small" variant="text" density="comfortable"></v-btn>
                </td>
              </tr>
            </tbody>
          </v-table>
          <v-divider></v-divider>
          <v-card-actions>
            <v-btn color="primary" variant="text" block to="/sales">
              مشاهده همه فروش‌ها
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useAuthStore } from '../store/auth';

const authStore = useAuthStore();
const selectedPeriod = ref('month');

// اطلاعات داشبورد (در یک پروژه واقعی از API دریافت می‌شود)
const dashboardStats = ref({
  totalSales: {
    value: 12350000,
    trend: '+15%',
    icon: 'mdi-cash-multiple',
    color: 'primary',
    title: 'فروش کل'
  },
  totalProducts: {
    value: 547,
    trend: '+23',
    icon: 'mdi-package-variant-closed',
    color: 'info',
    title: 'تعداد محصولات'
  },
  totalCustomers: {
    value: 142,
    trend: '+12',
    icon: 'mdi-account-group',
    color: 'success',
    title: 'مشتریان'
  },
  lowStock: {
    value: 8,
    trend: '-4',
    icon: 'mdi-alert-circle',
    color: 'warning',
    title: 'محصولات با موجودی کم'
  }
});

// فرمت‌کردن اعداد به فرمت پول ایران
const formatCurrency = (value) => {
  return new Intl.NumberFormat('fa-IR', {
    style: 'currency',
    currency: 'IRR',
    notation: 'compact',
    maximumFractionDigits: 0
  }).format(value).replace('IRR', 'تومان');
};

// نمودار فروش ماهانه
const chartData = ref({
  labels: [
    'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
    'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'
  ],
  datasets: [
    {
      label: 'فروش',
      data: [18, 12, 27, 36, 24, 35, 42, 50, 43, 38, 55, 62],
      backgroundColor: 'rgba(145, 85, 253, 0.2)',
      borderColor: '#9155FD',
      tension: 0.4,
      fill: true
    },
    {
      label: 'سود',
      data: [8, 5, 12, 16, 10, 15, 20, 25, 22, 18, 26, 32],
      backgroundColor: 'rgba(22, 177, 255, 0.2)',
      borderColor: '#16B1FF',
      tension: 0.4,
      fill: true
    }
  ]
});

// محصولات پرفروش
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
  },
  { 
    id: 5, 
    name: 'چراغ LED سقفی', 
    category: 'لوازم روشنایی',
    sales: 87,
    stock: 23,
    price: 420000
  }
]);

// فعالیت‌های اخیر
const recentActivities = ref([
  {
    type: 'sale',
    title: 'فروش جدید',
    description: 'سفارش جدید به مبلغ ۲,۵۰۰,۰۰۰ تومان ثبت شد',
    time: '۱۰ دقیقه پیش',
    icon: 'mdi-cart-outline',
    color: 'success'
  },
  {
    type: 'purchase',
    title: 'خرید جدید',
    description: 'خرید از تامین‌کننده به مبلغ ۱۲,۰۰۰,۰۰۰ تومان ثبت شد',
    time: '۲ ساعت پیش',
    icon: 'mdi-cart-plus',
    color: 'info'
  },
  {
    type: 'inventory',
    title: 'بروزرسانی موجودی',
    description: 'موجودی ۱۵ مورد از محصولات به‌روزرسانی شد',
    time: '۴ ساعت پیش',
    icon: 'mdi-update',
    color: 'primary'
  },
  {
    type: 'user',
    title: 'کاربر جدید',
    description: 'یک مشتری جدید در سیستم ثبت‌نام کرد',
    time: 'دیروز',
    icon: 'mdi-account-plus',
    color: 'warning'
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

// نام کاربر
const userGreeting = computed(() => {
  if (authStore.user?.first_name) {
    return `سلام، ${authStore.user.first_name} عزیز!`;
  }
  return 'سلام، خوش آمدید!';
});
</script>

<style scoped>
.dashboard-card {
  height: 100%;
}
</style> 