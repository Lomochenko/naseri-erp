import { defineStore } from 'pinia';
import axiosInstance from '../utils/axios';
import { useInventoryStore } from './inventory';

export const useSalesStore = defineStore('sales', {
  state: () => ({
    sales: [],
    customers: [],
    loading: false,
    error: null,
    
    // فیلترهای جستجو
    filters: {
      search: '',
      status: null,
      date_from: null,
      date_to: null
    },
    
    // پیجینیشن
    pagination: {
      page: 1,
      itemsPerPage: 10,
      totalItems: 0,
      totalPages: 0
    },
    
    // سبد خرید موقت برای ثبت فروش جدید
    cart: {
      customer: null,
      payment_method: 'CASH',
      status: 'PAID',
      notes: '',
      discount: 0,
      tax_percent: 9,
      items: []
    }
  }),
  
  getters: {
    getSaleById: (state) => (id) => {
      return state.sales.find(sale => sale.id === id);
    },
    
    getSalesByStatus: (state) => (status) => {
      return state.sales.filter(sale => sale.status === status);
    },
    
    getSalesByCustomer: (state) => (customerId) => {
      return state.sales.filter(sale => sale.customer.id === customerId);
    },
    
    getCustomerById: (state) => (id) => {
      return state.customers.find(customer => customer.id === id);
    },
    
    // محاسبه جمع کل قیمت محصولات در سبد خرید
    cartSubtotal: (state) => {
      return state.cart.items.reduce((total, item) => {
        const itemTotal = item.unit_price * item.quantity * (1 - (item.discount || 0) / 100);
        return total + itemTotal;
      }, 0);
    },
    
    // محاسبه مبلغ مالیات
    cartTaxAmount: (state, getters) => {
      return Math.round(getters.cartSubtotal * (state.cart.tax_percent / 100));
    },
    
    // محاسبه مبلغ تخفیف کل
    cartDiscountAmount: (state, getters) => {
      return Math.round(getters.cartSubtotal * (state.cart.discount / 100));
    },
    
    // محاسبه مبلغ نهایی
    cartTotalAmount: (state, getters) => {
      return getters.cartSubtotal - getters.cartDiscountAmount + getters.cartTaxAmount;
    }
  },
  
  actions: {
    // دریافت لیست فروش‌ها
    async fetchSales() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.get('/api/sales/sales/', {
          params: {
            search: this.filters.search,
            status: this.filters.status,
            date_from: this.filters.date_from,
            date_to: this.filters.date_to,
            page: this.pagination.page,
            page_size: this.pagination.itemsPerPage
          }
        });
        
        this.sales = response.data.results;
        this.pagination.totalItems = response.data.count;
        this.pagination.totalPages = Math.ceil(response.data.count / this.pagination.itemsPerPage);
        return this.sales;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در دریافت لیست فروش‌ها';
        console.error('Error fetching sales:', error);
        return [];
      } finally {
        this.loading = false;
      }
    },
    
    // دریافت جزئیات یک فروش
    async fetchSaleDetail(saleId) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.get(`/api/sales/sales/${saleId}/`);
        
        // به‌روزرسانی فروش در آرایه فروش‌ها
        const index = this.sales.findIndex(s => s.id === saleId);
        if (index !== -1) {
          this.sales[index] = response.data;
        } else {
          this.sales.push(response.data);
        }
        
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در دریافت جزئیات فروش';
        console.error('Error fetching sale details:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // دریافت لیست مشتریان
    async fetchCustomers() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.get('/api/sales/customers/');
        this.customers = response.data.results;
        return this.customers;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در دریافت لیست مشتریان';
        console.error('Error fetching customers:', error);
        return [];
      } finally {
        this.loading = false;
      }
    },
    
    // افزودن محصول به سبد خرید
    addToCart(product, quantity, unitPrice, discount = 0) {
      // بررسی تکراری نبودن محصول در سبد خرید
      const existingIndex = this.cart.items.findIndex(item => item.product.id === product.id);
      
      if (existingIndex !== -1) {
        // به‌روزرسانی تعداد محصول تکراری
        this.cart.items[existingIndex].quantity += quantity;
        this.cart.items[existingIndex].unit_price = unitPrice;
        this.cart.items[existingIndex].discount = discount;
      } else {
        // افزودن محصول جدید به سبد خرید
        this.cart.items.push({
          product,
          quantity,
          unit_price: unitPrice,
          discount,
          total_price: quantity * unitPrice * (1 - (discount / 100))
        });
      }
    },
    
    // حذف محصول از سبد خرید
    removeFromCart(productId) {
      this.cart.items = this.cart.items.filter(item => item.product.id !== productId);
    },
    
    // تنظیم تعداد محصول در سبد خرید
    updateCartItemQuantity(productId, quantity) {
      const index = this.cart.items.findIndex(item => item.product.id === productId);
      if (index !== -1) {
        this.cart.items[index].quantity = quantity;
        this.cart.items[index].total_price = quantity * this.cart.items[index].unit_price * (1 - (this.cart.items[index].discount / 100));
      }
    },
    
    // پاک کردن سبد خرید
    clearCart() {
      this.cart = {
        customer: null,
        payment_method: 'CASH',
        status: 'PAID',
        notes: '',
        discount: 0,
        tax_percent: 9,
        items: []
      };
    },
    
    // ثبت فروش جدید
    async createSale() {
      this.loading = true;
      this.error = null;
      
      try {
        // ساخت داده‌های فروش برای ارسال به سرور
        const saleData = {
          customer: this.cart.customer.id,
          payment_method: this.cart.payment_method,
          status: this.cart.status,
          notes: this.cart.notes,
          discount: this.cart.discount,
          tax_percent: this.cart.tax_percent,
          items: this.cart.items.map(item => ({
            product: item.product.id,
            quantity: item.quantity,
            unit_price: item.unit_price,
            discount: item.discount
          }))
        };
        
        const response = await axiosInstance.post('/api/sales/sales/', saleData);
        
        // کاهش موجودی محصولات فروخته شده
        const inventoryStore = useInventoryStore();
        for (const item of this.cart.items) {
          await inventoryStore.removeInventory({
            product: item.product.id,
            warehouse: 1, // انبار پیش‌فرض
            quantity: item.quantity,
            notes: `فروش به ${this.cart.customer.name} - فاکتور: ${response.data.invoice_number}`
          });
        }
        
        // افزودن فروش جدید به لیست فروش‌ها
        this.sales.unshift(response.data);
        
        // پاک کردن سبد خرید
        this.clearCart();
        
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در ثبت فروش';
        console.error('Error creating sale:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // ویرایش فروش
    async updateSale(saleId, saleData) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.put(`/api/sales/sales/${saleId}/`, saleData);
        
        // به‌روزرسانی فروش در آرایه فروش‌ها
        const index = this.sales.findIndex(s => s.id === saleId);
        if (index !== -1) {
          this.sales[index] = response.data;
        }
        
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در ویرایش فروش';
        console.error('Error updating sale:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // تغییر وضعیت فروش
    async updateSaleStatus(saleId, status) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.patch(`/api/sales/sales/${saleId}/`, {
          status
        });
        
        // به‌روزرسانی وضعیت فروش در آرایه فروش‌ها
        const index = this.sales.findIndex(s => s.id === saleId);
        if (index !== -1) {
          this.sales[index].status = status;
        }
        
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در تغییر وضعیت فروش';
        console.error('Error updating sale status:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // حذف فروش
    async deleteSale(saleId) {
      this.loading = true;
      this.error = null;
      
      try {
        await axiosInstance.delete(`/api/sales/sales/${saleId}/`);
        
        // حذف فروش از آرایه فروش‌ها
        this.sales = this.sales.filter(s => s.id !== saleId);
        
        return true;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در حذف فروش';
        console.error('Error deleting sale:', error);
        return false;
      } finally {
        this.loading = false;
      }
    },
    
    // افزودن مشتری جدید
    async addCustomer(customerData) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.post('/api/sales/customers/', customerData);
        this.customers.push(response.data);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در افزودن مشتری';
        console.error('Error adding customer:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // به‌روزرسانی فیلترها
    updateFilters(newFilters) {
      this.filters = { ...this.filters, ...newFilters };
      this.pagination.page = 1; // بازگشت به صفحه اول با تغییر فیلترها
    },
    
    // تنظیم صفحه جاری
    setPage(page) {
      this.pagination.page = page;
    },
    
    // تنظیم تعداد آیتم در هر صفحه
    setItemsPerPage(count) {
      this.pagination.itemsPerPage = count;
      this.pagination.page = 1; // بازگشت به صفحه اول با تغییر تعداد آیتم‌ها
    },
    
    // بازنشانی فیلترها
    resetFilters() {
      this.filters = {
        search: '',
        status: null,
        date_from: null,
        date_to: null
      };
      this.pagination.page = 1;
    }
  }
}); 