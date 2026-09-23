from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid
from products.models import Product
from inventory.models import Warehouse, InventoryTransaction

class Customer(models.Model):
    """Customer model."""
    CUSTOMER_TYPE_CHOICES = [
        ('individual', _('Individual')),
        ('business', _('Business')),
    ]

    BUSINESS_CATEGORY_CHOICES = [
        ('retail', _('Retail')),
        ('wholesale', _('Wholesale')),
        ('contractor', _('Contractor')),
        ('other', _('Other')),
    ]

    customer_code = models.CharField(_('customer code'), max_length=20, unique=True, blank=True)
    name = models.CharField(_('name'), max_length=255)
    phone = models.CharField(_('phone'), max_length=20, blank=True)
    email = models.EmailField(_('email'), blank=True)
    customer_type = models.CharField(_('customer type'), max_length=20,
                                   choices=CUSTOMER_TYPE_CHOICES, default='individual')
    business_category = models.CharField(_('business category'), max_length=20,
                                       choices=BUSINESS_CATEGORY_CHOICES, blank=True)
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
        try:
            return self.invoices.filter(status='unpaid').aggregate(
                total=models.Sum('remaining_amount'))['total'] or 0
        except:
            return 0

    @property
    def account_balance(self):
        """Calculate customer's account balance (negative = debt, positive = credit)."""
        try:
            # Total sales amount
            total_sales = self.sales.filter(status__in=['confirmed', 'completed']).aggregate(
                total=models.Sum('total_amount'))['total'] or 0

            # Total payments received
            total_payments = 0
            for sale in self.sales.filter(status__in=['confirmed', 'completed']):
                sale_payments = sale.payments.aggregate(total=models.Sum('amount'))['total'] or 0
                total_payments += sale_payments

            # Balance = Payments - Sales (negative means customer owes money)
            return total_payments - total_sales
        except:
            return 0

    def save(self, *args, **kwargs):
        """Override save to auto-generate customer code."""
        if not self.customer_code:
            # Generate customer code: CUST + 6-digit number
            last_customer = Customer.objects.filter(
                customer_code__startswith='CUST'
            ).order_by('customer_code').last()

            if last_customer and last_customer.customer_code:
                try:
                    last_number = int(last_customer.customer_code[4:])
                    new_number = last_number + 1
                except (ValueError, IndexError):
                    new_number = 1
            else:
                new_number = 1

            self.customer_code = f'CUST{new_number:06d}'

        super().save(*args, **kwargs)

class Sale(models.Model):
    """Sale model."""
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('confirmed', _('Confirmed')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    ]

    invoice_number = models.CharField(_('invoice number'), max_length=50, unique=True, blank=True, null=True)
    customer = models.ForeignKey(Customer, verbose_name=_('customer'),
                                on_delete=models.PROTECT, related_name='sales')
    warehouse = models.ForeignKey(Warehouse, verbose_name=_('warehouse'),
                                 on_delete=models.PROTECT, related_name='sales', blank=True, null=True)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='draft')
    sale_date = models.DateField(_('sale date'))
    notes = models.TextField(_('notes'), blank=True)
    discount_amount = models.DecimalField(_('discount amount'), max_digits=12, decimal_places=0,
                                         default=0, validators=[MinValueValidator(Decimal('0'))])
    tax_amount = models.DecimalField(_('tax amount'), max_digits=12, decimal_places=0,
                                    default=0, validators=[MinValueValidator(Decimal('0'))])
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

    def save(self, *args, **kwargs):
        """Override save to auto-assign warehouse, generate invoice number, and check stock on confirm."""
        is_new = self.pk is None
        old_status = None

        if not is_new:
            try:
                old_status = Sale.objects.values_list('status', flat=True).get(pk=self.pk)
            except Sale.DoesNotExist:
                pass

        # Auto-assign warehouse if not set
        if not self.warehouse_id:
            from inventory.models import Warehouse
            default_warehouse = Warehouse.objects.filter(is_active=True).first()
            if default_warehouse:
                self.warehouse = default_warehouse

        # Generate invoice number if not set
        if not self.invoice_number:
            self.generate_invoice_number()

        super().save(*args, **kwargs)

    def generate_invoice_number(self):
        """Generate unique invoice number."""
        from django.utils import timezone
        today = timezone.now().date()
        count = Sale.objects.filter(created_at__date=today).count() + 1
        self.invoice_number = f"INV-{today.strftime('%Y%m%d')}-{count:04d}"

class SaleItem(models.Model):
    """Sale item model."""
    sale = models.ForeignKey(Sale, verbose_name=_('sale'),
                            on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, verbose_name=_('product'),
                               on_delete=models.PROTECT, related_name='sale_items')
    quantity = models.DecimalField(_('quantity'), max_digits=10, decimal_places=2,
                                  validators=[MinValueValidator(Decimal('0.01'))])
    unit_price = models.DecimalField(_('unit price'), max_digits=12, decimal_places=0,
                                    validators=[MinValueValidator(Decimal('0'))])
    discount = models.DecimalField(_('discount'), max_digits=12, decimal_places=0,
                                  default=0, validators=[MinValueValidator(Decimal('0'))])
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
        """Override save - only creates inventory transaction when item is added to an already-confirmed sale."""
        is_new = self.pk is None
        old_sale_status = None

        if not is_new:
            old_sale_status = SaleItem.objects.values_list('sale__status', flat=True).get(pk=self.pk)

        super().save(*args, **kwargs)

        # Only create transaction if item is NEW and sale is already confirmed/completed
        # (status transitions are handled by update_status in views.py)
        if is_new and self.sale.status in ['confirmed', 'completed']:
            current_stock = self.product.current_stock
            if current_stock < self.quantity:
                raise ValueError(f'موجودی کافی نیست. موجودی فعلی: {current_stock}، مقدار درخواستی: {self.quantity}')

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
