from rest_framework import serializers
from .models import (
    AccountType, Account, JournalEntry, JournalTransaction,
    FiscalYear, ExpenseCategory, Expense
)

class AccountTypeSerializer(serializers.ModelSerializer):
    """Serializer for AccountType model."""
    category_display = serializers.ReadOnlyField(source='get_category_display')
    
    class Meta:
        model = AccountType
        fields = ['id', 'name', 'category', 'category_display', 'description']
        read_only_fields = ['id']

class AccountSerializer(serializers.ModelSerializer):
    """Serializer for Account model."""
    account_type_name = serializers.ReadOnlyField(source='account_type.name')
    account_type_category = serializers.ReadOnlyField(source='account_type.category')
    parent_name = serializers.ReadOnlyField(source='parent.name')
    
    class Meta:
        model = Account
        fields = [
            'id', 'code', 'name', 'account_type', 'account_type_name',
            'account_type_category', 'parent', 'parent_name', 'description',
            'is_active', 'created_at', 'updated_at', 'balance'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'balance']

class JournalTransactionSerializer(serializers.ModelSerializer):
    """Serializer for JournalTransaction model."""
    account_name = serializers.ReadOnlyField(source='account.name')
    account_code = serializers.ReadOnlyField(source='account.code')
    transaction_type_display = serializers.ReadOnlyField(source='get_transaction_type_display')
    
    class Meta:
        model = JournalTransaction
        fields = [
            'id', 'journal_entry', 'account', 'account_name', 'account_code',
            'transaction_type', 'transaction_type_display', 'amount', 'description'
        ]
        read_only_fields = ['id']

class JournalEntrySerializer(serializers.ModelSerializer):
    """Serializer for JournalEntry model."""
    created_by_name = serializers.ReadOnlyField(source='created_by.get_full_name')
    transactions = JournalTransactionSerializer(many=True, read_only=True)
    
    class Meta:
        model = JournalEntry
        fields = [
            'id', 'entry_number', 'date', 'reference_type', 'reference_id',
            'description', 'is_posted', 'created_by', 'created_by_name',
            'created_at', 'updated_at', 'transactions', 'is_balanced'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_balanced']

class FiscalYearSerializer(serializers.ModelSerializer):
    """Serializer for FiscalYear model."""
    
    class Meta:
        model = FiscalYear
        fields = [
            'id', 'name', 'start_date', 'end_date', 'is_active',
            'is_closed', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class ExpenseCategorySerializer(serializers.ModelSerializer):
    """Serializer for ExpenseCategory model."""
    account_name = serializers.ReadOnlyField(source='account.name')
    account_code = serializers.ReadOnlyField(source='account.code')
    
    class Meta:
        model = ExpenseCategory
        fields = ['id', 'name', 'description', 'account', 'account_name', 'account_code']
        read_only_fields = ['id']

class ExpenseSerializer(serializers.ModelSerializer):
    """Serializer for Expense model."""
    category_name = serializers.ReadOnlyField(source='category.name')
    created_by_name = serializers.ReadOnlyField(source='created_by.get_full_name')
    
    class Meta:
        model = Expense
        fields = [
            'id', 'reference_number', 'category', 'category_name', 'amount',
            'expense_date', 'description', 'payment_method', 'receipt',
            'created_by', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
