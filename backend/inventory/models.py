from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import MinValueValidator
from products.models import Product

class Warehouse(models.Model):
    """Warehouse model for inventory management."""
    name = models.CharField(_('name'), max_length=100)
    location = models.CharField(_('location'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('warehouse')
        verbose_name_plural = _('warehouses')
        ordering = ['name']

    def __str__(self):
        return self.name

class InventoryTransaction(models.Model):
    """Model for tracking inventory movements."""
    TRANSACTION_TYPES = [
        ('purchase', _('Purchase')),
        ('sale', _('Sale')),
        ('return_from_customer', _('Return from Customer')),
        ('return_to_supplier', _('Return to Supplier')),
        ('adjustment_add', _('Adjustment Add')),
        ('adjustment_subtract', _('Adjustment Subtract')),
        ('transfer', _('Transfer')),
    ]

    transaction_type = models.CharField(_('transaction type'), max_length=30, choices=TRANSACTION_TYPES)
    product = models.ForeignKey(Product, verbose_name=_('product'), on_delete=models.PROTECT,
                               related_name='inventory_transactions')
    warehouse = models.ForeignKey(Warehouse, verbose_name=_('warehouse'), on_delete=models.PROTECT,
                                 related_name='inventory_transactions')
    quantity = models.DecimalField(_('quantity'), max_digits=10, decimal_places=2,
                                  validators=[MinValueValidator(0.01)])
    unit_price = models.DecimalField(_('unit price'), max_digits=12, decimal_places=0,
                                    validators=[MinValueValidator(0)])
    reference_number = models.CharField(_('reference number'), max_length=100, blank=True, null=True)
    reference_type = models.CharField(_('reference type'), max_length=50, blank=True, null=True)
    reference_id = models.PositiveIntegerField(_('reference ID'), blank=True, null=True)
    notes = models.TextField(_('notes'), blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('created by'),
                                  on_delete=models.PROTECT, related_name='inventory_transactions')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('inventory transaction')
        verbose_name_plural = _('inventory transactions')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.product.name} - {self.quantity} - {self.created_at.strftime('%Y-%m-%d')}"

class StockAdjustment(models.Model):
    """Model for stock adjustments."""
    ADJUSTMENT_TYPES = [
        ('add', _('Add')),
        ('subtract', _('Subtract')),
    ]

    adjustment_type = models.CharField(_('adjustment type'), max_length=10, choices=ADJUSTMENT_TYPES)
    warehouse = models.ForeignKey(Warehouse, verbose_name=_('warehouse'), on_delete=models.PROTECT,
                                 related_name='stock_adjustments')
    reason = models.TextField(_('reason'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('created by'),
                                  on_delete=models.PROTECT, related_name='stock_adjustments')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('stock adjustment')
        verbose_name_plural = _('stock adjustments')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_adjustment_type_display()} - {self.warehouse.name} - {self.created_at.strftime('%Y-%m-%d')}"

class StockAdjustmentItem(models.Model):
    """Model for stock adjustment items."""
    adjustment = models.ForeignKey(StockAdjustment, verbose_name=_('adjustment'),
                                  on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, verbose_name=_('product'),
                               on_delete=models.PROTECT, related_name='adjustment_items')
    quantity = models.DecimalField(_('quantity'), max_digits=10, decimal_places=2,
                                  validators=[MinValueValidator(0.01)])
    notes = models.TextField(_('notes'), blank=True)

    class Meta:
        verbose_name = _('stock adjustment item')
        verbose_name_plural = _('stock adjustment items')

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    def save(self, *args, **kwargs):
        """Override save to create inventory transaction."""
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            # Create corresponding inventory transaction
            transaction_type = 'adjustment_add' if self.adjustment.adjustment_type == 'add' else 'adjustment_subtract'

            InventoryTransaction.objects.create(
                transaction_type=transaction_type,
                product=self.product,
                warehouse=self.adjustment.warehouse,
                quantity=self.quantity,
                unit_price=self.product.purchase_price,
                reference_type='stock_adjustment',
                reference_id=self.adjustment.id,
                notes=self.notes,
                created_by=self.adjustment.created_by
            )
