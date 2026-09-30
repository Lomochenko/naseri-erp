<template>
  <nav v-show="!hidden" class="mobile-dock" dir="rtl" aria-label="دسترسی سریع موبایل">
    <RouterLink to="/" class="dock-item" :class="{ selected: route.path === '/' }" :aria-current="route.path === '/' ? 'page' : undefined"><Home /><span>خانه</span></RouterLink>
    <RouterLink to="/sales" class="dock-item" :class="{ selected: route.path === '/sales' }" :aria-current="route.path === '/sales' ? 'page' : undefined"><ShoppingBag /><span>فروش</span></RouterLink>
    <button type="button" class="dock-item dock-create" :aria-expanded="sheet === 'create'" aria-controls="mobile-action-sheet" @click="openSheet('create', $event)"><span class="create-icon"><Plus /></span><span>ثبت جدید</span></button>
    <RouterLink to="/inventory" class="dock-item" :class="{ selected: route.path === '/inventory' }" :aria-current="route.path === '/inventory' ? 'page' : undefined"><Boxes /><span>موجودی</span></RouterLink>
    <button type="button" class="dock-item" :class="{ selected: moreActive }" :aria-expanded="sheet === 'more'" aria-controls="mobile-action-sheet" @click="openSheet('more', $event)"><Menu /><span>بیشتر</span></button>
  </nav>
  <Teleport to="body">
    <Transition name="dock-sheet">
      <div v-if="sheet" class="dock-sheet-backdrop" data-mobile-dock-sheet @click.self="closeSheet">
        <section id="mobile-action-sheet" ref="dialog" class="dock-sheet" dir="rtl" role="dialog" aria-modal="true" aria-labelledby="dock-sheet-title" tabindex="-1" @keydown="onSheetKeydown">
          <div class="sheet-handle" aria-hidden="true"></div>
          <header><div><p class="sheet-eyebrow">دسترسی سریع</p><h2 id="dock-sheet-title">{{ sheet === 'create' ? 'چه چیزی ثبت می‌کنید؟' : 'همهٔ بخش‌های شما' }}</h2></div><button type="button" class="sheet-close" aria-label="بستن منو" @click="closeSheet"><X /></button></header>
          <p v-if="sheet === 'create'" class="sheet-description">یک کار تازه، بدون گشتن میان منوها.</p>
          <div class="sheet-actions">
            <button v-for="item in actions" :key="item.label" type="button" class="sheet-action" :disabled="item.soon" @click="choose(item)"><span class="action-icon" :class="item.tone"><component :is="item.icon" /></span><span class="action-copy"><strong>{{ item.label }}</strong><small>{{ item.description }}</small></span><span v-if="item.soon" class="soon-label">به‌زودی</span><ChevronLeft v-else class="action-arrow" /></button>
          </div>
        </section>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Home, ShoppingBag, Plus, Boxes, Menu, X, ChevronLeft, PackagePlus, Truck, Users, Package, ChartNoAxesCombined, UserRound } from 'lucide-vue-next'
import { useSidebar } from '@/composables/useSidebar'
import { requestQuickCreate, clearQuickCreate } from '@/composables/useQuickCreate'
const router = useRouter(), route = useRoute()
const { isMobileOpen } = useSidebar()
const sheet = ref(null), dialog = ref(null), keyboardOpen = ref(false), otherModal = ref(false)
let returnFocus, observer, previousOverflow = ''
const hidden = computed(() => isMobileOpen.value || keyboardOpen.value || otherModal.value)
const moreActive = computed(() => sheet.value === 'more' || ['/customers', '/purchases', '/products', '/reports', '/profile'].some(path => route.path === path || route.path.startsWith(`${path}/`)))
const actions = computed(() => sheet.value === 'create' ? [
  { label: 'فروش جدید', description: 'ثبت سفارش و صدور فاکتور', icon: ShoppingBag, tone: 'blue', path: '/sales', kind: 'sale' },
  { label: 'خرید جدید', description: 'سفارش کالا از تأمین‌کننده', icon: Truck, tone: 'green', path: '/purchases', kind: 'purchase' },
  { label: 'کالای جدید', description: 'افزودن به فهرست محصولات', icon: PackagePlus, tone: 'amber', path: '/products/create' },
] : [
  { label: 'مشتریان', description: 'طرف‌حساب‌ها و اطلاعات تماس', icon: Users, tone: 'blue', path: '/customers' },
  { label: 'خرید', description: 'سفارش‌ها و تأمین کالا', icon: Truck, tone: 'green', path: '/purchases' },
  { label: 'کالاها', description: 'فهرست و مدیریت محصولات', icon: Package, tone: 'amber', path: '/products' },
  { label: 'گزارش‌ها', description: 'گزارش‌های مدیریتی', icon: ChartNoAxesCombined, tone: 'neutral', soon: true },
  { label: 'پروفایل', description: 'تنظیمات حساب کاربری', icon: UserRound, tone: 'neutral', soon: true },
])
async function openSheet(kind, event) {
  returnFocus = event.currentTarget
  sheet.value = kind
  await nextTick()
  dialog.value?.focus()
}
function closeSheet() { sheet.value = null; returnFocus?.focus() }
async function choose(item) {
  closeSheet()
  if (item.kind) requestQuickCreate(item.kind)
  try {
    await router.push(item.path)
    // Guards can resolve a cancelled/redirected navigation without throwing.
    if (route.path !== item.path) clearQuickCreate()
  } catch { clearQuickCreate() }
}
function onSheetKeydown(event) {
  if (event.key === 'Escape') { event.preventDefault(); closeSheet(); return }
  if (event.key !== 'Tab') return
  const buttons = [...dialog.value.querySelectorAll('button:not(:disabled)')]
  const first = buttons[0], last = buttons.at(-1)
  if (event.shiftKey && (document.activeElement === first || document.activeElement === dialog.value)) { event.preventDefault(); last?.focus() }
  else if (!event.shiftKey && (document.activeElement === last || document.activeElement === dialog.value)) { event.preventDefault(); first?.focus() }
}
function updateKeyboard() {
  const active = document.activeElement
  const editing = active?.matches('input:not([type="checkbox"]):not([type="radio"]), textarea, [contenteditable="true"]')
  const viewport = window.visualViewport
  // Compare the current layout and visual viewports, not a portrait-sized baseline.
  keyboardOpen.value = !!editing || !!(viewport && window.innerHeight - viewport.height > 150)
}
function onResize() {
  if (window.innerWidth >= 768 && sheet.value) closeSheet()
  updateKeyboard()
}
function updateModals() {
  otherModal.value = [...document.querySelectorAll('[role="dialog"], .fixed.inset-0, .invoice-overlay')].some(node => !node.closest('[data-mobile-dock-sheet]') && node.getClientRects().length > 0)
}
watch(() => route.fullPath, () => { sheet.value = null; updateKeyboard() })
watch(isMobileOpen, value => { if (value) closeSheet() })
watch(sheet, (value, previous) => {
  if (value && !previous) { previousOverflow = document.body.style.overflow; document.body.style.overflow = 'hidden' }
  else if (!value) document.body.style.overflow = previousOverflow
})
onMounted(() => {
  observer = new MutationObserver(updateModals)
  observer.observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['class', 'style', 'hidden'] })
  document.addEventListener('focusin', updateKeyboard)
  document.addEventListener('focusout', updateKeyboard)
  window.visualViewport?.addEventListener('resize', updateKeyboard)
  window.addEventListener('resize', onResize)
  updateModals()
})
onUnmounted(() => {
  clearQuickCreate()
  observer?.disconnect()
  document.removeEventListener('focusin', updateKeyboard)
  document.removeEventListener('focusout', updateKeyboard)
  window.visualViewport?.removeEventListener('resize', updateKeyboard)
  window.removeEventListener('resize', onResize)
  if (sheet.value) document.body.style.overflow = previousOverflow
})
</script>

<style scoped>
.mobile-dock{position:fixed;inset-inline:12px;bottom:calc(10px + env(safe-area-inset-bottom,0px));z-index:1000;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));padding:7px 5px;background:#fff;border:1px solid #dce5f1;border-radius:22px;box-shadow:0 8px 32px #163b6521;color:#52647c}
.dock-item{min-height:54px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;font-size:10px;font-weight:600;border-radius:14px;position:relative;cursor:pointer}
.dock-item>svg{width:22px;height:22px;stroke-width:1.8}.dock-item.selected{color:#245dde;background:#ecf2ff}.dock-create{color:#245dde}.create-icon{display:flex;align-items:center;justify-content:center;background:#285fe2;color:white;width:48px;height:43px;border-radius:15px;margin-top:-21px;border:3px solid #fff;box-shadow:0 4px 10px #285fe22b}.create-icon svg{width:25px;height:25px}.dock-item:focus-visible,.sheet-action:focus-visible,.sheet-close:focus-visible{outline:3px solid #75a1ff;outline-offset:2px}
.dock-sheet-backdrop{position:fixed;inset:0;z-index:999999;background:#07182f80;display:flex;align-items:flex-end;justify-content:center}.dock-sheet{width:100%;max-width:520px;background:#fff;border-radius:26px 26px 0 0;padding:10px 22px calc(24px + env(safe-area-inset-bottom,0px));color:#172b47;max-height:85dvh;overflow:auto;outline:none}.sheet-handle{width:38px;height:4px;background:#d4deeb;border-radius:4px;margin:0 auto 20px}.dock-sheet header{display:flex;align-items:center;justify-content:space-between;gap:16px}.sheet-eyebrow{font-size:10px;color:#526b8b;margin-bottom:5px;font-weight:700}.dock-sheet h2{font-size:20px;font-weight:800}.sheet-close{display:grid;place-items:center;width:44px;height:44px;background:#f0f4fa;border-radius:13px;color:#52647c}.sheet-close svg{width:19px}.sheet-description{font-size:12px;color:#52647c;margin-top:8px}.sheet-actions{display:flex;flex-direction:column;gap:6px;margin-top:20px}.sheet-action{display:flex;align-items:center;gap:13px;width:100%;text-align:right;padding:12px 8px;border-radius:14px;min-height:68px;cursor:pointer}.sheet-action:hover:not(:disabled){background:#f2f6fc}.action-icon{display:grid;place-items:center;flex:none;width:44px;height:44px;border-radius:13px}.action-icon svg{width:22px;height:22px;stroke-width:1.7}.blue{background:#eaf1ff;color:#285fe2}.green{background:#e5f5ef;color:#168164}.amber{background:#fff2dd;color:#a9680c}.neutral{background:#eef1f5;color:#6e7c90}.action-copy{display:flex;flex:1;flex-direction:column;gap:5px}.action-copy strong{font-size:13px;font-weight:700}.action-copy small{font-size:11px;color:#52647c}.action-arrow{width:18px;color:#8394aa}.soon-label{font-size:10px;background:#eef1f5;color:#64748b;border-radius:6px;padding:4px 7px}.sheet-action:disabled{cursor:default}.dock-sheet-enter-active,.dock-sheet-leave-active{transition:opacity 180ms ease}.dock-sheet-enter-active .dock-sheet,.dock-sheet-leave-active .dock-sheet{transition:transform 180ms ease}.dock-sheet-enter-from,.dock-sheet-leave-to{opacity:0}.dock-sheet-enter-from .dock-sheet,.dock-sheet-leave-to .dock-sheet{transform:translateY(24px)}
:global(.dark .mobile-dock),:global(.dark .dock-sheet){background:#142238;border-color:#2a3d58;color:#e2eaf5}:global(.dark .dock-item){color:#bac9df}:global(.dark .dock-item.selected){background:#233d65;color:#9abbff}:global(.dark .dock-create){color:#aac7ff}:global(.dark .create-icon){border-color:#142238}:global(.dark .sheet-close){background:#21334c;color:#c4d3e9}:global(.dark .sheet-description),:global(.dark .sheet-eyebrow),:global(.dark .action-copy small){color:#b0c1d9}:global(.dark .sheet-action:hover:not(:disabled)){background:#20334d}:global(.dark .dock-sheet .blue){background:#203d66;color:#a4c3ff}:global(.dark .dock-sheet .green){background:#1c453e;color:#91dcc3}:global(.dark .dock-sheet .amber){background:#493b24;color:#f1cc8c}:global(.dark .dock-sheet .neutral),:global(.dark .soon-label){background:#27364c;color:#c0ccdd}
@media(min-width:768px){.mobile-dock,.dock-sheet-backdrop{display:none}}@media print{.mobile-dock,.dock-sheet-backdrop{display:none!important}}@media(prefers-reduced-motion:reduce){.dock-sheet-enter-active,.dock-sheet-leave-active,.dock-sheet-enter-active .dock-sheet,.dock-sheet-leave-active .dock-sheet{transition:none}}
</style>
