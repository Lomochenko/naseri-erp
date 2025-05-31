from rest_framework import viewsets, permissions, generics, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import timedelta
from .models import (
    AccountType, Account, JournalEntry, JournalTransaction,
    FiscalYear, ExpenseCategory, Expense
)
from .serializers import (
    AccountTypeSerializer, AccountSerializer, JournalEntrySerializer,
    JournalTransactionSerializer, FiscalYearSerializer,
    ExpenseCategorySerializer, ExpenseSerializer
)

class AccountTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing AccountType instances."""
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'category']
    ordering = ['category', 'name']

class AccountViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Account instances."""
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['account_type', 'is_active']
    search_fields = ['code', 'name', 'description']
    ordering_fields = ['code', 'name', 'account_type__name']
    ordering = ['code']

class JournalEntryViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing JournalEntry instances."""
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_posted', 'reference_type']
    search_fields = ['entry_number', 'description']
    ordering_fields = ['date', 'entry_number', 'created_at']
    ordering = ['-date', '-entry_number']

class JournalTransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing JournalTransaction instances."""
    queryset = JournalTransaction.objects.all()
    serializer_class = JournalTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['journal_entry', 'account', 'transaction_type']
    search_fields = ['description']

class FiscalYearViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing FiscalYear instances."""
    queryset = FiscalYear.objects.all()
    serializer_class = FiscalYearSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['start_date', 'name']
    ordering = ['-start_date']

class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing ExpenseCategory instances."""
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    ordering = ['name']

class ExpenseViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Expense instances."""
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'payment_method']
    search_fields = ['reference_number', 'description']
    ordering_fields = ['expense_date', 'amount', 'created_at']
    ordering = ['-expense_date']

class ChartOfAccountsView(generics.ListAPIView):
    """API view for retrieving chart of accounts."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Handle GET requests for chart of accounts."""
        # Get all account types
        account_types = AccountType.objects.all()

        # Prepare chart of accounts data
        chart_data = []

        for account_type in account_types:
            type_data = {
                'id': account_type.id,
                'name': account_type.name,
                'category': account_type.category,
                'category_display': account_type.get_category_display(),
                'accounts': []
            }

            # Get all top-level accounts for this account type
            accounts = Account.objects.filter(account_type=account_type, parent=None)

            for account in accounts:
                account_data = {
                    'id': account.id,
                    'code': account.code,
                    'name': account.name,
                    'balance': account.balance,
                    'children': []
                }

                # Get child accounts
                children = Account.objects.filter(parent=account)

                for child in children:
                    child_data = {
                        'id': child.id,
                        'code': child.code,
                        'name': child.name,
                        'balance': child.balance
                    }
                    account_data['children'].append(child_data)

                type_data['accounts'].append(account_data)

            chart_data.append(type_data)

        return Response(chart_data)

class AccountBalanceView(generics.RetrieveAPIView):
    """API view for retrieving account balance and transactions."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, account_id):
        """Handle GET requests for account balance."""
        try:
            account = Account.objects.get(id=account_id)

            # Get query parameters
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')

            # Filter transactions by date range
            transactions_query = JournalTransaction.objects.filter(
                account=account,
                journal_entry__is_posted=True
            )

            if start_date:
                transactions_query = transactions_query.filter(journal_entry__date__gte=start_date)
            if end_date:
                transactions_query = transactions_query.filter(journal_entry__date__lte=end_date)

            # Prepare account data
            account_data = {
                'id': account.id,
                'code': account.code,
                'name': account.name,
                'account_type': account.account_type.name,
                'account_type_category': account.account_type.category,
                'balance': account.balance,
                'transactions': []
            }

            # Add transactions
            for transaction in transactions_query.order_by('journal_entry__date', 'journal_entry__entry_number'):
                account_data['transactions'].append({
                    'id': transaction.id,
                    'date': transaction.journal_entry.date,
                    'entry_number': transaction.journal_entry.entry_number,
                    'description': transaction.description or transaction.journal_entry.description,
                    'transaction_type': transaction.get_transaction_type_display(),
                    'amount': transaction.amount
                })

            return Response(account_data)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=404)

class TrialBalanceView(generics.ListAPIView):
    """API view for generating trial balance."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Handle GET requests for trial balance."""
        # Get query parameters
        as_of_date = request.query_params.get('as_of_date')

        # Default to current date if not provided
        if not as_of_date:
            as_of_date = timezone.now().date()

        # Get all accounts
        accounts = Account.objects.filter(is_active=True).order_by('code')

        # Prepare trial balance data
        trial_balance = {
            'as_of_date': as_of_date,
            'accounts': [],
            'total_debit': 0,
            'total_credit': 0
        }

        for account in accounts:
            # Calculate account balance as of the specified date
            debit_sum = JournalTransaction.objects.filter(
                account=account,
                transaction_type='debit',
                journal_entry__date__lte=as_of_date,
                journal_entry__is_posted=True
            ).aggregate(total=Sum('amount'))['total'] or 0

            credit_sum = JournalTransaction.objects.filter(
                account=account,
                transaction_type='credit',
                journal_entry__date__lte=as_of_date,
                journal_entry__is_posted=True
            ).aggregate(total=Sum('amount'))['total'] or 0

            # Calculate balance based on account type
            if account.account_type.category in ['asset', 'expense']:
                balance = debit_sum - credit_sum
                debit_amount = balance if balance > 0 else 0
                credit_amount = -balance if balance < 0 else 0
            else:
                balance = credit_sum - debit_sum
                debit_amount = -balance if balance < 0 else 0
                credit_amount = balance if balance > 0 else 0

            # Only include accounts with non-zero balances
            if debit_amount > 0 or credit_amount > 0:
                trial_balance['accounts'].append({
                    'id': account.id,
                    'code': account.code,
                    'name': account.name,
                    'account_type': account.account_type.name,
                    'account_type_category': account.account_type.category,
                    'debit': debit_amount,
                    'credit': credit_amount
                })

                trial_balance['total_debit'] += debit_amount
                trial_balance['total_credit'] += credit_amount

        return Response(trial_balance)

class IncomeStatementView(generics.ListAPIView):
    """API view for generating income statement."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Handle GET requests for income statement."""
        # Get query parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Default to current fiscal year if not provided
        if not start_date or not end_date:
            current_fiscal_year = FiscalYear.objects.filter(is_active=True).first()
            if current_fiscal_year:
                start_date = current_fiscal_year.start_date
                end_date = current_fiscal_year.end_date
            else:
                # Default to current year
                today = timezone.now().date()
                start_date = today.replace(month=1, day=1)
                end_date = today

        # Get income and expense accounts
        income_accounts = Account.objects.filter(
            account_type__category='income',
            is_active=True
        ).order_by('code')

        expense_accounts = Account.objects.filter(
            account_type__category='expense',
            is_active=True
        ).order_by('code')

        # Prepare income statement data
        income_statement = {
            'start_date': start_date,
            'end_date': end_date,
            'income': [],
            'total_income': 0,
            'expenses': [],
            'total_expenses': 0,
            'net_income': 0
        }

        # Calculate income
        for account in income_accounts:
            # For income accounts, credit increases the balance
            credit_sum = JournalTransaction.objects.filter(
                account=account,
                transaction_type='credit',
                journal_entry__date__range=[start_date, end_date],
                journal_entry__is_posted=True
            ).aggregate(total=Sum('amount'))['total'] or 0

            debit_sum = JournalTransaction.objects.filter(
                account=account,
                transaction_type='debit',
                journal_entry__date__range=[start_date, end_date],
                journal_entry__is_posted=True
            ).aggregate(total=Sum('amount'))['total'] or 0

            balance = credit_sum - debit_sum

            if balance != 0:
                income_statement['income'].append({
                    'id': account.id,
                    'code': account.code,
                    'name': account.name,
                    'amount': balance
                })

                income_statement['total_income'] += balance

        # Calculate expenses
        for account in expense_accounts:
            # For expense accounts, debit increases the balance
            debit_sum = JournalTransaction.objects.filter(
                account=account,
                transaction_type='debit',
                journal_entry__date__range=[start_date, end_date],
                journal_entry__is_posted=True
            ).aggregate(total=Sum('amount'))['total'] or 0

            credit_sum = JournalTransaction.objects.filter(
                account=account,
                transaction_type='credit',
                journal_entry__date__range=[start_date, end_date],
                journal_entry__is_posted=True
            ).aggregate(total=Sum('amount'))['total'] or 0

            balance = debit_sum - credit_sum

            if balance != 0:
                income_statement['expenses'].append({
                    'id': account.id,
                    'code': account.code,
                    'name': account.name,
                    'amount': balance
                })

                income_statement['total_expenses'] += balance

        # Calculate net income
        income_statement['net_income'] = income_statement['total_income'] - income_statement['total_expenses']

        return Response(income_statement)

class BalanceSheetView(generics.ListAPIView):
    """API view for generating balance sheet."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Handle GET requests for balance sheet."""
        # Get query parameters
        as_of_date = request.query_params.get('as_of_date')

        # Default to current date if not provided
        if not as_of_date:
            as_of_date = timezone.now().date()

        # Get asset, liability, and equity accounts
        asset_accounts = Account.objects.filter(
            account_type__category='asset',
            is_active=True
        ).order_by('code')

        liability_accounts = Account.objects.filter(
            account_type__category='liability',
            is_active=True
        ).order_by('code')

        equity_accounts = Account.objects.filter(
            account_type__category='equity',
            is_active=True
        ).order_by('code')

        # Prepare balance sheet data
        balance_sheet = {
            'as_of_date': as_of_date,
            'assets': [],
            'total_assets': 0,
            'liabilities': [],
            'total_liabilities': 0,
            'equity': [],
            'total_equity': 0
        }

        # Calculate assets
        for account in asset_accounts:
            # For asset accounts, debit increases the balance
            debit_sum = JournalTransaction.objects.filter(
                account=account,
                transaction_type='debit',
                journal_entry__date__lte=as_of_date,
                journal_entry__is_posted=True
            ).aggregate(total=Sum('amount'))['total'] or 0

            credit_sum = JournalTransaction.objects.filter(
                account=account,
                transaction_type='credit',
                journal_entry__date__lte=as_of_date,
                journal_entry__is_posted=True
            ).aggregate(total=Sum('amount'))['total'] or 0

            balance = debit_sum - credit_sum

            if balance != 0:
                balance_sheet['assets'].append({
                    'id': account.id,
                    'code': account.code,
                    'name': account.name,
                    'amount': balance
                })

                balance_sheet['total_assets'] += balance

        # Calculate liabilities
        for account in liability_accounts:
            # For liability accounts, credit increases the balance
            credit_sum = JournalTransaction.objects.filter(
                account=account,
                transaction_type='credit',
                journal_entry__date__lte=as_of_date,
                journal_entry__is_posted=True
            ).aggregate(total=Sum('amount'))['total'] or 0

            debit_sum = JournalTransaction.objects.filter(
                account=account,
                transaction_type='debit',
                journal_entry__date__lte=as_of_date,
                journal_entry__is_posted=True
            ).aggregate(total=Sum('amount'))['total'] or 0

            balance = credit_sum - debit_sum

            if balance != 0:
                balance_sheet['liabilities'].append({
                    'id': account.id,
                    'code': account.code,
                    'name': account.name,
                    'amount': balance
                })

                balance_sheet['total_liabilities'] += balance

        # Calculate equity
        for account in equity_accounts:
            # For equity accounts, credit increases the balance
            credit_sum = JournalTransaction.objects.filter(
                account=account,
                transaction_type='credit',
                journal_entry__date__lte=as_of_date,
                journal_entry__is_posted=True
            ).aggregate(total=Sum('amount'))['total'] or 0

            debit_sum = JournalTransaction.objects.filter(
                account=account,
                transaction_type='debit',
                journal_entry__date__lte=as_of_date,
                journal_entry__is_posted=True
            ).aggregate(total=Sum('amount'))['total'] or 0

            balance = credit_sum - debit_sum

            if balance != 0:
                balance_sheet['equity'].append({
                    'id': account.id,
                    'code': account.code,
                    'name': account.name,
                    'amount': balance
                })

                balance_sheet['total_equity'] += balance

        # Calculate retained earnings (net income for the current fiscal year)
        # This is a simplified approach - in a real system, you would need to handle retained earnings more carefully
        income_accounts = Account.objects.filter(account_type__category='income', is_active=True)
        expense_accounts = Account.objects.filter(account_type__category='expense', is_active=True)

        # Get current fiscal year
        current_fiscal_year = FiscalYear.objects.filter(is_active=True).first()
        if current_fiscal_year:
            start_date = current_fiscal_year.start_date
            end_date = min(as_of_date, current_fiscal_year.end_date)

            # Calculate income
            income_sum = 0
            for account in income_accounts:
                credit_sum = JournalTransaction.objects.filter(
                    account=account,
                    transaction_type='credit',
                    journal_entry__date__range=[start_date, end_date],
                    journal_entry__is_posted=True
                ).aggregate(total=Sum('amount'))['total'] or 0

                debit_sum = JournalTransaction.objects.filter(
                    account=account,
                    transaction_type='debit',
                    journal_entry__date__range=[start_date, end_date],
                    journal_entry__is_posted=True
                ).aggregate(total=Sum('amount'))['total'] or 0

                income_sum += credit_sum - debit_sum

            # Calculate expenses
            expense_sum = 0
            for account in expense_accounts:
                debit_sum = JournalTransaction.objects.filter(
                    account=account,
                    transaction_type='debit',
                    journal_entry__date__range=[start_date, end_date],
                    journal_entry__is_posted=True
                ).aggregate(total=Sum('amount'))['total'] or 0

                credit_sum = JournalTransaction.objects.filter(
                    account=account,
                    transaction_type='credit',
                    journal_entry__date__range=[start_date, end_date],
                    journal_entry__is_posted=True
                ).aggregate(total=Sum('amount'))['total'] or 0

                expense_sum += debit_sum - credit_sum

            # Calculate net income
            net_income = income_sum - expense_sum

            if net_income != 0:
                balance_sheet['equity'].append({
                    'id': 0,
                    'code': '',
                    'name': 'Retained Earnings (Current Year)',
                    'amount': net_income
                })

                balance_sheet['total_equity'] += net_income

        return Response(balance_sheet)

class CashFlowStatementView(generics.ListAPIView):
    """API view for generating cash flow statement."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Handle GET requests for cash flow statement."""
        # Get query parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Default to current fiscal year if not provided
        if not start_date or not end_date:
            current_fiscal_year = FiscalYear.objects.filter(is_active=True).first()
            if current_fiscal_year:
                start_date = current_fiscal_year.start_date
                end_date = current_fiscal_year.end_date
            else:
                # Default to current year
                today = timezone.now().date()
                start_date = today.replace(month=1, day=1)
                end_date = today

        # Get cash accounts
        cash_accounts = Account.objects.filter(
            Q(code__startswith='101') | Q(name__icontains='cash') | Q(name__icontains='bank'),
            account_type__category='asset',
            is_active=True
        )

        # Prepare cash flow statement data
        cash_flow = {
            'start_date': start_date,
            'end_date': end_date,
            'operating_activities': [],
            'total_operating': 0,
            'investing_activities': [],
            'total_investing': 0,
            'financing_activities': [],
            'total_financing': 0,
            'net_cash_flow': 0,
            'beginning_cash': 0,
            'ending_cash': 0
        }

        # Calculate beginning cash balance
        for account in cash_accounts:
            debit_sum = JournalTransaction.objects.filter(
                account=account,
                transaction_type='debit',
                journal_entry__date__lt=start_date,
                journal_entry__is_posted=True
            ).aggregate(total=Sum('amount'))['total'] or 0

            credit_sum = JournalTransaction.objects.filter(
                account=account,
                transaction_type='credit',
                journal_entry__date__lt=start_date,
                journal_entry__is_posted=True
            ).aggregate(total=Sum('amount'))['total'] or 0

            cash_flow['beginning_cash'] += debit_sum - credit_sum

        # Calculate ending cash balance
        for account in cash_accounts:
            debit_sum = JournalTransaction.objects.filter(
                account=account,
                transaction_type='debit',
                journal_entry__date__lte=end_date,
                journal_entry__is_posted=True
            ).aggregate(total=Sum('amount'))['total'] or 0

            credit_sum = JournalTransaction.objects.filter(
                account=account,
                transaction_type='credit',
                journal_entry__date__lte=end_date,
                journal_entry__is_posted=True
            ).aggregate(total=Sum('amount'))['total'] or 0

            cash_flow['ending_cash'] += debit_sum - credit_sum

        # Calculate net cash flow
        cash_flow['net_cash_flow'] = cash_flow['ending_cash'] - cash_flow['beginning_cash']

        # Note: In a real system, you would need to categorize transactions into operating, investing, and financing activities
        # This is a simplified approach that just shows the net change in cash

        return Response(cash_flow)
