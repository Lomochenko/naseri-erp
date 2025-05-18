import axios from 'axios';

// دریافت آدرس API از متغیرهای محیطی
const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// کلید توکن احرازهویت در localStorage
export const TOKEN_KEY = 'naseri_auth_token';

// تنظیمات retry برای درخواست‌های ناموفق
const MAX_RETRIES = 2;
const RETRY_DELAY = 1000; // milliseconds

// ایجاد نمونه axios با تنظیمات پایه
const api = axios.create({
  baseURL: BASE_URL,
  timeout: 60000, // افزایش timeout به 60 ثانیه
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// افزودن رهگیر برای درخواست‌ها
api.interceptors.request.use(
  config => {
    // افزودن توکن به هدرها در صورت وجود
    const token = localStorage.getItem(TOKEN_KEY);
    if (token) {
      config.headers['Authorization'] = `Token ${token}`;
    }
    
    // اضافه کردن شمارنده retry به درخواست
    config.retryCount = config.retryCount || 0;
    
    // لاگ درخواست برای دیباگ
    console.log('API Request:', {
      method: config.method?.toUpperCase(),
      url: config.baseURL + (config.url || ''),
      data: config.data,
      params: config.params,
      headers: config.headers,
      retryCount: config.retryCount
    });
    
    return config;
  },
  error => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// افزودن رهگیر برای پاسخ‌ها
api.interceptors.response.use(
  response => {
    // لاگ پاسخ برای دیباگ
    console.log('API Response:', {
      status: response.status,
      url: response.config.url,
      data: response.data
    });
    
    // آزمایشی: بررسی ساختار پاسخ برای دیباگ
    console.log('Response structure:', {
      hasData: !!response.data,
      hasResults: !!(response.data && response.data.results),
      resultType: response.data ? typeof response.data : 'undefined',
      keys: response.data ? Object.keys(response.data) : []
    });
    
    return response.data;
  },
  async error => {
    // لاگ خطا برای دیباگ
    console.error('API Response Error:', {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status,
      url: error.config?.url
    });
    
    // منطق retry برای خطاهای شبکه و خطاهای 5xx
    const config = error.config;
    
    // اگر درخواست هنوز به حداکثر تعداد retry نرسیده و خطا مربوط به شبکه یا سرور است
    if (
      config && 
      config.retryCount < MAX_RETRIES && 
      (error.code === 'ECONNABORTED' || error.code === 'ERR_NETWORK' || 
       (error.response && error.response.status >= 500))
    ) {
      config.retryCount += 1;
      
      console.log(`Retrying request (${config.retryCount}/${MAX_RETRIES})...`);
      
      // تاخیر قبل از retry
      await new Promise(resolve => setTimeout(resolve, RETRY_DELAY));
      
      // تلاش مجدد درخواست
      return api(config);
    }
    
    // بررسی خطاهای خاص
    if (error.response) {
      switch (error.response.status) {
        case 401: // خطای احراز هویت
          console.log('Authentication error. Redirecting to login...');
          // حذف توکن در صورت نامعتبر بودن
          localStorage.removeItem(TOKEN_KEY);
          
          // انتقال به صفحه ورود اگر در آن صفحه نیستیم
          if (window.location.pathname !== '/login') {
            window.location.href = '/login';
          }
          break;
          
        case 403: // خطای دسترسی
          console.error('Access forbidden');
          break;
          
        case 404: // خطای عدم وجود
          console.error('Resource not found');
          break;
          
        case 500: // خطای سرور
          console.error('Server error');
          break;
          
        default:
          console.error(`Error with status code: ${error.response.status}`);
      }
    } else if (error.request) {
      // درخواست ارسال شده اما پاسخی دریافت نشده
      console.error('No response received from server', error.request);
    }
    
    return Promise.reject(error);
  }
);

export default api; 