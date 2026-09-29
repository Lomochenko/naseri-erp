<template><Teleport to="body"><div v-if="show" class="invoice-modal" role="dialog" aria-modal="true" aria-label="مشاهده فاکتور" @keydown.esc="$emit('close')"><button class="invoice-backdrop" aria-label="بستن" @click="$emit('close')"></button><div class="invoice-dialog"><InvoiceViewer :invoice="invoice" :loading="loading" :load-error="error" closable @retry="load" @close="$emit('close')" /></div></div></Teleport></template>
<script setup>
import { ref, watch, onUnmounted } from 'vue'
import InvoiceViewer from '@/components/invoices/InvoiceViewer.vue'
import { getInvoiceDocument } from '@/services/invoiceDocuments'
const props = defineProps({ show: Boolean, salesOrder: { type: Object, default: null }, purchaseOrder: { type: Object, default: null } }); defineEmits(['close'])
const invoice = ref(null), loading = ref(false), error = ref(''); let request = 0
let previousOverflow = ''
watch(() => props.show, show => { if (show) { previousOverflow = document.body.style.overflow; document.body.style.overflow = 'hidden' } else document.body.style.overflow = previousOverflow })
onUnmounted(() => { if (props.show) document.body.style.overflow = previousOverflow })
async function load() { const current = ++request; invoice.value = null; error.value = ''; loading.value = true; try { const order = props.purchaseOrder || props.salesOrder; if (!order?.id) throw new Error('missing'); const { data } = await getInvoiceDocument(props.purchaseOrder ? 'purchase' : 'sale', order.id); if (current === request) invoice.value = data } catch { if (current === request) error.value = 'دریافت سند از سرور ممکن نشد. اطلاعات سفارش و اتصال را بررسی کنید.' } finally { if (current === request) loading.value = false } }
watch(() => [props.show, props.salesOrder?.id, props.purchaseOrder?.id], () => { if (props.show) load(); else request++ })
</script>
<style>.invoice-modal{position:fixed;inset:0;z-index:100000;display:flex;align-items:flex-start;justify-content:center;padding:32px 16px;overflow:auto}.invoice-backdrop{position:fixed;inset:0;border:0;background:#102b35b3;cursor:default}.invoice-dialog{position:relative;width:100%;max-width:980px;border-radius:8px;overflow:hidden}@media(max-width:600px){.invoice-modal{padding:0}.invoice-dialog{border-radius:0;min-height:100%}}</style>
