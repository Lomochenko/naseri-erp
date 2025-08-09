from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('warehouses', views.WarehouseViewSet)
router.register('transactions', views.InventoryTransactionViewSet)
router.register('adjustments', views.StockAdjustmentViewSet)
router.register('adjustment-items', views.StockAdjustmentItemViewSet)

urlpatterns = [
    path('stock-levels/', views.StockLevelsView.as_view(), name='stock-levels'),
    path('product-stock/<int:product_id>/', views.ProductStockView.as_view(), name='product-stock'),
    path('warehouse-stock/<int:warehouse_id>/', views.WarehouseStockView.as_view(), name='warehouse-stock'),
    path('low-stock-products/', views.LowStockProductsView.as_view(), name='low-stock-products'),
    path('simple-adjustment/', views.SimpleAdjustmentView.as_view(), name='simple-adjustment'),
]

urlpatterns += router.urls
