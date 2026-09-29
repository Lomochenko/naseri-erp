from rest_framework import serializers
from .models import Supplier, Purchase, PurchaseItem, PurchaseInvoice, SupplierPayment
from products.serializers import ProductSerializer
from naseri_erp.payment_balances import PaymentValidationSerializerMixin
from django.db import transaction
from naseri_erp.invoice_documents import invoice_document, purchase_invoice

class SupplierSerializer(serializers.ModelSerializer):
    """Serializer for Supplier model."""
    
    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'contact_person', 'phone', 'email', 'address',
            'tax_number', 'is_active', 'notes', 'created_at', 'updated_at',
            'total_due'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_due']

class PurchaseItemSerializer(serializers.ModelSerializer):
    """Serializer for PurchaseItem model."""
    product_name = serializers.ReadOnlyField(source='product.name')
    product_code = serializers.ReadOnlyField(source='product.code')
    
    class Meta:
        model = PurchaseItem
        fields = [
            'id', 'purchase', 'product', 'product_name', 'product_code',
            'quantity', 'received_quantity', 'unit_price', 'notes', 'total'
        ]
        read_only_fields = ['id', 'total']

class PurchaseLineSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_code = serializers.ReadOnlyField(source='product.code')

    class Meta:
        model = PurchaseItem
        fields = ['id', 'product', 'product_name', 'product_code', 'quantity',
                  'received_quantity', 'unit_price', 'notes', 'total']
        read_only_fields = ['id', 'total']

    def validate(self, attrs):
        missing = [field for field in ['product', 'quantity', 'unit_price'] if field not in attrs]
        if missing:
            raise serializers.ValidationError({field: 'این مقدار برای هر ردیف لازم است.' for field in missing})
        if attrs.get('received_quantity', 0) > attrs['quantity']:
            raise serializers.ValidationError('تعداد دریافتی نباید بیش از تعداد خرید باشد.')
        return attrs


class PurchaseSerializer(serializers.ModelSerializer):
    """Serializer for Purchase model."""
    supplier_name = serializers.ReadOnlyField(source='supplier.name')
    warehouse_name = serializers.ReadOnlyField(source='warehouse.name')
    status_display = serializers.ReadOnlyField(source='get_status_display')
    created_by_name = serializers.ReadOnlyField(source='created_by.get_full_name')
    items = PurchaseLineSerializer(many=True, required=False)
    invoice_document = serializers.SerializerMethodField()
    
    class Meta:
        model = Purchase
        fields = [
            'id', 'reference_number', 'supplier', 'supplier_name',
            'warehouse', 'warehouse_name', 'status', 'status_display',
            'purchase_date', 'expected_receipt_date', 'notes',
            'discount_amount', 'tax_amount', 'created_by', 'created_by_name',
            'created_at', 'updated_at', 'items', 'subtotal', 'total', 'invoice_document'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'subtotal', 'total', 'created_by']

    def get_invoice_document(self, obj):
        return invoice_document('purchase', obj)

    def validate(self, attrs):
        items = attrs.get('items')
        status = attrs.get('status', self.instance.status if self.instance else 'draft')
        if self.instance and status == 'draft' and getattr(self.instance, 'invoice', None):
            raise serializers.ValidationError({'status': 'خرید دارای فاکتور را نمی‌توان به پیش‌نویس برگرداند؛ در صورت نیاز آن را لغو کنید.'})
        if items is not None:
            if not items:
                raise serializers.ValidationError({'items': 'حداقل یک کالا لازم است.'})
            subtotal = sum(row['quantity'] * row['unit_price'] for row in items)
            if status != 'received' and any(row.get('received_quantity', 0) for row in items):
                raise serializers.ValidationError({'items': 'کالای سفارش‌داده‌شده هنوز وارد انبار نشده است.'})
            if status == 'received' and any(row.get('received_quantity', row['quantity']) != row['quantity'] for row in items):
                raise serializers.ValidationError({'items': 'وضعیت دریافت‌شده برای دریافت کامل است؛ برای دریافت جزئی خرید را سفارش‌داده‌شده نگه دارید.'})
        else:
            subtotal = self.instance.subtotal if self.instance else 0
        discount = attrs.get('discount_amount', self.instance.discount_amount if self.instance else 0)
        tax = attrs.get('tax_amount', self.instance.tax_amount if self.instance else 0)
        if subtotal + tax - discount < 0:
            raise serializers.ValidationError({'discount_amount': 'مبلغ نهایی نمی‌تواند منفی باشد.'})
        if self.instance and self.instance.status in ['received', 'cancelled']:
            if any(field in attrs for field in ['items', 'status', 'supplier', 'warehouse', 'discount_amount', 'tax_amount']):
                raise serializers.ValidationError('خرید دریافت‌شده یا لغوشده قابل تغییر مالی نیست؛ از فرایند برگشت استفاده کنید.')
        return attrs

    def create(self, validated_data):
        items = validated_data.pop('items', [])
        with transaction.atomic():
            purchase = Purchase.objects.create(**validated_data)
            for row in items:
                if purchase.status == 'received' and 'received_quantity' not in row:
                    row['received_quantity'] = row['quantity']
                PurchaseItem.objects.create(purchase=purchase, **row)
            purchase_invoice(purchase)
            return purchase

    def update(self, instance, validated_data):
        rows = validated_data.pop('items', None)
        with transaction.atomic():
            instance = Purchase.objects.select_for_update().get(pk=instance.pk)
            old_status = instance.status
            for field, value in validated_data.items():
                setattr(instance, field, value)
            instance.save()
            if rows is not None:
                instance.items.all().delete()
                for row in rows:
                    if instance.status == 'received' and 'received_quantity' not in row:
                        row['received_quantity'] = row['quantity']
                    PurchaseItem.objects.create(purchase=instance, **row)
            elif old_status != 'received' and instance.status == 'received':
                for item in instance.items.all():
                    item.received_quantity = item.quantity
                    item.save()
            if instance.status == 'cancelled':
                invoice = getattr(instance, 'invoice', None)
                if invoice:
                    if invoice.payments.exists():
                        raise serializers.ValidationError('خرید دارای پرداخت قابل لغو نیست.')
                    invoice.status = 'cancelled'
                    invoice.save()
            else:
                purchase_invoice(instance)
            return instance

class PurchaseInvoiceSerializer(serializers.ModelSerializer):
    """Serializer for PurchaseInvoice model."""
    supplier_name = serializers.ReadOnlyField(source='supplier.name')
    purchase_reference = serializers.ReadOnlyField(source='purchase.reference_number')
    status_display = serializers.ReadOnlyField(source='get_status_display')
    created_by_name = serializers.ReadOnlyField(source='created_by.get_full_name')
    
    class Meta:
        model = PurchaseInvoice
        fields = [
            'id', 'invoice_number', 'supplier', 'supplier_name',
            'purchase', 'purchase_reference', 'status', 'status_display',
            'issue_date', 'due_date', 'total_amount', 'paid_amount',
            'remaining_amount', 'notes', 'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'remaining_amount']

class SupplierPaymentSerializer(PaymentValidationSerializerMixin, serializers.ModelSerializer):
    """Serializer for SupplierPayment model."""
    invoice_number = serializers.ReadOnlyField(source='invoice.invoice_number')
    supplier_name = serializers.ReadOnlyField(source='invoice.supplier.name')
    payment_method_display = serializers.ReadOnlyField(source='get_payment_method_display')
    created_by_name = serializers.ReadOnlyField(source='created_by.get_full_name')
    
    class Meta:
        model = SupplierPayment
        fields = [
            'id', 'payment_number', 'invoice', 'invoice_number',
            'supplier_name', 'amount', 'payment_method', 'payment_method_display',
            'payment_date', 'reference', 'notes', 'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
