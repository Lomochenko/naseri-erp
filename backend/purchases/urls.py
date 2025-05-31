from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('suppliers', views.SupplierViewSet)
router.register('purchases', views.PurchaseViewSet)
router.register('purchase-items', views.PurchaseItemViewSet)
router.register('purchase-invoices', views.PurchaseInvoiceViewSet)
router.register('supplier-payments', views.SupplierPaymentViewSet)

urlpatterns = [
    path('supplier-purchases/<int:supplier_id>/', views.SupplierPurchasesView.as_view(), name='supplier-purchases'),
    path('supplier-invoices/<int:supplier_id>/', views.SupplierInvoicesView.as_view(), name='supplier-invoices'),
    path('purchases-report/', views.PurchasesReportView.as_view(), name='purchases-report'),
    path('purchases-by-product/', views.PurchasesByProductView.as_view(), name='purchases-by-product'),
]

urlpatterns += router.urls
