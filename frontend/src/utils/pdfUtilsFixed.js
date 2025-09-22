/**
 * Enhanced PDF utilities for generating receipts with Persian text support and proper UTF-8 encoding
 */
import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'
import { formatPrice, formatDate } from './qrCodeUtils'

/**
 * Download receipt PDF with proper Persian encoding
 * @param {Object} invoice - Invoice data
 * @returns {Promise} Promise that resolves when PDF is generated
 */
export const downloadReceiptPDF = async (invoice) => {
  try {
    console.log('Starting enhanced PDF generation for invoice:', invoice)

    // Create HTML content with proper UTF-8 encoding
    const receiptHTML = generateReceiptHTML(invoice)

    // Create temporary container
    const tempContainer = document.createElement('div')
    tempContainer.style.position = 'fixed'
    tempContainer.style.top = '-9999px'
    tempContainer.style.left = '-9999px'
    tempContainer.style.width = '800px'
    tempContainer.style.backgroundColor = 'white'
    tempContainer.style.fontFamily = 'Vazirmatn, Tahoma, Arial, sans-serif'
    tempContainer.style.direction = 'rtl'
    tempContainer.innerHTML = receiptHTML

    document.body.appendChild(tempContainer)

    // Wait for fonts to load
    await document.fonts.ready

    // Generate canvas with high quality
    const canvas = await html2canvas(tempContainer, {
      scale: 2,
      useCORS: true,
      allowTaint: false,
      backgroundColor: '#ffffff',
      width: 800,
      height: tempContainer.scrollHeight,
      scrollX: 0,
      scrollY: 0,
      windowWidth: 800,
      windowHeight: tempContainer.scrollHeight
    })

    // Clean up temporary container
    document.body.removeChild(tempContainer)

    // Create PDF with proper configuration
    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4',
      compress: true
    })

    // Add the canvas as image to PDF
    const imgData = canvas.toDataURL('image/png', 1.0)
    const imgWidth = 210 // A4 width in mm
    const pageHeight = 297 // A4 height in mm
    const imgHeight = (canvas.height * imgWidth) / canvas.width
    let heightLeft = imgHeight

    let position = 0

    // Add first page
    pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight, '', 'FAST')
    heightLeft -= pageHeight

    // Add additional pages if needed
    while (heightLeft >= 0) {
      position = heightLeft - imgHeight
      pdf.addPage()
      pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight, '', 'FAST')
      heightLeft -= pageHeight
    }

    // Generate filename with proper encoding
    const filename = `receipt_${invoice.invoice_number || invoice.id}_${new Date().getTime()}.pdf`

    // Save the PDF
    pdf.save(filename)

    console.log('Enhanced PDF generated and downloaded successfully')
    return { success: true, message: 'رسید PDF با موفقیت دانلود شد' }

  } catch (error) {
    console.error('Error downloading enhanced PDF:', error)
    return { success: false, error: `خطا در تولید PDF: ${error.message}` }
  }
}

/**
 * Generate HTML content for receipt with proper Persian encoding
 * @param {Object} invoice - Invoice data
 * @returns {string} HTML string
 */
const generateReceiptHTML = (invoice) => {
  // Generate QR code data with proper encoding
  const qrData = JSON.stringify({
    id: invoice.id,
    invoice_number: invoice.invoice_number,
    customer_name: invoice.customer_name,
    total: invoice.total,
    sale_date: invoice.sale_date,
    status: invoice.status,
    storage_key: invoice.qr_key || invoice.storage_key,
    app_name: 'Yaraghalat_Naseri_ERP'
  }, null, 0)

  // Generate items HTML
  const itemsHTML = generateItemsHTML(invoice.items || [])

  return `
    <div style="
      width: 100%;
      max-width: 800px;
      margin: 0 auto;
      padding: 40px;
      font-family: 'Vazirmatn', 'Tahoma', 'Arial', sans-serif;
      direction: rtl;
      background-color: white;
      color: #333;
      line-height: 1.6;
    ">
      <!-- Header -->
      <div style="text-align: center; margin-bottom: 40px; border-bottom: 3px solid #2563eb; padding-bottom: 20px;">
        <h1 style="
          font-size: 32px;
          font-weight: bold;
          color: #1e40af;
          margin: 0 0 10px 0;
          font-family: 'Vazirmatn', 'Tahoma', sans-serif;
        ">یراقالات ناصری</h1>
        <h2 style="
          font-size: 24px;
          color: #64748b;
          margin: 0;
          font-weight: normal;
        ">رسید فروش</h2>
      </div>

      <!-- Invoice Details -->
      <div style="
        display: flex;
        justify-content: space-between;
        margin-bottom: 30px;
        padding: 20px;
        background-color: #f8fafc;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
      ">
        <div style="flex: 1; text-align: right;">
          <div style="margin-bottom: 12px; font-size: 16px;">
            <strong style="color: #374151;">شماره فاکتور:</strong>
            <span style="margin-right: 10px; color: #1f2937;">${invoice.invoice_number || 'در انتظار تولید'}</span>
          </div>
          <div style="margin-bottom: 12px; font-size: 16px;">
            <strong style="color: #374151;">تاریخ:</strong>
            <span style="margin-right: 10px; color: #1f2937;">${formatDate(invoice.sale_date)}</span>
          </div>
          <div style="font-size: 16px;">
            <strong style="color: #374151;">وضعیت:</strong>
            <span style="margin-right: 10px; color: #1f2937;">${getStatusText(invoice.status)}</span>
          </div>
        </div>
        <div style="flex: 1; text-align: left;">
          <div style="margin-bottom: 12px; font-size: 16px;">
            <strong style="color: #374151;">مشتری:</strong>
            <span style="margin-right: 10px; color: #1f2937;">${invoice.customer_name || 'نامشخص'}</span>
          </div>
          <div style="font-size: 16px;">
            <strong style="color: #374151;">تاریخ صدور:</strong>
            <span style="margin-right: 10px; color: #1f2937;">${formatDate(new Date().toISOString())}</span>
          </div>
        </div>
      </div>

      <!-- Items Table -->
      <div style="margin-bottom: 30px;">
        <table style="
          width: 100%;
          border-collapse: collapse;
          border: 2px solid #e2e8f0;
          border-radius: 8px;
          overflow: hidden;
        ">
          <thead>
            <tr style="background-color: #1e40af; color: white;">
              <th style="padding: 15px; text-align: right; font-weight: bold; font-size: 16px; border: 1px solid #1e40af;">محصول</th>
              <th style="padding: 15px; text-align: center; font-weight: bold; font-size: 16px; border: 1px solid #1e40af;">تعداد</th>
              <th style="padding: 15px; text-align: center; font-weight: bold; font-size: 16px; border: 1px solid #1e40af;">قیمت واحد</th>
              <th style="padding: 15px; text-align: center; font-weight: bold; font-size: 16px; border: 1px solid #1e40af;">تخفیف</th>
              <th style="padding: 15px; text-align: center; font-weight: bold; font-size: 16px; border: 1px solid #1e40af;">جمع</th>
            </tr>
          </thead>
          <tbody>
            ${itemsHTML}
          </tbody>
        </table>
      </div>

      <!-- Total -->
      <div style="text-align: center; margin-bottom: 40px;">
        <div style="
          display: inline-block;
          padding: 20px 30px;
          background-color: #dbeafe;
          border: 2px solid #2563eb;
          border-radius: 12px;
          font-size: 24px;
          font-weight: bold;
          color: #1e40af;
        ">
          مبلغ نهایی: ${formatPrice(invoice.total)}
        </div>
      </div>

      <!-- QR Code Section -->
      <div style="
        display: flex;
        justify-content: center;
        align-items: center;
        border-top: 2px solid #e2e8f0;
      ">
        <div style="text-align: center; font-size: 14px; color: #6b7280;">
          <div style="margin-bottom: 8px;">
            تاریخ چاپ: ${formatDate(new Date().toISOString())}
          </div>
          <div style="font-weight: 500;">
            سیستم مدیریت یراقالات ناصری
          </div>
        </div>
      </div>
    </div>
  `
}

/**
 * Generate HTML for invoice items with proper encoding
 * @param {Array} items - Invoice items
 * @returns {string} HTML string
 */
const generateItemsHTML = (items) => {
  if (!items || items.length === 0) {
    return `
      <tr>
        <td colspan="5" style="
          padding: 20px;
          text-align: center;
          color: #6b7280;
          font-style: italic;
          border: 1px solid #e2e8f0;
        ">
          اطلاعات آیتم‌ها در دسترس نیست
        </td>
      </tr>
    `
  }

  return items.map((item, index) => `
    <tr style="${index % 2 === 0 ? 'background-color: #f8fafc;' : 'background-color: white;'}">
      <td style="
        padding: 15px;
        text-align: right;
        border: 1px solid #e2e8f0;
        font-size: 14px;
      ">${item.product_name || 'محصول نامشخص'}</td>
      <td style="
        padding: 15px;
        text-align: center;
        border: 1px solid #e2e8f0;
        font-size: 14px;
        font-weight: 500;
      ">${item.quantity || 0}</td>
      <td style="
        padding: 15px;
        text-align: center;
        border: 1px solid #e2e8f0;
        font-size: 14px;
      ">${formatPrice(item.unit_price || 0)}</td>
      <td style="
        padding: 15px;
        text-align: center;
        border: 1px solid #e2e8f0;
        font-size: 14px;
        color: #dc2626;
      ">${formatPrice(item.discount || 0)}</td>
      <td style="
        padding: 15px;
        text-align: center;
        border: 1px solid #e2e8f0;
        font-size: 14px;
        font-weight: 500;
        color: #059669;
      ">${formatPrice(((item.quantity || 0) * (item.unit_price || 0)) - (item.discount || 0))}</td>
    </tr>
  `).join('')
}

/**
 * Get status text in Persian
 * @param {string} status - Status code
 * @returns {string} Persian status text
 */
const getStatusText = (status) => {
  const statusMap = {
    'draft': 'پیش‌نویس',
    'confirmed': 'تأیید شده',
    'completed': 'تکمیل شده',
    'cancelled': 'لغو شده'
  }
  return statusMap[status] || status
}

/**
 * Load Persian fonts
 * @returns {Promise} Promise that resolves when fonts are loaded
 */
export const loadPersianFonts = async () => {
  try {
    // Check if Vazirmatn font is already loaded
    if (document.fonts.check('16px Vazirmatn')) {
      return Promise.resolve()
    }

    // Create font face for Vazirmatn
    const vazirmatn = new FontFace('Vazirmatn', 'url(https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/fonts/webfonts/Vazirmatn-Regular.woff2)')
    const vazirmatenBold = new FontFace('Vazirmatn', 'url(https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/fonts/webfonts/Vazirmatn-Bold.woff2)', { weight: 'bold' })

    // Load fonts
    await Promise.all([
      vazirmatn.load(),
      vazirmatenBold.load()
    ])

    // Add fonts to document
    document.fonts.add(vazirmatn)
    document.fonts.add(vazirmatenBold)

    console.log('Persian fonts loaded successfully')
    return Promise.resolve()
  } catch (error) {
    console.warn('Could not load Persian fonts:', error)
    return Promise.resolve() // Continue without custom fonts
  }
}
