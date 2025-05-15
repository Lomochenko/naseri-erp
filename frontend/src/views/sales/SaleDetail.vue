<template>
  <div>
    <v-card class="mb-6">
      <v-card-title class="d-flex align-center justify-space-between flex-wrap">
        <span class="text-h5">جزئیات فاکتور</span>
        <div>
          <v-btn 
            color="error" 
            variant="outlined" 
            class="mr-2"
            prepend-icon="mdi-delete" 
            v-if="userHasPermission('delete_sale')"
            @click="confirmDelete"
          >
            حذف فاکتور
          </v-btn>
          <v-btn 
            color="secondary" 
            variant="text" 
            prepend-icon="mdi-arrow-left" 
            to="/sales"
          >
            بازگشت به لیست فروش‌ها
          </v-btn>
        </div>
      </v-card-title>
    </v-card>

    <div v-if="loading">
      <v-skeleton-loader
        type="card"
        class="mb-6"
      ></v-skeleton-loader>
    </div>

    <div v-else-if="error">
      <v-alert type="error" title="خطا در بارگیری اطلاعات">
        {{ error }}
        <template v-slot:append>
          <v-btn color="error" variant="text" @click="fetchSaleDetails">تلاش مجدد</v-btn>
        </template>
      </v-alert>
    </div>

    <div v-else-if="sale">
      <v-row>
        <v-col cols="12" md="8">
          <!-- اطلاعات پایه فاکتور -->
          <v-card variant="outlined" class="mb-6">
            <v-card-title class="d-flex justify-space-between align-center">
              <span>اطلاعات فاکتور</span>
              <v-chip
                :color="getStatusColor(sale.status)"
                size="small"
                variant="elevated"
                class="mr-1"
              >
                {{ getStatusText(sale.status) }}
              </v-chip>
            </v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="12" md="6">
                  <v-list density="compact">
                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon icon="mdi-barcode" color="primary"></v-icon>
                      </template>
                      <v-list-item-title>شماره فاکتور:</v-list-item-title>
                      <v-list-item-subtitle class="text-right">{{ sale.invoice_number }}</v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon icon="mdi-calendar" color="primary"></v-icon>
                      </template>
                      <v-list-item-title>تاریخ فاکتور:</v-list-item-title>
                      <v-list-item-subtitle class="text-right">{{ formatDate(sale.date) }}</v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon icon="mdi-clock-outline" color="primary"></v-icon>
                      </template>
                      <v-list-item-title>زمان ثبت:</v-list-item-title>
                      <v-list-item-subtitle class="text-right">{{ formatDateTime(sale.created_at) }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-col>

                <v-col cols="12" md="6">
                  <v-list density="compact">
                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon icon="mdi-cash-multiple" color="primary"></v-icon>
                      </template>
                      <v-list-item-title>روش پرداخت:</v-list-item-title>
                      <v-list-item-subtitle class="text-right">{{ getPaymentMethodText(sale.payment_method) }}</v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon icon="mdi-account" color="primary"></v-icon>
                      </template>
                      <v-list-item-title>فروشنده:</v-list-item-title>
                      <v-list-item-subtitle class="text-right">{{ sale.created_by ? sale.created_by.name : 'نامشخص' }}</v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item v-if="sale.notes">
                      <template v-slot:prepend>
                        <v-icon icon="mdi-note-text" color="primary"></v-icon>
                      </template>
                      <v-list-item-title>توضیحات:</v-list-item-title>
                      <v-list-item-subtitle class="text-right">{{ sale.notes }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- اطلاعات مشتری -->
          <v-card variant="outlined" class="mb-6">
            <v-card-title>اطلاعات مشتری</v-card-title>
            <v-card-text v-if="sale.customer">
              <v-row>
                <v-col cols="12" md="6">
                  <v-list density="compact">
                    <v-list-item>
                      <template v-slot:prepend>
                        <v-avatar color="primary" variant="tonal" size="32">
                          <span class="text-primary">{{ sale.customer.name.charAt(0) }}</span>
                        </v-avatar>
                      </template>
                      <v-list-item-title>نام مشتری:</v-list-item-title>
                      <v-list-item-subtitle class="text-right">{{ sale.customer.name }}</v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item v-if="sale.customer.phone">
                      <template v-slot:prepend>
                        <v-icon icon="mdi-phone" color="primary"></v-icon>
                      </template>
                      <v-list-item-title>شماره تماس:</v-list-item-title>
                      <v-list-item-subtitle class="text-right">{{ sale.customer.phone }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-col>

                <v-col cols="12" md="6">
                  <v-list density="compact">
                    <v-list-item v-if="sale.customer.email">
                      <template v-slot:prepend>
                        <v-icon icon="mdi-email" color="primary"></v-icon>
                      </template>
                      <v-list-item-title>ایمیل:</v-list-item-title>
                      <v-list-item-subtitle class="text-right">{{ sale.customer.email }}</v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item v-if="sale.customer.address">
                      <template v-slot:prepend>
                        <v-icon icon="mdi-map-marker" color="primary"></v-icon>
                      </template>
                      <v-list-item-title>آدرس:</v-list-item-title>
                      <v-list-item-subtitle class="text-right">{{ sale.customer.address }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-col>
              </v-row>
            </v-card-text>
            <v-card-text v-else>
              <p class="text-center text-grey">مشتری متفرقه</p>
            </v-card-text>
          </v-card>

          <!-- اقلام فاکتور -->
          <v-card variant="outlined" class="mb-6">
            <v-card-title>اقلام فاکتور</v-card-title>
            <v-card-text>
              <v-table>
                <thead>
                  <tr>
                    <th class="text-center">#</th>
                    <th>محصول</th>
                    <th class="text-center">تعداد</th>
                    <th class="text-center">قیمت واحد (تومان)</th>
                    <th class="text-center">تخفیف</th>
                    <th class="text-center">قیمت کل (تومان)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, index) in sale.items" :key="index">
                    <td class="text-center">{{ index + 1 }}</td>
                    <td>
                      <div class="font-weight-medium">{{ item.product.name }}</div>
                      <div class="text-caption text-grey">کد: {{ item.product.code }}</div>
                    </td>
                    <td class="text-center">{{ item.quantity }} {{ item.product.unit_symbol }}</td>
                    <td class="text-center">{{ formatPrice(item.unit_price) }}</td>
                    <td class="text-center">{{ item.discount_percent || 0 }}%</td>
                    <td class="text-center font-weight-medium">{{ formatPrice(item.total_price) }}</td>
                  </tr>
                </tbody>
              </v-table>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="4">
          <!-- جمع‌بندی فاکتور -->
          <v-card variant="outlined" class="mb-6 sticky-card">
            <v-card-title>جمع‌بندی فاکتور</v-card-title>
            <v-card-text>
              <v-list density="compact">
                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-cart-outline"></v-icon>
                  </template>
                  <v-list-item-title>تعداد اقلام:</v-list-item-title>
                  <v-list-item-subtitle class="text-right">{{ sale.items.length }} قلم</v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-cash-multiple"></v-icon>
                  </template>
                  <v-list-item-title>جمع کل:</v-list-item-title>
                  <v-list-item-subtitle class="text-right">{{ formatPrice(sale.subtotal) }}</v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-sale"></v-icon>
                  </template>
                  <v-list-item-title>تخفیف کل:</v-list-item-title>
                  <v-list-item-subtitle class="text-right text-error">{{ formatPrice(sale.discount_amount) }}</v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-percent"></v-icon>
                  </template>
                  <v-list-item-title>مالیات ({{ sale.tax_percent }}%):</v-list-item-title>
                  <v-list-item-subtitle class="text-right">{{ formatPrice(sale.tax_amount) }}</v-list-item-subtitle>
                </v-list-item>

                <v-divider class="my-2"></v-divider>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-cash" color="primary"></v-icon>
                  </template>
                  <v-list-item-title class="text-primary font-weight-bold">مبلغ قابل پرداخت:</v-list-item-title>
                  <v-list-item-subtitle class="text-right text-primary text-h6">{{ formatPrice(sale.total_amount) }}</v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-check-circle" color="success"></v-icon>
                  </template>
                  <v-list-item-title>مبلغ پرداخت شده:</v-list-item-title>
                  <v-list-item-subtitle class="text-right text-success">{{ formatPrice(sale.paid_amount) }}</v-list-item-subtitle>
                </v-list-item>

                <v-list-item v-if="sale.total_amount > sale.paid_amount">
                  <template v-slot:prepend>
                    <v-icon icon="mdi-alert-circle" color="warning"></v-icon>
                  </template>
                  <v-list-item-title class="text-warning">مانده حساب:</v-list-item-title>
                  <v-list-item-subtitle class="text-right text-warning">{{ formatPrice(sale.total_amount - sale.paid_amount) }}</v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-btn 
                color="primary" 
                variant="elevated" 
                block 
                prepend-icon="mdi-printer" 
                @click="printInvoice"
              >
                چاپ فاکتور
              </v-btn>
            </v-card-actions>
          </v-card>
          
          <!-- وضعیت پرداخت -->
          <v-card variant="outlined" class="mb-6" v-if="userHasPermission('change_sale_status')">
            <v-card-title>تغییر وضعیت</v-card-title>
            <v-card-text>
              <v-select
                v-model="selectedStatus"
                :items="statusOptions"
                item-title="title"
                item-value="value"
                label="وضعیت فاکتور"
                variant="outlined"
                density="comfortable"
                :loading="statusLoading"
              ></v-select>
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-btn 
                color="info" 
                variant="outlined" 
                block 
                :disabled="selectedStatus === sale.status || statusLoading"
                prepend-icon="mdi-content-save" 
                :loading="statusLoading"
                @click="updateStatus"
              >
                ذخیره وضعیت
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </div>
    <div v-else>
      <v-alert type="info" title="فاکتور یافت نشد">
        فاکتور مورد نظر یافت نشد یا حذف شده است.
        <template v-slot:append>
          <v-btn color="info" variant="text" to="/sales">بازگشت به لیست فروش‌ها</v-btn>
        </template>
      </v-alert>
    </div>

    <!-- دیالوگ تایید حذف -->
    <v-dialog v-model="deleteDialog" max-width="500">
      <v-card>
        <v-card-title class="text-h5 text-error">حذف فاکتور</v-card-title>
        <v-card-text>
          آیا از حذف این فاکتور اطمینان دارید؟ این عملیات غیرقابل بازگشت است.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" variant="text" @click="deleteDialog = false">انصراف</v-btn>
          <v-btn 
            color="error" 
            variant="elevated"
            :loading="deleteLoading"
            @click="deleteSale"
          >
            حذف فاکتور
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useSalesStore } from '../../store/sales';
import { useAuthStore } from '../../store/auth';

// روتر و پارامترها
const route = useRoute();
const router = useRouter();
const saleId = parseInt(route.params.id);

// استورها
const salesStore = useSalesStore();
const authStore = useAuthStore();

// حالت‌ها
const loading = ref(false);
const statusLoading = ref(false);
const deleteLoading = ref(false);
const error = ref(null);
const deleteDialog = ref(false);
const selectedStatus = ref(null);

// گترها
const sale = computed(() => salesStore.getSaleById(saleId));

// تعاریف وضعیت‌ها
const statusOptions = [
  { title: 'پرداخت شده', value: 'PAID' },
  { title: 'معلق', value: 'PENDING' },
  { title: 'لغو شده', value: 'CANCELLED' }
];

// بررسی دسترسی کاربر
const userHasPermission = (permission) => {
  return authStore.hasPermission(permission);
};

// فرمت‌کننده‌ها
const formatPrice = (price) => {
  return new Intl.NumberFormat('fa-IR').format(price);
};

const formatDate = (dateString) => {
  if (!dateString) return 'نامشخص';
  return new Date(dateString).toLocaleDateString('fa-IR');
};

const formatDateTime = (dateTimeString) => {
  if (!dateTimeString) return 'نامشخص';
  const date = new Date(dateTimeString);
  return `${date.toLocaleDateString('fa-IR')} ${date.toLocaleTimeString('fa-IR')}`;
};

// تبدیل وضعیت به متن فارسی
const getStatusText = (status) => {
  switch (status) {
    case 'PAID': return 'پرداخت شده';
    case 'PENDING': return 'معلق';
    case 'CANCELLED': return 'لغو شده';
    default: return 'نامشخص';
  }
};

// تبدیل وضعیت به رنگ
const getStatusColor = (status) => {
  switch (status) {
    case 'PAID': return 'success';
    case 'PENDING': return 'warning';
    case 'CANCELLED': return 'error';
    default: return 'grey';
  }
};

// تبدیل روش پرداخت به متن فارسی
const getPaymentMethodText = (method) => {
  switch (method) {
    case 'cash': return 'نقدی';
    case 'card': return 'کارت بانکی';
    case 'transfer': return 'انتقال وجه';
    case 'cheque': return 'چک';
    default: return 'نامشخص';
  }
};

// دریافت جزئیات فروش
const fetchSaleDetails = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    await salesStore.fetchSaleDetail(saleId);
    if (sale.value) {
      selectedStatus.value = sale.value.status;
    } else {
      error.value = 'فاکتور مورد نظر یافت نشد.';
    }
  } catch (err) {
    console.error('Error fetching sale details:', err);
    error.value = err.message || 'خطا در دریافت اطلاعات فاکتور';
  } finally {
    loading.value = false;
  }
};

// به‌روزرسانی وضعیت فاکتور
const updateStatus = async () => {
  if (selectedStatus.value === sale.value.status) return;
  
  statusLoading.value = true;
  
  try {
    await salesStore.updateSaleStatus(saleId, selectedStatus.value);
  } catch (err) {
    console.error('Error updating sale status:', err);
  } finally {
    statusLoading.value = false;
  }
};

// نمایش دیالوگ تایید حذف
const confirmDelete = () => {
  deleteDialog.value = true;
};

// حذف فاکتور
const deleteSale = async () => {
  deleteLoading.value = true;
  
  try {
    const success = await salesStore.deleteSale(saleId);
    if (success) {
      router.push({ 
        path: '/sales',
        query: { 
          delete_success: 'true',
          invoice: sale.value.invoice_number
        }
      });
    }
  } catch (err) {
    console.error('Error deleting sale:', err);
  } finally {
    deleteLoading.value = false;
    deleteDialog.value = false;
  }
};

// چاپ فاکتور
const printInvoice = () => {
  if (!sale.value) return;
  
  // ایجاد صفحه چاپ
  const printWindow = window.open('', '_blank');
  printWindow.document.write(`
    <html dir="rtl">
      <head>
        <title>فاکتور فروش ${sale.value.invoice_number}</title>
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
            <p><strong>شماره فاکتور:</strong> ${sale.value.invoice_number}</p>
            <p><strong>تاریخ:</strong> ${formatDate(sale.value.date)}</p>
          </div>
          <div>
            <p><strong>مشتری:</strong> ${sale.value.customer?.name || 'فروش متفرقه'}</p>
            <p><strong>شماره تماس:</strong> ${sale.value.customer?.phone || '-'}</p>
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
              <th>تخفیف</th>
              <th>جمع (تومان)</th>
            </tr>
          </thead>
          <tbody>
            ${sale.value.items.map((item, index) => `
              <tr>
                <td>${index + 1}</td>
                <td>${item.product.code}</td>
                <td>${item.product.name}</td>
                <td>${item.quantity} ${item.product.unit_symbol}</td>
                <td>${formatPrice(item.unit_price)}</td>
                <td>${item.discount_percent || 0}%</td>
                <td>${formatPrice(item.total_price)}</td>
              </tr>
            `).join('')}
          </tbody>
          <tfoot>
            <tr>
              <td colspan="6" class="text-right">جمع کل:</td>
              <td>${formatPrice(sale.value.subtotal)}</td>
            </tr>
            <tr>
              <td colspan="6" class="text-right">تخفیف:</td>
              <td>${formatPrice(sale.value.discount_amount)}</td>
            </tr>
            <tr>
              <td colspan="6" class="text-right">مالیات (${sale.value.tax_percent}%):</td>
              <td>${formatPrice(sale.value.tax_amount)}</td>
            </tr>
            <tr class="total-row">
              <td colspan="6" class="text-right">مبلغ قابل پرداخت:</td>
              <td>${formatPrice(sale.value.total_amount)}</td>
            </tr>
            <tr>
              <td colspan="6" class="text-right">مبلغ پرداخت شده:</td>
              <td>${formatPrice(sale.value.paid_amount)}</td>
            </tr>
            <tr>
              <td colspan="6" class="text-right">مانده حساب:</td>
              <td>${formatPrice(sale.value.total_amount - sale.value.paid_amount)}</td>
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

// دریافت داده‌ها در هنگام لود صفحه
onMounted(() => {
  fetchSaleDetails();
});
</script>

<style scoped>
.sticky-card {
  position: sticky;
  top: 20px;
}

@media (max-width: 960px) {
  .sticky-card {
    position: static;
  }
}
</style> 