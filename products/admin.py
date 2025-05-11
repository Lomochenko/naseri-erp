from django.contrib import admin
from .models import Category, Unit, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol')
    search_fields = ('name', 'symbol')
    ordering = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'unit', 'purchase_price', 'selling_price', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('code', 'name', 'description', 'barcode')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('code', 'barcode', 'name', 'description', 'image')
        }),
        ('دسته‌بندی و واحد', {
            'fields': ('category', 'unit')
        }),
        ('قیمت‌گذاری', {
            'fields': ('purchase_price', 'selling_price')
        }),
        ('موجودی', {
            'fields': ('min_stock',)
        }),
        ('وضعیت', {
            'fields': ('is_active',)
        }),
        ('اطلاعات سیستمی', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
