from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import Report
from users.models import User

class ReportModelTest(TestCase):
    def test_create_report(self):
        report = Report.objects.create(name='Test Report', description='This is a test report.')
        self.assertEqual(report.name, 'Test Report')
        self.assertEqual(report.description, 'This is a test report.')

class ReportAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(phone_number='09123456789', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.report = Report.objects.create(name='Test Report', description='This is a test report')

    def test_get_reports(self):
        response = self.client.get(reverse('report-list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Report', str(response.data))

    def test_post_report(self):
        data = {
            'name': 'New Report',
            'description': 'This is a new report.'
        }
        response = self.client.post(reverse('report-list'), data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('New Report', str(response.data))