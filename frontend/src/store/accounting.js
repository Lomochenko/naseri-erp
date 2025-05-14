import { defineStore } from 'pinia';
import axiosInstance from '../utils/axios';

export const useAccountingStore = defineStore('accounting', {
  state: () => ({
    transactions: [],
    bankAccounts: [],
    duePayments: [],
    financialSummary: {
      revenue: 0,
      expenses: 0,
      profit: 0,
      dueAmount: 0
    },
    loading: false,
    error: null,
    
    // فیلترهای جستجو
    filters: {
      search: '',
      transaction_type: null,
      date_from: null,
      date_to: null,
      bankAccount: null
    },
    
    // پیجینیشن
    pagination: {
      page: 1,
      itemsPerPage: 10,
      totalItems: 0,
      totalPages: 0
    }
  }),
  
  getters: {
    // دریافت تراکنش‌ها براساس نوع
    getTransactionsByType: (state) => (type) => {
      return state.transactions.filter(transaction => transaction.transaction_type === type);
    },
    
    // دریافت تراکنش‌ها براساس حساب بانکی
    getTransactionsByBankAccount: (state) => (bankAccountId) => {
      return state.transactions.filter(transaction => transaction.bank_account?.id === bankAccountId);
    },
    
    // محاسبه مجموع تراکنش‌های ورودی (درآمد)
    totalIncome: (state) => {
      return state.transactions
        .filter(transaction => transaction.amount > 0)
        .reduce((total, transaction) => total + transaction.amount, 0);
    },
    
    // محاسبه مجموع تراکنش‌های خروجی (هزینه)
    totalExpenses: (state) => {
      return state.transactions
        .filter(transaction => transaction.amount < 0)
        .reduce((total, transaction) => total + Math.abs(transaction.amount), 0);
    },
    
    // گرفتن پرداخت‌های معوق گذشته
    getOverduePayments: (state) => {
      const today = new Date();
      return state.duePayments.filter(payment => {
        const dueDate = new Date(payment.due_date);
        return dueDate < today && payment.status === 'UPCOMING';
      });
    },
    
    // محاسبه مجموع پرداخت‌های معوق
    totalDueAmount: (state) => {
      return state.duePayments
        .filter(payment => payment.status !== 'PAID')
        .reduce((total, payment) => total + payment.amount, 0);
    },
    
    // دریافت حساب بانکی براساس شناسه
    getBankAccountById: (state) => (id) => {
      return state.bankAccounts.find(account => account.id === id);
    }
  },
  
  actions: {
    // دریافت تراکنش‌های مالی
    async fetchTransactions() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.get('/api/accounting/transactions/', {
          params: {
            search: this.filters.search,
            transaction_type: this.filters.transaction_type,
            date_from: this.filters.date_from,
            date_to: this.filters.date_to,
            bank_account: this.filters.bankAccount,
            page: this.pagination.page,
            page_size: this.pagination.itemsPerPage
          }
        });
        
        this.transactions = response.data.results;
        this.pagination.totalItems = response.data.count;
        this.pagination.totalPages = Math.ceil(response.data.count / this.pagination.itemsPerPage);
        return this.transactions;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در دریافت تراکنش‌های مالی';
        console.error('Error fetching transactions:', error);
        return [];
      } finally {
        this.loading = false;
      }
    },
    
    // دریافت حساب‌های بانکی
    async fetchBankAccounts() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.get('/api/accounting/bank-accounts/');
        this.bankAccounts = response.data.results;
        return this.bankAccounts;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در دریافت حساب‌های بانکی';
        console.error('Error fetching bank accounts:', error);
        return [];
      } finally {
        this.loading = false;
      }
    },
    
    // دریافت خلاصه مالی
    async fetchFinancialSummary(period = 'month') {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.get('/api/accounting/summary/', {
          params: { period }
        });
        this.financialSummary = response.data;
        return this.financialSummary;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در دریافت خلاصه مالی';
        console.error('Error fetching financial summary:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // دریافت پرداخت‌های معوق
    async fetchDuePayments() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.get('/api/accounting/due-payments/');
        this.duePayments = response.data.results;
        return this.duePayments;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در دریافت پرداخت‌های معوق';
        console.error('Error fetching due payments:', error);
        return [];
      } finally {
        this.loading = false;
      }
    },
    
    // ثبت تراکنش جدید
    async addTransaction(transactionData) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.post('/api/accounting/transactions/', transactionData);
        this.transactions.unshift(response.data);
        
        // به‌روزرسانی خلاصه مالی در صورت نیاز
        if (response.data.amount > 0) {
          this.financialSummary.revenue += response.data.amount;
          this.financialSummary.profit += response.data.amount;
        } else {
          this.financialSummary.expenses += Math.abs(response.data.amount);
          this.financialSummary.profit -= Math.abs(response.data.amount);
        }
        
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در ثبت تراکنش';
        console.error('Error adding transaction:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // حذف تراکنش
    async deleteTransaction(transactionId) {
      this.loading = true;
      this.error = null;
      
      try {
        await axiosInstance.delete(`/api/accounting/transactions/${transactionId}/`);
        
        // یافتن تراکنش برای به‌روزرسانی خلاصه مالی
        const transaction = this.transactions.find(t => t.id === transactionId);
        if (transaction) {
          if (transaction.amount > 0) {
            this.financialSummary.revenue -= transaction.amount;
            this.financialSummary.profit -= transaction.amount;
          } else {
            this.financialSummary.expenses -= Math.abs(transaction.amount);
            this.financialSummary.profit += Math.abs(transaction.amount);
          }
        }
        
        // حذف تراکنش از آرایه تراکنش‌ها
        this.transactions = this.transactions.filter(t => t.id !== transactionId);
        
        return true;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در حذف تراکنش';
        console.error('Error deleting transaction:', error);
        return false;
      } finally {
        this.loading = false;
      }
    },
    
    // افزودن حساب بانکی جدید
    async addBankAccount(bankAccountData) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.post('/api/accounting/bank-accounts/', bankAccountData);
        this.bankAccounts.push(response.data);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در افزودن حساب بانکی';
        console.error('Error adding bank account:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // به‌روزرسانی حساب بانکی
    async updateBankAccount(accountId, accountData) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.put(`/api/accounting/bank-accounts/${accountId}/`, accountData);
        
        // به‌روزرسانی حساب بانکی در آرایه حساب‌ها
        const index = this.bankAccounts.findIndex(a => a.id === accountId);
        if (index !== -1) {
          this.bankAccounts[index] = response.data;
        }
        
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در به‌روزرسانی حساب بانکی';
        console.error('Error updating bank account:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // حذف حساب بانکی
    async deleteBankAccount(accountId) {
      this.loading = true;
      this.error = null;
      
      try {
        await axiosInstance.delete(`/api/accounting/bank-accounts/${accountId}/`);
        
        // حذف حساب بانکی از آرایه حساب‌ها
        this.bankAccounts = this.bankAccounts.filter(a => a.id !== accountId);
        
        return true;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در حذف حساب بانکی';
        console.error('Error deleting bank account:', error);
        return false;
      } finally {
        this.loading = false;
      }
    },
    
    // به‌روزرسانی وضعیت پرداخت معوق
    async updateDuePaymentStatus(paymentId, status) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.patch(`/api/accounting/due-payments/${paymentId}/`, {
          status
        });
        
        // به‌روزرسانی وضعیت پرداخت در آرایه پرداخت‌های معوق
        const index = this.duePayments.findIndex(p => p.id === paymentId);
        if (index !== -1) {
          this.duePayments[index].status = status;
          
          // به‌روزرسانی مبلغ پرداخت‌های معوق در خلاصه مالی
          if (status === 'PAID') {
            this.financialSummary.dueAmount -= this.duePayments[index].amount;
          } else if (this.duePayments[index].status === 'PAID') {
            this.financialSummary.dueAmount += this.duePayments[index].amount;
          }
        }
        
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در به‌روزرسانی وضعیت پرداخت';
        console.error('Error updating due payment status:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // محاسبه آمار برای نمودارها
    async fetchChartData(chartType, period = 'month') {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.get('/api/accounting/chart-data/', {
          params: { 
            chart_type: chartType,
            period
          }
        });
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در دریافت داده‌های نمودار';
        console.error('Error fetching chart data:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // دریافت گزارش سود و زیان
    async fetchProfitLossReport(dateFrom, dateTo) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axiosInstance.get('/api/accounting/profit-loss-report/', {
          params: { 
            date_from: dateFrom,
            date_to: dateTo
          }
        });
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.detail || 'خطا در دریافت گزارش سود و زیان';
        console.error('Error fetching profit loss report:', error);
        return null;
      } finally {
        this.loading = false;
      }
    },
    
    // به‌روزرسانی فیلترها
    updateFilters(newFilters) {
      this.filters = { ...this.filters, ...newFilters };
      this.pagination.page = 1; // بازگشت به صفحه اول با تغییر فیلترها
    },
    
    // تنظیم صفحه جاری
    setPage(page) {
      this.pagination.page = page;
    },
    
    // تنظیم تعداد آیتم در هر صفحه
    setItemsPerPage(count) {
      this.pagination.itemsPerPage = count;
      this.pagination.page = 1; // بازگشت به صفحه اول با تغییر تعداد آیتم‌ها
    },
    
    // بازنشانی فیلترها
    resetFilters() {
      this.filters = {
        search: '',
        transaction_type: null,
        date_from: null,
        date_to: null,
        bankAccount: null
      };
      this.pagination.page = 1;
    }
  }
}); 