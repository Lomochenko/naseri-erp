import { defineStore } from 'pinia';
import apiService from '../utils/apiService';
import { ref, computed } from 'vue';

export const useCustomersStore = defineStore('customers', () => {
  // حالت‌ها (State)
  const customers = ref([]);
  const loading = ref(false);
  const error = ref(null);
  const currentPage = ref(1);
  const totalPages = ref(1);
  const totalItems = ref(0);
  const itemsPerPage = ref(10);
  const filters = ref({
    search: '',
    sortBy: 'created_at',
    sortDesc: true
  });

  // گترها (Getters)
  const getCustomerById = computed(() => {
    return (id) => customers.value.find(customer => customer.id === id);
  });

  // اکشن‌ها (Actions)
  // دریافت لیست مشتریان
  const fetchCustomers = async (params = {}) => {
    loading.value = true;
    error.value = null;
    
    try {
      const queryParams = {
        page: params.page || currentPage.value,
        limit: params.limit || itemsPerPage.value,
        search: params.search !== undefined ? params.search : filters.value.search,
        sort_by: params.sortBy || filters.value.sortBy,
        sort_desc: params.sortDesc !== undefined ? params.sortDesc : filters.value.sortDesc
      };
      
      console.log('Fetching customers with params:', queryParams);
      
      const response = await apiService.get('/api/customers/', { params: queryParams });
      
      customers.value = response.data.results || response.data;
      
      // اگر API پاسخ صفحه‌بندی می‌دهد، آن را پردازش کن
      if (response.data.count !== undefined) {
        totalItems.value = response.data.count;
        totalPages.value = Math.ceil(response.data.count / itemsPerPage.value);
        currentPage.value = params.page || currentPage.value;
      }
      
      console.log(`Loaded ${customers.value.length} customers successfully`);
      return response.data;
    } catch (err) {
      console.error('Error fetching customers:', err);
      error.value = err.message || 'خطا در دریافت لیست مشتریان';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // دریافت اطلاعات یک مشتری
  const fetchCustomerDetail = async (id) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await apiService.get(`/api/customers/${id}/`);
      
      // به‌روزرسانی مشتری در لیست
      const index = customers.value.findIndex(c => c.id === id);
      if (index !== -1) {
        customers.value[index] = response.data;
      } else {
        customers.value.push(response.data);
      }
      
      return response.data;
    } catch (err) {
      console.error(`Error fetching customer ${id}:`, err);
      error.value = err.message || 'خطا در دریافت اطلاعات مشتری';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // افزودن مشتری جدید
  const addCustomer = async (customerData) => {
    loading.value = true;
    error.value = null;
    
    try {
      console.log('Adding new customer:', customerData);
      const response = await apiService.post('/api/customers/', customerData);
      
      // افزودن مشتری جدید به لیست
      customers.value.unshift(response.data);
      
      console.log('Customer added successfully:', response.data);
      return response.data;
    } catch (err) {
      console.error('Error adding customer:', err);
      error.value = err.message || 'خطا در افزودن مشتری جدید';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // به‌روزرسانی اطلاعات مشتری
  const updateCustomer = async (id, customerData) => {
    loading.value = true;
    error.value = null;
    
    try {
      console.log(`Updating customer ${id}:`, customerData);
      const response = await apiService.put(`/api/customers/${id}/`, customerData);
      
      // به‌روزرسانی مشتری در لیست
      const index = customers.value.findIndex(c => c.id === id);
      if (index !== -1) {
        customers.value[index] = response.data;
      }
      
      console.log('Customer updated successfully:', response.data);
      return response.data;
    } catch (err) {
      console.error(`Error updating customer ${id}:`, err);
      error.value = err.message || 'خطا در به‌روزرسانی اطلاعات مشتری';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // حذف مشتری
  const deleteCustomer = async (id) => {
    loading.value = true;
    error.value = null;
    
    try {
      console.log(`Deleting customer ${id}`);
      await apiService.delete(`/api/customers/${id}/`);
      
      // حذف مشتری از لیست
      customers.value = customers.value.filter(c => c.id !== id);
      
      console.log(`Customer ${id} deleted successfully`);
      return true;
    } catch (err) {
      console.error(`Error deleting customer ${id}:`, err);
      error.value = err.message || 'خطا در حذف مشتری';
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
      sortBy: 'created_at',
      sortDesc: true
    };
    currentPage.value = 1;
  };

  return {
    // حالت‌ها
    customers,
    loading,
    error,
    currentPage,
    totalPages,
    totalItems,
    itemsPerPage,
    filters,
    
    // گترها
    getCustomerById,
    
    // اکشن‌ها
    fetchCustomers,
    fetchCustomerDetail,
    addCustomer,
    updateCustomer,
    deleteCustomer,
    updateFilters,
    setPage,
    setItemsPerPage,
    resetFilters
  };
}); 