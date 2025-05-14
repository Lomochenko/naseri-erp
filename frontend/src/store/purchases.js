import { defineStore } from 'pinia';
import axiosInstance from '../utils/axios';
import { useInventoryStore } from './inventory';

export const usePurchasesStore = defineStore('purchases', {
  state: () => ({
    purchases: [],
    suppliers: [],
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
    
    // سبد خرید موقت برای ثبت خرید جدید
    cart: {
      supplier: null,
      payment_method: 'CASH',
      status: 'PAID',
      notes: '',
      discount: 0,
      tax_percent: 9,
      items: []
    }
  }),
  
  getters: {
    getPurchaseById: (state) => (id) => {
      return state.purchases.find(purchase => purchase.id === id);
    },
    
    getPurchasesByStatus: (state) => (status) => {
      return state.purchases.filter(purchase => purchase.status === status);
    },
    
    getPurchasesBySupplier: (state) => (supplierId) => {
      return state.purchases.filter(purchase => purchase.supplier.id === supplierId);
    },
    
    getSupplierById: (state) => (id) => {
      return state.suppliers.find(supplier => supplier.id === id);
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
    // دریافت لیست خریدها
    async fetchPurchases() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.get('/api/purchases/purchases/', {
          params: {
            search: this.filters.search,
            status: this.filters.status,
            date_from: this.filters.date_from,
            date_to: this.filters.date_to,
            page: this.pagination.page,
            page_size: this.pagination.itemsPerPage
          }
        });
        
        this.purchases = response.data.results;
        this.pagination.totalItems = response.data.count;
        this.pagination.totalPages = Math.ceil(response.data.count / this.pagination.itemsPerPage);
        return this.purchases;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در دریافت لیست خریدها';
        console.error('Error fetching purchases:', error);
        return [];
      } finally {
        this.loading = false;
      }
    },
    
    // دریافت جزئیات یک خرید
    async fetchPurchaseDetail(purchaseId) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.get(`/api/purchases/purchases/${purchaseId}/`);
        
        // به‌روزرسانی خرید در آرایه خریدها
        const index = this.purchases.findIndex(p => p.id === purchaseId);
        if (index !== -1) {
          this.purchases[index] = response.data;
        } else {
          this.purchases.push(response.data);
        }
        
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در دریافت جزئیات خرید';
        console.error('Error fetching purchase details:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // دریافت لیست تامین‌کنندگان
    async fetchSuppliers() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.get('/api/purchases/suppliers/');
        this.suppliers = response.data.results;
        return this.suppliers;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در دریافت لیست تامین‌کنندگان';
        console.error('Error fetching suppliers:', error);
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
        supplier: null,
        payment_method: 'CASH',
        status: 'PAID',
        notes: '',
        discount: 0,
        tax_percent: 9,
        items: []
      };
    },
    
    // ثبت خرید جدید
    async createPurchase() {
      this.loading = true;
      this.error = null;
      
      try {
        // ساخت داده‌های خرید برای ارسال به سرور
        const purchaseData = {
          supplier: this.cart.supplier.id,
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
        
        const response = await axiosInstance.post('/api/purchases/purchases/', purchaseData);
        
        // افزایش موجودی محصولات خریداری شده
        const inventoryStore = useInventoryStore();
        for (const item of this.cart.items) {
          await inventoryStore.addInventory({
            product: item.product.id,
            warehouse: 1, // انبار پیش‌فرض
            quantity: item.quantity,
            notes: `خرید از ${this.cart.supplier.name} - سند: ${response.data.reference_number}`
          });
        }
        
        // افزودن خرید جدید به لیست خریدها
        this.purchases.unshift(response.data);
        
        // پاک کردن سبد خرید
        this.clearCart();
        
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در ثبت خرید';
        console.error('Error creating purchase:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // ویرایش خرید
    async updatePurchase(purchaseId, purchaseData) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.put(`/api/purchases/purchases/${purchaseId}/`, purchaseData);
        
        // به‌روزرسانی خرید در آرایه خریدها
        const index = this.purchases.findIndex(p => p.id === purchaseId);
        if (index !== -1) {
          this.purchases[index] = response.data;
        }
        
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در ویرایش خرید';
        console.error('Error updating purchase:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // تغییر وضعیت خرید
    async updatePurchaseStatus(purchaseId, status) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.patch(`/api/purchases/purchases/${purchaseId}/`, {
          status
        });
        
        // به‌روزرسانی وضعیت خرید در آرایه خریدها
        const index = this.purchases.findIndex(p => p.id === purchaseId);
        if (index !== -1) {
          this.purchases[index].status = status;
        }
        
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در تغییر وضعیت خرید';
        console.error('Error updating purchase status:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // حذف خرید
    async deletePurchase(purchaseId) {
      this.loading = true;
      this.error = null;
      
      try {
        await axiosInstance.delete(`/api/purchases/purchases/${purchaseId}/`);
        
        // حذف خرید از آرایه خریدها
        this.purchases = this.purchases.filter(p => p.id !== purchaseId);
        
        return true;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در حذف خرید';
        console.error('Error deleting purchase:', error);
        return false;
      } finally {
        this.loading = false;
      }
    },
    
    // افزودن تامین‌کننده جدید
    async addSupplier(supplierData) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.post('/api/purchases/suppliers/', supplierData);
        this.suppliers.push(response.data);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در افزودن تامین‌کننده';
        console.error('Error adding supplier:', error);
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