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
      status: null,
      sortBy: 'name',
      sortDesc: false
    },
    
    // اطلاعات صفحه‌بندی
    page: 1,
    itemsPerPage: 10,
    totalItems: 0
  }),
  
  getters: {
    getProductById: (state) => (id) => {
      return state.products.find(product => product.id === id);
    },
    
    getProductsByCategory: (state) => (categoryId) => {
      return state.products.filter(product => product.category?.id === categoryId);
    },
    
    getLowStockProducts: (state) => {
      return state.products.filter(product => 
        product.current_stock <= product.min_stock && product.current_stock > 0
      );
    },
    
    getOutOfStockProducts: (state) => {
      return state.products.filter(product => product.current_stock <= 0);
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
        // ساخت پارامترهای API
        const params = {
          search: this.filters.search || undefined,
          page: this.page,
          page_size: this.itemsPerPage
        };
        
        // اضافه کردن دسته‌بندی به پارامترها
        if (this.filters.category) {
          params.category = this.filters.category.id;
        }
        
        // اضافه کردن مرتب‌سازی
        let ordering = this.filters.sortBy;
        if (this.filters.sortDesc) {
          ordering = `-${ordering}`;
        }
        params.ordering = ordering;
        
        // اضافه کردن فیلتر وضعیت
        if (this.filters.status) {
          switch (this.filters.status) {
            case 'active':
              params.is_active = true;
              break;
            case 'inactive':
              params.is_active = false;
              break;
            case 'low_stock':
              params.low_stock = true;
              break;
            case 'out_of_stock':
              params.stock_lte = 0;
              break;
          }
        }
        
        console.log('Fetching products with params:', params);
        const response = await productsService.getList(params);
        
        this.products = response.results;
        this.totalItems = response.count;
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
        const response = await categoriesService.getList({
          ordering: 'name',
          page_size: 100 // تعداد بیشتری دسته‌بندی دریافت می‌کنیم
        });
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
        const response = await unitsService.getList({
          ordering: 'name',
          page_size: 100 // تعداد بیشتری واحد دریافت می‌کنیم
        });
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
        console.log('Adding new product:', productData);
        const response = await productsService.create(productData);
        
        // بروزرسانی لیست محصولات
        await this.fetchProducts();
        
        return response;
      } catch (error) {
        const errorMsg = error.response?.data?.detail || 
                        Object.values(error.response?.data || {}).flat().join(', ') ||
                        'خطا در افزودن محصول';
        this.error = errorMsg;
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
        console.log('Updating product:', productId, productData);
        const response = await productsService.update(productId, productData);
        
        // بروزرسانی لیست محصولات
        await this.fetchProducts();
        
        return response;
      } catch (error) {
        const errorMsg = error.response?.data?.detail || 
                        Object.values(error.response?.data || {}).flat().join(', ') ||
                        'خطا در ویرایش محصول';
        this.error = errorMsg;
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
        console.log('Adding new category:', categoryData);
        const response = await categoriesService.create(categoryData);
        
        // بروزرسانی لیست دسته‌بندی‌ها
        await this.fetchCategories();
        
        return response;
      } catch (error) {
        const errorMsg = error.response?.data?.detail || 
                        Object.values(error.response?.data || {}).flat().join(', ') ||
                        'خطا در افزودن دسته‌بندی';
        this.error = errorMsg;
        console.error('Error adding category:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // ویرایش دسته‌بندی
    async updateCategory(categoryId, categoryData) {
      this.loading = true;
      this.error = null;
      
      try {
        console.log('Updating category:', categoryId, categoryData);
        const response = await categoriesService.update(categoryId, categoryData);
        
        // بروزرسانی لیست دسته‌بندی‌ها
        await this.fetchCategories();
        
        return response;
      } catch (error) {
        const errorMsg = error.response?.data?.detail || 
                        Object.values(error.response?.data || {}).flat().join(', ') ||
                        'خطا در ویرایش دسته‌بندی';
        this.error = errorMsg;
        console.error('Error updating category:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // دریافت محصولات با موجودی کم
    async fetchLowStockProducts() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await productsService.request(
          'get', 
          'low-stock/', 
          null, 
          { ordering: 'name' }
        );
        
        return response.results || response;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در دریافت محصولات با موجودی کم';
        console.error('Error fetching low stock products:', error);
        return [];
      } finally {
        this.loading = false;
      }
    },
    
    // به‌روزرسانی فیلترها
    updateFilters(newFilters) {
      this.filters = { ...this.filters, ...newFilters };
      this.page = 1; // بازگشت به صفحه اول با تغییر فیلترها
      return this.fetchProducts();
    },
    
    // تنظیم صفحه جاری
    setPage(page) {
      this.page = page;
      return this.fetchProducts();
    },
    
    // تنظیم تعداد آیتم در هر صفحه
    setItemsPerPage(count) {
      this.itemsPerPage = count;
      this.page = 1; // بازگشت به صفحه اول با تغییر تعداد آیتم‌ها
      return this.fetchProducts();
    },
    
    // بازنشانی فیلترها
    resetFilters() {
      this.filters = {
        search: '',
        category: null,
        status: null,
        sortBy: 'name',
        sortDesc: false
      };
      this.page = 1;
      return this.fetchProducts();
    }
  }
}); 