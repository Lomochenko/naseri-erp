import html2canvas from 'html2canvas'
import { jsPDF } from 'jspdf'
async function exportHost(element) {
  await document.fonts.ready
  const host = document.createElement('div'); host.className = 'invoice-print-host'
  Object.assign(host.style, { position: 'absolute', left: '-10000px', top: '0', width: '794px', background: '#ffffff' })
  const sheet = element.cloneNode(true); sheet.classList.add('invoice-export'); host.appendChild(sheet); document.body.appendChild(host)
  await Promise.all([...sheet.querySelectorAll('img')].map(img => img.decode().catch(() => {})))
  await new Promise(resolve => requestAnimationFrame(resolve))
  return { host, sheet }
}
export async function downloadInvoicePDF(element, invoiceNumber) {
  const { host, sheet } = await exportHost(element)
  try {
    const canvas = await html2canvas(sheet, { scale: 2, backgroundColor: '#ffffff', logging: false })
    const pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4', compress: true })
    const width = 186, height = 273, ratio = canvas.width / width, rect = sheet.getBoundingClientRect()
    const blocks = [...sheet.querySelectorAll('[data-pdf-block]')].map(el => ({ start: Math.round((el.getBoundingClientRect().top - rect.top) * 2), end: Math.ceil((el.getBoundingClientRect().bottom - rect.top) * 2) }))
    // Keep the share QR lossless even though the page raster uses compact JPEG.
    const qr = sheet.querySelector('.qr-area img')
    const qrRect = qr?.getBoundingClientRect()
    const qrPosition = qrRect && { x: (qrRect.left - rect.left) * 2, y: (qrRect.top - rect.top) * 2, width: qrRect.width * 2, height: qrRect.height * 2 }
    const thead = sheet.querySelector('thead'), tableTop = Math.round((thead.getBoundingClientRect().top - rect.top) * 2), headerHeight = Math.ceil(thead.getBoundingClientRect().height * 2), tableBottom = Math.ceil((sheet.querySelector('table').getBoundingClientRect().bottom - rect.top) * 2)
    let start = 0, page = 0
    while (start < canvas.height) {
      if (page++) pdf.addPage()
      const repeat = start > tableTop && start < tableBottom, available = Math.floor(height * ratio) - (repeat ? headerHeight : 0)
      let end = Math.min(start + available, canvas.height)
      const crossing = blocks.find(block => block.start < end && block.end > end && block.start > start)
      if (crossing) end = crossing.start
      if (end <= start) end = Math.min(start + available, canvas.height)
      const piece = document.createElement('canvas'); piece.width = canvas.width; piece.height = end - start + (repeat ? headerHeight : 0)
      const context = piece.getContext('2d'); context.fillStyle = '#ffffff'; context.fillRect(0, 0, piece.width, piece.height)
      if (repeat) context.drawImage(canvas, 0, tableTop, canvas.width, headerHeight, 0, 0, canvas.width, headerHeight)
      context.drawImage(canvas, 0, start, canvas.width, end - start, 0, repeat ? headerHeight : 0, canvas.width, end - start)
      pdf.addImage(piece.toDataURL('image/jpeg', 0.92), 'JPEG', 12, 12, width, piece.height / ratio)
      if (qrPosition && qrPosition.y >= start && qrPosition.y + qrPosition.height <= end) {
        pdf.addImage(qr.src, 'PNG', 12 + qrPosition.x / ratio, 12 + (qrPosition.y - start + (repeat ? headerHeight : 0)) / ratio, qrPosition.width / ratio, qrPosition.height / ratio, 'invoice-share-qr', 'FAST')
      }
      start = end
    }
    pdf.save(`invoice-${String(invoiceNumber || 'naseri').replace(/[^\w\u0600-\u06ff-]/g, '-')}.pdf`)
    return pdf
  } finally { host.remove() }
}
export async function printInvoice(element) {
  const { host } = await exportHost(element); document.body.classList.add('invoice-printing')
  const cleanup = () => { document.body.classList.remove('invoice-printing'); host.remove(); window.removeEventListener('afterprint', cleanup) }
  window.addEventListener('afterprint', cleanup, { once: true })
  try { window.print() } catch (error) { cleanup(); throw error }
}
