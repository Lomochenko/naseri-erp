import { defineStore } from 'pinia';
import axiosInstance from '../utils/axios';

export const useInventoryStore = defineStore('inventory', {
  state: () => ({
    inventory: [],
    warehouses: [],
    transactionHistory: {},
    loading: false,
    error: null,
    
    // فیلترهای جستجو
    filters: {
      search: '',
      warehouse: null,
      lowStock: false
    },
    
    // پیجینیشن
    pagination: {
      page: 1,
      itemsPerPage: 10,
      totalItems: 0,
      totalPages: 0
    }
  }),
  
  getters: {
    getInventoryByProduct: (state) => (productId) => {
      return state.inventory.filter(item => item.product.id === productId);
    },
    
    getInventoryByWarehouse: (state) => (warehouseId) => {
      return state.inventory.filter(item => item.warehouse_id === warehouseId);
    },
    
    getLowStockItems: (state) => {
      return state.inventory.filter(item => item.quantity <= 10);
    },
    
    getCriticalStockItems: (state) => {
      return state.inventory.filter(item => item.quantity <= 5);
    },
    
    getTransactionHistoryByProduct: (state) => (productId) => {
      return state.transactionHistory[productId] || [];
    },
    
    getWarehouseById: (state) => (id) => {
      return state.warehouses.find(warehouse => warehouse.id === id);
    }
  },
  
  actions: {
    // دریافت لیست موجودی
    async fetchInventory() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.get('/api/inventory/inventory/', {
          params: {
            search: this.filters.search,
            warehouse: this.filters.warehouse,
            low_stock: this.filters.lowStock ? 1 : undefined,
            page: this.pagination.page,
            page_size: this.pagination.itemsPerPage
          }
        });
        
        this.inventory = response.data.results;
        this.pagination.totalItems = response.data.count;
        this.pagination.totalPages = Math.ceil(response.data.count / this.pagination.itemsPerPage);
        return this.inventory;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در دریافت لیست موجودی';
        console.error('Error fetching inventory:', error);
        return [];
      } finally {
        this.loading = false;
      }
    },
    
    // دریافت لیست انبارها
    async fetchWarehouses() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.get('/api/inventory/warehouses/');
        this.warehouses = response.data.results;
        return this.warehouses;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در دریافت لیست انبارها';
        console.error('Error fetching warehouses:', error);
        return [];
      } finally {
        this.loading = false;
      }
    },
    
    // دریافت تاریخچه تراکنش‌های یک محصول
    async fetchTransactionHistory(productId, warehouseId = null) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.get('/api/inventory/transactions/', {
          params: {
            product: productId,
            warehouse: warehouseId
          }
        });
        
        // ذخیره تاریخچه تراکنش‌ها در استور
        this.transactionHistory = {
          ...this.transactionHistory,
          [productId]: response.data.results
        };
        
        return response.data.results;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در دریافت تاریخچه تراکنش‌ها';
        console.error('Error fetching transaction history:', error);
        return [];
      } finally {
        this.loading = false;
      }
    },
    
    // ثبت ورود کالا به انبار
    async addInventory(inventoryData) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.post('/api/inventory/transactions/', {
          transaction_type: 'IN',
          ...inventoryData
        });
        
        // به‌روزرسانی موجودی در صورت نیاز
        await this.fetchInventory();
        
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در ثبت ورود کالا';
        console.error('Error adding inventory:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // ثبت خروج کالا از انبار
    async removeInventory(inventoryData) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.post('/api/inventory/transactions/', {
          transaction_type: 'OUT',
          ...inventoryData
        });
        
        // به‌روزرسانی موجودی در صورت نیاز
        await this.fetchInventory();
        
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در ثبت خروج کالا';
        console.error('Error removing inventory:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // تنظیم موجودی
    async adjustInventory(adjustmentData) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.post('/api/inventory/adjustments/', adjustmentData);
        
        // به‌روزرسانی موجودی در صورت نیاز
        await this.fetchInventory();
        
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در تنظیم موجودی';
        console.error('Error adjusting inventory:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // انتقال بین انبارها
    async transferInventory(transferData) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.post('/api/inventory/transfers/', transferData);
        
        // به‌روزرسانی موجودی در صورت نیاز
        await this.fetchInventory();
        
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در انتقال بین انبارها';
        console.error('Error transferring inventory:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // افزودن انبار جدید
    async addWarehouse(warehouseData) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.post('/api/inventory/warehouses/', warehouseData);
        this.warehouses.push(response.data);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در افزودن انبار';
        console.error('Error adding warehouse:', error);
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
        warehouse: null,
        lowStock: false
      };
      this.pagination.page = 1;
    }
  }
}); 