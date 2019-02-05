from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from register.models import Subject
from users.models import Profile

#
# class ClassModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         user = User.objects.create(username='testuser',
#                                    email='a@a.com',
#                                    password='testpassword',
#                                    first_name='testing',
#                                    last_name='user')
#         Profile.objects.create(user=user, role=2)
#         Subject.objects.create(name='Biology')




class LoggedOutTest(TestCase):
    def test_home_view_logged_out(self):
        url = reverse("main")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/login/?next=/')

