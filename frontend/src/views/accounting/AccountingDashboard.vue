<template>
  <div>
    <h1 class="text-h4 mb-6">داشبورد حسابداری</h1>
    
    <!-- Financial Summary Cards -->
    <v-row>
      <!-- Revenue card -->
      <v-col cols="12" md="3">
        <v-card>
          <v-card-title class="text-subtitle-1">درآمد ماهانه</v-card-title>
          <v-card-text>
            <div class="text-h5 mb-2">۵۸,۴۵۰,۰۰۰ تومان</div>
            <v-progress-linear model-value="75" color="success" height="8"></v-progress-linear>
            <div class="text-caption mt-2">+۱۲٪ نسبت به ماه قبل</div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <!-- Expenses card -->
      <v-col cols="12" md="3">
        <v-card>
          <v-card-title class="text-subtitle-1">هزینه‌های ماهانه</v-card-title>
          <v-card-text>
            <div class="text-h5 mb-2">۴۲,۸۳۰,۰۰۰ تومان</div>
            <v-progress-linear model-value="65" color="error" height="8"></v-progress-linear>
            <div class="text-caption mt-2">+۵٪ نسبت به ماه قبل</div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <!-- Profit card -->
      <v-col cols="12" md="3">
        <v-card>
          <v-card-title class="text-subtitle-1">سود خالص</v-card-title>
          <v-card-text>
            <div class="text-h5 mb-2">۱۵,۶۲۰,۰۰۰ تومان</div>
            <v-progress-linear model-value="45" color="info" height="8"></v-progress-linear>
            <div class="text-caption mt-2">+۲۰٪ نسبت به ماه قبل</div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <!-- Outstanding invoices card -->
      <v-col cols="12" md="3">
        <v-card>
          <v-card-title class="text-subtitle-1">مطالبات معوق</v-card-title>
          <v-card-text>
            <div class="text-h5 mb-2">۸,۲۰۰,۰۰۰ تومان</div>
            <v-progress-linear model-value="25" color="warning" height="8"></v-progress-linear>
            <div class="text-caption mt-2">-۸٪ نسبت به ماه قبل</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- Charts -->
    <v-row class="mt-6">
      <!-- Revenue vs Expenses Chart -->
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>درآمد و هزینه‌ها</v-card-title>
          <v-card-text>
            <div class="text-center mt-10 mb-10 text-h6 text-medium-emphasis">
              (نمودار ستونی درآمد و هزینه‌ها به صورت ماهانه)
            </div>
            <div class="d-flex justify-center mb-4">
              <v-chip-group mandatory selected-class="primary">
                <v-chip>ماهانه</v-chip>
                <v-chip>فصلی</v-chip>
                <v-chip>سالانه</v-chip>
              </v-chip-group>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <!-- Profit Trend Chart -->
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>روند سود</v-card-title>
          <v-card-text>
            <div class="text-center mt-10 mb-10 text-h6 text-medium-emphasis">
              (نمودار خطی روند سود به صورت ماهانه)
            </div>
            <div class="d-flex justify-center mb-4">
              <v-chip-group mandatory selected-class="primary">
                <v-chip>۳ ماه اخیر</v-chip>
                <v-chip>۶ ماه اخیر</v-chip>
                <v-chip>۱۲ ماه اخیر</v-chip>
              </v-chip-group>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- Recent Transactions and Due Payments -->
    <v-row class="mt-6">
      <!-- Recent Transactions -->
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>تراکنش‌های اخیر</span>
            <v-btn variant="text" color="primary" density="compact">
              مشاهده همه
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-table>
              <thead>
                <tr>
                  <th>شماره</th>
                  <th>تاریخ</th>
                  <th>شرح</th>
                  <th>مبلغ</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="transaction in recentTransactions" :key="transaction.id">
                  <td>{{ transaction.id }}</td>
                  <td>{{ transaction.date }}</td>
                  <td>{{ transaction.description }}</td>
                  <td :class="transaction.amount > 0 ? 'text-success' : 'text-error'">
                    {{ transaction.amount > 0 ? '+' : '' }}{{ transaction.amount.toLocaleString() }} تومان
                  </td>
                </tr>
              </tbody>
            </v-table>
          </v-card-text>
        </v-card>
      </v-col>
      
      <!-- Due Payments -->
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>پرداخت‌های معوق</span>
            <v-btn variant="text" color="primary" density="compact">
              مشاهده همه
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-table>
              <thead>
                <tr>
                  <th>شماره</th>
                  <th>مشتری</th>
                  <th>تاریخ سررسید</th>
                  <th>مبلغ</th>
                  <th>وضعیت</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="payment in duePayments" :key="payment.id">
                  <td>{{ payment.invoice_number }}</td>
                  <td>{{ payment.customer }}</td>
                  <td>{{ payment.due_date }}</td>
                  <td>{{ payment.amount.toLocaleString() }} تومان</td>
                  <td>
                    <v-chip
                      :color="getDueStatusColor(payment.status)"
                      size="small"
                    >
                      {{ getDueStatusLabel(payment.status) }}
                    </v-chip>
                  </td>
                </tr>
              </tbody>
            </v-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- Action Buttons -->
    <v-row class="mt-6">
      <v-col cols="12" class="d-flex justify-center">
        <v-btn class="mx-2" color="primary" prepend-icon="mdi-file-document-outline">
          گزارش سود و زیان
        </v-btn>
        <v-btn class="mx-2" color="success" prepend-icon="mdi-cash-register">
          ثبت تراکنش جدید
        </v-btn>
        <v-btn class="mx-2" color="info" prepend-icon="mdi-chart-box-outline">
          گزارش جریان نقدی
        </v-btn>
        <v-btn class="mx-2" color="warning" prepend-icon="mdi-bank-outline">
          حساب‌های بانکی
        </v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// Sample data
const recentTransactions = ref([
  { id: 'TRX-10045', date: '۱۴۰۳/۰۲/۲۵', description: 'دریافت از مشتری - شرکت ساختمانی البرز', amount: 4500000 },
  { id: 'TRX-10044', date: '۱۴۰۳/۰۲/۲۴', description: 'پرداخت به تامین‌کننده - شرکت فروش یراق میلاد', amount: -3200000 },
  { id: 'TRX-10043', date: '۱۴۰۳/۰۲/۲۴', description: 'دریافت از مشتری - نجاری مهرگان', amount: 2800000 },
  { id: 'TRX-10042', date: '۱۴۰۳/۰۲/۲۳', description: 'پرداخت حقوق کارکنان', amount: -12500000 },
  { id: 'TRX-10041', date: '۱۴۰۳/۰۲/۲۳', description: 'دریافت از مشتری - کابینت سازی نوین', amount: 5800000 }
]);

const duePayments = ref([
  { id: 1, invoice_number: 'INV-1003', customer: 'فروشگاه لوازم خانگی پارس', due_date: '۱۴۰۳/۰۳/۱۰', amount: 1417000, status: 'UPCOMING' },
  { id: 2, invoice_number: 'INV-1006', customer: 'تعمیرگاه مرکزی ایران', due_date: '۱۴۰۳/۰۲/۳۰', amount: 2750000, status: 'OVERDUE' },
  { id: 3, invoice_number: 'INV-1008', customer: 'شرکت تولیدی مبلمان شیراز', due_date: '۱۴۰۳/۰۳/۱۵', amount: 1870000, status: 'UPCOMING' },
  { id: 4, invoice_number: 'INV-1009', customer: 'کارگاه صنعتی رضا', due_date: '۱۴۰۳/۰۲/۲۰', amount: 950000, status: 'OVERDUE' },
  { id: 5, invoice_number: 'INV-1010', customer: 'فروشگاه ساختمانی پارس', due_date: '۱۴۰۳/۰۳/۰۵', amount: 1213000, status: 'UPCOMING' }
]);

// Helper functions
const getDueStatusColor = (status) => {
  switch(status) {
    case 'OVERDUE': return 'error';
    case 'UPCOMING': return 'warning';
    case 'PAID': return 'success';
    default: return 'grey';
  }
};

const getDueStatusLabel = (status) => {
  switch(status) {
    case 'OVERDUE': return 'گذشته';
    case 'UPCOMING': return 'در انتظار';
    case 'PAID': return 'پرداخت شده';
    default: return 'نامشخص';
  }
};
</script> 