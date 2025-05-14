import axios from 'axios';

// تنظیم URL پایه برای تمام درخواست‌ها
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// نام کلید توکن در localStorage
const TOKEN_KEY = 'naseri_auth_token';

const axiosInstance = axios.create({
  baseURL: API_URL,
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  }
});

// افزودن توکن احراز هویت به هدر درخواست‌ها
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(TOKEN_KEY);
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    
    // برای دیباگ‌کردن
    console.log('Request Config:', {
      url: config.url,
      method: config.method,
      headers: config.headers,
      data: config.data,
      params: config.params
    });
    
    return config;
  },
  (error) => {
    console.error('Request Error:', error);
    return Promise.reject(error);
  }
);

// مدیریت پاسخ‌های خطا
axiosInstance.interceptors.response.use(
  (response) => {
    // برای دیباگ‌کردن
    console.log('Response Data:', {
      status: response.status,
      data: response.data,
      headers: response.headers
    });
    
    return response;
  },
  (error) => {
    // برای دیباگ‌کردن
    console.error('Response Error:', {
      message: error.message,
      response: error.response ? {
        status: error.response.status,
        data: error.response.data,
        headers: error.response.headers
      } : 'No Response',
      request: error.request ? 'Request was made but no response' : 'No Request'
    });
    
    if (error.response) {
      // خطاهای سرور (400+)
      const { status } = error.response;
      
      if (status === 401) {
        // احراز هویت نشده (توکن منقضی شده یا نامعتبر)
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem('naseri_user');
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }
      }
      
      if (status === 403) {
        // دسترسی غیرمجاز
        console.error('دسترسی غیرمجاز');
        if (window.location.pathname !== '/forbidden') {
          window.location.href = '/forbidden';
        }
      }
      
      if (status === 404) {
        // منبع یافت نشد
        console.error('منبع مورد نظر یافت نشد');
      }
      
      if (status === 500) {
        // خطای سرور
        console.error('خطای سرور رخ داده است');
      }
    } else if (error.request) {
      // درخواست انجام شده اما پاسخی دریافت نشده است
      console.error('خطا در ارتباط با سرور');
    } else {
      // خطا در تنظیم درخواست
      console.error('خطا در تنظیم درخواست:', error.message);
    }
    
    return Promise.reject(error);
  }
);

export default axiosInstance; 