// Public, build-time identity. Each business gets its own frontend build and API.
const isDehghan = import.meta.env.VITE_BUSINESS_ID === 'dehghan'

export const brand = Object.freeze(isDehghan ? {
  businessName: 'سیستم مدیریتی مدیر دهقان',
  dashboardName: 'داشبورد مدیر دهقان',
  shortName: 'مدیر دهقان',
  invoiceName: 'مدیر دهقان',
  invoiceSubtitle: 'سند معاملات · DEHGHAN ERP',
  digitalDocumentName: 'سند دیجیتال مدیر دهقان',
  qrAppName: 'Modir_Dehghan_ERP',
} : {
  businessName: 'سیستم مدیریت یراقالات ناصری',
  dashboardName: 'داشبورد یراقالات ناصری',
  shortName: 'یراقالات ناصری',
  invoiceName: 'یراق‌آلات ناصری',
  invoiceSubtitle: 'سند معاملات · NASERI ERP',
  digitalDocumentName: 'سند دیجیتال ناصری',
  qrAppName: 'Yaraghalat_Naseri_ERP',
})
