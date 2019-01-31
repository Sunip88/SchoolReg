from django.test import TestCase
from django.urls import reverse


class LoggedOutTest(TestCase):
    def test_home_view_logged_out(self):
        url = reverse("main")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/login/?next=/')

