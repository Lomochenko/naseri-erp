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
        console.log('API URL:', productsService.endpoint);
        console.log('Headers:', {
          Authorization: localStorage.getItem('naseri_auth_token') ? 
            `Token ${localStorage.getItem('naseri_auth_token')}` : 'No token'
        });
        
        try {
          const response = await productsService.getList(params);
          console.log('Products API response:', response);
          
          // بررسی ساختار پاسخ API برای دیباگ
          console.log('Products response structure check:', {
            responseType: typeof response,
            hasResults: !!(response && response.results),
            hasCount: !!(response && response.count !== undefined),
            isArray: Array.isArray(response),
            keys: response ? Object.keys(response) : []
          });
          
          // مدیریت انواع مختلف پاسخ API
          if (response && response.results) {
            // ساختار پاسخ استاندارد Django REST framework
            this.products = response.results;
            this.totalItems = response.count || response.results.length;
          } else if (Array.isArray(response)) {
            // پاسخ به صورت آرایه
            this.products = response;
            this.totalItems = response.length;
          } else if (response && typeof response === 'object') {
            // اگر یک آبجکت ساده بود، تلاش کنیم آن را پردازش کنیم
            if (Array.isArray(response.data)) {
              this.products = response.data;
              this.totalItems = response.total || response.data.length;
            } else {
              this.products = [response];
              this.totalItems = 1;
            }
          } else {
            // نمی‌توان داده‌ها را پردازش کرد
            this.products = [];
            this.totalItems = 0;
            console.warn('Response does not contain expected results structure:', response);
          }
          
          return this.products;
        } catch (apiError) {
          console.error('API Error details:', {
            message: apiError.message,
            response: apiError.response?.data,
            status: apiError.response?.status
          });
          throw apiError;
        }
      } catch (error) {
        console.error('Error fetching products:', error);
        this.error = error.response?.data?.detail || error.message || 'خطا در دریافت لیست محصولات';
        this.products = [];
        this.totalItems = 0;
        return [];
      } finally {
        this.loading = false;
      }
    },
    
    // دریافت دسته‌بندی‌ها
    async fetchCategories(searchTerm = '') {
      this.loading = true;
      this.error = null;
      
      try {
        console.log('Calling categories API...');
        
        // برای اطمینان از اینکه درخواست به صورت کامل انجام شود
        await new Promise(resolve => setTimeout(resolve, 50));
        
        // اضافه کردن پارامتر جستجو به درخواست API
        const params = {
          ordering: 'name',
          page_size: 100 // تعداد بیشتری دسته‌بندی دریافت می‌کنیم
        };
        
        // اگر عبارت جستجو موجود بود، به پارامترها اضافه کن
        if (searchTerm) {
          params.search = searchTerm;
        }
        
        const response = await categoriesService.getList(params);
        
        // بررسی ساختار پاسخ API برای دیباگ
        console.log('Categories API response received:', response);
        console.log('Categories response structure:', {
          responseType: typeof response,
          hasResults: !!(response && response.results),
          isArray: Array.isArray(response),
          keys: response ? Object.keys(response) : []
        });
        
        // بررسی و پردازش داده‌های پاسخ API
        if (!response) {
          console.log('No response received, using empty array');
          this.categories = [];
          return [];
        }
        
        if (response && response.results) {
          console.log('Using results from DRF response');
          this.categories = response.results;
        } else if (Array.isArray(response)) {
          console.log('Using array response');
          this.categories = response;
        } else if (response && typeof response === 'object') {
          if (Array.isArray(response.data)) {
            console.log('Using data array from object response');
            this.categories = response.data;
          } else {
            console.log('Converting single object to array');
            this.categories = [response];
          }
        } else {
          console.log('No valid response format found, using empty array');
          this.categories = [];
        }
        
        // اطمینان از اینکه آرایه برگشتی معتبر است
        if (!Array.isArray(this.categories)) {
          console.warn('Invalid categories array, resetting to empty array');
          this.categories = [];
        }
        
        console.log('Categories processed:', this.categories.length);
        return this.categories;
      } catch (error) {
        console.error('Error details in fetchCategories:', error);
        
        // پیام خطای دقیق‌تر
        if (error.response) {
          // پاسخ سرور با کد خطا
          this.error = `خطا از سرور: ${error.response.status} - ${error.response.data?.detail || 'بدون توضیحات'}`;
        } else if (error.request) {
          // درخواست ارسال شده اما پاسخی دریافت نشده
          this.error = 'خطا در ارتباط با سرور: پاسخی از سرور دریافت نشد';
        } else {
          // خطا در تنظیم درخواست
          this.error = `خطا در ارسال درخواست: ${error.message}`;
        }
        
        console.error('Error fetching categories:', error);
        this.categories = [];
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
        
        // بررسی ساختار پاسخ API برای دیباگ
        console.log('Units response structure:', {
          responseType: typeof response,
          hasResults: !!(response && response.results),
          isArray: Array.isArray(response),
          keys: response ? Object.keys(response) : []
        });
        
        if (response && response.results) {
          this.units = response.results;
        } else if (Array.isArray(response)) {
          this.units = response;
        } else if (response && typeof response === 'object') {
          if (Array.isArray(response.data)) {
            this.units = response.data;
          } else {
            this.units = [response];
          }
        } else {
          this.units = [];
        }
        
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
        console.log('Add product response:', response);
        
        // بروزرسانی لیست محصولات
        await this.fetchProducts();
        
        return response || {
          ...productData,
          id: 'temporary-id-' + Date.now(),
          created_at: new Date().toISOString()
        };
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
        console.log('Update product response:', response);
        
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
        console.log('Deleting product:', productId);
        await productsService.delete(productId);
        
        // بروزرسانی لیست محصولات
        const index = this.products.findIndex(p => p.id === productId);
        if (index !== -1) {
          this.products.splice(index, 1);
          this.totalItems--;
        }
        
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
        console.log('Category update response:', response);
        
        // بروزرسانی لیست دسته‌بندی‌ها
        await this.fetchCategories();
        
        // اگر پاسخ معتبر نیست، یک آبجکت با اطلاعات دسته‌بندی برگردان
        if (!response) {
          console.log('No response from API, creating mock response');
          return {
            id: categoryId,
            ...categoryData,
            updated_at: new Date().toISOString()
          };
        }
        
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
    
    // حذف دسته‌بندی
    async deleteCategory(categoryId) {
      this.loading = true;
      this.error = null;
      
      try {
        console.log('Deleting category:', categoryId);
        await categoriesService.delete(categoryId);
        
        // بروزرسانی لیست دسته‌بندی‌ها
        await this.fetchCategories();
        
        return true;
      } catch (error) {
        const errorMsg = error.response?.data?.detail || 
                        Object.values(error.response?.data || {}).flat().join(', ') ||
                        'خطا در حذف دسته‌بندی';
        this.error = errorMsg;
        console.error('Error deleting category:', error);
        return false;
      } finally {
        this.loading = false;
      }
    },
    
    // افزودن واحد جدید
    async addUnit(unitData) {
      this.loading = true;
      this.error = null;
      
      try {
        console.log('Adding new unit:', unitData);
        const response = await unitsService.create(unitData);
        
        // بروزرسانی لیست واحدها
        await this.fetchUnits();
        
        return response;
      } catch (error) {
        const errorMsg = error.response?.data?.detail || 
                        Object.values(error.response?.data || {}).flat().join(', ') ||
                        'خطا در افزودن واحد';
        this.error = errorMsg;
        console.error('Error adding unit:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // ویرایش واحد
    async updateUnit(unitId, unitData) {
      this.loading = true;
      this.error = null;
      
      try {
        console.log('Updating unit:', unitId, unitData);
        const response = await unitsService.update(unitId, unitData);
        
        // بروزرسانی لیست واحدها
        await this.fetchUnits();
        
        return response;
      } catch (error) {
        const errorMsg = error.response?.data?.detail || 
                        Object.values(error.response?.data || {}).flat().join(', ') ||
                        'خطا در ویرایش واحد';
        this.error = errorMsg;
        console.error('Error updating unit:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // حذف واحد
    async deleteUnit(unitId) {
      this.loading = true;
      this.error = null;
      
      try {
        console.log('Deleting unit:', unitId);
        await unitsService.delete(unitId);
        
        // بروزرسانی لیست واحدها
        await this.fetchUnits();
        
        return true;
      } catch (error) {
        const errorMsg = error.response?.data?.detail || 
                        Object.values(error.response?.data || {}).flat().join(', ') ||
                        'خطا در حذف واحد';
        this.error = errorMsg;
        console.error('Error deleting unit:', error);
        return false;
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