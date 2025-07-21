<template>
  <div>
    <div class="p-5 mb-6 border border-gray-200 rounded-2xl dark:border-gray-800 lg:p-6">
      <div class="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
        <div class="flex-1">
          <h4 class="mb-6 text-lg font-semibold text-gray-800 dark:text-white/90">
            اطلاعات حقوق و دستمزد
          </h4>

          <div class="grid grid-cols-1 gap-4 lg:grid-cols-3 lg:gap-7">
            <div class="p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">حقوق ماهانه</p>
              <p class="text-lg font-semibold text-gray-800 dark:text-white/90">
                {{ formatCurrency(paymentData.monthly_salary) }}
              </p>
            </div>

            <div class="p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">حقوق سالانه</p>
              <p class="text-lg font-semibold text-gray-800 dark:text-white/90">
                {{ formatCurrency(paymentData.yearly_salary) }}
              </p>
            </div>

            <div class="p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">آخرین پرداخت</p>
              <p class="text-sm font-medium text-gray-800 dark:text-white/90">
                {{ paymentData.last_payment_date || 'تعریف نشده' }}
              </p>
            </div>

            <div class="p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">وضعیت پرداخت</p>
              <span :class="[
                'inline-flex px-2 py-1 text-xs font-medium rounded-full',
                paymentData.payment_status === 'paid' 
                  ? 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
                  : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400'
              ]">
                {{ getPaymentStatusText(paymentData.payment_status) }}
              </span>
            </div>

            <div class="p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">تاریخ استخدام</p>
              <p class="text-sm font-medium text-gray-800 dark:text-white/90">
                {{ paymentData.hire_date || 'تعریف نشده' }}
              </p>
            </div>

            <div class="p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
              <p class="mb-2 text-xs leading-normal text-gray-500 dark:text-gray-400">نوع قرارداد</p>
              <p class="text-sm font-medium text-gray-800 dark:text-white/90">
                {{ getContractTypeText(paymentData.contract_type) }}
              </p>
            </div>
          </div>

          <!-- Payment History -->
          <div class="mt-6">
            <h5 class="mb-4 text-base font-medium text-gray-800 dark:text-white/90">
              تاریخچه پرداخت‌ها
            </h5>
            <div class="overflow-x-auto">
              <table class="w-full text-sm">
                <thead>
                  <tr class="border-b border-gray-200 dark:border-gray-700">
                    <th class="pb-2 text-right text-gray-600 dark:text-gray-400">تاریخ</th>
                    <th class="pb-2 text-right text-gray-600 dark:text-gray-400">مبلغ</th>
                    <th class="pb-2 text-right text-gray-600 dark:text-gray-400">نوع</th>
                    <th class="pb-2 text-right text-gray-600 dark:text-gray-400">وضعیت</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="payment in paymentHistory" :key="payment.id" 
                      class="border-b border-gray-100 dark:border-gray-800">
                    <td class="py-2 text-gray-800 dark:text-white/90">{{ payment.date }}</td>
                    <td class="py-2 text-gray-800 dark:text-white/90">{{ formatCurrency(payment.amount) }}</td>
                    <td class="py-2 text-gray-800 dark:text-white/90">{{ payment.type }}</td>
                    <td class="py-2">
                      <span :class="[
                        'inline-flex px-2 py-1 text-xs font-medium rounded-full',
                        payment.status === 'paid' 
                          ? 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
                          : 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400'
                      ]">
                        {{ payment.status === 'paid' ? 'پرداخت شده' : 'پرداخت نشده' }}
                      </span>
                    </td>
                  </tr>
                  <tr v-if="paymentHistory.length === 0">
                    <td colspan="4" class="py-4 text-center text-gray-500 dark:text-gray-400">
                      هیچ تاریخچه پرداختی موجود نیست
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Edit Button (Only for System Owner) -->
        <button 
          v-if="canEdit"
          @click="isPaymentModal = true" 
          class="edit-button"
        >
          <svg
            class="fill-current"
            width="18"
            height="18"
            viewBox="0 0 18 18"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fill-rule="evenodd"
              clip-rule="evenodd"
              d="M8.09914 0.300781C8.51335 0.300781 8.84914 0.636567 8.84914 1.05078V8.84914H16.6475C17.0617 8.84914 17.3975 9.18493 17.3975 9.59914C17.3975 10.0134 17.0617 10.3491 16.6475 10.3491H8.84914V18.1475C8.84914 18.5617 8.51335 18.8975 8.09914 18.8975C7.68493 18.8975 7.34914 18.5617 7.34914 18.1475V10.3491H-0.449219C-0.863433 10.3491 -1.19922 10.0134 -1.19922 9.59914C-1.19922 9.18493 -0.863433 8.84914 -0.449219 8.84914H7.34914V1.05078C7.34914 0.636567 7.68493 0.300781 8.09914 0.300781Z"
              fill=""
            />
          </svg>
          ویرایش حقوق
        </button>
      </div>
    </div>

    <!-- Payment Edit Modal -->
    <Modal v-if="isPaymentModal" @close="isPaymentModal = false">
      <template #body>
        <div class="no-scrollbar relative w-full max-w-[600px] overflow-y-auto rounded-3xl bg-white p-4 dark:bg-gray-900 lg:p-11">
          <!-- close btn -->
          <button
            @click="isPaymentModal = false"
            class="transition-color absolute right-5 top-5 z-999 flex h-11 w-11 items-center justify-center rounded-full bg-gray-100 text-gray-400 hover:bg-gray-200 hover:text-gray-600 dark:bg-white/[0.05] dark:text-gray-400 dark:hover:bg-white/[0.07] dark:hover:text-gray-300"
          >
            <svg class="fill-current" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" clip-rule="evenodd" d="M6.04289 16.5418C5.65237 16.9323 5.65237 17.5655 6.04289 17.956C6.43342 18.3465 7.06658 18.3465 7.45711 17.956L11.9987 13.4144L16.5408 17.9565C16.9313 18.347 17.5645 18.347 17.955 17.9565C18.3455 17.566 18.3455 16.9328 17.955 16.5423L13.4129 12.0002L17.955 7.45808C18.3455 7.06756 18.3455 6.43439 17.955 6.04387C17.5645 5.65335 16.9313 5.65335 16.5408 6.04387L11.9987 10.586L7.45711 6.04439C7.06658 5.65386 6.43342 5.65386 6.04289 6.04439C5.65237 6.43491 5.65237 7.06808 6.04289 7.4586L10.5845 12.0002L6.04289 16.5418Z" fill="" />
            </svg>
          </button>
          
          <div class="px-2 pr-14">
            <h4 class="mb-2 text-2xl font-semibold text-gray-800 dark:text-white/90">
              ویرایش اطلاعات حقوق و دستمزد
            </h4>
            <p class="mb-6 text-sm text-gray-500 dark:text-gray-400 lg:mb-7">
              اطلاعات حقوق و دستمزد کارمند را به روز کنید.
            </p>
          </div>

          <form class="flex flex-col">
            <div class="custom-scrollbar h-[400px] overflow-y-auto p-2">
              <div class="grid grid-cols-1 gap-x-6 gap-y-5 lg:grid-cols-2">
                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
                    حقوق ماهانه (تومان)
                  </label>
                  <input
                    type="number"
                    v-model="editForm.monthly_salary"
                    placeholder="مبلغ حقوق ماهانه"
                    class="h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/30 dark:focus:border-brand-800"
                  />
                </div>

                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
                    نوع قرارداد
                  </label>
                  <select
                    v-model="editForm.contract_type"
                    class="h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800"
                  >
                    <option value="full_time">تمام وقت</option>
                    <option value="part_time">پاره وقت</option>
                    <option value="contract">قراردادی</option>
                    <option value="temporary">موقت</option>
                  </select>
                </div>

                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
                    تاریخ استخدام
                  </label>
                  <input
                    type="date"
                    v-model="editForm.hire_date"
                    class="h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800"
                  />
                </div>

                <div>
                  <label class="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-400">
                    وضعیت پرداخت
                  </label>
                  <select
                    v-model="editForm.payment_status"
                    class="h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-800"
                  >
                    <option value="paid">پرداخت شده</option>
                    <option value="pending">در انتظار پرداخت</option>
                    <option value="overdue">معوقه</option>
                  </select>
                </div>
              </div>
            </div>

            <div class="flex flex-col gap-3 pt-6 sm:flex-row sm:justify-end">
              <button
                @click="isPaymentModal = false"
                type="button"
                class="flex w-full justify-center rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-white/[0.03] sm:w-auto"
              >
                بستن
              </button>
              <button
                @click="savePaymentData"
                type="button"
                class="flex w-full justify-center rounded-lg bg-brand-500 px-4 py-2.5 text-sm font-medium text-white hover:bg-brand-600 sm:w-auto"
              >
                ذخیره تغییرات
              </button>
            </div>
          </form>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Modal from './Modal.vue'

const authStore = useAuthStore()
const isPaymentModal = ref(false)

// Payment data
const paymentData = ref({
  monthly_salary: 15000000,
  yearly_salary: 180000000,
  last_payment_date: '1403/08/15',
  payment_status: 'paid',
  hire_date: '1402/01/01',
  contract_type: 'full_time'
})

// Edit form
const editForm = ref({
  monthly_salary: 0,
  contract_type: 'full_time',
  hire_date: '',
  payment_status: 'paid'
})

// Payment history
const paymentHistory = ref([
  { id: 1, date: '1403/08/15', amount: 15000000, type: 'حقوق ماهانه', status: 'paid' },
  { id: 2, date: '1403/07/15', amount: 15000000, type: 'حقوق ماهانه', status: 'paid' },
  { id: 3, date: '1403/06/15', amount: 15000000, type: 'حقوق ماهانه', status: 'paid' }
])

// Computed properties
const canEdit = computed(() => {
  return authStore.user?.is_superuser === true
})

// Methods
const formatCurrency = (amount) => {
  if (!amount) return '0 تومان'
  return new Intl.NumberFormat('fa-IR').format(amount) + ' تومان'
}

const getPaymentStatusText = (status) => {
  const statusMap = {
    'paid': 'پرداخت شده',
    'pending': 'در انتظار پرداخت',
    'overdue': 'معوقه'
  }
  return statusMap[status] || 'نامشخص'
}

const getContractTypeText = (type) => {
  const typeMap = {
    'full_time': 'تمام وقت',
    'part_time': 'پاره وقت',
    'contract': 'قراردادی',
    'temporary': 'موقت'
  }
  return typeMap[type] || 'نامشخص'
}

const loadPaymentData = () => {
  editForm.value = {
    monthly_salary: paymentData.value.monthly_salary,
    contract_type: paymentData.value.contract_type,
    hire_date: paymentData.value.hire_date,
    payment_status: paymentData.value.payment_status
  }
}

const savePaymentData = async () => {
  try {
    // TODO: Implement actual API call to update payment data
    // const response = await paymentAPI.updatePaymentData(editForm.value)
    
    // For now, just update local data
    paymentData.value = {
      ...paymentData.value,
      ...editForm.value,
      yearly_salary: editForm.value.monthly_salary * 12
    }
    
    console.log('Payment data saved successfully')
    isPaymentModal.value = false
  } catch (error) {
    console.error('Error saving payment data:', error)
    alert('خطا در ذخیره اطلاعات')
  }
}

onMounted(() => {
  loadPaymentData()
})
</script>

<style scoped>
.edit-button {
  @apply flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-700 dark:hover:bg-white/[0.03] transition-colors;
}
</style>
