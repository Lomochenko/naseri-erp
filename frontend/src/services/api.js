import axios from 'axios'

// Base API configuration
const API_BASE_URL = 'http://127.0.0.1:8000/api'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user_data')
      window.location.href = '/signin'
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  login: (phone, password) => api.post('/users/login/', { phone_number: phone, password }),
  logout: () => api.post('/users/logout/'),
  getCurrentUser: () => api.get('/users/profile/'),
}

// Products API
export const productsAPI = {
  getCategories: () => api.get('/products/categories/'),
  createCategory: (data) => api.post('/products/categories/', data),
  updateCategory: (id, data) => api.put(`/products/categories/${id}/`, data),
  deleteCategory: (id) => api.delete(`/products/categories/${id}/`),

  getUnits: () => api.get('/products/units/'),
  createUnit: (data) => api.post('/products/units/', data),

  getProducts: (params = {}) => api.get('/products/products/', { params }),
  createProduct: (data) => api.post('/products/products/', data),
  updateProduct: (id, data) => api.put(`/products/products/${id}/`, data),
  deleteProduct: (id) => api.delete(`/products/products/${id}/`),
  getProduct: (id) => api.get(`/products/products/${id}/`),
}

// Sales API
export const salesAPI = {
  getCustomers: (params = {}) => api.get('/sales/customers/', { params }),
  createCustomer: (data) => api.post('/sales/customers/', data),
  updateCustomer: (id, data) => api.put(`/sales/customers/${id}/`, data),
  deleteCustomer: (id) => api.delete(`/sales/customers/${id}/`),

  getSalesOrders: (params = {}) => api.get('/sales/sales-orders/', { params }),
  createSalesOrder: (data) => api.post('/sales/sales-orders/', data),
  updateSalesOrder: (id, data) => api.put(`/sales/sales-orders/${id}/`, data),
  deleteSalesOrder: (id) => api.delete(`/sales/sales-orders/${id}/`),

  getInvoices: (params = {}) => api.get('/sales/invoices/', { params }),
  createInvoice: (data) => api.post('/sales/invoices/', data),

  getPayments: (params = {}) => api.get('/sales/payments/', { params }),
  createPayment: (data) => api.post('/sales/payments/', data),
}

// Inventory API
export const inventoryAPI = {
  getWarehouses: () => api.get('/inventory/warehouses/'),
  createWarehouse: (data) => api.post('/inventory/warehouses/', data),

  getTransactions: (params = {}) => api.get('/inventory/transactions/', { params }),
  createTransaction: (data) => api.post('/inventory/transactions/', data),

  getStockLevels: (params = {}) => api.get('/inventory/stock-levels/', { params }),

  getAdjustments: (params = {}) => api.get('/inventory/adjustments/', { params }),
  createAdjustment: (data) => api.post('/inventory/adjustments/', data),
}

// Purchases API
export const purchasesAPI = {
  getSuppliers: (params = {}) => api.get('/purchases/suppliers/', { params }),
  createSupplier: (data) => api.post('/purchases/suppliers/', data),
  updateSupplier: (id, data) => api.put(`/purchases/suppliers/${id}/`, data),
  deleteSupplier: (id) => api.delete(`/purchases/suppliers/${id}/`),

  getPurchaseOrders: (params = {}) => api.get('/purchases/purchase-orders/', { params }),
  createPurchaseOrder: (data) => api.post('/purchases/purchase-orders/', data),

  getInvoices: (params = {}) => api.get('/purchases/invoices/', { params }),
  createInvoice: (data) => api.post('/purchases/invoices/', data),

  getPayments: (params = {}) => api.get('/purchases/payments/', { params }),
  createPayment: (data) => api.post('/purchases/payments/', data),
}

// Accounting API
export const accountingAPI = {
  getAccounts: () => api.get('/accounting/accounts/'),
  createAccount: (data) => api.post('/accounting/accounts/', data),

  getJournalEntries: (params = {}) => api.get('/accounting/journal-entries/', { params }),
  createJournalEntry: (data) => api.post('/accounting/journal-entries/', data),

  getTrialBalance: () => api.get('/accounting/trial-balance/'),
  getIncomeStatement: (params = {}) => api.get('/accounting/income-statement/', { params }),
  getBalanceSheet: (params = {}) => api.get('/accounting/balance-sheet/', { params }),
}

export default api
