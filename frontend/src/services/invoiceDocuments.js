import axios from 'axios'
import api from './api'

// Deliberately separate from the admin client: shared links never send auth tokens.
const publicApi = axios.create({ baseURL: import.meta.env.VITE_API_BASE_URL || '/api', timeout: 15000, withCredentials: false })
export const getInvoiceDocument = (kind, id) => api.get(`/invoice-documents/${kind}/${id}/`)
export const getPublicInvoice = (token) => publicApi.get(`/invoice-documents/public/${encodeURIComponent(token)}/`)
export const invoiceURL = (document) => document.share_token ? `${window.location.origin}/invoice/${encodeURIComponent(document.share_token)}` : ''
