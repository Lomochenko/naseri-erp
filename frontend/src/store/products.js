import { defineStore } from 'pinia';
import { productsService, categoriesService, unitsService } from '../utils/apiService';

export const useProductsStore = defineStore('products', {
  state: () => ({
    products: [],
    categories: [],
    units: [],
    loading: false,
    error: null,
    
    // فیلترهای جستجو
    filters: {
      search: '',
      category: null,
      sortBy: 'name'
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
    getProductById: (state) => (id) => {
      return state.products.find(product => product.id === id);
    },
    
    getProductsByCategory: (state) => (categoryId) => {
      return state.products.filter(product => product.category.id === categoryId);
    },
    
    getLowStockProducts: (state) => {
      return state.products.filter(product => product.stock <= 10);
    },
    
    getCriticalStockProducts: (state) => {
      return state.products.filter(product => product.stock <= 5);
    },
    
    getCategoryById: (state) => (id) => {
      return state.categories.find(category => category.id === id);
    },
    
    getUnitById: (state) => (id) => {
      return state.units.find(unit => unit.id === id);
    }
  },
  
  actions: {
    // دریافت لیست محصولات
    async fetchProducts() {
      this.loading = true;
      this.error = null;
      
      try {
        const params = {
          search: this.filters.search,
          category: this.filters.category?.id,
          ordering: this.filters.sortBy,
          page: this.pagination.page,
          page_size: this.pagination.itemsPerPage
        };
        
        const response = await productsService.getList(params);
        
        this.products = response.results;
        this.pagination.totalItems = response.count;
        this.pagination.totalPages = Math.ceil(response.count / this.pagination.itemsPerPage);
        return this.products;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در دریافت لیست محصولات';
        console.error('Error fetching products:', error);
        return [];
      } finally {
        this.loading = false;
      }
    },
    
    // دریافت دسته‌بندی‌ها
    async fetchCategories() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await categoriesService.getList();
        this.categories = response.results;
        return this.categories;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در دریافت دسته‌بندی‌ها';
        console.error('Error fetching categories:', error);
        return [];
      } finally {
        this.loading = false;
      }
    },
    
    // دریافت واحدهای اندازه‌گیری
    async fetchUnits() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await unitsService.getList();
        this.units = response.results;
        return this.units;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در دریافت واحدها';
        console.error('Error fetching units:', error);
        return [];
      } finally {
        this.loading = false;
      }
    },
    
    // دریافت جزئیات یک محصول
    async fetchProductDetail(productId) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await productsService.getDetail(productId);
        
        // به‌روزرسانی محصول در آرایه محصولات
        const index = this.products.findIndex(p => p.id === productId);
        if (index !== -1) {
          this.products[index] = response;
        } else {
          this.products.push(response);
        }
        
        return response;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در دریافت جزئیات محصول';
        console.error('Error fetching product details:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // افزودن محصول جدید
    async addProduct(productData) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await productsService.create(productData);
        this.products.push(response);
        return response;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در افزودن محصول';
        console.error('Error adding product:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // ویرایش محصول
    async updateProduct(productId, productData) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await productsService.update(productId, productData);
        
        // به‌روزرسانی محصول در آرایه محصولات
        const index = this.products.findIndex(p => p.id === productId);
        if (index !== -1) {
          this.products[index] = response;
        }
        
        return response;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در ویرایش محصول';
        console.error('Error updating product:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // حذف محصول
    async deleteProduct(productId) {
      this.loading = true;
      this.error = null;
      
      try {
        await productsService.delete(productId);
        
        // حذف محصول از آرایه محصولات
        this.products = this.products.filter(p => p.id !== productId);
        
        return true;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در حذف محصول';
        console.error('Error deleting product:', error);
        return false;
      } finally {
        this.loading = false;
      }
    },
    
    // افزودن دسته‌بندی جدید
    async addCategory(categoryData) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await categoriesService.create(categoryData);
        this.categories.push(response);
        return response;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در افزودن دسته‌بندی';
        console.error('Error adding category:', error);
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
        category: null,
        sortBy: 'name'
      };
      this.pagination.page = 1;
    }
  }
}); 