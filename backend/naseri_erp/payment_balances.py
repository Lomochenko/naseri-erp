"""Keep invoice balances consistent with the payment ledger."""
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models, transaction


def refresh_invoice_balance(invoice):
    invoice.paid_amount = invoice.payments.aggregate(total=models.Sum('amount'))['total'] or Decimal('0')
    invoice.save()


class PaymentBalanceMixin:
    def save(self, *args, **kwargs):
        invoice_model = self._meta.get_field('invoice').remote_field.model
        with transaction.atomic():
            old_invoice_id = None
            if self.pk:
                old_invoice_id = type(self).objects.values_list('invoice_id', flat=True).get(pk=self.pk)
            invoice_ids = {self.invoice_id}
            if old_invoice_id:
                invoice_ids.add(old_invoice_id)
            invoices = list(invoice_model.objects.select_for_update().filter(
                pk__in=invoice_ids).order_by('pk'))
            target = next(invoice for invoice in invoices if invoice.pk == self.invoice_id)
            paid = target.payments.exclude(pk=self.pk).aggregate(total=models.Sum('amount'))['total'] or Decimal('0')
            amount = Decimal(str(self.amount))
            if target.status == 'cancelled':
                raise ValidationError({'invoice': 'ثبت پرداخت برای فاکتور لغوشده مجاز نیست.'})
            if amount <= 0 or paid + amount > target.total_amount:
                raise ValidationError({'amount': 'مبلغ باید مثبت و حداکثر برابر مانده فاکتور باشد.'})
            super().save(*args, **kwargs)
            for invoice in invoices:
                refresh_invoice_balance(invoice)


def lock_payment_invoice(sender, instance, using, **kwargs):
    invoice_model = sender._meta.get_field('invoice').remote_field.model
    # Django's deletion collector runs signals inside an atomic transaction.
    invoice_model.objects.using(using).select_for_update().get(pk=instance.invoice_id)


def payment_deleted(sender, instance, using, **kwargs):
    invoice_model = sender._meta.get_field('invoice').remote_field.model
    invoice = invoice_model.objects.using(using).get(pk=instance.invoice_id)
    refresh_invoice_balance(invoice)


class PaymentValidationSerializerMixin:
    """Expose model validation failures as HTTP 400, including concurrent saves."""
    def create(self, validated_data):
        from rest_framework import serializers
        try:
            return super().create(validated_data)
        except ValidationError as error:
            raise serializers.ValidationError(error.message_dict) from error

    def update(self, instance, validated_data):
        from rest_framework import serializers
        try:
            return super().update(instance, validated_data)
        except ValidationError as error:
            raise serializers.ValidationError(error.message_dict) from error
