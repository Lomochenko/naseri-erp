import axios from './axios';
import cacheService from './cacheService';

/**
 * کلاس سرویس API برای مدیریت تمام درخواست‌های HTTP
 */
export class ApiService {
  /**
   * سازنده کلاس
   * @constructor
   */
  constructor() {
    this.axios = axios;
  }

  /**
   * ارسال درخواست GET
   * @param {string} url - آدرس API
   * @param {Object} params - پارامترهای Query String
   * @param {Object} config - تنظیمات اضافی Axios
   * @returns {Promise<any>} - پاسخ API
   */
  async get(url, params = {}, config = {}) {
    try {
      const response = await this.axios.get(url, { 
        params,
        ...config
      });
      return response.data;
    } catch (error) {
      console.error(`[API Error] GET ${url}:`, error);
      throw error;
    }
  }

  /**
   * ارسال درخواست POST
   * @param {string} url - آدرس API
   * @param {Object} data - داده‌های ارسالی
   * @param {Object} config - تنظیمات اضافی Axios
   * @returns {Promise<any>} - پاسخ API
   */
  async post(url, data = {}, config = {}) {
    try {
      const response = await this.axios.post(url, data, config);
      return response.data;
    } catch (error) {
      console.error(`[API Error] POST ${url}:`, error);
      throw error;
    }
  }

  /**
   * ارسال درخواست PUT
   * @param {string} url - آدرس API
   * @param {Object} data - داده‌های بروزرسانی
   * @param {Object} config - تنظیمات اضافی Axios
   * @returns {Promise<any>} - پاسخ API
   */
  async put(url, data = {}, config = {}) {
    try {
      const response = await this.axios.put(url, data, config);
      return response.data;
    } catch (error) {
      console.error(`[API Error] PUT ${url}:`, error);
      throw error;
    }
  }

  /**
   * ارسال درخواست PATCH
   * @param {string} url - آدرس API
   * @param {Object} data - داده‌های بروزرسانی جزئی
   * @param {Object} config - تنظیمات اضافی Axios
   * @returns {Promise<any>} - پاسخ API
   */
  async patch(url, data = {}, config = {}) {
    try {
      const response = await this.axios.patch(url, data, config);
      return response.data;
    } catch (error) {
      console.error(`[API Error] PATCH ${url}:`, error);
      throw error;
    }
  }

  /**
   * ارسال درخواست DELETE
   * @param {string} url - آدرس API
   * @param {Object} config - تنظیمات اضافی Axios
   * @returns {Promise<any>} - پاسخ API
   */
  async delete(url, config = {}) {
    try {
      const response = await this.axios.delete(url, config);
      return response.data;
    } catch (error) {
      console.error(`[API Error] DELETE ${url}:`, error);
      throw error;
    }
  }

  /**
   * آپلود فایل به سرور
   * @param {string} url - آدرس API
   * @param {FormData} formData - داده‌های فرم شامل فایل
   * @param {Function} progressCallback - تابع برای دریافت پیشرفت آپلود
   * @returns {Promise<any>} - پاسخ API
   */
  async upload(url, formData, progressCallback = null) {
    try {
      const config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      };
      
      if (progressCallback) {
        config.onUploadProgress = (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          progressCallback(percentCompleted);
        };
      }
      
      const response = await this.axios.post(url, formData, config);
      return response.data;
    } catch (error) {
      console.error(`[API Error] UPLOAD ${url}:`, error);
      throw error;
    }
  }

  /**
   * دانلود فایل از سرور
   * @param {string} url - آدرس API
   * @param {Object} params - پارامترهای Query String
   * @param {Function} progressCallback - تابع برای دریافت پیشرفت دانلود
   * @returns {Promise<any>} - پاسخ API
   */
  async download(url, params = {}, progressCallback = null) {
    try {
      const config = {
        responseType: 'blob',
        params
      };
      
      if (progressCallback) {
        config.onDownloadProgress = (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          progressCallback(percentCompleted);
        };
      }
      
      const response = await this.axios.get(url, config);
      return response;
    } catch (error) {
      console.error(`[API Error] DOWNLOAD ${url}:`, error);
      throw error;
    }
  }
}

/**
 * کلاس سرویس EntityApiService برای عملیات CRUD استاندارد
 * این کلاس برای کاهش تکرار کد در استورهای مختلف طراحی شده است
 */
export class EntityApiService {
  /**
   * سازنده کلاس
   * @param {string} endpoint - نقطه پایانی API (مانند 'products', 'customers', ...)
   * @param {string} cacheKey - کلید ذخیره‌سازی در کش
   * @param {number} cacheDuration - مدت زمان اعتبار کش به دقیقه
   */
  constructor(endpoint, cacheKey = null, cacheDuration = 30) {
    this.api = new ApiService();
    this.endpoint = endpoint;
    this.cacheKey = cacheKey || endpoint;
    this.cacheDuration = cacheDuration;
  }

  /**
   * دریافت لیست آیتم‌ها
   * @param {Object} params - پارامترهای درخواست
   * @param {boolean} bypassCache - نادیده گرفتن کش
   * @returns {Promise<Array>} - لیست آیتم‌ها
   */
  async fetchList(params = {}, bypassCache = false) {
    const cacheKey = `${this.cacheKey}_list`;
    
    // بررسی کش
    if (!bypassCache) {
      const cachedData = cacheService.get(cacheKey);
      if (cachedData) {
        return cachedData;
      }
    }
    
    const data = await this.api.get(`/${this.endpoint}/`, params);
    
    // ذخیره در کش
    cacheService.set(cacheKey, data, this.cacheDuration);
    
    return data;
  }

  /**
   * دریافت جزئیات یک آیتم با شناسه
   * @param {number|string} id - شناسه آیتم
   * @param {Object} params - پارامترهای درخواست
   * @param {boolean} bypassCache - نادیده گرفتن کش
   * @returns {Promise<Object>} - جزئیات آیتم
   */
  async fetchDetail(id, params = {}, bypassCache = false) {
    const cacheKey = `${this.cacheKey}_${id}`;
    
    // بررسی کش
    if (!bypassCache) {
      const cachedData = cacheService.get(cacheKey);
      if (cachedData) {
        return cachedData;
      }
    }
    
    const data = await this.api.get(`/${this.endpoint}/${id}/`, params);
    
    // ذخیره در کش
    cacheService.set(cacheKey, data, this.cacheDuration);
    
    return data;
  }

  /**
   * ایجاد آیتم جدید
   * @param {Object} itemData - داده‌های آیتم جدید
   * @returns {Promise<Object>} - آیتم ایجاد شده
   */
  async create(itemData) {
    const result = await this.api.post(`/${this.endpoint}/`, itemData);
    
    // پاک کردن کش لیست
    cacheService.remove(`${this.cacheKey}_list`);
    
    return result;
  }

  /**
   * بروزرسانی آیتم موجود
   * @param {number|string} id - شناسه آیتم
   * @param {Object} itemData - داده‌های بروزرسانی
   * @returns {Promise<Object>} - آیتم بروزرسانی شده
   */
  async update(id, itemData) {
    const result = await this.api.put(`/${this.endpoint}/${id}/`, itemData);
    
    // پاک کردن کش‌های مرتبط
    cacheService.remove(`${this.cacheKey}_${id}`);
    cacheService.remove(`${this.cacheKey}_list`);
    
    return result;
  }

  /**
   * بروزرسانی جزئی آیتم موجود
   * @param {number|string} id - شناسه آیتم
   * @param {Object} itemData - داده‌های بروزرسانی جزئی
   * @returns {Promise<Object>} - آیتم بروزرسانی شده
   */
  async partialUpdate(id, itemData) {
    const result = await this.api.patch(`/${this.endpoint}/${id}/`, itemData);
    
    // پاک کردن کش‌های مرتبط
    cacheService.remove(`${this.cacheKey}_${id}`);
    cacheService.remove(`${this.cacheKey}_list`);
    
    return result;
  }

  /**
   * حذف آیتم
   * @param {number|string} id - شناسه آیتم
   * @returns {Promise<any>} - نتیجه حذف
   */
  async delete(id) {
    const result = await this.api.delete(`/${this.endpoint}/${id}/`);
    
    // پاک کردن کش‌های مرتبط
    cacheService.remove(`${this.cacheKey}_${id}`);
    cacheService.remove(`${this.cacheKey}_list`);
    
    return result;
  }

  /**
   * ارسال درخواست سفارشی
   * @param {string} method - متد HTTP (get, post, put, patch, delete)
   * @param {string} url - آدرس API نسبی
   * @param {Object} data - داده‌های درخواست
   * @param {Object} config - تنظیمات درخواست
   * @returns {Promise<any>} - نتیجه درخواست
   */
  async request(method, url, data = {}, config = {}) {
    let fullUrl = url.startsWith('/') ? url : `/${this.endpoint}/${url}`;
    
    switch (method.toLowerCase()) {
      case 'get':
        return this.api.get(fullUrl, data, config);
      case 'post':
        return this.api.post(fullUrl, data, config);
      case 'put':
        return this.api.put(fullUrl, data, config);
      case 'patch':
        return this.api.patch(fullUrl, data, config);
      case 'delete':
        return this.api.delete(fullUrl, config);
      default:
        throw new Error(`درخواست نامعتبر: ${method}`);
    }
  }

  /**
   * پاک کردن تمام کش‌های مرتبط با این سرویس
   */
  clearCache() {
    cacheService.removePattern(this.cacheKey);
  }
}

// سرویس‌های آماده برای استفاده در استورها
export const productsService = new EntityApiService('products');
export const categoriesService = new EntityApiService('categories');
export const unitsService = new EntityApiService('units');
export const warehousesService = new EntityApiService('warehouses');
export const inventoryService = new EntityApiService('inventory');
export const salesService = new EntityApiService('sales');
export const customersService = new EntityApiService('customers');
export const purchasesService = new EntityApiService('purchases');
export const suppliersService = new EntityApiService('suppliers');
export const accountingService = new EntityApiService('accounting');
export const bankAccountsService = new EntityApiService('bankaccounts'); 