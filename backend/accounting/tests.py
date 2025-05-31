from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from .models import AccountType, Account, JournalEntry, JournalTransaction, FiscalYear, ExpenseCategory, Expense
from datetime import date

User = get_user_model()

class AccountingAPITest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            phone_number="09120000000",
            password="adminpass123",
            first_name="ادمین",
            last_name="سیستم"
        )
        self.client.force_authenticate(user=self.admin)
        self.account_type = AccountType.objects.create(name="دارایی جاری", category="asset")
        self.account = Account.objects.create(code="1010", name="صندوق", account_type=self.account_type)
        self.fiscal_year = FiscalYear.objects.create(name="سال 1404", start_date=date(2025,1,1), end_date=date(2025,12,31), is_active=True)
        self.expense_category = ExpenseCategory.objects.create(name="هزینه اداری", account=self.account)

    def test_create_account_type(self):
        url = reverse('accounttype-list')
        data = {"name": "درآمد عملیاتی", "category": "income"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(AccountType.objects.filter(name="درآمد عملیاتی").exists())

    def test_create_account(self):
        url = reverse('account-list')
        data = {"code": "2010", "name": "بانک ملت", "account_type": self.account_type.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Account.objects.filter(code="2010").exists())

    def test_create_journal_entry_and_transaction(self):
        url = reverse('journalentry-list')
        data = {
            "entry_number": "JE-001",
            "date": date.today(),
            "description": "ثبت تستی",
            "is_posted": True,
            "created_by": self.admin.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        entry_id = response.data['id']
        url_tr = reverse('journaltransaction-list')
        data_tr = {
            "journal_entry": entry_id,
            "account": self.account.id,
            "transaction_type": "debit",
            "amount": 10000
        }
        response_tr = self.client.post(url_tr, data_tr, format='json')
        self.assertEqual(response_tr.status_code, status.HTTP_201_CREATED)
        self.assertTrue(JournalTransaction.objects.filter(journal_entry=entry_id).exists())

    def test_create_fiscal_year(self):
        url = reverse('fiscalyear-list')
        data = {"name": "سال 1405", "start_date": date(2026,1,1), "end_date": date(2026,12,31)}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(FiscalYear.objects.filter(name="سال 1405").exists())

    def test_create_expense_category_and_expense(self):
        url = reverse('expensecategory-list')
        data = {"name": "هزینه بازاریابی", "account": self.account.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cat_id = response.data['id']
        url_exp = reverse('expense-list')
        data_exp = {
            "reference_number": "EXP-001",
            "category": cat_id,
            "amount": 5000,
            "expense_date": date.today(),
            "description": "هزینه تبلیغات",
            "payment_method": "cash",
            "created_by": self.admin.id
        }
        response_exp = self.client.post(url_exp, data_exp, format='json')
        self.assertEqual(response_exp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Expense.objects.filter(reference_number="EXP-001").exists())

    def test_chart_of_accounts(self):
        url = reverse('chart-of-accounts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_trial_balance(self):
        url = reverse('trial-balance')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('accounts', response.data)

    def test_income_statement(self):
        url = reverse('income-statement')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('income', response.data)
        self.assertIn('expenses', response.data)

    def test_balance_sheet(self):
        url = reverse('balance-sheet')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('assets', response.data)
        self.assertIn('liabilities', response.data)
        self.assertIn('equity', response.data)

    def test_cash_flow_statement(self):
        url = reverse('cash-flow-statement')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('beginning_cash', response.data)
        self.assertIn('ending_cash', response.data)
