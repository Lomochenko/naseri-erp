import { useAuthStore } from '../store/auth';
import { PERMISSIONS } from '../utils/rbac';

/**
 * محافظ مسیر برای احراز هویت
 * کاربران غیرمجاز را به صفحه ورود هدایت می‌کند
 */
export const authGuard = async (to, from, next) => {
  const authStore = useAuthStore();
  
  // اگر مسیر نیاز به احراز هویت دارد
  if (to.meta.requiresAuth) {
    // اگر کاربر وارد شده است
    if (authStore.isLoggedIn) {
      // اطمینان از به‌روز بودن اطلاعات کاربر
      if (!authStore.user.roles) {
        try {
          // بارگذاری پروفایل کاربر اگر اطلاعات کامل نیست
          await authStore.fetchProfile();
        } catch (error) {
          // در صورت خطا به صفحه ورود هدایت می‌شود
          console.error('Failed to fetch user profile:', error);
        }
      }
      
      // بررسی دسترسی‌های مورد نیاز
      if (to.meta.permissions) {
        const requiredPermissions = to.meta.permissions;
        
        if (!authStore.hasAnyPermission(requiredPermissions)) {
          // اگر کاربر دسترسی ندارد، به صفحه 403 هدایت می‌شود
          next({ name: 'forbidden' });
          return;
        }
      }
      
      // بررسی نقش‌های مورد نیاز
      if (to.meta.roles) {
        const requiredRoles = to.meta.roles;
        
        if (!authStore.hasAnyRole(requiredRoles)) {
          // اگر کاربر نقش مورد نیاز را ندارد، به صفحه 403 هدایت می‌شود
          next({ name: 'forbidden' });
          return;
        }
      }
      
      // اجازه دسترسی به مسیر
      next();
      return;
    }
    
    // اگر کاربر وارد نشده است، به صفحه ورود هدایت می‌شود
    next({
      name: 'login',
      query: { redirect: to.fullPath } // ذخیره مسیر فعلی برای بازگشت پس از ورود
    });
    return;
  }
  
  // اگر کاربر وارد شده است و می‌خواهد به صفحه ورود/ثبت‌نام برود، به داشبورد هدایت می‌شود
  if (authStore.isLoggedIn && (to.name === 'login' || to.name === 'register')) {
    next({ name: 'dashboard' });
    return;
  }
  
  // در سایر موارد، اجازه دسترسی به مسیر
  next();
};

/**
 * محافظ مسیر برای بررسی دسترسی به صفحات محصولات
 */
export const productsGuard = (to, from, next) => {
  const authStore = useAuthStore();
  
  // حداقل نیاز به دسترسی مشاهده محصولات است
  if (authStore.hasPermission(PERMISSIONS.PRODUCT_VIEW)) {
    next();
  } else {
    next({ name: 'forbidden' });
  }
};

/**
 * محافظ مسیر برای بررسی دسترسی به صفحات موجودی
 */
export const inventoryGuard = (to, from, next) => {
  const authStore = useAuthStore();
  
  // حداقل نیاز به دسترسی مشاهده موجودی است
  if (authStore.hasPermission(PERMISSIONS.INVENTORY_VIEW)) {
    next();
  } else {
    next({ name: 'forbidden' });
  }
};

/**
 * محافظ مسیر برای بررسی دسترسی به صفحات فروش
 */
export const salesGuard = (to, from, next) => {
  const authStore = useAuthStore();
  
  // حداقل نیاز به دسترسی مشاهده فروش است
  if (authStore.hasPermission(PERMISSIONS.SALE_VIEW)) {
    next();
  } else {
    next({ name: 'forbidden' });
  }
};

/**
 * محافظ مسیر برای بررسی دسترسی به صفحات خرید
 */
export const purchasesGuard = (to, from, next) => {
  const authStore = useAuthStore();
  
  // حداقل نیاز به دسترسی مشاهده خرید است
  if (authStore.hasPermission(PERMISSIONS.PURCHASE_VIEW)) {
    next();
  } else {
    next({ name: 'forbidden' });
  }
};

/**
 * محافظ مسیر برای بررسی دسترسی به صفحات حسابداری
 */
export const accountingGuard = (to, from, next) => {
  const authStore = useAuthStore();
  
  // حداقل نیاز به دسترسی مشاهده حسابداری است
  if (authStore.hasPermission(PERMISSIONS.ACCOUNTING_VIEW)) {
    next();
  } else {
    next({ name: 'forbidden' });
  }
};

/**
 * محافظ مسیر برای بررسی دسترسی به صفحات تنظیمات
 */
export const settingsGuard = (to, from, next) => {
  const authStore = useAuthStore();
  
  // حداقل نیاز به دسترسی مشاهده تنظیمات است
  if (authStore.hasPermission(PERMISSIONS.SETTINGS_VIEW)) {
    next();
  } else {
    next({ name: 'forbidden' });
  }
};

/**
 * محافظ مسیر برای بررسی دسترسی به صفحات مدیریت کاربران
 */
export const usersGuard = (to, from, next) => {
  const authStore = useAuthStore();
  
  // حداقل نیاز به دسترسی مشاهده کاربران است
  if (authStore.hasPermission(PERMISSIONS.USER_VIEW)) {
    next();
  } else {
    next({ name: 'forbidden' });
  }
}; 