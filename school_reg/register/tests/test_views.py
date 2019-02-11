from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from register.models import Teacher, Classes, Parent, Student, Subject, Lessons, ClassRoom, WorkingHours, Schedule


class TeacherPanelViewTest(TestCase):
    def setUp(self):
        # Create three users
        test_user_1 = User.objects.create_user(username='testuser1',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing',
                                               last_name='user')
        test_user_1.profile.role = 2
        test_user_1.save()
        teacher = Teacher.objects.create(user=test_user_1)
        classes_new = Classes.objects.create(educator=teacher, name='1a', description='test')

        test_user_2 = User.objects.create_user(username='testuser2',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing2',
                                               last_name='user2')
        test_user_2.profile.role = 0
        test_user_2.save()

        test_user_3 = User.objects.create_user(username='testuser3',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing3',
                                               last_name='user3')
        test_user_3.profile.role = 1
        test_user_3.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('teacher-panel-view'))
        self.assertRedirects(response, '/login/?next=/teacher_panel/')

    def test_logged_in_user_teacher(self):
        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(reverse('teacher-panel-view'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/teacher_view.html')

    def test_logged_in_user_different_than_teacher(self):
        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(reverse('teacher-panel-view'))
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(reverse('teacher-panel-view'))
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)


class ParentPanelViewTest(TestCase):
    def setUp(self):
        # Create three users
        test_user_1 = User.objects.create_user(username='testuser1',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing',
                                               last_name='user')
        test_user_1.profile.role = 1
        test_user_1.save()
        parent = Parent.objects.create(user=test_user_1)
        test_user_2 = User.objects.create_user(username='testuser2',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing2',
                                               last_name='user2')
        test_user_2.profile.role = 0
        test_user_2.save()

        test_user_3 = User.objects.create_user(username='testuser3',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing3',
                                               last_name='user3')
        test_user_3.profile.role = 2
        test_user_3.save()
        teacher = Teacher.objects.create(user=test_user_3)
        classes_new = Classes.objects.create(educator=teacher, name='1a', description='test')

        student = Student.objects.create(user=test_user_2, year_of_birth=1988, classes=classes_new)
        parent.students.add(student)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('parent-panel-view'))
        self.assertRedirects(response, '/login/?next=/parent_panel/')

    def test_logged_in_user_parent(self):
        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(reverse('parent-panel-view'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/parent_view.html')

    def test_logged_in_user_different_than_parent(self):
        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(reverse('parent-panel-view'))
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(reverse('parent-panel-view'))
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)


class StudentViewTest(TestCase):
    def setUp(self):
        # Create three users
        test_user_1 = User.objects.create_user(username='testuser1',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing',
                                               last_name='user')
        test_user_1.profile.role = 1
        test_user_1.save()
        parent = Parent.objects.create(user=test_user_1)
        test_user_2 = User.objects.create_user(username='testuser2',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing2',
                                               last_name='user2')
        test_user_2.profile.role = 0
        test_user_2.save()

        test_user_3 = User.objects.create_user(username='testuser3',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing3',
                                               last_name='user3')
        test_user_3.profile.role = 2
        test_user_3.save()
        teacher = Teacher.objects.create(user=test_user_3)
        classes_new = Classes.objects.create(educator=teacher, name='1a', description='test')

        student = Student.objects.create(user=test_user_2, year_of_birth=1988, classes=classes_new)
        parent.students.add(student)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('student-panel-view'))
        self.assertRedirects(response, '/login/?next=/student_panel/')

    def test_logged_in_user_parent(self):
        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(reverse('student-panel-view'))
        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/student_view.html')

    def test_logged_in_user_different_than_parent(self):
        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(reverse('student-panel-view'))
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(reverse('student-panel-view'))
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)


class TeacherSubjectsClassesViewTest(TestCase):
    def setUp(self):
        # Create three users
        test_user_1 = User.objects.create_user(username='testuser1',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing',
                                               last_name='user')
        test_user_1.profile.role = 1
        test_user_1.save()
        parent = Parent.objects.create(user=test_user_1)
        test_user_2 = User.objects.create_user(username='testuser2',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing2',
                                               last_name='user2')
        test_user_2.profile.role = 0
        test_user_2.save()

        test_user_3 = User.objects.create_user(username='testuser3',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing3',
                                               last_name='user3')
        test_user_3.profile.role = 2
        test_user_3.save()
        teacher = Teacher.objects.create(user=test_user_3)

        classes_new = Classes.objects.create(educator=teacher, name='1a', description='test')

        student = Student.objects.create(user=test_user_2, year_of_birth=1988, classes=classes_new)
        parent.students.add(student)

        subject = Subject.objects.create(name='testSubject')
        subject.classes.add(classes_new)
        subject.save()
        lesson = Lessons.objects.create(classes=classes_new, subject=subject, teacher=teacher)
        room = ClassRoom.objects.create(name="testRoom")
        time_s = datetime.strptime('8:00', '%H:%M').time()
        time_e = datetime.strptime('8:45', '%H:%M').time()
        hours = WorkingHours.objects.create(nr=1, start_time=time_s, end_time=time_e)
        schedule = Schedule.objects.create(lesson=lesson, room=room, hours=hours, weekday=1)

        test_user_4 = User.objects.create_user(username='testuser4',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing4',
                                               last_name='user4')
        test_user_4.profile.role = 2
        test_user_4.save()
        teacher2 = Teacher.objects.create(user=test_user_4)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('teacher-subjects-view'))
        self.assertRedirects(response, '/login/?next=/teacher_subjects/')

    def test_logged_in_user_teacher(self):
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(reverse('teacher-subjects-view'))
        self.assertEqual(str(response.context['user']), 'testuser3')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/teacher_class_subject.html')

    def test_logged_in_user_teacher_no_schedule(self):
        login = self.client.login(username='testuser4', password='testpassword')
        response = self.client.get(reverse('teacher-subjects-view'))
        self.assertEqual(str(response.context['user']), 'testuser4')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/teacher_class_subject.html')

    def test_logged_in_user_different_than_teacher(self):
        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(reverse('teacher-subjects-view'))
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(reverse('teacher-subjects-view'))
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)


class TeacherGradesViewTest(TestCase):
    def setUp(self):
        # Create three users
        test_user_1 = User.objects.create_user(username='testuser1',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing',
                                               last_name='user')
        test_user_1.profile.role = 1
        test_user_1.save()
        parent = Parent.objects.create(user=test_user_1)
        test_user_2 = User.objects.create_user(username='testuser2',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing2',
                                               last_name='user2')
        test_user_2.profile.role = 0
        test_user_2.save()

        test_user_3 = User.objects.create_user(username='testuser3',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing3',
                                               last_name='user3')
        test_user_3.profile.role = 2
        test_user_3.save()
        teacher = Teacher.objects.create(user=test_user_3)

        classes_new = Classes.objects.create(educator=teacher, name='1a', description='test')

        student = Student.objects.create(user=test_user_2, year_of_birth=1988, classes=classes_new)
        parent.students.add(student)

        subject = Subject.objects.create(name='testSubject')
        subject.classes.add(classes_new)
        subject.save()

    def test_redirect_if_not_logged_in(self):
        subject = Subject.objects.all().first()
        classes = Classes.objects.all().first()
        url = reverse("class-details-grades", kwargs={'subject_id': subject.id, 'class_id': classes.id})
        response = self.client.get(url)
        self.assertRedirects(response, f'/login/?next=/detailed_class_grades/{subject.id}/{classes.id}/')

    def test_logged_in_user_teacher(self):
        subject = Subject.objects.all().first()
        classes = Classes.objects.all().first()
        url = reverse("class-details-grades", kwargs={'subject_id': subject.id, 'class_id': classes.id})
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser3')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/teacher_class_grades.html')

    def test_logged_in_user_different_than_teacher(self):
        subject = Subject.objects.all().first()
        classes = Classes.objects.all().first()
        url = reverse("class-details-grades", kwargs={'subject_id': subject.id, 'class_id': classes.id})
        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(reverse('teacher-subjects-view'))
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)


class ClassViewTest(TestCase):
    def setUp(self):
        # Create three users
        test_user_1 = User.objects.create_user(username='testuser1',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing',
                                               last_name='user')
        test_user_1.profile.role = 1
        test_user_1.save()
        parent = Parent.objects.create(user=test_user_1)
        test_user_2 = User.objects.create_user(username='testuser2',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing2',
                                               last_name='user2')
        test_user_2.profile.role = 0
        test_user_2.save()

        test_user_3 = User.objects.create_user(username='testuser3',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing3',
                                               last_name='user3')
        test_user_3.profile.role = 2
        test_user_3.save()
        teacher = Teacher.objects.create(user=test_user_3)

        classes_new = Classes.objects.create(educator=teacher, name='1a', description='test')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("class-view"))
        self.assertRedirects(response, '/login/?next=/classes/')

    def test_logged_in_user_teacher(self):
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(reverse("class-view"))
        self.assertEqual(str(response.context['user']), 'testuser3')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/classes.html')

    def test_logged_in_user_different_than_teacher(self):
        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(reverse("class-view"))
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(reverse("class-view"))
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)
