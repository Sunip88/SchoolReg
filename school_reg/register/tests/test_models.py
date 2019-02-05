from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from register.models import Subject, Teacher, Classes
from users.models import Profile


class ClassModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser',
                                   email='a@a.com',
                                   password='testpassword',
                                   first_name='testing',
                                   last_name='user')
        user.profile.role = 2
        teacher = Teacher.objects.create(user=user)
        Classes.objects.create(educator=teacher, name='1a', description='test')

    def test_educator_label(self):
        classes = Classes.objects.get(id=1)
        field_label = classes._meta.get_field('educator').verbose_name
        self.assertEqual(field_label, 'educator')

    def test_name_label(self):
        classes = Classes.objects.get(id=1)
        field_label = classes._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_description_label(self):
        classes = Classes.objects.get(id=1)
        field_label = classes._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_name_max_lenght(self):
        classes = Classes.objects.get(id=1)
        max_length = classes._meta.get_field('name').max_length
        self.assertEqual(max_length, 32)

    def test_description_max_lenght(self):
        classes = Classes.objects.get(id=1)
        max_length = classes._meta.get_field('description').max_length
        self.assertEqual(max_length, 512)

    def test_object_name_is_name(self):
        classes = Classes.objects.get(id=1)
        expected_object_name = f'{classes.name}'
        self.assertEqual(expected_object_name, str(classes))


class SubjectModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser',
                                   email='a@a.com',
                                   password='testpassword',
                                   first_name='testing',
                                   last_name='user')
        user.profile.role = 2
        teacher = Teacher.objects.create(user=user)
        classes_new = Classes.objects.create(educator=teacher, name='1a', description='test')
        subject = Subject.objects.create(name='testSubject')
        subject.classes.add(classes_new)
        subject.save()

    def test_name_label(self):
        subject = Subject.objects.get(id=1)
        field_label = subject._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_classes_label(self):
        subject = Subject.objects.get(id=1)
        field_label = subject._meta.get_field('classes').verbose_name
        self.assertEqual(field_label, 'classes')

    def test_name_max_lenght(self):
        subject = Subject.objects.get(id=1)
        max_length = subject._meta.get_field('name').max_length
        self.assertEqual(max_length, 128)

    def test_object_name_is_name(self):
        subject = Subject.objects.get(id=1)
        expected_object_name = f'{subject.name}'
        self.assertEqual(expected_object_name, str(subject))



class LoggedOutTest(TestCase):
    def test_home_view_logged_out(self):
        url = reverse("main")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/login/?next=/')

