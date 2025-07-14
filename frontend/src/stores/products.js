import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { productsAPI } from '../services/api'

export const useProductsStore = defineStore('products', () => {
  // State
  const products = ref([])
  const categories = ref([])
  const units = ref([])
  const currentProduct = ref(null)
  const isLoading = ref(false)
  const error = ref(null)
  const pagination = ref({
    count: 0,
    next: null,
    previous: null,
    page: 1,
    pageSize: 20
  })

  // Getters
  const totalProducts = computed(() => pagination.value.count)
  const hasNextPage = computed(() => !!pagination.value.next)
  const hasPreviousPage = computed(() => !!pagination.value.previous)

  // Actions
  const fetchProducts = async (params = {}) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await productsAPI.getProducts(params)
      products.value = response.data.results
      pagination.value = {
        count: response.data.count,
        next: response.data.next,
        previous: response.data.previous,
        page: params.page || 1,
        pageSize: params.page_size || 20
      }
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در دریافت محصولات'
      console.error('Fetch products error:', err)
    } finally {
      isLoading.value = false
    }
  }

  const fetchCategories = async () => {
    try {
      const response = await productsAPI.getCategories()
      categories.value = response.data.results || response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در دریافت دسته‌بندی‌ها'
      console.error('Fetch categories error:', err)
    }
  }

  const fetchUnits = async () => {
    try {
      const response = await productsAPI.getUnits()
      units.value = response.data.results || response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در دریافت واحدها'
      console.error('Fetch units error:', err)
    }
  }

  const createProduct = async (productData) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await productsAPI.createProduct(productData)
      products.value.unshift(response.data)
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در ایجاد محصول'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const updateProduct = async (id, productData) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await productsAPI.updateProduct(id, productData)
      const index = products.value.findIndex(p => p.id === id)
      if (index !== -1) {
        products.value[index] = response.data
      }
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در به‌روزرسانی محصول'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const deleteProduct = async (id) => {
    isLoading.value = true
    error.value = null
    
    try {
      await productsAPI.deleteProduct(id)
      products.value = products.value.filter(p => p.id !== id)
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در حذف محصول'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const getProduct = async (id) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await productsAPI.getProduct(id)
      currentProduct.value = response.data
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در دریافت محصول'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const createCategory = async (categoryData) => {
    try {
      const response = await productsAPI.createCategory(categoryData)
      categories.value.push(response.data)
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در ایجاد دسته‌بندی'
      return { success: false, error: error.value }
    }
  }

  const createUnit = async (unitData) => {
    try {
      const response = await productsAPI.createUnit(unitData)
      units.value.push(response.data)
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || 'خطا در ایجاد واحد'
      return { success: false, error: error.value }
    }
  }

  const clearError = () => {
    error.value = null
  }

  const clearCurrentProduct = () => {
    currentProduct.value = null
  }

  return {
    // State
    products,
    categories,
    units,
    currentProduct,
    isLoading,
    error,
    pagination,
    
    // Getters
    totalProducts,
    hasNextPage,
    hasPreviousPage,
    
    // Actions
    fetchProducts,
    fetchCategories,
    fetchUnits,
    createProduct,
    updateProduct,
    deleteProduct,
    getProduct,
    createCategory,
    createUnit,
    clearError,
    clearCurrentProduct,
  }
})
