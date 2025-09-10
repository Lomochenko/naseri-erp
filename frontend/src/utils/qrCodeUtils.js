/**
 * QR Code utilities for offline invoice management
 */

/**
 * Generate QR code data for an invoice
 * @param {Object} order - Sales order object
 * @returns {Object} QR code data
 */
export const generateQRCodeData = (order) => {
  const qrData = {
    id: order.id,
    invoice_number: order.invoice_number,
    customer_name: order.customer_name,
    total: order.total,
    sale_date: order.sale_date,
    status: order.status,
    generated_at: new Date().toISOString(),
    app_name: 'Yaraghalat_Naseri_ERP',
    version: '1.0'
  }

  return qrData
}

/**
 * Generate mobile-compatible QR code URL
 * @param {Object} order - Sales order object
 * @returns {string} Mobile-compatible URL for QR code
 */
export const generateMobileQRCodeURL = (order) => {
  // Store invoice offline first
  const storageKey = storeInvoiceOffline(order)

  // Get current domain (works in both development and production)
  const baseURL = window.location.origin

  // Create mobile-friendly URL
  const mobileURL = `${baseURL}/mobile-receipt/${storageKey}`

  return mobileURL
}

/**
 * Store invoice data in localStorage for offline access
 * @param {Object} order - Sales order object
 * @returns {string} Storage key
 */
export const storeInvoiceOffline = (order) => {
  const invoiceKey = `invoice_${order.id}_${Date.now()}`
  const qrData = generateQRCodeData(order)

  const storageData = {
    ...order,
    ...qrData,
    qr_key: invoiceKey,
    storage_key: invoiceKey
  }

  localStorage.setItem(invoiceKey, JSON.stringify(storageData))

  // Also store in a master index for easy retrieval
  const masterIndex = getStoredInvoicesIndex()
  masterIndex[invoiceKey] = {
    id: order.id,
    invoice_number: order.invoice_number,
    customer_name: order.customer_name,
    total: order.total,
    sale_date: order.sale_date,
    stored_at: new Date().toISOString()
  }
  localStorage.setItem('invoices_index', JSON.stringify(masterIndex))

  return invoiceKey
}

/**
 * Retrieve invoice from localStorage
 * @param {string} storageKey - Storage key
 * @returns {Object|null} Invoice data or null if not found
 */
export const retrieveStoredInvoice = (storageKey) => {
  try {
    const storedData = localStorage.getItem(storageKey)
    return storedData ? JSON.parse(storedData) : null
  } catch (error) {
    console.error('Error retrieving stored invoice:', error)
    return null
  }
}

/**
 * Get all stored invoices
 * @returns {Array} Array of stored invoices
 */
export const getAllStoredInvoices = () => {
  const invoices = []

  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i)
    if (key && key.startsWith('invoice_')) {
      try {
        const invoice = JSON.parse(localStorage.getItem(key))
        invoices.push(invoice)
      } catch (error) {
        console.error('Error parsing stored invoice:', error)
      }
    }
  }

  return invoices.sort((a, b) => new Date(b.generated_at) - new Date(a.generated_at))
}

/**
 * Get stored invoices index
 * @returns {Object} Invoices index
 */
export const getStoredInvoicesIndex = () => {
  try {
    const index = localStorage.getItem('invoices_index')
    return index ? JSON.parse(index) : {}
  } catch (error) {
    console.error('Error getting invoices index:', error)
    return {}
  }
}

/**
 * Parse QR code data
 * @param {string} qrCodeString - QR code string
 * @returns {Object|null} Parsed data or null if invalid
 */
export const parseQRCode = (qrCodeString) => {
  try {
    const parsedData = JSON.parse(qrCodeString)

    // Validate that it's our app's QR code
    if (parsedData.app_name !== 'Yaraghalat_Naseri_ERP') {
      throw new Error('Invalid QR code - not from this app')
    }

    return parsedData
  } catch (error) {
    console.error('Error parsing QR code:', error)
    return null
  }
}

/**
 * Retrieve invoice by QR code data
 * @param {string} qrCodeString - QR code string
 * @returns {Object|null} Invoice data or null if not found
 */
export const getInvoiceByQRCode = (qrCodeString) => {
  const qrData = parseQRCode(qrCodeString)

  if (!qrData) {
    return null
  }

  // If QR code contains storage key, retrieve from localStorage
  if (qrData.storage_key) {
    return retrieveStoredInvoice(qrData.storage_key)
  }

  // If QR code contains direct invoice data, return it
  if (qrData.id) {
    return qrData
  }

  return null
}

/**
 * Clean up old stored invoices (older than 30 days)
 */
export const cleanupOldInvoices = () => {
  const thirtyDaysAgo = new Date()
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30)

  const keysToRemove = []

  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i)
    if (key && key.startsWith('invoice_')) {
      try {
        const invoice = JSON.parse(localStorage.getItem(key))
        const storedDate = new Date(invoice.generated_at)

        if (storedDate < thirtyDaysAgo) {
          keysToRemove.push(key)
        }
      } catch (error) {
        // If we can't parse it, remove it
        keysToRemove.push(key)
      }
    }
  }

  // Remove old invoices
  keysToRemove.forEach(key => {
    localStorage.removeItem(key)
  })

  // Update master index
  const masterIndex = getStoredInvoicesIndex()
  keysToRemove.forEach(key => {
    delete masterIndex[key]
  })
  localStorage.setItem('invoices_index', JSON.stringify(masterIndex))

  return keysToRemove.length
}

/**
 * Export invoice data as downloadable file
 * @param {Object} invoice - Invoice data
 * @returns {string} Download URL
 */
export const exportInvoiceAsFile = (invoice) => {
  const dataStr = JSON.stringify(invoice, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })

  return URL.createObjectURL(dataBlob)
}

/**
 * Format price for display
 * @param {number} price - Price value
 * @returns {string} Formatted price
 */
export const formatPrice = (price) => {
  if (!price) return '0 تومان'
  return new Intl.NumberFormat('fa-IR').format(price) + ' تومان'
}

/**
 * Format date for display
 * @param {string} dateString - Date string
 * @returns {string} Formatted date
 */
export const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('fa-IR-u-ca-persian')
}

/**
 * Format date and time for display
 * @param {string} dateString - Date string
 * @returns {string} Formatted date and time
 */
export const formatDateTime = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('fa-IR-u-ca-persian')
}
