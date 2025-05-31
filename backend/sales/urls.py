from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('customers', views.CustomerViewSet)
router.register('sales', views.SaleViewSet)
router.register('sale-items', views.SaleItemViewSet)
router.register('invoices', views.InvoiceViewSet)
router.register('payments', views.PaymentViewSet)

urlpatterns = [
    path('customer-sales/<int:customer_id>/', views.CustomerSalesView.as_view(), name='customer-sales'),
    path('customer-invoices/<int:customer_id>/', views.CustomerInvoicesView.as_view(), name='customer-invoices'),
    path('sales-report/', views.SalesReportView.as_view(), name='sales-report'),
    path('sales-by-product/', views.SalesByProductView.as_view(), name='sales-by-product'),
]

urlpatterns += router.urls
