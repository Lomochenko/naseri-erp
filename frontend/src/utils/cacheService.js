/**
 * سرویس کش‌کردن درخواست‌های API
 * این سرویس برای ذخیره موقت پاسخ‌های API و بهبود کارایی استفاده می‌شود
 */

class CacheService {
  constructor() {
    this.cache = new Map();
    this.expirationTimes = new Map();
  }

  /**
   * کلید کش را براساس URL و پارامترها تولید می‌کند
   * @param {string} url - آدرس درخواست
   * @param {Object|null} params - پارامترهای درخواست
   * @returns {string} - کلید کش
   */
  generateKey(url, params = null) {
    if (!params) {
      return url;
    }
    
    // مرتب کردن کلیدها و تبدیل به رشته JSON برای تولید کلید یکتا
    const sortedParams = Object.keys(params)
      .sort()
      .reduce((acc, key) => {
        if (params[key] !== undefined && params[key] !== null) {
          acc[key] = params[key];
        }
        return acc;
      }, {});
      
    return `${url}:${JSON.stringify(sortedParams)}`;
  }

  /**
   * داده‌ها را در کش ذخیره می‌کند
   * @param {string} url - آدرس درخواست
   * @param {Object|null} params - پارامترهای درخواست
   * @param {*} data - داده‌های پاسخ
   * @param {number} expirationMinutes - زمان انقضا بر حسب دقیقه
   */
  set(url, params, data, expirationMinutes = 5) {
    const key = this.generateKey(url, params);
    this.cache.set(key, data);
    
    // تنظیم زمان انقضا
    const expirationTime = Date.now() + (expirationMinutes * 60 * 1000);
    this.expirationTimes.set(key, expirationTime);
    
    // حذف کش منقضی شده بعد از مدت زمان مشخص
    setTimeout(() => {
      this.invalidate(url, params);
    }, expirationMinutes * 60 * 1000);
  }

  /**
   * داده‌ها را از کش دریافت می‌کند
   * @param {string} url - آدرس درخواست
   * @param {Object|null} params - پارامترهای درخواست
   * @returns {*|null} - داده‌های کش شده یا null
   */
  get(url, params) {
    const key = this.generateKey(url, params);
    
    // بررسی انقضای کش
    const expirationTime = this.expirationTimes.get(key);
    if (expirationTime && expirationTime < Date.now()) {
      this.invalidate(url, params);
      return null;
    }
    
    return this.cache.get(key) || null;
  }

  /**
   * داده‌های کش را باطل (حذف) می‌کند
   * @param {string} url - آدرس درخواست
   * @param {Object|null} params - پارامترهای درخواست
   */
  invalidate(url, params) {
    const key = this.generateKey(url, params);
    this.cache.delete(key);
    this.expirationTimes.delete(key);
  }

  /**
   * تمام داده‌های کش مرتبط با یک URL را باطل (حذف) می‌کند
   * @param {string} url - آدرس درخواست
   */
  invalidateAll(url) {
    // حذف تمام کلیدهایی که با URL مورد نظر شروع می‌شوند
    for (const key of this.cache.keys()) {
      if (key === url || key.startsWith(`${url}:`)) {
        this.cache.delete(key);
        this.expirationTimes.delete(key);
      }
    }
  }

  /**
   * تمام داده‌های کش را پاک می‌کند
   */
  clear() {
    this.cache.clear();
    this.expirationTimes.clear();
  }
}

// صادر کردن یک نمونه از سرویس کش
export const cacheService = new CacheService();

/**
 * افزودن قابلیت کش‌کردن به یک تابع
 * @param {Function} fn - تابع اصلی
 * @param {string} url - آدرس درخواست
 * @param {number} expirationMinutes - زمان انقضا بر حسب دقیقه
 * @returns {Function} - تابع جدید با قابلیت کش
 */
export function withCache(fn, url, expirationMinutes = 5) {
  return async function(...args) {
    // پارامترهای درخواست معمولاً اولین آرگومان تابع هستند
    const params = args[0] || null;
    
    // بررسی کش
    const cachedData = cacheService.get(url, params);
    if (cachedData) {
      return cachedData;
    }
    
    // اجرای تابع اصلی
    const result = await fn(...args);
    
    // ذخیره در کش
    cacheService.set(url, params, result, expirationMinutes);
    
    return result;
  };
} 