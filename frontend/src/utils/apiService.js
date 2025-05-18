import api from './axios';
import { cacheService } from './cacheService';

/**
 * کلاس سرویس API برای مدیریت تمام درخواست‌های HTTP
 */
export class ApiService {
  /**
   * سازنده کلاس
   * @constructor
   */
  constructor(endpoint) {
    this.endpoint = endpoint;
    this.api = api;
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
      const finalConfig = {
        ...config
      };
      
      if (params && Object.keys(params).length > 0) {
        finalConfig.params = params;
      }
      
      // اطمینان از اینکه آدرس با / شروع می‌شود
      const finalUrl = url.startsWith('/') ? url : `/${url}`;
      
      console.log(`Sending GET request to ${finalUrl} with config:`, finalConfig);
      const response = await this.api.get(finalUrl, finalConfig);
      return response;
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
      const response = await this.api.post(url, data, config);
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
      const response = await this.api.put(url, data, config);
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
      const response = await this.api.patch(url, data, config);
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
      const response = await this.api.delete(url, config);
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
      
      const response = await this.api.post(url, formData, config);
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
      
      const response = await this.api.get(url, config);
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
    this.api = new ApiService(endpoint);
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
  async getList(params = {}, bypassCache = false) {
    const apiPath = `/api/${this.endpoint}/`;
    console.log(`Fetching from ${apiPath} with params:`, params);
    
    try {
      const response = await this.api.get(apiPath, params);
      console.log(`API Response from ${apiPath}:`, response);
      return response;
    } catch (error) {
      console.error(`Error fetching from ${apiPath}:`, error);
      throw error;
    }
  }

  /**
   * دریافت جزئیات یک آیتم
   * @param {string|number} id - شناسه آیتم
   * @param {Object} params - پارامترهای اضافی
   * @param {boolean} bypassCache - نادیده گرفتن کش
   * @returns {Promise<Object>} - جزئیات آیتم
   */
  async getDetail(id, params = {}, bypassCache = false) {
    const apiPath = `/api/${this.endpoint}/${id}/`;
    console.log(`Fetching details from ${apiPath} with params:`, params);
    
    try {
      const response = await this.api.get(apiPath, params);
      console.log(`API Detail Response from ${apiPath}:`, response);
      return response;
    } catch (error) {
      console.error(`Error fetching details from ${apiPath}:`, error);
      throw error;
    }
  }

  /**
   * ایجاد آیتم جدید
   * @param {Object} itemData - داده‌های آیتم جدید
   * @returns {Promise<Object>} - آیتم ایجاد شده
   */
  async create(itemData) {
    const apiPath = `/api/${this.endpoint}/`;
    console.log(`Creating new item at ${apiPath} with data:`, itemData);
    
    try {
      const result = await this.api.post(apiPath, itemData);
      
      // پاک کردن کش لیست
      cacheService.invalidateAll(`/api/${this.endpoint}/`);
      
      return result;
    } catch (error) {
      console.error(`Error creating item at ${apiPath}:`, error);
      throw error;
    }
  }

  /**
   * بروزرسانی آیتم موجود
   * @param {number|string} id - شناسه آیتم
   * @param {Object} itemData - داده‌های بروزرسانی
   * @returns {Promise<Object>} - آیتم بروزرسانی شده
   */
  async update(id, itemData) {
    const apiPath = `/api/${this.endpoint}/${id}/`;
    console.log(`Updating item at ${apiPath} with data:`, itemData);
    
    try {
      const result = await this.api.put(apiPath, itemData);
      
      // پاک کردن کش‌های مرتبط
      cacheService.invalidate(`/api/${this.endpoint}/${id}/`);
      cacheService.invalidateAll(`/api/${this.endpoint}/`);
      
      return result;
    } catch (error) {
      console.error(`Error updating item at ${apiPath}:`, error);
      throw error;
    }
  }

  /**
   * بروزرسانی جزئی آیتم موجود
   * @param {number|string} id - شناسه آیتم
   * @param {Object} itemData - داده‌های بروزرسانی جزئی
   * @returns {Promise<Object>} - آیتم بروزرسانی شده
   */
  async partialUpdate(id, itemData) {
    const apiPath = `/api/${this.endpoint}/${id}/`;
    console.log(`Partially updating item at ${apiPath} with data:`, itemData);
    
    try {
      const result = await this.api.patch(apiPath, itemData);
      
      // پاک کردن کش‌های مرتبط
      cacheService.invalidate(`/api/${this.endpoint}/${id}/`);
      cacheService.invalidateAll(`/api/${this.endpoint}/`);
      
      return result;
    } catch (error) {
      console.error(`Error partially updating item at ${apiPath}:`, error);
      throw error;
    }
  }

  /**
   * حذف آیتم
   * @param {number|string} id - شناسه آیتم
   * @returns {Promise<any>} - نتیجه حذف
   */
  async delete(id) {
    const apiPath = `/api/${this.endpoint}/${id}/`;
    console.log(`Deleting item at ${apiPath}`);
    
    try {
      const result = await this.api.delete(apiPath);
      
      // پاک کردن کش‌های مرتبط
      cacheService.invalidate(`/api/${this.endpoint}/${id}/`);
      cacheService.invalidateAll(`/api/${this.endpoint}/`);
      
      return result;
    } catch (error) {
      console.error(`Error deleting item at ${apiPath}:`, error);
      throw error;
    }
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
    let fullUrl = url.startsWith('/') ? url : `/api/${this.endpoint}/${url}`;
    
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
    cacheService.invalidateAll(`/api/${this.endpoint}/`);
  }
}

// Services for Modules
export const productsService = new EntityApiService('products');
export const categoriesService = new EntityApiService('products/categories');
export const unitsService = new EntityApiService('products/units');
export const customersService = new EntityApiService('customers');
export const suppliersService = new EntityApiService('suppliers');
export const warehousesService = new EntityApiService('warehouses');
export const salesService = new EntityApiService('sales');
export const invoicesService = new EntityApiService('invoices');
export const paymentsService = new EntityApiService('payments');
export const accountingService = new EntityApiService('accounting');
export const bankAccountsService = new EntityApiService('bankaccounts'); 