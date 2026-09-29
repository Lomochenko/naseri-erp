<template><main class="public-invoice"><InvoiceViewer :invoice="invoice" :loading="loading" :load-error="error" title="سند دیجیتال ناصری" @retry="load" /></main></template>
<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import InvoiceViewer from '@/components/invoices/InvoiceViewer.vue'
import { getPublicInvoice } from '@/services/invoiceDocuments'
const route = useRoute(), invoice = ref(null), loading = ref(true), error = ref(''); let request = 0
async function load() { const current = ++request; loading.value = true; invoice.value = null; error.value = ''; try { const { data } = await getPublicInvoice(route.params.token); if (current === request) invoice.value = data } catch (failure) { if (current === request) error.value = [400, 403, 404, 410].includes(failure.response?.status) ? 'این لینک نامعتبر، منقضی یا حذف شده است. از صادرکنندهٔ سند لینک تازه بگیرید.' : 'ارتباط با سرور ممکن نشد. اینترنت را بررسی و دوباره تلاش کنید.' } finally { if (current === request) loading.value = false } }
const metas = []; onMounted(() => { for (const [name, content] of [['robots', 'noindex,nofollow'], ['referrer', 'no-referrer']]) { const el = document.createElement('meta'); el.name = name; el.content = content; document.head.appendChild(el); metas.push(el) } }); onUnmounted(() => { request++; metas.forEach(el => el.remove()) }); watch(() => route.params.token, load, { immediate: true })
</script>
<style>.public-invoice{min-height:100vh;background:#eaf0ef;padding:40px 20px}.public-invoice .invoice-toolbar{padding-bottom:24px}@media(max-width:600px){.public-invoice{padding:0}}</style>
