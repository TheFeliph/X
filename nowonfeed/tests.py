from django.test import TestCase
from django.urls import reverse

class FeedTests(TestCase):
    def test_login(self):
        response = self.client.post(reverse('login'), {'username': 'user', 'password': 'user'})
        self.assertEqual(response.status_code, 302)