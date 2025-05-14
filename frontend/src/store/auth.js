import { defineStore } from 'pinia';
import axiosInstance from '../utils/axios';
import { rbacService, ROLES } from '../utils/rbac';
import router from '../router';

// نام کلید توکن در localStorage
const TOKEN_KEY = 'naseri_auth_token';
const USER_KEY = 'naseri_user';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem(TOKEN_KEY) || null,
    user: JSON.parse(localStorage.getItem(USER_KEY) || 'null'),
    loading: false,
    error: null
  }),
  
  getters: {
    isLoggedIn: (state) => !!state.token && !!state.user,
    
    // دریافت کاربر جاری
    currentUser: (state) => state.user,
    
    // بررسی دسترسی کاربر
    hasPermission: () => (permission) => {
      return rbacService.hasPermission(permission);
    },
    
    // بررسی وجود حداقل یکی از دسترسی‌ها
    hasAnyPermission: () => (permissions) => {
      return rbacService.hasAnyPermission(permissions);
    },
    
    // بررسی نقش کاربر
    hasRole: () => (role) => {
      return rbacService.hasRole(role);
    },
    
    // دریافت تمام نقش‌های کاربر
    userRoles: () => {
      return rbacService.getUserRoles();
    },
    
    // دریافت تمام دسترسی‌های کاربر
    userPermissions: () => {
      return rbacService.getUserPermissions();
    },
    
    // بررسی آیا کاربر مدیر است
    isAdmin: () => {
      return rbacService.hasRole(ROLES.ADMIN);
    }
  },
  
  actions: {
    // ورود کاربر
    async login(credentials) {
      this.loading = true;
      this.error = null;
      
      try {
        console.log('Login credentials:', credentials);
        
        const response = await axiosInstance.post('/api/users/login/', credentials);
        console.log('Login response:', response);
        
        if (response.data.token && response.data.user) {
          this.setAuthData(response.data.token, response.data.user);
          return response.data.user;
        } else {
          throw new Error('Token or user data missing in response');
        }
      } catch (error) {
        console.error('Login error details:', error);
        this.error = error.response?.data?.error || error.response?.data?.detail || 'خطا در ورود به سیستم';
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // خروج کاربر
    async logout() {
      this.loading = true;
      
      try {
        // ارسال درخواست خروج به سرور (در صورت وجود توکن)
        if (this.token) {
          await axiosInstance.post('/api/users/logout/');
        }
      } catch (error) {
        console.error('Logout error:', error);
      } finally {
        // پاک کردن داده‌های احراز هویت
        this.clearAuthData();
        this.loading = false;
        
        // هدایت به صفحه ورود
        if (router.currentRoute.value.meta.requiresAuth) {
          router.push({ name: 'login' });
        }
      }
    },
    
    // دریافت اطلاعات پروفایل کاربر
    async fetchProfile() {
      if (!this.token) return null;
      
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.get('/api/users/profile/');
        this.setUser(response.data);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در دریافت پروفایل';
        console.error('Fetch profile error:', error);
        
        // اگر خطای 401 (غیرمجاز) دریافت شد، کاربر خارج شود
        if (error.response?.status === 401) {
          this.clearAuthData();
        }
        
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // تنظیم داده‌های احراز هویت
    setAuthData(token, user) {
      console.log('Setting auth data:', { token, user });
      
      this.token = token;
      this.user = user;
      
      // ذخیره در localStorage
      localStorage.setItem(TOKEN_KEY, token);
      localStorage.setItem(USER_KEY, JSON.stringify(user));
      
      // تنظیم هدر Authorization برای تمام درخواست‌ها
      axiosInstance.defaults.headers.common['Authorization'] = `Token ${token}`;
      
      // تنظیم نقش‌های کاربر
      this.setUserRoles(user);
    },
    
    // به‌روزرسانی اطلاعات کاربر
    setUser(user) {
      this.user = user;
      localStorage.setItem(USER_KEY, JSON.stringify(user));
      
      // تنظیم نقش‌های کاربر
      this.setUserRoles(user);
    },
    
    // پاک کردن داده‌های احراز هویت
    clearAuthData() {
      this.token = null;
      this.user = null;
      
      // پاک کردن از localStorage
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(USER_KEY);
      
      // حذف هدر Authorization
      delete axiosInstance.defaults.headers.common['Authorization'];
      
      // پاک کردن نقش‌های کاربر
      rbacService.setUserRoles([]);
    },
    
    // تنظیم نقش‌های کاربر براساس اطلاعات کاربر
    setUserRoles(user) {
      if (!user) return;
      
      // نقش‌های پیش‌فرض
      const roles = [];
      
      // تعیین نقش‌ها براساس فیلد is_staff و سایر اطلاعات کاربر
      if (user.is_staff === true) {
        roles.push(ROLES.ADMIN);
      } else if (user.role) {
        // استفاده از فیلد role در صورت وجود
        roles.push(user.role);
      } else {
        // در غیر این صورت، نقش پیش‌فرض VIEWER
        roles.push(ROLES.VIEWER);
      }
      
      // تنظیم نقش‌ها در سرویس RBAC
      rbacService.setUserRoles(roles);
    },
    
    // بررسی وضعیت احراز هویت در هنگام شروع برنامه
    initAuth() {
      // اگر توکن وجود دارد، هدر را تنظیم کن
      if (this.token) {
        axiosInstance.defaults.headers.common['Authorization'] = `Token ${this.token}`;
        
        // تنظیم نقش‌های کاربر
        this.setUserRoles(this.user);
        
        // دریافت اطلاعات پروفایل برای اطمینان از معتبر بودن توکن
        return this.fetchProfile();
      }
      
      return Promise.resolve(null);
    }
  }
}); 