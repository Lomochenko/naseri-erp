from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import MinValueValidator
from sales.models import Sale, Invoice, Payment
from purchases.models import Purchase, PurchaseInvoice, SupplierPayment

class AccountType(models.Model):
    """Account type model."""
    ACCOUNT_CATEGORIES = [
        ('asset', _('Asset')),
        ('liability', _('Liability')),
        ('equity', _('Equity')),
        ('income', _('Income')),
        ('expense', _('Expense')),
    ]

    name = models.CharField(_('name'), max_length=100)
    category = models.CharField(_('category'), max_length=20, choices=ACCOUNT_CATEGORIES)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('account type')
        verbose_name_plural = _('account types')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class Account(models.Model):
    """Account model for chart of accounts."""
    code = models.CharField(_('account code'), max_length=20, unique=True)
    name = models.CharField(_('name'), max_length=100)
    account_type = models.ForeignKey(AccountType, verbose_name=_('account type'),
                                    on_delete=models.PROTECT, related_name='accounts')
    parent = models.ForeignKey('self', verbose_name=_('parent account'),
                              on_delete=models.CASCADE, null=True, blank=True,
                              related_name='children')
    description = models.TextField(_('description'), blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('account')
        verbose_name_plural = _('accounts')
        ordering = ['code', 'name']

    def __str__(self):
        return f"{self.code} - {self.name}"

    @property
    def balance(self):
        """Calculate account balance from transactions."""
        debit_sum = self.journal_transactions.filter(transaction_type='debit').aggregate(total=models.Sum('amount'))['total'] or 0
        credit_sum = self.journal_transactions.filter(transaction_type='credit').aggregate(total=models.Sum('amount'))['total'] or 0
        if self.account_type.category in ['asset', 'expense']:
            return debit_sum - credit_sum
        else:
            return credit_sum - debit_sum

class JournalEntry(models.Model):
    """Journal entry model for accounting transactions."""
    entry_number = models.CharField(_('entry number'), max_length=50, unique=True)
    date = models.DateField(_('date'))
    reference_type = models.CharField(_('reference type'), max_length=50, blank=True, null=True)
    reference_id = models.PositiveIntegerField(_('reference ID'), blank=True, null=True)
    description = models.TextField(_('description'))
    is_posted = models.BooleanField(_('posted'), default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('created by'),
                                  on_delete=models.PROTECT, related_name='journal_entries')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('journal entry')
        verbose_name_plural = _('journal entries')
        ordering = ['-date', '-entry_number']

    def __str__(self):
        return f"{self.entry_number} - {self.date}"

    @property
    def is_balanced(self):
        """Check if the journal entry is balanced (debits = credits)."""
        debit_sum = self.transactions.filter(transaction_type='debit').aggregate(
            total=models.Sum('amount'))['total'] or 0
        credit_sum = self.transactions.filter(transaction_type='credit').aggregate(
            total=models.Sum('amount'))['total'] or 0
        return debit_sum == credit_sum

class JournalTransaction(models.Model):
    """Journal transaction model for individual debit/credit entries."""
    TRANSACTION_TYPES = [
        ('debit', _('Debit')),
        ('credit', _('Credit')),
    ]

    journal_entry = models.ForeignKey(JournalEntry, verbose_name=_('journal entry'),
                                     on_delete=models.CASCADE, related_name='transactions')
    account = models.ForeignKey(Account, verbose_name=_('account'),
                               on_delete=models.PROTECT,
                               related_name='journal_transactions')
    transaction_type = models.CharField(_('transaction type'), max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(_('amount'), max_digits=12, decimal_places=0,
                                validators=[MinValueValidator(0.01)])
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('journal transaction')
        verbose_name_plural = _('journal transactions')

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.account.name} - {self.amount}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # دیگر نیازی به افزودن دستی به related_name نیست

class FiscalYear(models.Model):
    """Fiscal year model."""
    name = models.CharField(_('name'), max_length=100)
    start_date = models.DateField(_('start date'))
    end_date = models.DateField(_('end date'))
    is_active = models.BooleanField(_('active'), default=False)
    is_closed = models.BooleanField(_('closed'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('fiscal year')
        verbose_name_plural = _('fiscal years')
        ordering = ['-start_date']

    def __str__(self):
        return self.name

    def clean(self):
        """Validate that end_date is after start_date."""
        from django.core.exceptions import ValidationError
        if self.end_date <= self.start_date:
            raise ValidationError(_('End date must be after start date.'))

class ExpenseCategory(models.Model):
    """Expense category model."""
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    account = models.ForeignKey(Account, verbose_name=_('account'),
                               on_delete=models.PROTECT, related_name='expense_categories')

    class Meta:
        verbose_name = _('expense category')
        verbose_name_plural = _('expense categories')
        ordering = ['name']

    def __str__(self):
        return self.name

class Expense(models.Model):
    """Expense model for tracking business expenses."""
    reference_number = models.CharField(_('reference number'), max_length=50, unique=True)
    category = models.ForeignKey(ExpenseCategory, verbose_name=_('category'),
                                on_delete=models.PROTECT, related_name='expenses')
    amount = models.DecimalField(_('amount'), max_digits=12, decimal_places=0,
                                validators=[MinValueValidator(0.01)])
    expense_date = models.DateField(_('expense date'))
    description = models.TextField(_('description'))
    payment_method = models.CharField(_('payment method'), max_length=50)
    receipt = models.FileField(_('receipt'), upload_to='expenses/receipts/', blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('created by'),
                                  on_delete=models.PROTECT, related_name='expenses')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('expense')
        verbose_name_plural = _('expenses')
        ordering = ['-expense_date']

    def __str__(self):
        return f"{self.reference_number} - {self.category.name} - {self.amount}"

    def save(self, *args, **kwargs):
        """Override save to create journal entry for expense."""
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            # Create journal entry for expense
            journal_entry = JournalEntry.objects.create(
                entry_number=f"EXP-{self.reference_number}",
                date=self.expense_date,
                reference_type='expense',
                reference_id=self.pk,
                description=f"Expense: {self.description}",
                is_posted=True,
                created_by=self.created_by
            )

            # Create debit transaction for expense account
            JournalTransaction.objects.create(
                journal_entry=journal_entry,
                account=self.category.account,
                transaction_type='debit',
                amount=self.amount,
                description=self.description
            )

            # Create credit transaction for cash/bank account based on payment method
            # This is simplified - in a real system, you would have a mapping of payment methods to accounts
            cash_account = Account.objects.get(code='1010')  # Assuming 1010 is the cash account code

            JournalTransaction.objects.create(
                journal_entry=journal_entry,
                account=cash_account,
                transaction_type='credit',
                amount=self.amount,
                description=self.description
            )
