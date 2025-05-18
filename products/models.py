from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
import uuid

class Category(models.Model):
    """Product category model."""
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['name']

    def __str__(self):
        return self.name

class Unit(models.Model):
    """Measurement unit model for products."""
    name = models.CharField(_('name'), max_length=50)
    symbol = models.CharField(_('symbol'), max_length=10)

    class Meta:
        verbose_name = _('unit')
        verbose_name_plural = _('units')

    def __str__(self):
        return f"{self.name} ({self.symbol})"

class Product(models.Model):
    """Product model."""
    code = models.CharField(_('product code'), max_length=50, unique=True)
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    category = models.ForeignKey(Category, verbose_name=_('category'),
                                on_delete=models.SET_NULL, null=True,
                                related_name='products')
    unit = models.ForeignKey(Unit, verbose_name=_('unit'),
                            on_delete=models.PROTECT,
                            related_name='products')
    purchase_price = models.DecimalField(_('purchase price'), max_digits=12, decimal_places=0,
                                        validators=[MinValueValidator(0)])
    selling_price = models.DecimalField(_('selling price'), max_digits=12, decimal_places=0,
                                       validators=[MinValueValidator(0)])
    min_stock = models.DecimalField(_('minimum stock'), max_digits=10, decimal_places=2,
                                   default=0, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

    @property
    def current_stock(self):
        """Calculate current stock from inventory transactions."""
        from inventory.models import InventoryTransaction

        incoming = InventoryTransaction.objects.filter(
            product=self,
            transaction_type__in=['purchase', 'return_from_customer', 'adjustment_add']
        ).aggregate(total=models.Sum('quantity'))['total'] or 0

        outgoing = InventoryTransaction.objects.filter(
            product=self,
            transaction_type__in=['sale', 'return_to_supplier', 'adjustment_subtract']
        ).aggregate(total=models.Sum('quantity'))['total'] or 0

        return incoming - outgoing
