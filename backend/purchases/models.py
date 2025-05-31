from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import MinValueValidator
from products.models import Product
from inventory.models import Warehouse, InventoryTransaction

class Supplier(models.Model):
    """Supplier model."""
    name = models.CharField(_('name'), max_length=255)
    contact_person = models.CharField(_('contact person'), max_length=255, blank=True)
    phone = models.CharField(_('phone'), max_length=20, blank=True)
    email = models.EmailField(_('email'), blank=True)
    address = models.TextField(_('address'), blank=True)
    tax_number = models.CharField(_('tax number'), max_length=50, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    notes = models.TextField(_('notes'), blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('supplier')
        verbose_name_plural = _('suppliers')
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def total_due(self):
        """Calculate total amount due to supplier."""
        return self.purchase_invoices.filter(status='unpaid').aggregate(
            total=models.Sum('remaining_amount'))['total'] or 0

class Purchase(models.Model):
    """Purchase model."""
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('ordered', _('Ordered')),
        ('received', _('Received')),
        ('cancelled', _('Cancelled')),
    ]

    reference_number = models.CharField(_('reference number'), max_length=50, unique=True)
    supplier = models.ForeignKey(Supplier, verbose_name=_('supplier'),
                                on_delete=models.PROTECT, related_name='purchases')
    warehouse = models.ForeignKey(Warehouse, verbose_name=_('warehouse'),
                                 on_delete=models.PROTECT, related_name='purchases')
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='draft')
    purchase_date = models.DateField(_('purchase date'))
    expected_receipt_date = models.DateField(_('expected receipt date'), null=True, blank=True)
    notes = models.TextField(_('notes'), blank=True)
    discount_amount = models.DecimalField(_('discount amount'), max_digits=12, decimal_places=0,
                                         default=0, validators=[MinValueValidator(0)])
    tax_amount = models.DecimalField(_('tax amount'), max_digits=12, decimal_places=0,
                                    default=0, validators=[MinValueValidator(0)])
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('created by'),
                                  on_delete=models.PROTECT, related_name='purchases')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('purchase')
        verbose_name_plural = _('purchases')
        ordering = ['-purchase_date']

    def __str__(self):
        return f"{self.reference_number} - {self.supplier.name}"

    @property
    def subtotal(self):
        """Calculate subtotal of all items."""
        return self.items.aggregate(total=models.Sum(
            models.F('quantity') * models.F('unit_price')))['total'] or 0

    @property
    def total(self):
        """Calculate total amount including tax and discount."""
        return self.subtotal + self.tax_amount - self.discount_amount

class PurchaseItem(models.Model):
    """Purchase item model."""
    purchase = models.ForeignKey(Purchase, verbose_name=_('purchase'),
                                on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, verbose_name=_('product'),
                               on_delete=models.PROTECT, related_name='purchase_items')
    quantity = models.DecimalField(_('quantity'), max_digits=10, decimal_places=2,
                                  validators=[MinValueValidator(0.01)])
    received_quantity = models.DecimalField(_('received quantity'), max_digits=10, decimal_places=2,
                                          default=0, validators=[MinValueValidator(0)])
    unit_price = models.DecimalField(_('unit price'), max_digits=12, decimal_places=0,
                                    validators=[MinValueValidator(0)])
    notes = models.TextField(_('notes'), blank=True)

    class Meta:
        verbose_name = _('purchase item')
        verbose_name_plural = _('purchase items')

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    @property
    def total(self):
        """Calculate total amount for this item."""
        return self.quantity * self.unit_price

    def save(self, *args, **kwargs):
        """Override save to create inventory transaction when purchase is received."""
        is_new = self.pk is None
        old_received_quantity = 0

        if not is_new:
            # Get old received quantity
            old_item = PurchaseItem.objects.get(pk=self.pk)
            old_received_quantity = old_item.received_quantity

        super().save(*args, **kwargs)

        # Create inventory transaction if purchase status is received and received quantity changed
        if self.purchase.status == 'received' and self.received_quantity > old_received_quantity:
            # Calculate the difference in received quantity
            quantity_difference = self.received_quantity - old_received_quantity

            if quantity_difference > 0:
                InventoryTransaction.objects.create(
                    transaction_type='purchase',
                    product=self.product,
                    warehouse=self.purchase.warehouse,
                    quantity=quantity_difference,
                    unit_price=self.unit_price,
                    reference_number=self.purchase.reference_number,
                    reference_type='purchase',
                    reference_id=self.purchase.id,
                    created_by=self.purchase.created_by
                )

class PurchaseInvoice(models.Model):
    """Purchase invoice model for tracking payments to suppliers."""
    STATUS_CHOICES = [
        ('unpaid', _('Unpaid')),
        ('partially_paid', _('Partially Paid')),
        ('paid', _('Paid')),
        ('cancelled', _('Cancelled')),
    ]

    invoice_number = models.CharField(_('invoice number'), max_length=50, unique=True)
    supplier = models.ForeignKey(Supplier, verbose_name=_('supplier'),
                                on_delete=models.PROTECT, related_name='purchase_invoices')
    purchase = models.OneToOneField(Purchase, verbose_name=_('purchase'),
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
                                  on_delete=models.PROTECT, related_name='purchase_invoices')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('purchase invoice')
        verbose_name_plural = _('purchase invoices')
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.invoice_number} - {self.supplier.name}"

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

class SupplierPayment(models.Model):
    """Supplier payment model for tracking payments to suppliers."""
    PAYMENT_METHODS = [
        ('cash', _('Cash')),
        ('bank_transfer', _('Bank Transfer')),
        ('check', _('Check')),
        ('credit_card', _('Credit Card')),
        ('other', _('Other')),
    ]

    payment_number = models.CharField(_('payment number'), max_length=50, unique=True)
    invoice = models.ForeignKey(PurchaseInvoice, verbose_name=_('invoice'),
                               on_delete=models.PROTECT, related_name='payments')
    amount = models.DecimalField(_('amount'), max_digits=12, decimal_places=0,
                                validators=[MinValueValidator(0.01)])
    payment_method = models.CharField(_('payment method'), max_length=20, choices=PAYMENT_METHODS)
    payment_date = models.DateField(_('payment date'))
    reference = models.CharField(_('reference'), max_length=100, blank=True)
    notes = models.TextField(_('notes'), blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('created by'),
                                  on_delete=models.PROTECT, related_name='supplier_payments')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('supplier payment')
        verbose_name_plural = _('supplier payments')
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
