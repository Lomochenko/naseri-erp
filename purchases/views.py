from rest_framework import viewsets, permissions, generics, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import Supplier, Purchase, PurchaseItem, PurchaseInvoice, SupplierPayment
from .serializers import (
    SupplierSerializer, PurchaseSerializer, PurchaseItemSerializer,
    PurchaseInvoiceSerializer, SupplierPaymentSerializer
)

class SupplierViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Supplier instances."""
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'contact_person', 'phone', 'email', 'address']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

class PurchaseViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Purchase instances."""
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'supplier', 'warehouse']
    search_fields = ['reference_number', 'notes']
    ordering_fields = ['purchase_date', 'created_at']
    ordering = ['-purchase_date']

class PurchaseItemViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing PurchaseItem instances."""
    queryset = PurchaseItem.objects.all()
    serializer_class = PurchaseItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['purchase', 'product']
    search_fields = ['notes']

class PurchaseInvoiceViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing PurchaseInvoice instances."""
    queryset = PurchaseInvoice.objects.all()
    serializer_class = PurchaseInvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'supplier']
    search_fields = ['invoice_number', 'notes']
    ordering_fields = ['issue_date', 'due_date', 'created_at']
    ordering = ['-issue_date']

class SupplierPaymentViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing SupplierPayment instances."""
    queryset = SupplierPayment.objects.all()
    serializer_class = SupplierPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['payment_method', 'invoice']
    search_fields = ['payment_number', 'reference', 'notes']
    ordering_fields = ['payment_date', 'created_at']
    ordering = ['-payment_date']

class SupplierPurchasesView(generics.RetrieveAPIView):
    """API view for retrieving supplier purchases information."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, supplier_id):
        """Handle GET requests for supplier purchases."""
        try:
            supplier = Supplier.objects.get(id=supplier_id)
            purchases = Purchase.objects.filter(supplier=supplier)

            purchases_data = {
                'supplier_id': supplier.id,
                'supplier_name': supplier.name,
                'total_purchases': purchases.count(),
                'total_amount': sum(purchase.total for purchase in purchases),
                'purchases': []
            }

            for purchase in purchases:
                purchases_data['purchases'].append({
                    'id': purchase.id,
                    'reference_number': purchase.reference_number,
                    'purchase_date': purchase.purchase_date,
                    'status': purchase.get_status_display(),
                    'total': purchase.total,
                    'items_count': purchase.items.count()
                })

            return Response(purchases_data)
        except Supplier.DoesNotExist:
            return Response({'error': 'Supplier not found'}, status=404)

class SupplierInvoicesView(generics.RetrieveAPIView):
    """API view for retrieving supplier invoices information."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, supplier_id):
        """Handle GET requests for supplier invoices."""
        try:
            supplier = Supplier.objects.get(id=supplier_id)
            invoices = PurchaseInvoice.objects.filter(supplier=supplier)

            invoices_data = {
                'supplier_id': supplier.id,
                'supplier_name': supplier.name,
                'total_invoices': invoices.count(),
                'total_amount': invoices.aggregate(total=Sum('total_amount'))['total'] or 0,
                'paid_amount': invoices.aggregate(total=Sum('paid_amount'))['total'] or 0,
                'remaining_amount': invoices.aggregate(total=Sum('remaining_amount'))['total'] or 0,
                'invoices': []
            }

            for invoice in invoices:
                invoices_data['invoices'].append({
                    'id': invoice.id,
                    'invoice_number': invoice.invoice_number,
                    'issue_date': invoice.issue_date,
                    'due_date': invoice.due_date,
                    'status': invoice.get_status_display(),
                    'total_amount': invoice.total_amount,
                    'paid_amount': invoice.paid_amount,
                    'remaining_amount': invoice.remaining_amount
                })

            return Response(invoices_data)
        except Supplier.DoesNotExist:
            return Response({'error': 'Supplier not found'}, status=404)

class PurchasesReportView(generics.ListAPIView):
    """API view for generating purchases reports."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Handle GET requests for purchases reports."""
        # Get query parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        period = request.query_params.get('period', 'daily')  # daily, weekly, monthly

        # Filter purchases by date range
        purchases_query = Purchase.objects.filter(status__in=['ordered', 'received'])

        if start_date:
            purchases_query = purchases_query.filter(purchase_date__gte=start_date)
        if end_date:
            purchases_query = purchases_query.filter(purchase_date__lte=end_date)

        # Default to last 30 days if no dates provided
        if not start_date and not end_date:
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=30)
            purchases_query = purchases_query.filter(purchase_date__range=[start_date, end_date])

        # Prepare report data
        report_data = {
            'start_date': start_date,
            'end_date': end_date,
            'period': period,
            'total_purchases': purchases_query.count(),
            'total_amount': sum(purchase.total for purchase in purchases_query),
            'purchases_by_period': []
        }

        # Group purchases by period
        if period == 'daily':
            purchases_by_day = {}
            for purchase in purchases_query:
                day_str = purchase.purchase_date.strftime('%Y-%m-%d')
                if day_str not in purchases_by_day:
                    purchases_by_day[day_str] = {'count': 0, 'amount': 0}
                purchases_by_day[day_str]['count'] += 1
                purchases_by_day[day_str]['amount'] += purchase.total

            for day, data in sorted(purchases_by_day.items()):
                report_data['purchases_by_period'].append({
                    'period': day,
                    'purchases_count': data['count'],
                    'purchases_amount': data['amount']
                })

        elif period == 'weekly':
            purchases_by_week = {}
            for purchase in purchases_query:
                week_str = f"{purchase.purchase_date.isocalendar()[0]}-W{purchase.purchase_date.isocalendar()[1]}"
                if week_str not in purchases_by_week:
                    purchases_by_week[week_str] = {'count': 0, 'amount': 0}
                purchases_by_week[week_str]['count'] += 1
                purchases_by_week[week_str]['amount'] += purchase.total

            for week, data in sorted(purchases_by_week.items()):
                report_data['purchases_by_period'].append({
                    'period': week,
                    'purchases_count': data['count'],
                    'purchases_amount': data['amount']
                })

        elif period == 'monthly':
            purchases_by_month = {}
            for purchase in purchases_query:
                month_str = purchase.purchase_date.strftime('%Y-%m')
                if month_str not in purchases_by_month:
                    purchases_by_month[month_str] = {'count': 0, 'amount': 0}
                purchases_by_month[month_str]['count'] += 1
                purchases_by_month[month_str]['amount'] += purchase.total

            for month, data in sorted(purchases_by_month.items()):
                report_data['purchases_by_period'].append({
                    'period': month,
                    'purchases_count': data['count'],
                    'purchases_amount': data['amount']
                })

        return Response(report_data)

class PurchasesByProductView(generics.ListAPIView):
    """API view for generating purchases by product reports."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Handle GET requests for purchases by product reports."""
        # Get query parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Filter purchases by date range
        purchases_query = Purchase.objects.filter(status__in=['ordered', 'received'])

        if start_date:
            purchases_query = purchases_query.filter(purchase_date__gte=start_date)
        if end_date:
            purchases_query = purchases_query.filter(purchase_date__lte=end_date)

        # Default to last 30 days if no dates provided
        if not start_date and not end_date:
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=30)
            purchases_query = purchases_query.filter(purchase_date__range=[start_date, end_date])

        # Get purchase items for these purchases
        purchase_items = PurchaseItem.objects.filter(purchase__in=purchases_query)

        # Group by product
        product_purchases = {}
        for item in purchase_items:
            product_id = item.product.id
            if product_id not in product_purchases:
                product_purchases[product_id] = {
                    'product_id': product_id,
                    'product_name': item.product.name,
                    'product_code': item.product.code,
                    'quantity': 0,
                    'amount': 0
                }
            product_purchases[product_id]['quantity'] += item.quantity
            product_purchases[product_id]['amount'] += item.quantity * item.unit_price

        # Prepare report data
        report_data = {
            'start_date': start_date,
            'end_date': end_date,
            'total_products': len(product_purchases),
            'products': sorted(product_purchases.values(), key=lambda x: x['amount'], reverse=True)
        }

        return Response(report_data)
