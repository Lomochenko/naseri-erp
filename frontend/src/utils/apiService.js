import axiosInstance from './axios';
import { cacheService } from './cacheService';

/**
 * سرویس API مشترک برای عملیات CRUD استاندارد
 * این کلاس برای کاهش کد تکراری در استورهای مختلف استفاده می‌شود
 */
export class ApiService {
  /**
   * سازنده کلاس
   * @param {string} baseUrl - آدرس پایه API
   */
  constructor(baseUrl) {
    this.baseUrl = baseUrl;
  }

  /**
   * دریافت لیست آیتم‌ها
   * @param {Object} params - پارامترهای پرس‌وجو
   * @param {boolean} useCache - آیا از کش استفاده شود؟
   * @param {number} cacheExpiration - مدت زمان انقضای کش به دقیقه
   * @returns {Promise<Object>} - نتیجه درخواست
   */
  async getList(params = {}, useCache = true, cacheExpiration = 5) {
    try {
      // بررسی کش در صورت فعال بودن
      if (useCache) {
        const cachedData = cacheService.get(this.baseUrl, params);
        if (cachedData) {
          return cachedData;
        }
      }

      const response = await axiosInstance.get(this.baseUrl, { params });
      const data = response.data;

      // ذخیره در کش در صورت فعال بودن
      if (useCache) {
        cacheService.set(this.baseUrl, params, data, cacheExpiration);
      }

      return data;
    } catch (error) {
      console.error(`Error fetching list from ${this.baseUrl}:`, error);
      throw error;
    }
  }

  /**
   * دریافت جزئیات یک آیتم
   * @param {number|string} id - شناسه آیتم
   * @param {boolean} useCache - آیا از کش استفاده شود؟
   * @param {number} cacheExpiration - مدت زمان انقضای کش به دقیقه
   * @returns {Promise<Object>} - نتیجه درخواست
   */
  async getDetail(id, useCache = true, cacheExpiration = 10) {
    try {
      const url = `${this.baseUrl}${id}/`;

      // بررسی کش در صورت فعال بودن
      if (useCache) {
        const cachedData = cacheService.get(url, null);
        if (cachedData) {
          return cachedData;
        }
      }

      const response = await axiosInstance.get(url);
      const data = response.data;

      // ذخیره در کش در صورت فعال بودن
      if (useCache) {
        cacheService.set(url, null, data, cacheExpiration);
      }

      return data;
    } catch (error) {
      console.error(`Error fetching detail from ${this.baseUrl}${id}/:`, error);
      throw error;
    }
  }

  /**
   * ایجاد آیتم جدید
   * @param {Object} data - داده‌های آیتم جدید
   * @returns {Promise<Object>} - نتیجه درخواست
   */
  async create(data) {
    try {
      const response = await axiosInstance.post(this.baseUrl, data);
      
      // باطل کردن کش لیست پس از ایجاد آیتم جدید
      cacheService.invalidateAll(this.baseUrl);
      
      return response.data;
    } catch (error) {
      console.error(`Error creating item at ${this.baseUrl}:`, error);
      throw error;
    }
  }

  /**
   * به‌روزرسانی آیتم
   * @param {number|string} id - شناسه آیتم
   * @param {Object} data - داده‌های به‌روزرسانی
   * @returns {Promise<Object>} - نتیجه درخواست
   */
  async update(id, data) {
    try {
      const url = `${this.baseUrl}${id}/`;
      const response = await axiosInstance.put(url, data);
      
      // باطل کردن کش‌ها پس از به‌روزرسانی
      cacheService.invalidate(url, null);
      cacheService.invalidateAll(this.baseUrl);
      
      return response.data;
    } catch (error) {
      console.error(`Error updating item at ${this.baseUrl}${id}/:`, error);
      throw error;
    }
  }

  /**
   * به‌روزرسانی جزئی آیتم
   * @param {number|string} id - شناسه آیتم
   * @param {Object} data - داده‌های به‌روزرسانی جزئی
   * @returns {Promise<Object>} - نتیجه درخواست
   */
  async patch(id, data) {
    try {
      const url = `${this.baseUrl}${id}/`;
      const response = await axiosInstance.patch(url, data);
      
      // باطل کردن کش‌ها پس از به‌روزرسانی
      cacheService.invalidate(url, null);
      cacheService.invalidateAll(this.baseUrl);
      
      return response.data;
    } catch (error) {
      console.error(`Error patching item at ${this.baseUrl}${id}/:`, error);
      throw error;
    }
  }

  /**
   * حذف آیتم
   * @param {number|string} id - شناسه آیتم
   * @returns {Promise<boolean>} - نتیجه درخواست
   */
  async delete(id) {
    try {
      const url = `${this.baseUrl}${id}/`;
      await axiosInstance.delete(url);
      
      // باطل کردن کش‌ها پس از حذف
      cacheService.invalidate(url, null);
      cacheService.invalidateAll(this.baseUrl);
      
      return true;
    } catch (error) {
      console.error(`Error deleting item at ${this.baseUrl}${id}/:`, error);
      throw error;
    }
  }

  /**
   * ارسال درخواست سفارشی
   * @param {string} method - روش HTTP (GET, POST, PUT, DELETE)
   * @param {string} url - آدرس نسبی API
   * @param {Object} data - داده‌های درخواست (برای POST، PUT، PATCH)
   * @param {Object} params - پارامترهای پرس‌وجو (برای GET)
   * @param {boolean} useCache - آیا از کش استفاده شود؟ (فقط برای GET)
   * @param {number} cacheExpiration - مدت زمان انقضای کش به دقیقه
   * @returns {Promise<Object>} - نتیجه درخواست
   */
  async request(method, url, data = null, params = null, useCache = false, cacheExpiration = 5) {
    try {
      const fullUrl = `${this.baseUrl}${url}`;
      const config = { method, url: fullUrl };
      
      if (params) {
        config.params = params;
      }
      
      if (data) {
        config.data = data;
      }
      
      // بررسی کش برای درخواست‌های GET
      if (method.toLowerCase() === 'get' && useCache) {
        const cachedData = cacheService.get(fullUrl, params);
        if (cachedData) {
          return cachedData;
        }
      }
      
      const response = await axiosInstance.request(config);
      const responseData = response.data;
      
      // ذخیره در کش برای درخواست‌های GET
      if (method.toLowerCase() === 'get' && useCache) {
        cacheService.set(fullUrl, params, responseData, cacheExpiration);
      }
      
      // باطل کردن کش برای درخواست‌های غیر GET
      if (method.toLowerCase() !== 'get') {
        cacheService.invalidateAll(this.baseUrl);
      }
      
      return responseData;
    } catch (error) {
      console.error(`Error in custom request to ${this.baseUrl}${url}:`, error);
      throw error;
    }
  }
  
  /**
   * پاک کردن کش مربوط به این سرویس
   */
  clearCache() {
    cacheService.invalidateAll(this.baseUrl);
  }
}

/**
 * ایجاد نمونه‌های سرویس API برای هر ماژول
 */
export const productsService = new ApiService('/api/products/');
export const categoriesService = new ApiService('/api/products/categories/');
export const unitsService = new ApiService('/api/products/units/');
export const inventoryService = new ApiService('/api/inventory/inventory/');
export const warehousesService = new ApiService('/api/inventory/warehouses/');
export const inventoryTransactionsService = new ApiService('/api/inventory/transactions/');
export const salesService = new ApiService('/api/sales/sales/');
export const customersService = new ApiService('/api/sales/customers/');
export const purchasesService = new ApiService('/api/purchases/purchases/');
export const suppliersService = new ApiService('/api/purchases/suppliers/');
export const transactionsService = new ApiService('/api/accounting/transactions/');
export const bankAccountsService = new ApiService('/api/accounting/bank-accounts/');
export const duePaymentsService = new ApiService('/api/accounting/due-payments/'); 