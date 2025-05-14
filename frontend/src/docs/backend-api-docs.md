# مستندات API بک‌اند سیستم ERP یراق‌آلات ناصری

این سند مستندات کاملی برای API بک‌اند سیستم ERP یراق‌آلات ناصری ارائه می‌دهد. این مستندات راهنمای پیاده‌سازی بک‌اند است.

## ساختار API

تمام API‌ها با پیشوند `/api/` شروع می‌شوند و به‌صورت RESTful طراحی شده‌اند.

## احراز هویت

برای احراز هویت از توکن استفاده می‌شود. توکن در هدر `Authorization` ارسال می‌شود:

```
Authorization: Token <token_value>
```

### API‌های احراز هویت

#### ورود به سیستم
```
POST /api/users/login/
```

**پارامترها**:
- `phone_number`: شماره تلفن کاربر
- `password`: رمز عبور

**پاسخ**:
```json
{
  "token": "string",
  "user": {
    "id": 1,
    "first_name": "string",
    "last_name": "string",
    "phone_number": "string",
    "email": "string",
    "is_staff": false,
    "is_active": true
  }
}
```

#### خروج از سیستم
```
POST /api/users/logout/
```

**پاسخ**:
```json
{
  "detail": "خروج موفقیت‌آمیز"
}
```

#### دریافت پروفایل کاربر
```
GET /api/users/profile/
```

**پاسخ**:
```json
{
  "id": 1,
  "first_name": "string",
  "last_name": "string",
  "phone_number": "string",
  "email": "string",
  "is_staff": false,
  "is_active": true
}
```

## محصولات

### API‌های محصولات

#### دریافت لیست محصولات
```
GET /api/products/products/
```

**پارامترهای پرس‌وجو**:
- `search`: متن جستجو
- `category`: شناسه دسته‌بندی
- `ordering`: فیلد مرتب‌سازی (با - برای نزولی)
- `page`: شماره صفحه
- `page_size`: تعداد آیتم در هر صفحه

**پاسخ**:
```json
{
  "count": 100,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 1,
      "code": "string",
      "name": "string",
      "category": {
        "id": 1,
        "name": "string"
      },
      "unit": {
        "id": 1,
        "name": "string"
      },
      "price": 125000,
      "stock": 24,
      "image": "string",
      "description": "string"
    }
  ]
}
```

#### دریافت جزئیات محصول
```
GET /api/products/products/{id}/
```

**پاسخ**:
```json
{
  "id": 1,
  "code": "string",
  "name": "string",
  "category": {
    "id": 1,
    "name": "string"
  },
  "unit": {
    "id": 1,
    "name": "string"
  },
  "price": 125000,
  "stock": 24,
  "image": "string",
  "description": "string"
}
```

#### افزودن محصول جدید
```
POST /api/products/products/
```

**پارامترها**:
- `code`: کد محصول
- `name`: نام محصول
- `category`: شناسه دسته‌بندی
- `unit`: شناسه واحد
- `price`: قیمت
- `image`: تصویر (اختیاری)
- `description`: توضیحات (اختیاری)

#### به‌روزرسانی محصول
```
PUT /api/products/products/{id}/
```

**پارامترها**: مشابه افزودن محصول

#### حذف محصول
```
DELETE /api/products/products/{id}/
```

### API‌های دسته‌بندی

#### دریافت لیست دسته‌بندی‌ها
```
GET /api/products/categories/
```

**پاسخ**:
```json
{
  "results": [
    {
      "id": 1,
      "name": "string"
    }
  ]
}
```

#### افزودن دسته‌بندی جدید
```
POST /api/products/categories/
```

**پارامترها**:
- `name`: نام دسته‌بندی

### API‌های واحد اندازه‌گیری

#### دریافت لیست واحدها
```
GET /api/products/units/
```

**پاسخ**:
```json
{
  "results": [
    {
      "id": 1,
      "name": "string"
    }
  ]
}
```

## موجودی

### API‌های موجودی

#### دریافت لیست موجودی
```
GET /api/inventory/inventory/
```

**پارامترهای پرس‌وجو**:
- `search`: متن جستجو
- `warehouse`: شناسه انبار
- `low_stock`: فقط موجودی کم (1 یا 0)
- `page`: شماره صفحه
- `page_size`: تعداد آیتم در هر صفحه

**پاسخ**:
```json
{
  "count": 100,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "code": "string",
        "name": "string",
        "category": {
          "id": 1,
          "name": "string"
        },
        "unit": {
          "id": 1,
          "name": "string"
        },
        "price": 125000,
        "image": "string"
      },
      "warehouse_id": 1,
      "quantity": 24
    }
  ]
}
```

#### دریافت لیست انبارها
```
GET /api/inventory/warehouses/
```

**پاسخ**:
```json
{
  "results": [
    {
      "id": 1,
      "name": "string",
      "location": "string"
    }
  ]
}
```

#### دریافت تاریخچه تراکنش‌ها
```
GET /api/inventory/transactions/
```

**پارامترهای پرس‌وجو**:
- `product`: شناسه محصول
- `warehouse`: شناسه انبار

**پاسخ**:
```json
{
  "results": [
    {
      "id": 1,
      "product_id": 1,
      "warehouse_id": 1,
      "transaction_type": "IN",
      "quantity": 10,
      "created_at": "string",
      "notes": "string",
      "created_by": "string"
    }
  ]
}
```

#### ثبت تراکنش جدید
```
POST /api/inventory/transactions/
```

**پارامترها**:
- `product`: شناسه محصول
- `warehouse`: شناسه انبار
- `transaction_type`: نوع تراکنش (IN, OUT, ADJUST, TRANSFER)
- `quantity`: مقدار
- `notes`: توضیحات (اختیاری)

#### تنظیم موجودی
```
POST /api/inventory/adjustments/
```

**پارامترها**:
- `product`: شناسه محصول
- `warehouse`: شناسه انبار
- `quantity`: مقدار جدید
- `reason`: دلیل تغییر
- `notes`: توضیحات (اختیاری)

## فروش

### API‌های فروش

#### دریافت لیست فروش‌ها
```
GET /api/sales/sales/
```

**پارامترهای پرس‌وجو**:
- `search`: متن جستجو
- `status`: وضعیت (PAID, PENDING, CANCELLED)
- `date_from`: از تاریخ
- `date_to`: تا تاریخ
- `page`: شماره صفحه
- `page_size`: تعداد آیتم در هر صفحه

**پاسخ**:
```json
{
  "count": 100,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 1,
      "invoice_number": "string",
      "customer": {
        "id": 1,
        "name": "string",
        "phone_number": "string"
      },
      "date": "string",
      "subtotal": 4500000,
      "discount": 0,
      "tax_percent": 9,
      "tax_amount": 405000,
      "total_amount": 4905000,
      "payment_method": "CASH",
      "status": "PAID",
      "notes": "string",
      "created_by": "string"
    }
  ]
}
```

#### دریافت جزئیات فروش
```
GET /api/sales/sales/{id}/
```

**پاسخ**:
```json
{
  "id": 1,
  "invoice_number": "string",
  "customer": {
    "id": 1,
    "name": "string",
    "phone_number": "string"
  },
  "date": "string",
  "subtotal": 4500000,
  "discount": 0,
  "tax_percent": 9,
  "tax_amount": 405000,
  "total_amount": 4905000,
  "payment_method": "CASH",
  "status": "PAID",
  "notes": "string",
  "created_by": "string",
  "items": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "code": "string",
        "name": "string",
        "unit": {
          "id": 1,
          "name": "string"
        }
      },
      "quantity": 20,
      "unit_price": 125000,
      "discount": 0,
      "total_price": 2500000
    }
  ]
}
```

#### ثبت فروش جدید
```
POST /api/sales/sales/
```

**پارامترها**:
- `customer`: شناسه مشتری
- `payment_method`: روش پرداخت (CASH, CARD, TRANSFER, CHEQUE)
- `status`: وضعیت (PAID, PENDING, CANCELLED)
- `notes`: توضیحات (اختیاری)
- `discount`: درصد تخفیف کل
- `tax_percent`: درصد مالیات
- `items`: آرایه‌ای از اقلام فروش
  - `product`: شناسه محصول
  - `quantity`: تعداد
  - `unit_price`: قیمت واحد
  - `discount`: درصد تخفیف

#### به‌روزرسانی فروش
```
PUT /api/sales/sales/{id}/
```

**پارامترها**: مشابه ثبت فروش جدید

#### تغییر وضعیت فروش
```
PATCH /api/sales/sales/{id}/
```

**پارامترها**:
- `status`: وضعیت جدید (PAID, PENDING, CANCELLED)

#### حذف فروش
```
DELETE /api/sales/sales/{id}/
```

### API‌های مشتریان

#### دریافت لیست مشتریان
```
GET /api/sales/customers/
```

**پاسخ**:
```json
{
  "results": [
    {
      "id": 1,
      "name": "string",
      "phone_number": "string",
      "address": "string",
      "email": "string"
    }
  ]
}
```

#### افزودن مشتری جدید
```
POST /api/sales/customers/
```

**پارامترها**:
- `name`: نام مشتری
- `phone_number`: شماره تلفن
- `address`: آدرس (اختیاری)
- `email`: ایمیل (اختیاری)

## خرید

### API‌های خرید

#### دریافت لیست خریدها
```
GET /api/purchases/purchases/
```

**پارامترهای پرس‌وجو**:
- `search`: متن جستجو
- `status`: وضعیت (PAID, PENDING, CANCELLED)
- `date_from`: از تاریخ
- `date_to`: تا تاریخ
- `page`: شماره صفحه
- `page_size`: تعداد آیتم در هر صفحه

**پاسخ**:
```json
{
  "count": 100,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 1,
      "reference_number": "string",
      "supplier": {
        "id": 1,
        "name": "string",
        "phone_number": "string"
      },
      "date": "string",
      "subtotal": 3200000,
      "discount": 200000,
      "tax_percent": 9,
      "tax_amount": 270000,
      "total_amount": 3270000,
      "payment_method": "TRANSFER",
      "status": "PAID",
      "notes": "string",
      "created_by": "string"
    }
  ]
}
```

#### دریافت جزئیات خرید
```
GET /api/purchases/purchases/{id}/
```

**پاسخ**:
```json
{
  "id": 1,
  "reference_number": "string",
  "supplier": {
    "id": 1,
    "name": "string",
    "phone_number": "string"
  },
  "date": "string",
  "subtotal": 3200000,
  "discount": 200000,
  "tax_percent": 9,
  "tax_amount": 270000,
  "total_amount": 3270000,
  "payment_method": "TRANSFER",
  "status": "PAID",
  "notes": "string",
  "created_by": "string",
  "items": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "code": "string",
        "name": "string",
        "unit": {
          "id": 1,
          "name": "string"
        }
      },
      "quantity": 20,
      "unit_price": 100000,
      "discount": 10,
      "total_price": 1800000
    }
  ]
}
```

#### ثبت خرید جدید
```
POST /api/purchases/purchases/
```

**پارامترها**:
- `supplier`: شناسه تامین‌کننده
- `payment_method`: روش پرداخت (CASH, CARD, TRANSFER, CHEQUE)
- `status`: وضعیت (PAID, PENDING, CANCELLED)
- `notes`: توضیحات (اختیاری)
- `discount`: درصد تخفیف کل
- `tax_percent`: درصد مالیات
- `items`: آرایه‌ای از اقلام خرید
  - `product`: شناسه محصول
  - `quantity`: تعداد
  - `unit_price`: قیمت واحد
  - `discount`: درصد تخفیف

#### به‌روزرسانی خرید
```
PUT /api/purchases/purchases/{id}/
```

**پارامترها**: مشابه ثبت خرید جدید

#### تغییر وضعیت خرید
```
PATCH /api/purchases/purchases/{id}/
```

**پارامترها**:
- `status`: وضعیت جدید (PAID, PENDING, CANCELLED)

#### حذف خرید
```
DELETE /api/purchases/purchases/{id}/
```

### API‌های تامین‌کنندگان

#### دریافت لیست تامین‌کنندگان
```
GET /api/purchases/suppliers/
```

**پاسخ**:
```json
{
  "results": [
    {
      "id": 1,
      "name": "string",
      "phone_number": "string",
      "address": "string",
      "email": "string"
    }
  ]
}
```

#### افزودن تامین‌کننده جدید
```
POST /api/purchases/suppliers/
```

**پارامترها**:
- `name`: نام تامین‌کننده
- `phone_number`: شماره تلفن
- `address`: آدرس (اختیاری)
- `email`: ایمیل (اختیاری)

## حسابداری

### API‌های تراکنش‌های مالی

#### دریافت لیست تراکنش‌ها
```
GET /api/accounting/transactions/
```

**پارامترهای پرس‌وجو**:
- `search`: متن جستجو
- `transaction_type`: نوع تراکنش (INCOME, EXPENSE)
- `date_from`: از تاریخ
- `date_to`: تا تاریخ
- `bank_account`: شناسه حساب بانکی
- `page`: شماره صفحه
- `page_size`: تعداد آیتم در هر صفحه

**پاسخ**:
```json
{
  "count": 100,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 1,
      "transaction_type": "INCOME",
      "amount": 4500000,
      "description": "string",
      "date": "string",
      "bank_account": {
        "id": 1,
        "name": "string",
        "bank_name": "string"
      },
      "created_by": "string",
      "created_at": "string"
    }
  ]
}
```

#### ثبت تراکنش جدید
```
POST /api/accounting/transactions/
```

**پارامترها**:
- `transaction_type`: نوع تراکنش (INCOME, EXPENSE)
- `amount`: مبلغ (برای EXPENSE مقدار منفی)
- `description`: توضیحات
- `date`: تاریخ
- `bank_account`: شناسه حساب بانکی (اختیاری)

#### حذف تراکنش
```
DELETE /api/accounting/transactions/{id}/
```

### API‌های حساب‌های بانکی

#### دریافت لیست حساب‌های بانکی
```
GET /api/accounting/bank-accounts/
```

**پاسخ**:
```json
{
  "results": [
    {
      "id": 1,
      "name": "string",
      "bank_name": "string",
      "account_number": "string",
      "balance": 10000000
    }
  ]
}
```

#### افزودن حساب بانکی جدید
```
POST /api/accounting/bank-accounts/
```

**پارامترها**:
- `name`: نام حساب
- `bank_name`: نام بانک
- `account_number`: شماره حساب
- `initial_balance`: موجودی اولیه (اختیاری)

### API‌های خلاصه مالی

#### دریافت خلاصه مالی
```
GET /api/accounting/summary/
```

**پارامترهای پرس‌وجو**:
- `period`: دوره زمانی (day, week, month, year)

**پاسخ**:
```json
{
  "revenue": 58450000,
  "expenses": 42830000,
  "profit": 15620000,
  "dueAmount": 8200000
}
```

### API‌های پرداخت‌های معوق

#### دریافت لیست پرداخت‌های معوق
```
GET /api/accounting/due-payments/
```

**پاسخ**:
```json
{
  "results": [
    {
      "id": 1,
      "invoice_number": "string",
      "customer": "string",
      "due_date": "string",
      "amount": 1417000,
      "status": "UPCOMING"
    }
  ]
}
```

#### به‌روزرسانی وضعیت پرداخت
```
PATCH /api/accounting/due-payments/{id}/
```

**پارامترها**:
- `status`: وضعیت جدید (UPCOMING, OVERDUE, PAID)

### API‌های گزارش‌گیری

#### دریافت داده‌های نمودار
```
GET /api/accounting/chart-data/
```

**پارامترهای پرس‌وجو**:
- `chart_type`: نوع نمودار (revenue-expenses, profit-trend)
- `period`: دوره زمانی (month, quarter, year)

**پاسخ**:
```json
{
  "labels": ["فروردین", "اردیبهشت", "خرداد"],
  "datasets": [
    {
      "label": "درآمد",
      "data": [45000000, 52000000, 58450000]
    },
    {
      "label": "هزینه",
      "data": [35000000, 38000000, 42830000]
    }
  ]
}
```

#### دریافت گزارش سود و زیان
```
GET /api/accounting/profit-loss-report/
```

**پارامترهای پرس‌وجو**:
- `date_from`: از تاریخ
- `date_to`: تا تاریخ

**پاسخ**:
```json
{
  "revenue": {
    "total": 58450000,
    "categories": [
      {
        "name": "فروش محصولات",
        "amount": 55450000
      },
      {
        "name": "سایر درآمدها",
        "amount": 3000000
      }
    ]
  },
  "expenses": {
    "total": 42830000,
    "categories": [
      {
        "name": "خرید کالا",
        "amount": 28420000
      },
      {
        "name": "حقوق و دستمزد",
        "amount": 12500000
      },
      {
        "name": "سایر هزینه‌ها",
        "amount": 1910000
      }
    ]
  },
  "profit": 15620000
}
``` 