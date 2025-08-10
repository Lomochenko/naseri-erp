import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { inventoryAPI } from '../services/api'

export const useInventoryStore = defineStore('inventory', () => {
  // State
  const warehouses = ref([])
  const transactions = ref([])
  const stockLevels = ref([])
  const adjustments = ref([])
  const currentWarehouse = ref(null)
  const isLoading = ref(false)
  const error = ref(null)
  const pagination = ref({
    count: 0,
    next: null,
    previous: null,
    page: 1,
    pageSize: 20
  })

  // Initialize empty state - data will be loaded from API
  const initializeData = () => {
    // This function can be used for any initial setup if needed
    // Real data will be loaded from the API
  }

  // Getters - computed from real stock data
  const totalWarehouses = computed(() => warehouses.value.length)
  const totalProducts = computed(() => {
    return stockLevels.value.length
  })
  const inStockProducts = computed(() => {
    return stockLevels.value.filter(item => item.current_stock > 0).length
  })
  const lowStockProducts = computed(() => {
    return stockLevels.value.filter(item => 
      item.current_stock > 0 && item.current_stock <= item.min_stock
    ).length
  })
  const outOfStockProducts = computed(() => {
    return stockLevels.value.filter(item => item.current_stock <= 0).length
  })

  // Warehouse Actions
  const fetchWarehouses = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await inventoryAPI.getWarehouses()
      warehouses.value = response.data.results || response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در دریافت انبارها'
      console.error('Fetch warehouses error:', err)
    } finally {
      isLoading.value = false
    }
  }

  const createWarehouse = async (warehouseData) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await inventoryAPI.createWarehouse(warehouseData)
      warehouses.value.unshift(response.data)
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در ایجاد انبار'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  // Transaction Actions
  const fetchTransactions = async (params = {}) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await inventoryAPI.getTransactions(params)
      transactions.value = response.data.results || response.data
      pagination.value = {
        count: response.data.count || transactions.value.length,
        next: response.data.next,
        previous: response.data.previous,
        page: params.page || 1,
        pageSize: params.page_size || 20
      }
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در دریافت تراکنش‌ها'
      console.error('Fetch transactions error:', err)
    } finally {
      isLoading.value = false
    }
  }

  const createTransaction = async (transactionData) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await inventoryAPI.createTransaction(transactionData)
      transactions.value.unshift(response.data)
      // Update stock levels after transaction
      await fetchStockLevels()
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در ایجاد تراکنش'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  // Stock Level Actions
  const fetchStockLevels = async (params = {}) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await inventoryAPI.getStockLevels(params)
      stockLevels.value = response.data.results || response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در دریافت سطح موجودی'
      console.error('Fetch stock levels error:', err)
    } finally {
      isLoading.value = false
    }
  }

  // Adjustment Actions
  const fetchAdjustments = async (params = {}) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await inventoryAPI.getAdjustments(params)
      adjustments.value = response.data.results || response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در دریافت تعدیلات'
      console.error('Fetch adjustments error:', err)
    } finally {
      isLoading.value = false
    }
  }

  const createAdjustment = async (adjustmentData) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await inventoryAPI.createAdjustment(adjustmentData)
      adjustments.value.unshift(response.data)
      // Update stock levels after adjustment
      await fetchStockLevels()
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در ایجاد تعدیل'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  // Helper Methods
  const getStockStatus = (quantity, minLevel = 10) => {
    if (quantity <= 0) return 'out_of_stock'
    if (quantity <= minLevel) return 'low_stock'
    return 'in_stock'
  }

  const getStockStatusText = (quantity, minLevel = 10) => {
    const status = getStockStatus(quantity, minLevel)
    switch (status) {
      case 'out_of_stock': return 'ناموجود'
      case 'low_stock': return 'موجودی کم'
      case 'in_stock': return 'موجود'
      default: return 'نامشخص'
    }
  }

  const getStockStatusClass = (quantity, minLevel = 10) => {
    const status = getStockStatus(quantity, minLevel)
    switch (status) {
      case 'out_of_stock': return 'text-danger'
      case 'low_stock': return 'text-warning'
      case 'in_stock': return 'text-success'
      default: return 'text-gray-500'
    }
  }

  const clearError = () => {
    error.value = null
  }

  const clearCurrentWarehouse = () => {
    currentWarehouse.value = null
  }

  return {
    // State
    warehouses,
    transactions,
    stockLevels,
    adjustments,
    currentWarehouse,
    isLoading,
    error,
    pagination,
    
    // Getters
    totalWarehouses,
    totalProducts,
    inStockProducts,
    lowStockProducts,
    outOfStockProducts,
    
    // Actions
    fetchWarehouses,
    createWarehouse,
    fetchTransactions,
    createTransaction,
    fetchStockLevels,
    fetchAdjustments,
    createAdjustment,
    
    // Helper Methods
    getStockStatus,
    getStockStatusText,
    getStockStatusClass,
    clearError,
    clearCurrentWarehouse,
  }
})
