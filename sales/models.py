from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import MinValueValidator
import uuid
from products.models import Product
from inventory.models import Warehouse, InventoryTransaction

class Customer(models.Model):
    """Customer model."""
    name = models.CharField(_('name'), max_length=255)
    phone = models.CharField(_('phone'), max_length=20, blank=True)
    email = models.EmailField(_('email'), blank=True)
    address = models.TextField(_('address'), blank=True)
    tax_number = models.CharField(_('tax number'), max_length=50, blank=True)
    credit_limit = models.DecimalField(_('credit limit'), max_digits=12, decimal_places=0,
                                      default=0, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(_('active'), default=True)
    notes = models.TextField(_('notes'), blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('customer')
        verbose_name_plural = _('customers')
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def total_due(self):
        """Calculate total amount due from customer."""
        return self.invoices.filter(status='unpaid').aggregate(
            total=models.Sum('remaining_amount'))['total'] or 0

class Sale(models.Model):
    """Sale model."""
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('confirmed', _('Confirmed')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    ]

    invoice_number = models.CharField(_('invoice number'), max_length=50, unique=True)
    customer = models.ForeignKey(Customer, verbose_name=_('customer'),
                                on_delete=models.PROTECT, related_name='sales')
    warehouse = models.ForeignKey(Warehouse, verbose_name=_('warehouse'),
                                 on_delete=models.PROTECT, related_name='sales')
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='draft')
    sale_date = models.DateField(_('sale date'))
    notes = models.TextField(_('notes'), blank=True)
    discount_amount = models.DecimalField(_('discount amount'), max_digits=12, decimal_places=0,
                                         default=0, validators=[MinValueValidator(0)])
    tax_amount = models.DecimalField(_('tax amount'), max_digits=12, decimal_places=0,
                                    default=0, validators=[MinValueValidator(0)])
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('created by'),
                                  on_delete=models.PROTECT, related_name='sales')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('sale')
        verbose_name_plural = _('sales')
        ordering = ['-sale_date']

    def __str__(self):
        return f"{self.invoice_number} - {self.customer.name}"

    @property
    def subtotal(self):
        """Calculate subtotal of all items."""
        return self.items.aggregate(total=models.Sum(
            models.F('quantity') * models.F('unit_price')))['total'] or 0

    @property
    def total(self):
        """Calculate total amount including tax and discount."""
        return self.subtotal + self.tax_amount - self.discount_amount

class SaleItem(models.Model):
    """Sale item model."""
    sale = models.ForeignKey(Sale, verbose_name=_('sale'),
                            on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, verbose_name=_('product'),
                               on_delete=models.PROTECT, related_name='sale_items')
    quantity = models.DecimalField(_('quantity'), max_digits=10, decimal_places=2,
                                  validators=[MinValueValidator(0.01)])
    unit_price = models.DecimalField(_('unit price'), max_digits=12, decimal_places=0,
                                    validators=[MinValueValidator(0)])
    discount = models.DecimalField(_('discount'), max_digits=12, decimal_places=0,
                                  default=0, validators=[MinValueValidator(0)])
    notes = models.TextField(_('notes'), blank=True)

    class Meta:
        verbose_name = _('sale item')
        verbose_name_plural = _('sale items')

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    @property
    def total(self):
        """Calculate total amount for this item."""
        return (self.quantity * self.unit_price) - self.discount

    def save(self, *args, **kwargs):
        """Override save to create inventory transaction when sale is confirmed."""
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Create inventory transaction if sale status is confirmed or completed
        if is_new and self.sale.status in ['confirmed', 'completed']:
            InventoryTransaction.objects.create(
                transaction_type='sale',
                product=self.product,
                warehouse=self.sale.warehouse,
                quantity=self.quantity,
                unit_price=self.unit_price,
                reference_number=self.sale.invoice_number,
                reference_type='sale',
                reference_id=self.sale.id,
                created_by=self.sale.created_by
            )

class Invoice(models.Model):
    """Invoice model for tracking payments."""
    STATUS_CHOICES = [
        ('unpaid', _('Unpaid')),
        ('partially_paid', _('Partially Paid')),
        ('paid', _('Paid')),
        ('cancelled', _('Cancelled')),
    ]

    invoice_number = models.CharField(_('invoice number'), max_length=50, unique=True)
    customer = models.ForeignKey(Customer, verbose_name=_('customer'),
                                on_delete=models.PROTECT, related_name='invoices')
    sale = models.OneToOneField(Sale, verbose_name=_('sale'),
                               on_delete=models.PROTECT, related_name='invoice')
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='unpaid')
    issue_date = models.DateField(_('issue date'))
    due_date = models.DateField(_('due date'))
    total_amount = models.DecimalField(_('total amount'), max_digits=12, decimal_places=0,
                                      validators=[MinValueValidator(0)])
    paid_amount = models.DecimalField(_('paid amount'), max_digits=12, decimal_places=0,
                                     default=0, validators=[MinValueValidator(0)])
    remaining_amount = models.DecimalField(_('remaining amount'), max_digits=12, decimal_places=0,
                                          validators=[MinValueValidator(0)])
    notes = models.TextField(_('notes'), blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('created by'),
                                  on_delete=models.PROTECT, related_name='invoices')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('invoice')
        verbose_name_plural = _('invoices')
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.invoice_number} - {self.customer.name}"

    def save(self, *args, **kwargs):
        """Override save to update remaining amount."""
        self.remaining_amount = self.total_amount - self.paid_amount

        # Update status based on payment
        if self.remaining_amount <= 0:
            self.status = 'paid'
        elif self.paid_amount > 0:
            self.status = 'partially_paid'
        else:
            self.status = 'unpaid'

        super().save(*args, **kwargs)

class Payment(models.Model):
    """Payment model for tracking customer payments."""
    PAYMENT_METHODS = [
        ('cash', _('Cash')),
        ('bank_transfer', _('Bank Transfer')),
        ('check', _('Check')),
        ('credit_card', _('Credit Card')),
        ('other', _('Other')),
    ]

    payment_number = models.CharField(_('payment number'), max_length=50, unique=True)
    invoice = models.ForeignKey(Invoice, verbose_name=_('invoice'),
                               on_delete=models.PROTECT, related_name='payments')
    amount = models.DecimalField(_('amount'), max_digits=12, decimal_places=0,
                                validators=[MinValueValidator(0.01)])
    payment_method = models.CharField(_('payment method'), max_length=20, choices=PAYMENT_METHODS)
    payment_date = models.DateField(_('payment date'))
    reference = models.CharField(_('reference'), max_length=100, blank=True)
    notes = models.TextField(_('notes'), blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('created by'),
                                  on_delete=models.PROTECT, related_name='payments')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')
        ordering = ['-payment_date']

    def __str__(self):
        return f"{self.payment_number} - {self.invoice.invoice_number}"

    def save(self, *args, **kwargs):
        """Override save to update invoice paid amount."""
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            # Update invoice paid amount
            invoice = self.invoice
            invoice.paid_amount = invoice.payments.aggregate(total=models.Sum('amount'))['total'] or 0
            invoice.save()
