from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import AdminTheme

class AdminThemeTests(APITestCase):
    def setUp(self):
        self.theme1 = AdminTheme.objects.create(
            name="Test Theme 1",
            css_url="https://example.com/theme1.css",
            js_url="https://example.com/theme1.js"
        )
        self.theme2 = AdminTheme.objects.create(
            name="Test Theme 2",
            css_url="https://example.com/theme2.css",
            js_url="https://example.com/theme2.js",
            is_active=True
        )

    def test_list_themes(self):
        url = reverse('admintheme-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_toggle_active(self):
        url = reverse('admintheme-toggle-active')
        data = {'id': self.theme1.id, 'is_active': True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(AdminTheme.objects.get(pk=self.theme1.id).is_active)
        self.assertFalse(AdminTheme.objects.get(pk=self.theme2.id).is_active)
