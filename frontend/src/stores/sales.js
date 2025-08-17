import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { salesAPI } from '../services/api'

export const useSalesStore = defineStore('sales', () => {
  // State
  const customers = ref([])
  const salesOrders = ref([])
  const invoices = ref([])
  const payments = ref([])
  const currentCustomer = ref(null)
  const currentSalesOrder = ref(null)
  const isLoading = ref(false)
  const error = ref(null)
  const pagination = ref({
    count: 0,
    next: null,
    previous: null,
    page: 1,
    pageSize: 20
  })
  const stats = ref({
    todaySales: 0,
    monthSales: 0,
    totalCustomers: 0,
    pendingOrders: 0
  })

  // Getters
  const totalCustomers = computed(() => customers.value.length)
  const totalSalesOrders = computed(() => salesOrders.value.length)
  const totalRevenue = computed(() => {
    return invoices.value.reduce((sum, invoice) => sum + parseFloat(invoice.total_amount || 0), 0)
  })

  // Customer Actions
  const fetchCustomers = async (params = {}) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await salesAPI.getCustomers(params)
      customers.value = response.data.results || response.data
      pagination.value = {
        count: response.data.count || customers.value.length,
        next: response.data.next,
        previous: response.data.previous,
        page: params.page || 1,
        pageSize: params.page_size || 20
      }
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در دریافت مشتریان'
      console.error('Fetch customers error:', err)
    } finally {
      isLoading.value = false
    }
  }

  const createCustomer = async (customerData) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await salesAPI.createCustomer(customerData)
      customers.value.unshift(response.data)
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در ایجاد مشتری'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const updateCustomer = async (id, customerData) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await salesAPI.updateCustomer(id, customerData)
      const index = customers.value.findIndex(c => c.id === id)
      if (index !== -1) {
        customers.value[index] = response.data
      }
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در به‌روزرسانی مشتری'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const deleteCustomer = async (id) => {
    isLoading.value = true
    error.value = null

    try {
      await salesAPI.deleteCustomer(id)
      customers.value = customers.value.filter(c => c.id !== id)
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در حذف مشتری'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  // Sales Order Actions
  const fetchSalesOrders = async (params = {}) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await salesAPI.getSalesOrders(params)
      salesOrders.value = response.data.results || response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در دریافت سفارشات فروش'
      console.error('Fetch sales orders error:', err)
    } finally {
      isLoading.value = false
    }
  }

  const createSalesOrder = async (orderData) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await salesAPI.createSalesOrder(orderData)
      salesOrders.value.unshift(response.data)
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در ایجاد سفارش فروش'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const updateSalesOrder = async (id, orderData) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await salesAPI.updateSalesOrder(id, orderData)
      const index = salesOrders.value.findIndex(o => o.id === id)
      if (index !== -1) {
        salesOrders.value[index] = response.data
      }
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در به‌روزرسانی سفارش فروش'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  // Invoice Actions
  const fetchInvoices = async (params = {}) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await salesAPI.getInvoices(params)
      invoices.value = response.data.results || response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در دریافت فاکتورها'
      console.error('Fetch invoices error:', err)
    } finally {
      isLoading.value = false
    }
  }

  const createInvoice = async (invoiceData) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await salesAPI.createInvoice(invoiceData)
      invoices.value.unshift(response.data)
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در ایجاد فاکتور'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  // Payment Actions
  const fetchPayments = async (params = {}) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await salesAPI.getPayments(params)
      payments.value = response.data.results || response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در دریافت پرداخت‌ها'
      console.error('Fetch payments error:', err)
    } finally {
      isLoading.value = false
    }
  }

  const createPayment = async (paymentData) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await salesAPI.createPayment(paymentData)
      payments.value.unshift(response.data)
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در ثبت پرداخت'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const clearError = () => {
    error.value = null
  }

  const clearCurrentCustomer = () => {
    currentCustomer.value = null
  }

  const clearCurrentSalesOrder = () => {
    currentSalesOrder.value = null
  }

  // Stats Actions
  const fetchStats = async () => {
    try {
      // For now, calculate stats from existing data
      const today = new Date().toISOString().split('T')[0]
      const thisMonth = new Date().toISOString().slice(0, 7)

      stats.value = {
        todaySales: salesOrders.value
          .filter(order => order.sale_date?.startsWith(today) && order.status === 'completed')
          .reduce((sum, order) => sum + (order.total || 0), 0),
        monthSales: salesOrders.value
          .filter(order => order.sale_date?.startsWith(thisMonth) && order.status === 'completed')
          .reduce((sum, order) => sum + (order.total || 0), 0),
        totalCustomers: customers.value.length,
        pendingOrders: salesOrders.value.filter(order => order.status === 'draft').length
      }
    } catch (err) {
      console.error('Error fetching stats:', err)
    }
  }

  return {
    // State
    customers,
    salesOrders,
    invoices,
    payments,
    currentCustomer,
    currentSalesOrder,
    isLoading,
    error,
    pagination,
    stats,

    // Getters
    totalCustomers,
    totalSalesOrders,
    totalRevenue,

    // Actions
    fetchCustomers,
    createCustomer,
    updateCustomer,
    deleteCustomer,
    fetchSalesOrders,
    createSalesOrder,
    updateSalesOrder,
    fetchInvoices,
    createInvoice,
    fetchPayments,
    createPayment,
    fetchStats,
    clearError,
    clearCurrentCustomer,
    clearCurrentSalesOrder,
  }
})
