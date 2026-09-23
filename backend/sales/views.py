from rest_framework import viewsets, permissions, generics, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, F, Count
from django.utils import timezone
from datetime import timedelta
from .models import Customer, Sale, SaleItem, Invoice, Payment
from inventory.models import InventoryTransaction
from .serializers import (
    CustomerSerializer, SaleSerializer, SaleCreateUpdateSerializer, SaleItemSerializer,
    InvoiceSerializer, PaymentSerializer
)

class CustomerViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Customer instances."""
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'phone', 'address']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

class SaleViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Sale instances."""
    queryset = Sale.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'customer', 'warehouse']
    search_fields = ['invoice_number', 'notes']
    ordering_fields = ['sale_date', 'created_at']
    ordering = ['-sale_date']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SaleCreateUpdateSerializer
        return SaleSerializer

    def create(self, request, *args, **kwargs):
        print(f"=== SALE CREATE REQUEST ===")
        print(f"Request data: {request.data}")
        print(f"Request user: {request.user}")
        print(f"Content type: {request.content_type}")

        try:
            response = super().create(request, *args, **kwargs)
            print(f"Sale created successfully: {response.data}")
            return response
        except Exception as e:
            print(f"Error in create: {str(e)}")
            print(f"Error type: {type(e)}")
            if hasattr(e, 'detail'):
                print(f"Error detail: {e.detail}")
            raise

    def perform_create(self, serializer):
        print(f"Perform create called")
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, pk=None):
        """Update sale status."""
        from rest_framework.response import Response
        from rest_framework import status as http_status
        from django.db import transaction

        sale = self.get_object()
        new_status = request.data.get('status')

        print(f"=== UPDATING SALE STATUS ===")
        print(f"Sale ID: {sale.id}")
        print(f"Current status: {sale.status}")
        print(f"New status: {new_status}")

        # Validate status
        valid_statuses = ['draft', 'confirmed', 'completed', 'cancelled']
        if new_status not in valid_statuses:
            return Response(
                {'error': f'Invalid status. Must be one of: {valid_statuses}'},
                status=http_status.HTTP_400_BAD_REQUEST
            )

        # Business logic for status transitions
        if sale.status == 'cancelled':
            return Response(
                {'error': 'Cannot change status of cancelled sale'},
                status=http_status.HTTP_400_BAD_REQUEST
            )

        if sale.status == 'completed' and new_status != 'completed':
            return Response(
                {'error': 'Cannot change status of completed sale'},
                status=http_status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                old_status = sale.status
                sale.status = new_status
                sale.save()

                # Handle inventory updates based on status change
                if new_status == 'confirmed' and old_status == 'draft':
                    # When confirming, ensure stock is still available
                    for item in sale.items.all():
                        if item.product.current_stock < item.quantity:
                            raise ValueError(f'Insufficient stock for {item.product.name}')

                elif new_status == 'cancelled':
                    # When cancelling, restore stock via inventory transaction
                    if old_status in ['confirmed', 'completed']:
                        for item in sale.items.all():
                            InventoryTransaction.objects.create(
                                transaction_type='return_from_customer',
                                product=item.product,
                                warehouse=sale.warehouse,
                                quantity=item.quantity,
                                unit_price=item.unit_price,
                                reference_number=sale.invoice_number,
                                reference_type='sale_cancel',
                                reference_id=sale.id,
                                created_by=request.user
                            )
                            print(f"Restored stock for {item.product.name}: +{item.quantity}")

                print(f"Status updated successfully: {old_status} -> {new_status}")

                # Return updated sale data
                serializer = self.get_serializer(sale)
                return Response(serializer.data, status=http_status.HTTP_200_OK)

        except Exception as e:
            print(f"Error updating status: {str(e)}")
            return Response(
                {'error': str(e)},
                status=http_status.HTTP_400_BAD_REQUEST
            )

class SaleItemViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing SaleItem instances."""
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['sale', 'product']
    search_fields = ['notes']

class InvoiceViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Invoice instances."""
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'customer']
    search_fields = ['invoice_number', 'notes']
    ordering_fields = ['issue_date', 'due_date', 'created_at']
    ordering = ['-issue_date']

class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Payment instances."""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['payment_method', 'invoice']
    search_fields = ['payment_number', 'reference', 'notes']
    ordering_fields = ['payment_date', 'created_at']
    ordering = ['-payment_date']

class CustomerSalesView(generics.RetrieveAPIView):
    """API view for retrieving customer sales information."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SaleSerializer  # For swagger documentation

    def get(self, request, customer_id):
        """Handle GET requests for customer sales."""
        try:
            customer = Customer.objects.get(id=customer_id)
            sales = Sale.objects.filter(customer=customer)

            sales_data = {
                'customer_id': customer.id,
                'customer_name': customer.name,
                'total_sales': sales.count(),
                'total_amount': sum(sale.total for sale in sales),
                'sales': []
            }

            for sale in sales:
                sales_data['sales'].append({
                    'id': sale.id,
                    'invoice_number': sale.invoice_number,
                    'sale_date': sale.sale_date,
                    'status': sale.get_status_display(),
                    'total': sale.total,
                    'items_count': sale.items.count()
                })

            return Response(sales_data)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=404)

class CustomerInvoicesView(generics.RetrieveAPIView):
    """API view for retrieving customer invoices information."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InvoiceSerializer  # For swagger documentation

    def get(self, request, customer_id):
        """Handle GET requests for customer invoices."""
        try:
            customer = Customer.objects.get(id=customer_id)
            invoices = Invoice.objects.filter(customer=customer)

            invoices_data = {
                'customer_id': customer.id,
                'customer_name': customer.name,
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
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=404)

class SalesReportView(generics.ListAPIView):
    """API view for generating sales reports."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SaleSerializer  # For swagger documentation

    def get(self, request):
        """Handle GET requests for sales reports."""
        # Get query parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        period = request.query_params.get('period', 'daily')  # daily, weekly, monthly

        # Filter sales by date range
        sales_query = Sale.objects.filter(status__in=['confirmed', 'completed'])

        if start_date:
            sales_query = sales_query.filter(sale_date__gte=start_date)
        if end_date:
            sales_query = sales_query.filter(sale_date__lte=end_date)

        # Default to last 30 days if no dates provided
        if not start_date and not end_date:
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=30)
            sales_query = sales_query.filter(sale_date__range=[start_date, end_date])

        # Prepare report data
        report_data = {
            'start_date': start_date,
            'end_date': end_date,
            'period': period,
            'total_sales': sales_query.count(),
            'total_amount': sum(sale.total for sale in sales_query),
            'sales_by_period': []
        }

        # Group sales by period
        if period == 'daily':
            sales_by_day = {}
            for sale in sales_query:
                day_str = sale.sale_date.strftime('%Y-%m-%d')
                if day_str not in sales_by_day:
                    sales_by_day[day_str] = {'count': 0, 'amount': 0}
                sales_by_day[day_str]['count'] += 1
                sales_by_day[day_str]['amount'] += sale.total

            for day, data in sorted(sales_by_day.items()):
                report_data['sales_by_period'].append({
                    'period': day,
                    'sales_count': data['count'],
                    'sales_amount': data['amount']
                })

        elif period == 'weekly':
            sales_by_week = {}
            for sale in sales_query:
                week_str = f"{sale.sale_date.isocalendar()[0]}-W{sale.sale_date.isocalendar()[1]}"
                if week_str not in sales_by_week:
                    sales_by_week[week_str] = {'count': 0, 'amount': 0}
                sales_by_week[week_str]['count'] += 1
                sales_by_week[week_str]['amount'] += sale.total

            for week, data in sorted(sales_by_week.items()):
                report_data['sales_by_period'].append({
                    'period': week,
                    'sales_count': data['count'],
                    'sales_amount': data['amount']
                })

        elif period == 'monthly':
            sales_by_month = {}
            for sale in sales_query:
                month_str = sale.sale_date.strftime('%Y-%m')
                if month_str not in sales_by_month:
                    sales_by_month[month_str] = {'count': 0, 'amount': 0}
                sales_by_month[month_str]['count'] += 1
                sales_by_month[month_str]['amount'] += sale.total

            for month, data in sorted(sales_by_month.items()):
                report_data['sales_by_period'].append({
                    'period': month,
                    'sales_count': data['count'],
                    'sales_amount': data['amount']
                })

        return Response(report_data)

class SalesByProductView(generics.ListAPIView):
    """API view for generating sales by product reports."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SaleSerializer  # For swagger documentation

    def get(self, request):
        """Handle GET requests for sales by product reports."""
        # Get query parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Filter sales by date range
        sales_query = Sale.objects.filter(status__in=['confirmed', 'completed'])

        if start_date:
            sales_query = sales_query.filter(sale_date__gte=start_date)
        if end_date:
            sales_query = sales_query.filter(sale_date__lte=end_date)

        # Default to last 30 days if no dates provided
        if not start_date and not end_date:
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=30)
            sales_query = sales_query.filter(sale_date__range=[start_date, end_date])

        # Get sale items for these sales
        sale_items = SaleItem.objects.filter(sale__in=sales_query)

        # Group by product
        product_sales = {}
        for item in sale_items:
            product_id = item.product.id
            if product_id not in product_sales:
                product_sales[product_id] = {
                    'product_id': product_id,
                    'product_name': item.product.name,
                    'product_code': item.product.code,
                    'quantity': 0,
                    'amount': 0
                }
            product_sales[product_id]['quantity'] += item.quantity
            product_sales[product_id]['amount'] += (item.quantity * item.unit_price) - item.discount

        # Prepare report data
        report_data = {
            'start_date': start_date,
            'end_date': end_date,
            'total_products': len(product_sales),
            'products': sorted(product_sales.values(), key=lambda x: x['amount'], reverse=True)
        }

        return Response(report_data)
