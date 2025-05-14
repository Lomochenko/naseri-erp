import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../store/auth';
import { PERMISSIONS } from '../utils/rbac';

// تنبل‌بارگذاری (Lazy Loading) کامپوننت‌ها برای بهبود کارایی
const Login = () => import('../views/auth/Login.vue');
const Dashboard = () => import('../views/Dashboard.vue');
const ProductsList = () => import('../views/products/ProductsList.vue');
const AccountingDashboard = () => import('../views/accounting/AccountingDashboard.vue');
const InventoryList = () => import('../views/inventory/InventoryList.vue');
const NotFound = () => import('../views/errors/NotFound.vue');
const Forbidden = () => import('../views/errors/Forbidden.vue');

// تعریف مسیرها
const routes = [
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: { 
      title: 'ورود به سیستم',
      requiresAuth: false
    }
  },
  {
    path: '/forbidden',
    name: 'forbidden',
    component: Forbidden,
    meta: { 
      title: 'دسترسی غیرمجاز',
      requiresAuth: false
    }
  },
  {
    path: '/',
    name: 'dashboard',
    component: Dashboard,
    meta: { 
      title: 'داشبورد',
      requiresAuth: true
    }
  },
  {
    path: '/products',
    name: 'products',
    component: ProductsList,
    meta: { 
      title: 'مدیریت محصولات',
      requiresAuth: true,
      permissions: [PERMISSIONS.PRODUCT_VIEW]
    }
  },
  {
    path: '/inventory',
    name: 'inventory',
    component: InventoryList,
    meta: { 
      title: 'مدیریت موجودی',
      requiresAuth: true,
      permissions: [PERMISSIONS.INVENTORY_VIEW]
    }
  },
  {
    path: '/accounting',
    name: 'accounting',
    component: AccountingDashboard,
    meta: { 
      title: 'داشبورد حسابداری',
      requiresAuth: true,
      permissions: [PERMISSIONS.ACCOUNTING_VIEW]
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFound,
    meta: { title: 'صفحه یافت نشد' }
  }
];

// ایجاد روتر
const router = createRouter({
  history: createWebHistory(),
  routes
});

// محافظ مسیرها برای احراز هویت و دسترسی‌ها
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const isLoggedIn = authStore.isLoggedIn;
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  
  // مسیر نیازمند احراز هویت اما کاربر وارد نشده است
  if (requiresAuth && !isLoggedIn) {
    next({ name: 'login', query: { redirect: to.fullPath } });
    return;
  }
  
  // کاربر وارد شده و می‌خواهد به صفحه ورود برود
  if (isLoggedIn && to.name === 'login') {
    next({ name: 'dashboard' });
    return;
  }
  
  // بررسی دسترسی‌های لازم برای مسیر
  if (requiresAuth && to.meta.permissions) {
    const requiredPermissions = to.meta.permissions;
    const hasAccess = authStore.hasAnyPermission(requiredPermissions);
    
    if (!hasAccess) {
      // کاربر دسترسی ندارد
      next({ name: 'forbidden' });
      return;
    }
  }
  
  // در سایر موارد، اجازه دسترسی داده می‌شود
  next();
});

// تنظیم عنوان صفحه براساس متادیتای مسیر
router.afterEach((to) => {
  document.title = to.meta.title ? `${to.meta.title} | یراق‌آلات ناصری` : 'سیستم مدیریت یراق‌آلات ناصری';
});

export default router; 