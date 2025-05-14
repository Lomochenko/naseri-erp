/**
 * سیستم مدیریت دسترسی‌های کاربران (RBAC)
 * این سیستم برای کنترل دسترسی‌های کاربران به بخش‌های مختلف سیستم استفاده می‌شود
 */

// تعریف نقش‌های کاربری
export const ROLES = {
  ADMIN: 'admin',          // مدیر کل سیستم
  MANAGER: 'manager',      // مدیر
  SALES: 'sales',          // فروشنده
  INVENTORY: 'inventory',  // کارمند انبار
  ACCOUNTING: 'accounting', // حسابدار
  VIEWER: 'viewer'         // بازدیدکننده (فقط مشاهده)
};

// تعریف دسترسی‌های مختلف
export const PERMISSIONS = {
  // دسترسی‌های کاربران
  USER_VIEW: 'user:view',
  USER_CREATE: 'user:create',
  USER_EDIT: 'user:edit',
  USER_DELETE: 'user:delete',
  
  // دسترسی‌های محصولات
  PRODUCT_VIEW: 'product:view',
  PRODUCT_CREATE: 'product:create',
  PRODUCT_EDIT: 'product:edit',
  PRODUCT_DELETE: 'product:delete',
  
  // دسترسی‌های موجودی
  INVENTORY_VIEW: 'inventory:view',
  INVENTORY_ADD: 'inventory:add',
  INVENTORY_REMOVE: 'inventory:remove',
  INVENTORY_ADJUST: 'inventory:adjust',
  INVENTORY_TRANSFER: 'inventory:transfer',
  
  // دسترسی‌های فروش
  SALE_VIEW: 'sale:view',
  SALE_CREATE: 'sale:create',
  SALE_EDIT: 'sale:edit',
  SALE_DELETE: 'sale:delete',
  SALE_CANCEL: 'sale:cancel',
  CUSTOMER_MANAGE: 'customer:manage',
  
  // دسترسی‌های خرید
  PURCHASE_VIEW: 'purchase:view',
  PURCHASE_CREATE: 'purchase:create',
  PURCHASE_EDIT: 'purchase:edit',
  PURCHASE_DELETE: 'purchase:delete',
  PURCHASE_CANCEL: 'purchase:cancel',
  SUPPLIER_MANAGE: 'supplier:manage',
  
  // دسترسی‌های حسابداری
  ACCOUNTING_VIEW: 'accounting:view',
  ACCOUNTING_MANAGE: 'accounting:manage',
  REPORT_VIEW: 'report:view',
  REPORT_EXPORT: 'report:export',
  
  // دسترسی‌های تنظیمات
  SETTINGS_VIEW: 'settings:view',
  SETTINGS_EDIT: 'settings:edit'
};

// تعریف دسترسی‌های هر نقش
export const ROLE_PERMISSIONS = {
  [ROLES.ADMIN]: Object.values(PERMISSIONS), // مدیر کل تمام دسترسی‌ها را دارد
  
  [ROLES.MANAGER]: [
    // دسترسی‌های کاربران
    PERMISSIONS.USER_VIEW,
    
    // دسترسی کامل به محصولات
    PERMISSIONS.PRODUCT_VIEW,
    PERMISSIONS.PRODUCT_CREATE,
    PERMISSIONS.PRODUCT_EDIT,
    PERMISSIONS.PRODUCT_DELETE,
    
    // دسترسی کامل به موجودی
    PERMISSIONS.INVENTORY_VIEW,
    PERMISSIONS.INVENTORY_ADD,
    PERMISSIONS.INVENTORY_REMOVE,
    PERMISSIONS.INVENTORY_ADJUST,
    PERMISSIONS.INVENTORY_TRANSFER,
    
    // دسترسی کامل به فروش
    PERMISSIONS.SALE_VIEW,
    PERMISSIONS.SALE_CREATE,
    PERMISSIONS.SALE_EDIT,
    PERMISSIONS.SALE_DELETE,
    PERMISSIONS.SALE_CANCEL,
    PERMISSIONS.CUSTOMER_MANAGE,
    
    // دسترسی کامل به خرید
    PERMISSIONS.PURCHASE_VIEW,
    PERMISSIONS.PURCHASE_CREATE,
    PERMISSIONS.PURCHASE_EDIT,
    PERMISSIONS.PURCHASE_DELETE,
    PERMISSIONS.PURCHASE_CANCEL,
    PERMISSIONS.SUPPLIER_MANAGE,
    
    // دسترسی به حسابداری و گزارش‌ها
    PERMISSIONS.ACCOUNTING_VIEW,
    PERMISSIONS.REPORT_VIEW,
    PERMISSIONS.REPORT_EXPORT,
    
    // دسترسی به مشاهده تنظیمات
    PERMISSIONS.SETTINGS_VIEW
  ],
  
  [ROLES.SALES]: [
    // دسترسی به محصولات
    PERMISSIONS.PRODUCT_VIEW,
    
    // دسترسی به مشاهده موجودی
    PERMISSIONS.INVENTORY_VIEW,
    
    // دسترسی کامل به فروش
    PERMISSIONS.SALE_VIEW,
    PERMISSIONS.SALE_CREATE,
    PERMISSIONS.SALE_EDIT,
    PERMISSIONS.CUSTOMER_MANAGE,
    
    // دسترسی به گزارش‌ها
    PERMISSIONS.REPORT_VIEW
  ],
  
  [ROLES.INVENTORY]: [
    // دسترسی به محصولات
    PERMISSIONS.PRODUCT_VIEW,
    
    // دسترسی کامل به موجودی
    PERMISSIONS.INVENTORY_VIEW,
    PERMISSIONS.INVENTORY_ADD,
    PERMISSIONS.INVENTORY_REMOVE,
    PERMISSIONS.INVENTORY_ADJUST,
    PERMISSIONS.INVENTORY_TRANSFER,
    
    // دسترسی محدود به خرید و فروش
    PERMISSIONS.PURCHASE_VIEW,
    PERMISSIONS.SALE_VIEW,
    
    // دسترسی به گزارش‌ها
    PERMISSIONS.REPORT_VIEW
  ],
  
  [ROLES.ACCOUNTING]: [
    // دسترسی به مشاهده
    PERMISSIONS.PRODUCT_VIEW,
    PERMISSIONS.INVENTORY_VIEW,
    PERMISSIONS.SALE_VIEW,
    PERMISSIONS.PURCHASE_VIEW,
    
    // دسترسی کامل به حسابداری
    PERMISSIONS.ACCOUNTING_VIEW,
    PERMISSIONS.ACCOUNTING_MANAGE,
    PERMISSIONS.REPORT_VIEW,
    PERMISSIONS.REPORT_EXPORT
  ],
  
  [ROLES.VIEWER]: [
    // دسترسی فقط مشاهده
    PERMISSIONS.PRODUCT_VIEW,
    PERMISSIONS.INVENTORY_VIEW,
    PERMISSIONS.SALE_VIEW,
    PERMISSIONS.PURCHASE_VIEW,
    PERMISSIONS.ACCOUNTING_VIEW,
    PERMISSIONS.REPORT_VIEW
  ]
};

/**
 * کلاس مدیریت دسترسی‌ها
 */
class RBACService {
  constructor() {
    this.userRoles = [];
    this.userPermissions = [];
  }
  
  /**
   * تنظیم نقش‌های کاربر
   * @param {Array<string>} roles - آرایه‌ای از نقش‌های کاربر
   */
  setUserRoles(roles) {
    this.userRoles = roles || [];
    this.computePermissions();
  }
  
  /**
   * محاسبه دسترسی‌های کاربر براساس نقش‌ها
   */
  computePermissions() {
    // پاک کردن دسترسی‌های قبلی
    this.userPermissions = [];
    
    // جمع‌آوری تمام دسترسی‌های مرتبط با نقش‌های کاربر
    this.userRoles.forEach(role => {
      const permissions = ROLE_PERMISSIONS[role] || [];
      
      permissions.forEach(permission => {
        if (!this.userPermissions.includes(permission)) {
          this.userPermissions.push(permission);
        }
      });
    });
  }
  
  /**
   * بررسی دسترسی کاربر
   * @param {string} permission - دسترسی مورد نظر
   * @returns {boolean} - آیا کاربر دسترسی دارد؟
   */
  hasPermission(permission) {
    return this.userPermissions.includes(permission);
  }
  
  /**
   * بررسی وجود حداقل یکی از دسترسی‌ها
   * @param {Array<string>} permissions - آرایه‌ای از دسترسی‌ها
   * @returns {boolean} - آیا کاربر حداقل یکی از دسترسی‌ها را دارد؟
   */
  hasAnyPermission(permissions) {
    return permissions.some(permission => this.hasPermission(permission));
  }
  
  /**
   * بررسی وجود تمام دسترسی‌ها
   * @param {Array<string>} permissions - آرایه‌ای از دسترسی‌ها
   * @returns {boolean} - آیا کاربر تمام دسترسی‌ها را دارد؟
   */
  hasAllPermissions(permissions) {
    return permissions.every(permission => this.hasPermission(permission));
  }
  
  /**
   * بررسی نقش کاربر
   * @param {string} role - نقش مورد نظر
   * @returns {boolean} - آیا کاربر این نقش را دارد؟
   */
  hasRole(role) {
    return this.userRoles.includes(role);
  }
  
  /**
   * بررسی وجود حداقل یکی از نقش‌ها
   * @param {Array<string>} roles - آرایه‌ای از نقش‌ها
   * @returns {boolean} - آیا کاربر حداقل یکی از نقش‌ها را دارد؟
   */
  hasAnyRole(roles) {
    return roles.some(role => this.hasRole(role));
  }
  
  /**
   * دریافت لیست نقش‌های کاربر
   * @returns {Array<string>} - آرایه‌ای از نقش‌های کاربر
   */
  getUserRoles() {
    return [...this.userRoles];
  }
  
  /**
   * دریافت لیست دسترسی‌های کاربر
   * @returns {Array<string>} - آرایه‌ای از دسترسی‌های کاربر
   */
  getUserPermissions() {
    return [...this.userPermissions];
  }
}

// صادر کردن یک نمونه از سرویس RBAC
export const rbacService = new RBACService(); 