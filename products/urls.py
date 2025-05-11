from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('units', views.UnitViewSet)
router.register('', views.ProductViewSet)

urlpatterns = router.urls
