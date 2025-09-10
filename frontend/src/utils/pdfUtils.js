/**
 * PDF utilities for generating receipts with Persian text support
 */
import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'
import { formatPrice, formatDate } from './qrCodeUtils'

/**
 * Generate PDF receipt with Persian text support
 * @param {Object} invoice - Invoice data
 * @param {boolean} autoDownload - Whether to auto-download the PDF
 * @returns {Promise<Blob>} PDF blob
 */
export const generateReceiptPDF = async (invoice, autoDownload = true) => {
  try {
    // Create a temporary HTML element for rendering
    const tempDiv = document.createElement('div')
    tempDiv.style.position = 'absolute'
    tempDiv.style.left = '-9999px'
    tempDiv.style.top = '-9999px'
    tempDiv.style.width = '800px'
    tempDiv.style.padding = '40px'
    tempDiv.style.fontFamily = 'Tahoma, Arial, sans-serif'
    tempDiv.style.direction = 'rtl'
    tempDiv.style.backgroundColor = 'white'

    // Generate QR code data
    const qrData = JSON.stringify({
      id: invoice.id,
      invoice_number: invoice.invoice_number,
      customer_name: invoice.customer_name,
      total: invoice.total,
      sale_date: invoice.sale_date,
      status: invoice.status,
      storage_key: invoice.qr_key || invoice.storage_key,
      app_name: 'Yaraghalat_Naseri_ERP'
    })

    // Create receipt HTML
    tempDiv.innerHTML = `
      <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="font-size: 28px; margin: 0; color: #333;">یراقالات ناصری</h1>
        <h2 style="font-size: 20px; margin: 10px 0; color: #666;">رسید فروش</h2>
      </div>

      <div style="display: flex; justify-content: space-between; margin-bottom: 30px; border-bottom: 2px solid #eee; padding-bottom: 20px;">
        <div style="text-align: right;">
          <div style="margin-bottom: 10px;"><strong>شماره فاکتور:</strong> ${invoice.invoice_number || 'در انتظار تولید'}</div>
          <div style="margin-bottom: 10px;"><strong>تاریخ:</strong> ${formatDate(invoice.sale_date)}</div>
          <div><strong>وضعیت:</strong> ${getStatusText(invoice.status)}</div>
        </div>
        <div style="text-align: left;">
          <div style="margin-bottom: 10px;"><strong>مشتری:</strong> ${invoice.customer_name}</div>
          <div><strong>تاریخ صدور:</strong> ${formatDate(new Date().toISOString())}</div>
        </div>
      </div>

      <table style="width: 100%; border-collapse: collapse; margin-bottom: 30px;">
        <thead>
          <tr style="background-color: #f8f9fa;">
            <th style="border: 1px solid #dee2e6; padding: 12px; text-align: right; font-weight: bold;">محصول</th>
            <th style="border: 1px solid #dee2e6; padding: 12px; text-align: center; font-weight: bold;">تعداد</th>
            <th style="border: 1px solid #dee2e6; padding: 12px; text-align: center; font-weight: bold;">قیمت واحد</th>
            <th style="border: 1px solid #dee2e6; padding: 12px; text-align: center; font-weight: bold;">تخفیف</th>
            <th style="border: 1px solid #dee2e6; padding: 12px; text-align: center; font-weight: bold;">جمع</th>
          </tr>
        </thead>
        <tbody>
          ${generateItemsHTML(invoice.items)}
        </tbody>
      </table>

      <div style="text-align: right; margin-bottom: 30px;">
        <div style="font-size: 18px; font-weight: bold; padding: 15px; background-color: #f8f9fa; border: 2px solid #dee2e6; border-radius: 8px;">
          مبلغ نهایی: ${formatPrice(invoice.total)}
        </div>
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 40px; border-top: 2px solid #eee; padding-top: 20px;">
        <div style="text-align: right;">
          <div style="font-size: 12px; color: #666; margin-bottom: 5px;">کد QR برای دسترسی آفلاین:</div>
          <div id="qr-placeholder" style="width: 120px; height: 120px; border: 2px solid #ddd; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #999;">
            QR Code
          </div>
        </div>
        <div style="text-align: left; font-size: 12px; color: #666;">
          <div>تاریخ چاپ: ${formatDate(new Date().toISOString())}</div>
          <div style="margin-top: 5px;">سیستم مدیریت یراقالات ناصری</div>
        </div>
      </div>
    `

    document.body.appendChild(tempDiv)

    // Generate QR code and add to the placeholder
    await addQRCodeToElement(tempDiv.querySelector('#qr-placeholder'), qrData)

    // Convert to canvas
    const canvas = await html2canvas(tempDiv, {
      scale: 2,
      useCORS: true,
      allowTaint: true,
      backgroundColor: '#ffffff',
      width: 800,
      height: tempDiv.scrollHeight
    })

    // Remove temporary element
    document.body.removeChild(tempDiv)

    // Create PDF
    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4'
    })

    const imgData = canvas.toDataURL('image/png')
    const imgWidth = 210 // A4 width in mm
    const pageHeight = 297 // A4 height in mm
    const imgHeight = (canvas.height * imgWidth) / canvas.width
    let heightLeft = imgHeight

    let position = 0

    // Add first page
    pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight)
    heightLeft -= pageHeight

    // Add additional pages if needed
    while (heightLeft >= 0) {
      position = heightLeft - imgHeight
      pdf.addPage()
      pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight)
      heightLeft -= pageHeight
    }

    // Generate filename
    const filename = `receipt_${invoice.invoice_number || invoice.id}_${new Date().getTime()}.pdf`

    if (autoDownload) {
      // Auto-download the PDF
      pdf.save(filename)
    }

    // Return PDF blob for further processing if needed
    return pdf.output('blob')

  } catch (error) {
    console.error('Error generating PDF:', error)
    throw new Error('خطا در تولید PDF: ' + error.message)
  }
}

/**
 * Add QR code to HTML element
 * @param {HTMLElement} element - Target element
 * @param {string} qrData - QR code data
 */
const addQRCodeToElement = async (element, qrData) => {
  try {
    // Use QRCode library if available
    if (window.QRCode) {
      const canvas = document.createElement('canvas')
      await window.QRCode.toCanvas(canvas, qrData, {
        width: 120,
        height: 120,
        margin: 2,
        color: {
          dark: '#000000',
          light: '#FFFFFF'
        }
      })
      element.innerHTML = ''
      element.appendChild(canvas)
    } else {
      // Fallback: show QR data as text
      element.innerHTML = `<div style="font-size: 8px; word-break: break-all; padding: 5px;">${qrData.substring(0, 50)}...</div>`
    }
  } catch (error) {
    console.error('Error generating QR code:', error)
    element.innerHTML = '<div style="font-size: 10px; color: #999;">QR Code Error</div>'
  }
}

/**
 * Generate HTML for invoice items
 * @param {Array} items - Invoice items
 * @returns {string} HTML string
 */
const generateItemsHTML = (items) => {
  if (!items || items.length === 0) {
    return '<tr><td colspan="5" style="border: 1px solid #dee2e6; padding: 12px; text-align: center; color: #666;">اطلاعات آیتم‌ها در دسترس نیست</td></tr>'
  }

  return items.map(item => `
    <tr>
      <td style="border: 1px solid #dee2e6; padding: 12px; text-align: right;">${item.product_name || 'محصول نامشخص'}</td>
      <td style="border: 1px solid #dee2e6; padding: 12px; text-align: center;">${item.quantity || 0}</td>
      <td style="border: 1px solid #dee2e6; padding: 12px; text-align: center;">${formatPrice(item.unit_price || 0)}</td>
      <td style="border: 1px solid #dee2e6; padding: 12px; text-align: center;">${formatPrice(item.discount || 0)}</td>
      <td style="border: 1px solid #dee2e6; padding: 12px; text-align: center;">${formatPrice(((item.quantity || 0) * (item.unit_price || 0)) - (item.discount || 0))}</td>
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
 * Load QRCode library dynamically
 * @returns {Promise} Promise that resolves when library is loaded
 */
export const loadQRCodeLibrary = () => {
  return new Promise((resolve, reject) => {
    if (window.QRCode) {
      resolve()
      return
    }

    const script = document.createElement('script')
    script.src = 'https://cdn.jsdelivr.net/npm/qrcode@1.5.3/build/qrcode.min.js'
    script.onload = () => resolve()
    script.onerror = () => reject(new Error('Failed to load QRCode library'))
    document.head.appendChild(script)
  })
}

/**
 * Generate and download PDF receipt
 * @param {Object} invoice - Invoice data
 * @returns {Promise} Promise that resolves when PDF is generated
 */
export const downloadReceiptPDF = async (invoice) => {
  try {
    console.log('Starting PDF generation for invoice:', invoice)

    // Create a simple PDF using jsPDF directly
    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4'
    })

    // Set font for Persian text support (use helvetica for better compatibility)
    pdf.setFont('helvetica')

    // Add content to PDF
    let yPosition = 20

    // Add mobile-friendly header
    pdf.setFontSize(18)
    pdf.text('Yaraghalat Naseri Hardware Store', 105, yPosition, { align: 'center' })
    yPosition += 8

    // Persian Header (for Persian-capable devices)
    pdf.setFontSize(16)
    pdf.text('یراقالات ناصری', 105, yPosition, { align: 'center' })
    yPosition += 8

    pdf.setFontSize(14)
    pdf.text('رسید فروش', 105, yPosition, { align: 'center' })
    yPosition += 15

    // Invoice details
    pdf.setFontSize(12)
    pdf.text(`شماره فاکتور: ${invoice.invoice_number || 'در انتظار تولید'}`, 20, yPosition)
    yPosition += 8

    pdf.text(`مشتری: ${invoice.customer_name || 'نامشخص'}`, 20, yPosition)
    yPosition += 8

    pdf.text(`تاریخ: ${formatDate(invoice.sale_date)}`, 20, yPosition)
    yPosition += 8

    pdf.text(`وضعیت: ${getStatusText(invoice.status)}`, 20, yPosition)
    yPosition += 15

    // Items table header
    pdf.text('محصولات:', 20, yPosition)
    yPosition += 8

    // Items
    if (invoice.items && invoice.items.length > 0) {
      invoice.items.forEach((item, index) => {
        const itemText = `${index + 1}. ${item.product_name || 'محصول نامشخص'} - تعداد: ${item.quantity || 0} - قیمت: ${formatPrice(item.unit_price || 0)}`
        pdf.text(itemText, 25, yPosition)
        yPosition += 6
      })
    } else {
      pdf.text('اطلاعات آیتم‌ها در دسترس نیست', 25, yPosition)
      yPosition += 6
    }

    yPosition += 10

    // Total
    pdf.setFontSize(14)
    pdf.text(`مبلغ نهایی: ${formatPrice(invoice.total)}`, 20, yPosition)
    yPosition += 20

    // QR Code placeholder
    pdf.setFontSize(10)
    pdf.text('کد QR برای دسترسی آفلاین:', 20, yPosition)
    yPosition += 6

    // Add QR code data as text (simplified)
    const qrData = JSON.stringify({
      id: invoice.id,
      invoice_number: invoice.invoice_number,
      total: invoice.total,
      app_name: 'Yaraghalat_Naseri_ERP'
    })

    pdf.setFontSize(8)
    const qrLines = pdf.splitTextToSize(qrData, 170)
    pdf.text(qrLines, 20, yPosition)
    yPosition += qrLines.length * 3

    // Footer
    yPosition += 10
    pdf.setFontSize(10)
    pdf.text(`تاریخ چاپ: ${formatDate(new Date().toISOString())}`, 20, yPosition)
    yPosition += 5
    pdf.text('سیستم مدیریت یراقالات ناصری', 20, yPosition)

    // Generate filename and download
    const filename = `receipt_${invoice.invoice_number || invoice.id}_${new Date().getTime()}.pdf`
    pdf.save(filename)

    console.log('PDF generated and downloaded successfully')
    return { success: true, message: 'PDF رسید با موفقیت دانلود شد' }

  } catch (error) {
    console.error('Error downloading PDF:', error)
    return { success: false, error: error.message }
  }
}
