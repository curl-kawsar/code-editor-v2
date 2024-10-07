from django.test import TestCase
from rest_framework.test import APIClient
from .models import CodeSnippet

class CodeSnippetTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_code_execution(self):
        response = self.client.post('/api/codesnippets/', {'code': 'print("Hello, World!")'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Hello, World!', response.data['result'])