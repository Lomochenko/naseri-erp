import { defineStore } from 'pinia';
import axiosInstance from '../utils/axios';
import { useInventoryStore } from './inventory';
import { ref, computed } from 'vue';

export const useSalesStore = defineStore('sales', () => {
  // حالت‌ها (State)
  const sales = ref([]);
  const saleDetails = ref({});
  const loading = ref(false);
  const error = ref(null);
  const currentPage = ref(1);
  const totalPages = ref(1);
  const totalItems = ref(0);
  const itemsPerPage = ref(10);
  const filters = ref({
    search: '',
    customer: null,
    dateFrom: null,
    dateTo: null,
    minAmount: null,
    maxAmount: null,
    status: null,
    sortBy: 'date',
    sortDesc: true
  });

  // گترها (Getters)
  const getSaleById = computed(() => {
    return (id) => {
      // ابتدا در جزئیات ذخیره شده بررسی کنید
      if (saleDetails.value[id]) {
        return saleDetails.value[id];
      }
      // سپس در لیست فروش‌ها بررسی کنید
      return sales.value.find(sale => sale.id === id);
    };
  });

  const groupedByDate = computed(() => {
    const grouped = {};
    sales.value.forEach(sale => {
      const date = new Date(sale.date).toLocaleDateString('fa-IR');
      if (!grouped[date]) {
        grouped[date] = [];
      }
      grouped[date].push(sale);
    });
    return grouped;
  });

  const totalSalesAmount = computed(() => {
    return sales.value.reduce((total, sale) => total + sale.total_amount, 0);
  });

  // اکشن‌ها (Actions)
  // دریافت لیست فروش‌ها
  const fetchSales = async (params = {}) => {
    loading.value = true;
    error.value = null;
    
    try {
      const queryParams = {
        page: params.page || currentPage.value,
        limit: params.limit || itemsPerPage.value,
        search: params.search !== undefined ? params.search : filters.value.search,
        customer: params.customer !== undefined ? params.customer : filters.value.customer,
        date_from: params.dateFrom || filters.value.dateFrom,
        date_to: params.dateTo || filters.value.dateTo,
        min_amount: params.minAmount || filters.value.minAmount,
        max_amount: params.maxAmount || filters.value.maxAmount,
        status: params.status || filters.value.status,
        sort_by: params.sortBy || filters.value.sortBy,
        sort_desc: params.sortDesc !== undefined ? params.sortDesc : filters.value.sortDesc,
      };
      
      console.log('Fetching sales with params:', queryParams);
      
      const response = await axiosInstance.get('/api/sales/sales/', { params: queryParams });
      
      sales.value = response.data.results || response.data;
      
      // اگر API پاسخ صفحه‌بندی می‌دهد، آن را پردازش کن
      if (response.data.count !== undefined) {
        totalItems.value = response.data.count;
        totalPages.value = Math.ceil(response.data.count / itemsPerPage.value);
        currentPage.value = params.page || currentPage.value;
      }
      
      console.log(`Loaded ${sales.value.length} sales successfully`);
      return response.data;
    } catch (err) {
      console.error('Error fetching sales:', err);
      error.value = err.response?.data?.detail || 'خطا در دریافت لیست فروش‌ها';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // دریافت اطلاعات یک فروش
  const fetchSaleDetail = async (id) => {
    loading.value = true;
    error.value = null;
    
    try {
      console.log(`Fetching sale details for ID: ${id}`);
      const response = await axiosInstance.get(`/api/sales/sales/${id}/`);
      
      // ذخیره جزئیات در آبجکت جزئیات
      saleDetails.value[id] = response.data;
      
      // به‌روزرسانی در لیست اصلی اگر وجود داشته باشد
      const index = sales.value.findIndex(s => s.id === id);
      if (index !== -1) {
        sales.value[index] = response.data;
      }
      
      console.log('Sale details loaded:', response.data);
      return response.data;
    } catch (err) {
      console.error(`Error fetching sale ${id}:`, err);
      error.value = err.response?.data?.detail || 'خطا در دریافت اطلاعات فروش';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // افزودن فروش جدید
  const addSale = async (saleData) => {
    loading.value = true;
    error.value = null;
    
    try {
      console.log('Adding new sale:', saleData);
      const response = await axiosInstance.post('/api/sales/sales/', saleData);
      
      // افزودن فروش جدید به لیست
      sales.value.unshift(response.data);
      
      // ذخیره جزئیات
      saleDetails.value[response.data.id] = response.data;
      
      console.log('Sale added successfully:', response.data);
      return response.data;
    } catch (err) {
      console.error('Error adding sale:', err);
      error.value = err.response?.data?.detail || 'خطا در ثبت فروش جدید';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // به‌روزرسانی اطلاعات فروش
  const updateSale = async (id, saleData) => {
    loading.value = true;
    error.value = null;
    
    try {
      console.log(`Updating sale ${id}:`, saleData);
      const response = await axiosInstance.put(`/api/sales/sales/${id}/`, saleData);
      
      // به‌روزرسانی در لیست اصلی
      const index = sales.value.findIndex(s => s.id === id);
      if (index !== -1) {
        sales.value[index] = response.data;
      }
      
      // به‌روزرسانی در جزئیات
      saleDetails.value[id] = response.data;
      
      console.log('Sale updated successfully:', response.data);
      return response.data;
    } catch (err) {
      console.error(`Error updating sale ${id}:`, err);
      error.value = err.response?.data?.detail || 'خطا در به‌روزرسانی اطلاعات فروش';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // حذف فروش
  const deleteSale = async (id) => {
    loading.value = true;
    error.value = null;
    
    try {
      console.log(`Deleting sale ${id}`);
      await axiosInstance.delete(`/api/sales/sales/${id}/`);
      
      // حذف از لیست اصلی
      sales.value = sales.value.filter(s => s.id !== id);
      
      // حذف از جزئیات
      delete saleDetails.value[id];
      
      console.log(`Sale ${id} deleted successfully`);
      return true;
    } catch (err) {
      console.error(`Error deleting sale ${id}:`, err);
      error.value = err.response?.data?.detail || 'خطا در حذف فروش';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // به‌روزرسانی وضعیت فروش
  const updateSaleStatus = async (id, status) => {
    loading.value = true;
    error.value = null;
    
    try {
      console.log(`Updating sale ${id} status to ${status}`);
      const response = await axiosInstance.patch(`/api/sales/sales/${id}/`, {
        status
      });
      
      // به‌روزرسانی در لیست اصلی
      const index = sales.value.findIndex(s => s.id === id);
      if (index !== -1) {
        sales.value[index].status = status;
      }
      
      // به‌روزرسانی در جزئیات اگر وجود داشته باشد
      if (saleDetails.value[id]) {
        saleDetails.value[id].status = status;
      }
      
      console.log(`Sale ${id} status updated successfully`);
      return response.data;
    } catch (err) {
      console.error(`Error updating sale ${id} status:`, err);
      error.value = err.response?.data?.detail || 'خطا در به‌روزرسانی وضعیت فروش';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // دریافت گزارش فروش
  const fetchSaleReport = async (params = {}) => {
    loading.value = true;
    error.value = null;
    
    try {
      console.log('Fetching sales report with params:', params);
      const response = await axiosInstance.get('/api/sales/report/', { params });
      
      console.log('Sales report loaded successfully:', response.data);
      return response.data;
    } catch (err) {
      console.error('Error fetching sales report:', err);
      error.value = err.response?.data?.detail || 'خطا در دریافت گزارش فروش';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // به‌روزرسانی فیلترها
  const updateFilters = (newFilters) => {
    filters.value = { ...filters.value, ...newFilters };
    // بازگشت به صفحه اول هنگام تغییر فیلترها
    currentPage.value = 1;
  };

  // تنظیم صفحه فعلی
  const setPage = (page) => {
    currentPage.value = page;
  };

  // تنظیم تعداد آیتم‌ها در هر صفحه
  const setItemsPerPage = (limit) => {
    itemsPerPage.value = limit;
    // بازگشت به صفحه اول هنگام تغییر تعداد آیتم‌ها
    currentPage.value = 1;
  };

  // بازنشانی فیلترها
  const resetFilters = () => {
    filters.value = {
      search: '',
      customer: null,
      dateFrom: null,
      dateTo: null,
      minAmount: null,
      maxAmount: null,
      status: null,
      sortBy: 'date',
      sortDesc: true
    };
    currentPage.value = 1;
  };

  return {
    // حالت‌ها
    sales,
    saleDetails,
    loading,
    error,
    currentPage,
    totalPages,
    totalItems,
    itemsPerPage,
    filters,
    
    // گترها
    getSaleById,
    groupedByDate,
    totalSalesAmount,
    
    // اکشن‌ها
    fetchSales,
    fetchSaleDetail,
    addSale,
    updateSale,
    deleteSale,
    updateSaleStatus,
    fetchSaleReport,
    updateFilters,
    setPage,
    setItemsPerPage,
    resetFilters
  };
}); 