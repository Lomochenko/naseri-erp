from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('account-types', views.AccountTypeViewSet)
router.register('accounts', views.AccountViewSet)
router.register('journal-entries', views.JournalEntryViewSet)
router.register('journal-transactions', views.JournalTransactionViewSet)
router.register('fiscal-years', views.FiscalYearViewSet)
router.register('expense-categories', views.ExpenseCategoryViewSet)
router.register('expenses', views.ExpenseViewSet)

urlpatterns = [
    path('chart-of-accounts/', views.ChartOfAccountsView.as_view(), name='chart-of-accounts'),
    path('account-balance/<int:account_id>/', views.AccountBalanceView.as_view(), name='account-balance'),
    path('trial-balance/', views.TrialBalanceView.as_view(), name='trial-balance'),
    path('income-statement/', views.IncomeStatementView.as_view(), name='income-statement'),
    path('balance-sheet/', views.BalanceSheetView.as_view(), name='balance-sheet'),
    path('cash-flow-statement/', views.CashFlowStatementView.as_view(), name='cash-flow-statement'),
]

urlpatterns += router.urls
