<template>
  <div>
    <v-card class="mb-6">
      <v-card-title class="d-flex align-center justify-space-between flex-wrap">
        <span class="text-h5">ثبت فروش جدید</span>
        <v-btn 
          color="secondary" 
          variant="text" 
          prepend-icon="mdi-arrow-left" 
          to="/sales"
        >
          بازگشت به لیست فروش‌ها
        </v-btn>
      </v-card-title>
    </v-card>

    <v-form ref="form" @submit.prevent="saveSale" class="pb-12">
      <v-row>
        <!-- اطلاعات پایه فاکتور -->
        <v-col cols="12" lg="8">
          <v-card variant="outlined" class="mb-6">
            <v-card-title>اطلاعات پایه فاکتور</v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="12" md="6">
                  <v-autocomplete
                    v-model="sale.customer"
                    :items="customers"
                    item-title="name"
                    item-value="id"
                    label="مشتری"
                    variant="outlined"
                    density="comfortable"
                    :rules="[v => !!v || 'انتخاب مشتری الزامی است']"
                    return-object
                    clearable
                    :loading="customersLoading"
                  >
                    <template v-slot:prepend-item>
                      <v-list-item
                        color="primary"
                        title="افزودن مشتری جدید"
                        prepend-icon="mdi-plus"
                        @click="openNewCustomerDialog"
                      ></v-list-item>
                      <v-divider class="mt-2"></v-divider>
                    </template>
                    <template v-slot:item="{ item, props }">
                      <v-list-item v-bind="props">
                        <template v-slot:prepend>
                          <v-avatar color="primary" variant="tonal" size="32">
                            <span class="text-primary">{{ item.name.charAt(0) }}</span>
                          </v-avatar>
                        </template>
                        <v-list-item-title>{{ item.name }}</v-list-item-title>
                        <v-list-item-subtitle v-if="item.phone">{{ item.phone }}</v-list-item-subtitle>
                      </v-list-item>
                    </template>
                  </v-autocomplete>
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="sale.invoice_number"
                    label="شماره فاکتور"
                    variant="outlined"
                    density="comfortable"
                    :rules="[v => !!v || 'شماره فاکتور الزامی است']"
                    :readonly="true"
                    :hint="`فاکتور به صورت خودکار شماره گذاری می‌شود: ${sale.invoice_number}`"
                    persistent-hint
                  ></v-text-field>
                </v-col>

                <v-col cols="12" md="6">
                  <v-menu
                    ref="dateMenu"
                    v-model="dateMenu"
                    :close-on-content-click="false"
                    transition="scale-transition"
                    min-width="auto"
                  >
                    <template v-slot:activator="{ props }">
                      <v-text-field
                        v-model="sale.date"
                        label="تاریخ فاکتور"
                        variant="outlined"
                        density="comfortable"
                        append-inner-icon="mdi-calendar"
                        readonly
                        v-bind="props"
                      ></v-text-field>
                    </template>
                    <v-date-picker
                      v-model="sale.date"
                      @update:model-value="dateMenu = false"
                    ></v-date-picker>
                  </v-menu>
                </v-col>

                <v-col cols="12" md="6">
                  <v-select
                    v-model="sale.payment_method"
                    :items="paymentMethods"
                    item-title="title"
                    item-value="value"
                    label="روش پرداخت"
                    variant="outlined"
                    density="comfortable"
                    :rules="[v => !!v || 'انتخاب روش پرداخت الزامی است']"
                  ></v-select>
                </v-col>

                <v-col cols="12">
                  <v-textarea
                    v-model="sale.notes"
                    label="توضیحات فاکتور"
                    variant="outlined"
                    density="comfortable"
                    auto-grow
                    rows="2"
                    counter
                    maxlength="500"
                  ></v-textarea>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- انتخاب محصولات -->
          <v-card variant="outlined" class="mb-6">
            <v-card-title class="d-flex align-center justify-space-between">
              <span>اقلام فاکتور</span>
              <v-btn 
                color="primary" 
                variant="text" 
                prepend-icon="mdi-plus" 
                @click="openProductSelector"
              >
                افزودن محصول
              </v-btn>
            </v-card-title>
            
            <v-card-text>
              <div v-if="sale.items.length === 0" class="text-center py-12">
                <v-icon size="64" icon="mdi-cart-outline" color="grey-lighten-1" class="mb-4"></v-icon>
                <div class="text-h6 text-grey">هیچ محصولی به فاکتور اضافه نشده است</div>
                <v-btn 
                  color="primary" 
                  variant="tonal" 
                  class="mt-4"
                  prepend-icon="mdi-plus"
                  @click="openProductSelector"
                >
                  افزودن محصول به فاکتور
                </v-btn>
              </div>

              <v-table v-else>
                <thead>
                  <tr>
                    <th class="text-center">#</th>
                    <th>محصول</th>
                    <th class="text-center">تعداد</th>
                    <th class="text-center">قیمت واحد (تومان)</th>
                    <th class="text-center">تخفیف</th>
                    <th class="text-center">قیمت کل (تومان)</th>
                    <th class="text-center">عملیات</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, index) in sale.items" :key="index">
                    <td class="text-center">{{ index + 1 }}</td>
                    <td>
                      <div class="font-weight-medium">{{ item.product.name }}</div>
                      <div class="text-caption text-grey">کد: {{ item.product.code }}</div>
                    </td>
                    <td class="text-center">
                      <v-text-field
                        v-model.number="item.quantity"
                        type="number"
                        min="1"
                        variant="underlined"
                        density="compact"
                        hide-details
                        class="text-center"
                        style="max-width: 80px"
                        @input="calculateItemTotal(item)"
                      ></v-text-field>
                      <span class="text-caption text-grey">{{ item.product.unit_symbol }}</span>
                    </td>
                    <td class="text-center">
                      <v-text-field
                        v-model.number="item.unit_price"
                        type="number"
                        min="0"
                        variant="underlined"
                        density="compact"
                        hide-details
                        class="text-center"
                        @input="calculateItemTotal(item)"
                      ></v-text-field>
                    </td>
                    <td class="text-center">
                      <v-text-field
                        v-model.number="item.discount_percent"
                        type="number"
                        min="0"
                        max="100"
                        variant="underlined"
                        density="compact"
                        hide-details
                        class="text-center"
                        style="max-width: 80px"
                        suffix="%"
                        @input="calculateItemTotal(item)"
                      ></v-text-field>
                    </td>
                    <td class="text-center font-weight-medium">{{ formatPrice(item.total_price) }}</td>
                    <td class="text-center">
                      <v-btn 
                        icon="mdi-delete" 
                        size="small" 
                        color="error" 
                        variant="text"
                        @click="removeItem(index)"
                      ></v-btn>
                    </td>
                  </tr>
                </tbody>
              </v-table>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- جمع بندی فاکتور -->
        <v-col cols="12" lg="4">
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
                  <v-list-item-subtitle class="text-right">{{ formatPrice(calculateSubtotal()) }}</v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-sale"></v-icon>
                  </template>
                  <v-list-item-title>تخفیف کل:</v-list-item-title>
                  <v-list-item-subtitle class="text-right text-error">{{ formatPrice(calculateTotalDiscount()) }}</v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-percent"></v-icon>
                  </template>
                  <v-list-item-title>مالیات ({{ sale.tax_percent }}%):</v-list-item-title>
                  <v-list-item-subtitle class="text-right">{{ formatPrice(calculateTax()) }}</v-list-item-subtitle>
                </v-list-item>

                <v-divider class="my-2"></v-divider>

                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon icon="mdi-cash" color="primary"></v-icon>
                  </template>
                  <v-list-item-title class="text-primary font-weight-bold">مبلغ قابل پرداخت:</v-list-item-title>
                  <v-list-item-subtitle class="text-right text-primary text-h6">{{ formatPrice(calculateTotal()) }}</v-list-item-subtitle>
                </v-list-item>
              </v-list>

              <v-text-field
                v-model.number="sale.paid_amount"
                label="مبلغ پرداخت شده (تومان)"
                variant="outlined"
                density="comfortable"
                type="number"
                min="0"
                :max="calculateTotal()"
                class="mt-4"
                :rules="[v => v !== null || 'وارد کردن مبلغ پرداخت شده الزامی است']"
                :hint="`مانده: ${formatPrice(calculateTotal() - (sale.paid_amount || 0))}`"
                persistent-hint
              ></v-text-field>

              <v-switch
                v-model="sale.print_after_save"
                color="primary"
                label="چاپ فاکتور پس از ثبت"
                density="comfortable"
                class="mt-4"
                hide-details
              ></v-switch>
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-btn 
                color="error" 
                variant="text" 
                block 
                prepend-icon="mdi-close"
                @click="resetForm"
              >
                انصراف
              </v-btn>
              <v-btn 
                color="primary" 
                variant="elevated" 
                block 
                :disabled="sale.items.length === 0 || loading"
                prepend-icon="mdi-content-save" 
                :loading="loading"
                type="submit"
                @click="saveSale"
              >
                ثبت فاکتور
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-form>

    <!-- دیالوگ انتخاب محصول -->
    <v-dialog v-model="productDialog" max-width="900px" scrollable persistent>
      <v-card>
        <v-card-title class="text-h5 d-flex justify-space-between align-center">
          <span>انتخاب محصول</span>
          <v-text-field
            v-model="productSearchQuery"
            label="جستجو در محصولات"
            variant="outlined"
            density="compact"
            prepend-inner-icon="mdi-magnify"
            hide-details
            style="max-width: 300px"
            clearable
            @update:model-value="searchProducts"
          ></v-text-field>
        </v-card-title>

        <v-divider></v-divider>

        <v-card-text style="height: 400px;">
          <v-data-table
            v-if="!productsLoading"
            :headers="productHeaders"
            :items="filteredProducts"
            :search="productSearchQuery"
            density="comfortable"
            class="elevation-1"
            item-value="id"
            :loading="productsLoading"
            :items-per-page="5"
          >
            <template v-slot:item.image="{ item }">
              <v-avatar size="40" rounded>
                <v-img :src="item.image || '/images/no-image.png'" :alt="item.name"></v-img>
              </v-avatar>
            </template>

            <template v-slot:item.name="{ item }">
              <div>{{ item.name }}</div>
              <div class="text-caption">کد: {{ item.code }}</div>
            </template>

            <template v-slot:item.selling_price="{ item }">
              {{ formatPrice(item.selling_price) }}
            </template>

            <template v-slot:item.current_stock="{ item }">
              <v-chip
                :color="getStockColor(item.current_stock, item.min_stock)"
                size="small"
                variant="flat"
              >
                {{ item.current_stock }} {{ item.unit_symbol }}
              </v-chip>
            </template>

            <template v-slot:item.actions="{ item }">
              <v-btn
                icon="mdi-cart-plus"
                size="small"
                color="primary"
                variant="text"
                :disabled="isProductInCart(item.id) || item.current_stock <= 0"
                @click="addProductToCart(item)"
              ></v-btn>
            </template>
          </v-data-table>

          <div v-else class="d-flex justify-center align-center" style="height: 100%">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
          </div>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" variant="text" @click="productDialog = false">بستن</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- دیالوگ افزودن مشتری جدید -->
    <v-dialog v-model="customerDialog" max-width="600px" persistent>
      <v-card>
        <v-card-title class="text-h5">افزودن مشتری جدید</v-card-title>
        <v-card-text>
          <v-form ref="customerForm" @submit.prevent="saveCustomer">
            <v-text-field
              v-model="newCustomer.name"
              label="نام مشتری"
              variant="outlined"
              density="comfortable"
              :rules="[v => !!v || 'نام مشتری الزامی است']"
              class="mb-4"
            ></v-text-field>

            <v-text-field
              v-model="newCustomer.phone"
              label="شماره تماس"
              variant="outlined"
              density="comfortable"
              class="mb-4"
            ></v-text-field>

            <v-text-field
              v-model="newCustomer.email"
              label="ایمیل"
              variant="outlined"
              density="comfortable"
              class="mb-4"
            ></v-text-field>

            <v-textarea
              v-model="newCustomer.address"
              label="آدرس"
              variant="outlined"
              density="comfortable"
              rows="3"
            ></v-textarea>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" variant="text" @click="customerDialog = false">انصراف</v-btn>
          <v-btn 
            color="primary" 
            variant="elevated" 
            :loading="customersLoading"
            @click="saveCustomer"
          >
            ذخیره
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useProductsStore } from '../../store/products';
import { useCustomersStore } from '../../store/customers';
import { useSalesStore } from '../../store/sales';

// روتر برای هدایت کاربر
const router = useRouter();

// استورها
const productsStore = useProductsStore();
const customersStore = useCustomersStore();
const salesStore = useSalesStore();

// فرم
const form = ref(null);
const customerForm = ref(null);
const loading = ref(false);

// دیالوگ‌ها
const dateMenu = ref(false);
const productDialog = ref(false);
const customerDialog = ref(false);

// جستجوی محصول
const productSearchQuery = ref('');
const filteredProducts = ref([]);

// مشتری جدید
const newCustomer = ref({
  name: '',
  phone: '',
  email: '',
  address: ''
});

// اطلاعات فروش
const sale = ref({
  invoice_number: generateInvoiceNumber(),
  customer: null,
  date: new Date().toISOString().substr(0, 10),
  payment_method: 'cash',
  tax_percent: 9, // مالیات بر ارزش افزوده
  notes: '',
  items: [],
  paid_amount: 0,
  print_after_save: true
});

// روش‌های پرداخت
const paymentMethods = [
  { title: 'نقدی', value: 'cash' },
  { title: 'کارت بانکی', value: 'card' },
  { title: 'انتقال وجه', value: 'transfer' },
  { title: 'چک', value: 'cheque' }
];

// هدرهای جدول محصولات
const productHeaders = [
  { title: 'تصویر', key: 'image', align: 'center', sortable: false },
  { title: 'نام محصول', key: 'name', align: 'start', sortable: true },
  { title: 'قیمت فروش', key: 'selling_price', align: 'center', sortable: true },
  { title: 'موجودی', key: 'current_stock', align: 'center', sortable: true },
  { title: 'افزودن', key: 'actions', align: 'center', sortable: false }
];

// دریافت داده‌ها از استور
const products = computed(() => productsStore.products);
const customers = computed(() => customersStore.customers);
const productsLoading = computed(() => productsStore.loading);
const customersLoading = computed(() => customersStore.loading);

// تولید شماره فاکتور
function generateInvoiceNumber() {
  const date = new Date();
  const year = date.getFullYear().toString().substring(2);
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const day = date.getDate().toString().padStart(2, '0');
  const random = Math.floor(Math.random() * 9000 + 1000);
  return `INV-${year}${month}${day}-${random}`;
}

// فرمت‌کننده قیمت
const formatPrice = (price) => {
  return new Intl.NumberFormat('fa-IR').format(price);
};

// رنگ برای نمایش وضعیت موجودی
const getStockColor = (stock, minStock) => {
  if (stock <= 0) return 'error';
  if (stock <= minStock) return 'warning';
  return 'success';
};

// بررسی اینکه آیا محصول در سبد خرید هست یا نه
const isProductInCart = (productId) => {
  return sale.value.items.some(item => item.product.id === productId);
};

// باز کردن دیالوگ انتخاب محصول
const openProductSelector = async () => {
  // اگر محصولات قبلاً لود نشده‌اند، آنها را لود کن
  if (products.value.length === 0) {
    await productsStore.fetchProducts();
  }
  
  // تنظیم لیست محصولات فیلتر شده
  filteredProducts.value = [...products.value];
  productSearchQuery.value = '';
  productDialog.value = true;
};

// جستجوی محصولات
const searchProducts = () => {
  if (!productSearchQuery.value) {
    filteredProducts.value = [...products.value];
    return;
  }
  
  const query = productSearchQuery.value.toLowerCase();
  filteredProducts.value = products.value.filter(
    product => product.name.toLowerCase().includes(query) || 
               product.code.toLowerCase().includes(query)
  );
};

// افزودن محصول به سبد خرید
const addProductToCart = (product) => {
  // بررسی این که محصول قبلاً در سبد خرید هست یا نه
  if (isProductInCart(product.id)) {
    return;
  }
  
  // افزودن محصول به لیست با مقادیر پیش‌فرض
  sale.value.items.push({
    product: product,
    quantity: 1,
    unit_price: product.selling_price,
    discount_percent: 0,
    total_price: product.selling_price
  });
  
  // بستن دیالوگ
  productDialog.value = false;
};

// محاسبه قیمت کل یک آیتم
const calculateItemTotal = (item) => {
  if (!item.quantity || !item.unit_price) {
    item.total_price = 0;
    return;
  }
  
  // محاسبه قیمت با در نظر گرفتن تخفیف
  const discount = (item.discount_percent || 0) / 100;
  item.total_price = item.quantity * item.unit_price * (1 - discount);
};

// حذف آیتم از سبد خرید
const removeItem = (index) => {
  sale.value.items.splice(index, 1);
};

// محاسبه جمع کل قبل از تخفیف
const calculateSubtotal = () => {
  return sale.value.items.reduce((sum, item) => {
    return sum + (item.quantity * item.unit_price);
  }, 0);
};

// محاسبه میزان تخفیف کل
const calculateTotalDiscount = () => {
  return sale.value.items.reduce((sum, item) => {
    const discount = (item.discount_percent || 0) / 100;
    return sum + (item.quantity * item.unit_price * discount);
  }, 0);
};

// محاسبه مالیات
const calculateTax = () => {
  const subtotal = calculateSubtotal() - calculateTotalDiscount();
  return subtotal * (sale.value.tax_percent / 100);
};

// محاسبه مبلغ کل
const calculateTotal = () => {
  const subtotal = calculateSubtotal();
  const discount = calculateTotalDiscount();
  const tax = calculateTax();
  return subtotal - discount + tax;
};

// باز کردن دیالوگ افزودن مشتری جدید
const openNewCustomerDialog = () => {
  newCustomer.value = {
    name: '',
    phone: '',
    email: '',
    address: ''
  };
  customerDialog.value = true;
};

// ذخیره مشتری جدید
const saveCustomer = async () => {
  const { valid } = await customerForm.value.validate();
  
  if (!valid) return;
  
  try {
    const customer = await customersStore.addCustomer(newCustomer.value);
    if (customer) {
      sale.value.customer = customer;
      customerDialog.value = false;
    }
  } catch (error) {
    console.error('Error saving customer:', error);
  }
};

// ثبت فاکتور فروش
const saveSale = async () => {
  const { valid } = await form.value.validate();
  
  if (!valid) return;
  
  if (sale.value.items.length === 0) {
    alert('لطفاً حداقل یک محصول به فاکتور اضافه کنید.');
    return;
  }
  
  loading.value = true;
  
  try {
    // آماده‌سازی داده‌ها برای ارسال به سرور
    const saleData = {
      customer: sale.value.customer?.id,
      invoice_number: sale.value.invoice_number,
      date: sale.value.date,
      payment_method: sale.value.payment_method,
      tax_percent: sale.value.tax_percent,
      notes: sale.value.notes,
      paid_amount: sale.value.paid_amount || 0,
      items: sale.value.items.map(item => ({
        product: item.product.id,
        quantity: item.quantity,
        unit_price: item.unit_price,
        discount_percent: item.discount_percent || 0
      }))
    };
    
    const result = await salesStore.addSale(saleData);
    
    if (result) {
      // اگر چاپ فاکتور فعال است، فاکتور را چاپ کن
      if (sale.value.print_after_save) {
        printInvoice(result);
      }
      
      // برگشت به صفحه لیست فروش‌ها
      router.push({ path: '/sales', query: { success: 'true' } });
    }
  } catch (error) {
    console.error('Error saving sale:', error);
  } finally {
    loading.value = false;
  }
};

// چاپ فاکتور
const printInvoice = (sale) => {
  // ایجاد صفحه چاپ
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
            <p><strong>تاریخ:</strong> ${sale.date}</p>
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
              <th>تخفیف</th>
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
                <td>${item.discount_percent || 0}%</td>
                <td>${formatPrice(item.total_price)}</td>
              </tr>
            `).join('')}
          </tbody>
          <tfoot>
            <tr>
              <td colspan="6" class="text-right">جمع کل:</td>
              <td>${formatPrice(calculateSubtotal())}</td>
            </tr>
            <tr>
              <td colspan="6" class="text-right">تخفیف:</td>
              <td>${formatPrice(calculateTotalDiscount())}</td>
            </tr>
            <tr>
              <td colspan="6" class="text-right">مالیات (${sale.tax_percent}%):</td>
              <td>${formatPrice(calculateTax())}</td>
            </tr>
            <tr class="total-row">
              <td colspan="6" class="text-right">مبلغ قابل پرداخت:</td>
              <td>${formatPrice(calculateTotal())}</td>
            </tr>
            <tr>
              <td colspan="6" class="text-right">مبلغ پرداخت شده:</td>
              <td>${formatPrice(sale.paid_amount || 0)}</td>
            </tr>
            <tr>
              <td colspan="6" class="text-right">مانده حساب:</td>
              <td>${formatPrice(calculateTotal() - (sale.paid_amount || 0))}</td>
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

// بازنشانی فرم
const resetForm = () => {
  // پرسیدن از کاربر برای تایید
  if (sale.value.items.length > 0) {
    if (!confirm('آیا مطمئن هستید که می‌خواهید فرم را بازنشانی کنید؟ تمام اطلاعات وارد شده از بین خواهد رفت.')) {
      return;
    }
  }
  
  // بازنشانی فرم
  sale.value = {
    invoice_number: generateInvoiceNumber(),
    customer: null,
    date: new Date().toISOString().substr(0, 10),
    payment_method: 'cash',
    tax_percent: 9,
    notes: '',
    items: [],
    paid_amount: 0,
    print_after_save: true
  };
  
  // بازنشانی validations
  if (form.value) {
    form.value.resetValidation();
  }
};

// دریافت داده‌های اولیه
onMounted(async () => {
  // دریافت لیست مشتریان
  if (customers.value.length === 0) {
    await customersStore.fetchCustomers();
  }
});
</script>

<style scoped>
.sticky-card {
  position: sticky;
  top: 20px;
}

@media (max-width: 1264px) {
  .sticky-card {
    position: static;
  }
}
</style> 