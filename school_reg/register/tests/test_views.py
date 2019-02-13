from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from register.forms import AddAdvertForm, EditAdvertForm, AddClassAdvertForm, EditClassAdvertForm, AddNoticeForm, \
    EditNoticeForm, AnswerNoticeForm, AddEventForm
from register.models import Teacher, Classes, Parent, Student, Subject, Lessons, ClassRoom, WorkingHours, Schedule, \
    Grades, GradeCategory, Adverts, AdvertsClass, Notice, Announcements, Event


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


class DetailsClassViewTest(TestCase):
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

        test_user_4 = User.objects.create_user(username='testuser4',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing4',
                                               last_name='user4')
        test_user_4.profile.role = 1
        test_user_4.save()
        parent = Parent.objects.create(user=test_user_4)

        test_user_5 = User.objects.create_user(username='testuser5',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing5',
                                               last_name='user5')
        test_user_5.profile.role = 0
        test_user_5.save()
        classes_new_2 = Classes.objects.create(educator=teacher, name='1b', description='test')
        student = Student.objects.create(user=test_user_5, year_of_birth=1988, classes=classes_new_2)


    def test_redirect_if_not_logged_in(self):
        classes = Classes.objects.all().first()
        url = reverse("class-details", kwargs={'pk': classes.id})
        response = self.client.get(url)
        self.assertRedirects(response, f'/login/?next=/detailed_class/{classes.id}/')

    def test_logged_in_user_teacher(self):
        login = self.client.login(username='testuser3', password='testpassword')
        classes = Classes.objects.all().first()
        url = reverse("class-details", kwargs={'pk': classes.id})
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser3')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/detail_classes.html')

    def test_logged_in_user_different_than_teacher(self):
        login = self.client.login(username='testuser1', password='testpassword')
        classes = Classes.objects.all().first()
        url = reverse("class-details", kwargs={'pk': classes.id})
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertEqual(response.status_code, 200)

        login = self.client.login(username='testuser4', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser5', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)


class AddGradeCategoryViewTest(TestCase):
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
        response = self.client.get(reverse("add-grade-category"))
        self.assertRedirects(response, '/login/?next=/add_grade_category/')

    def test_logged_in_user_teacher(self):
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(reverse("add-grade-category"))
        self.assertEqual(str(response.context['user']), 'testuser3')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/add_class.html')

    def test_logged_in_user_different_than_teacher(self):
        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(reverse("add-grade-category"))
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(reverse("add-grade-category"))
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)


class TeacherDetailViewTest(TestCase):
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
        category_grade = GradeCategory.objects.create(name="test")
        grade = Grades.objects.create(subject=subject, student=student, category=category_grade, grade=5)

        test_user_4 = User.objects.create_user(username='testuser4',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing4',
                                               last_name='user4')
        test_user_4.profile.role = 1
        test_user_4.save()
        parent = Parent.objects.create(user=test_user_4)

        test_user_5 = User.objects.create_user(username='testuser5',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing5',
                                               last_name='user5')
        test_user_5.profile.role = 0
        test_user_5.save()
        classes_new_2 = Classes.objects.create(educator=teacher, name='1b', description='test')
        student = Student.objects.create(user=test_user_5, year_of_birth=1988, classes=classes_new_2)

    def test_redirect_if_not_logged_in(self):
        student = Student.objects.all().first()
        url = reverse("student-details", kwargs={'pk': student.id})
        response = self.client.get(url)
        self.assertRedirects(response, f'/login/?next=/detailed_student/{student.id}/')

    def test_logged_in_user_teacher(self):
        login = self.client.login(username='testuser3', password='testpassword')
        student = Student.objects.all().first()
        url = reverse("student-details", kwargs={'pk': student.id})
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser3')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/student_details.html')

    def test_logged_in_user_different_than_teacher(self):
        login = self.client.login(username='testuser1', password='testpassword')
        student = Student.objects.all().first()
        url = reverse("student-details", kwargs={'pk': student.id})
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertEqual(response.status_code, 200)

        login = self.client.login(username='testuser4', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser5', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)


class SchedulesViewTest(TestCase):
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
        response = self.client.get(reverse("schedules"))
        self.assertRedirects(response, '/login/?next=/schedules/')

    def test_logged_in_user(self):
        url = reverse("schedules")

        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser3')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/schedules.html')

        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertEqual(response.status_code, 200)


class ScheduleClassesTest(TestCase):
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
        classes = Classes.objects.first()
        response = self.client.get(reverse("class-schedule", kwargs={'id_class': classes.id}))
        self.assertRedirects(response, f'/login/?next=/class_schedule/{classes.id}/')

    def test_logged_in_user(self):
        classes = Classes.objects.first()
        url = reverse("class-schedule", kwargs={'id_class': classes.id})

        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser3')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/schedule_class.html')

        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertEqual(response.status_code, 200)


class ScheduleTeacherViewTest(TestCase):
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
        teacher = Teacher.objects.first()
        response = self.client.get(reverse("teacher-schedule", kwargs={'id_teacher': teacher.id}))
        self.assertRedirects(response, f'/login/?next=/teacher_schedule/{teacher.id}/')

    def test_logged_in_user(self):
        teacher = Teacher.objects.first()
        url = reverse("teacher-schedule", kwargs={'id_teacher': teacher.id})

        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser3')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/schedule_class.html')

        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertEqual(response.status_code, 200)


class ScheduleRoomViewTest(TestCase):
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
        room = ClassRoom.objects.create(name='test room')
        classes_new = Classes.objects.create(educator=teacher, name='1a', description='test')

    def test_redirect_if_not_logged_in(self):
        room = ClassRoom.objects.first()
        response = self.client.get(reverse("room-schedule", kwargs={'id_room': room.id}))
        self.assertRedirects(response, f'/login/?next=/room_schedule/{room.id}/')

    def test_logged_in_user(self):
        room = ClassRoom.objects.first()
        url = reverse("room-schedule", kwargs={'id_room': room.id})

        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser3')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/schedule_class.html')

        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertEqual(response.status_code, 200)


class AddGradesClassTest(TestCase):
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
        room = ClassRoom.objects.create(name='test room')
        classes_new = Classes.objects.create(educator=teacher, name='1a', description='test')
        Student.objects.create(year_of_birth=1988, classes=classes_new, user=test_user_2)
        subject_new = Subject(name='testSubject')
        subject_new.save()
        subject_new.classes.add(classes_new)
        subject_new.save()
        Lessons.objects.create(classes=classes_new, subject=subject_new, teacher=teacher)
        category_grade = GradeCategory.objects.create(name="test")

        test_user_4 = User.objects.create_user(username='testuser4',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing4',
                                               last_name='user4')
        test_user_4.profile.role = 2
        test_user_4.save()
        teacher2 = Teacher.objects.create(user=test_user_4)

    def test_redirect_if_not_logged_in(self):
        classes = Classes.objects.first()
        subject = Subject.objects.first()
        response = self.client.get(reverse("class-grade-add", kwargs={'id_class': classes.id, 'id_subject': subject.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next=/add_grades/{classes.id}/{subject.id}/')

    def test_logged_in_user_teacher(self):
        classes = Classes.objects.first()
        subject = Subject.objects.first()
        url = reverse("class-grade-add", kwargs={'id_class': classes.id, 'id_subject': subject.id})
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser3')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/detail_classes_add_grade.html')

    def test_logged_in_user_different_than_teacher(self):
        classes = Classes.objects.first()
        subject = Subject.objects.first()
        url = reverse("class-grade-add", kwargs={'id_class': classes.id, 'id_subject': subject.id})

        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser4', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

    def test_post_good_data_good_user(self):
        classes = Classes.objects.first()
        subject = Subject.objects.first()
        student = Student.objects.first()
        url = reverse("class-grade-add", kwargs={'id_class': classes.id, 'id_subject': subject.id})
        category_grade = GradeCategory.objects.first()
        data = {'category': category_grade.id, 'grade': 5, 'button': student.id}
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

    def test_post_bad_data_wrong_category_good_user(self):
        classes = Classes.objects.first()
        subject = Subject.objects.first()
        student = Student.objects.first()
        url = reverse("class-grade-add", kwargs={'id_class': classes.id, 'id_subject': subject.id})
        category_grade = GradeCategory.objects.first()
        data = {'category': 'bad', 'grade': 5, 'button': student.id}
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_post_bad_data_lack_button_good_user(self):
        classes = Classes.objects.first()
        subject = Subject.objects.first()
        student = Student.objects.first()
        url = reverse("class-grade-add", kwargs={'id_class': classes.id, 'id_subject': subject.id})
        category_grade = GradeCategory.objects.first()
        data = {'category': category_grade.id, 'grade': 5}
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)

    def test_post_good_data_bad_user(self):
        classes = Classes.objects.first()
        subject = Subject.objects.first()
        student = Student.objects.first()
        url = reverse("class-grade-add", kwargs={'id_class': classes.id, 'id_subject': subject.id})
        category_grade = GradeCategory.objects.first()
        data = {'category': category_grade.id, 'grade': 5, 'button': student.id}
        login = self.client.login(username='testuser4', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)


class PresenceViewTest(TestCase):
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
        room = ClassRoom.objects.create(name='test room')
        classes_new = Classes.objects.create(educator=teacher, name='1a', description='test')
        Student.objects.create(year_of_birth=1988, classes=classes_new, user=test_user_2)
        subject_new = Subject(name='testSubject')
        subject_new.save()
        subject_new.classes.add(classes_new)
        subject_new.save()
        lesson = Lessons.objects.create(classes=classes_new, subject=subject_new, teacher=teacher)
        category_grade = GradeCategory.objects.create(name="test")

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

        test_user_5 = User.objects.create_user(username='testuser5',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing5',
                                               last_name='user5')
        test_user_5.profile.role = 0
        test_user_5.save()
        Student.objects.create(year_of_birth=1988, classes=classes_new, user=test_user_5)

    def test_redirect_if_not_logged_in(self):
        classes = Classes.objects.first()
        schedule = Schedule.objects.first()
        response = self.client.get(reverse("class-presence-add", kwargs={'id_class': classes.id, 'id_schedule': schedule.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next=/add_presence/{classes.id}/{schedule.id}/')

    def test_logged_in_user_teacher(self):
        classes = Classes.objects.first()
        schedule = Schedule.objects.first()
        url = reverse("class-presence-add", kwargs={'id_class': classes.id, 'id_schedule': schedule.id})
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser3')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/presence_check.html')

    def test_logged_in_user_different_than_teacher(self):
        classes = Classes.objects.first()
        schedule = Schedule.objects.first()
        url = reverse("class-presence-add", kwargs={'id_class': classes.id, 'id_schedule': schedule.id})

        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser4', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

    def test_post_good_data_good_user(self):
        classes = Classes.objects.first()
        schedule = Schedule.objects.first()
        student = Student.objects.first()
        student_2 = Student.objects.last()
        url = reverse("class-presence-add", kwargs={'id_class': classes.id, 'id_schedule': schedule.id})
        category_grade = GradeCategory.objects.first()
        data = {'student': student.id, 'student': student_2.id}
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        url = reverse("class-presence-add", kwargs={'id_class': classes.id, 'id_schedule': schedule.id})
        category_grade = GradeCategory.objects.first()
        data = {'student': student.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

    def test_post_good_data_bad_user(self):
        classes = Classes.objects.first()
        schedule = Schedule.objects.first()
        student = Student.objects.first()
        url = reverse("class-presence-add", kwargs={'id_class': classes.id, 'id_schedule': schedule.id})
        category_grade = GradeCategory.objects.first()
        data = {'student': student.id}
        login = self.client.login(username='testuser4', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)


class AdvertAddViewTest(TestCase):
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

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("add-advert"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/add_advert/')

    def test_logged_in_user_teacher(self):
        url = reverse("add-advert")
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(url)
        form = response.context['form']
        self.assertEqual(str(response.context['user']), 'testuser3')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(form, AddAdvertForm)
        self.assertTemplateUsed(response, 'register/add_advert.html')

    def test_logged_in_user_different_than_teacher(self):
        url = reverse("add-advert")

        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

    def test_post_good_data(self):
        url = reverse("add-advert")
        data = {'title': 'test title', 'text': 'test content'}
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

    def test_post_bad_data(self):
        url = reverse("add-advert")
        data = {'title': 'test title'}
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


class AdvertEditViewTest(TestCase):
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
        Adverts.objects.create(text='test content', title='test title', author=test_user_3)

    def test_redirect_if_not_logged_in(self):
        advert = Adverts.objects.first()
        response = self.client.get(reverse("edit-advert", kwargs={'id_advert': advert.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next=/edit_advert/{advert.id}/')

    def test_logged_in_user_teacher(self):
        advert = Adverts.objects.first()
        url = reverse("edit-advert", kwargs={'id_advert': advert.id})
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(url)
        form = response.context['form']
        self.assertEqual(str(response.context['user']), 'testuser3')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(form, EditAdvertForm)
        self.assertTemplateUsed(response, 'register/add_advert.html')

    def test_logged_in_user_different_than_teacher(self):
        advert = Adverts.objects.first()
        url = reverse("edit-advert", kwargs={'id_advert': advert.id})

        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

    def test_post_good_data(self):
        advert = Adverts.objects.first()
        url = reverse("edit-advert", kwargs={'id_advert': advert.id})
        data = {'title': 'test title', 'text': 'test content', 'deleted': False}
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

    def test_post_bad_data(self):
        advert = Adverts.objects.first()
        url = reverse("edit-advert", kwargs={'id_advert': advert.id})
        data = {'title': 'test title'}
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


class AdvertClassAddViewTest(TestCase):
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
        classes = Classes.objects.first()
        response = self.client.get(reverse("add-advert-class", kwargs={'id_class': classes.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next=/add_advert_class/{classes.id}/')

    def test_logged_in_user_teacher(self):
        classes = Classes.objects.first()
        url = reverse("add-advert-class", kwargs={'id_class': classes.id})
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(url)
        form = response.context['form']
        self.assertEqual(str(response.context['user']), 'testuser3')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(form, AddClassAdvertForm)
        self.assertTemplateUsed(response, 'register/add_advert.html')

    def test_logged_in_user_different_than_teacher(self):
        classes = Classes.objects.first()
        url = reverse("add-advert-class", kwargs={'id_class': classes.id})

        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

    def test_post_good_data(self):
        classes = Classes.objects.first()
        url = reverse("add-advert-class", kwargs={'id_class': classes.id})
        data = {'title': 'test title', 'text': 'test content'}
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

    def test_post_bad_data(self):
        classes = Classes.objects.first()
        url = reverse("add-advert-class", kwargs={'id_class': classes.id})
        data = {'title': 'test title'}
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


class AdvertClassEditViewTest(TestCase):
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
        AdvertsClass.objects.create(text='test content',
                                    title='test title',
                                    author=teacher,
                                    classes=classes_new)

    def test_redirect_if_not_logged_in(self):
        advert = AdvertsClass.objects.first()
        response = self.client.get(reverse("edit-advert-class", kwargs={'id_advert': advert.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next=/edit_advert_class/{advert.id}/')

    def test_logged_in_user_teacher(self):
        advert = AdvertsClass.objects.first()
        url = reverse("edit-advert-class", kwargs={'id_advert': advert.id})
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(url)
        form = response.context['form']
        self.assertEqual(str(response.context['user']), 'testuser3')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(form, EditClassAdvertForm)
        self.assertTemplateUsed(response, 'register/add_advert.html')

    def test_logged_in_user_different_than_teacher(self):
        advert = AdvertsClass.objects.first()
        url = reverse("edit-advert-class", kwargs={'id_advert': advert.id})

        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

    def test_post_good_data(self):
        advert = AdvertsClass.objects.first()
        url = reverse("edit-advert-class", kwargs={'id_advert': advert.id})
        data = {'title': 'test title', 'text': 'test content', 'deleted': False}
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

    def test_post_bad_data(self):
        advert = AdvertsClass.objects.first()
        url = reverse("edit-advert-class", kwargs={'id_advert': advert.id})
        data = {'title': 'test title'}
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


class NoticeAddViewTest(TestCase):
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
        student = Student.objects.create(year_of_birth=1988, classes=classes_new, user=test_user_2)

    def test_redirect_if_not_logged_in(self):
        student = Student.objects.first()
        response = self.client.get(reverse("add-notice", kwargs={'id_student': student.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next=/add_notice/{student.id}/')

    def test_logged_in_user_teacher(self):
        student = Student.objects.first()
        url = reverse("add-notice", kwargs={'id_student': student.id})
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(url)
        form = response.context['form']
        self.assertEqual(str(response.context['user']), 'testuser3')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(form, AddNoticeForm)
        self.assertTemplateUsed(response, 'register/add_notice.html')

    def test_logged_in_user_different_than_teacher(self):
        student = Student.objects.first()
        url = reverse("add-notice", kwargs={'id_student': student.id})

        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

    def test_post_good_data(self):
        student = Student.objects.first()
        url = reverse("add-notice", kwargs={'id_student': student.id})
        data = {'text': 'test content'}
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

    def test_post_bad_data(self):
        student = Student.objects.first()
        url = reverse("add-notice", kwargs={'id_student': student.id})
        data = {}
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


class NoticeEditViewTest(TestCase):
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
        student = Student.objects.create(year_of_birth=1988, classes=classes_new, user=test_user_2)
        Notice.objects.create(text='test content', from_user=teacher, to_user=student, accepted=False)

    def test_redirect_if_not_logged_in(self):
        notice = Notice.objects.first()
        response = self.client.get(reverse("edit-notice", kwargs={'id_notice': notice.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next=/edit_notice/{notice.id}/')

    def test_logged_in_user_teacher(self):
        notice = Notice.objects.first()
        url = reverse("edit-notice", kwargs={'id_notice': notice.id})
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(url)
        form = response.context['form']
        self.assertEqual(str(response.context['user']), 'testuser3')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(form, EditNoticeForm)
        self.assertTemplateUsed(response, 'register/add_notice.html')

    def test_logged_in_user_different_than_teacher(self):
        notice = Notice.objects.first()
        url = reverse("edit-notice", kwargs={'id_notice': notice.id})

        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

    def test_post_good_data(self):
        notice = Notice.objects.first()
        url = reverse("edit-notice", kwargs={'id_notice': notice.id})
        data = {'text': 'test content', 'deleted': False}
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

    def test_post_bad_data(self):
        notice = Notice.objects.first()
        url = reverse("edit-notice", kwargs={'id_notice': notice.id})
        data = {}
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


class NoticeParentViewTest(TestCase):
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
        student = Student.objects.create(year_of_birth=1988, classes=classes_new, user=test_user_2)
        Notice.objects.create(text='test content', from_user=teacher, to_user=student, accepted=False)

    def test_redirect_if_not_logged_in(self):
        student = Student.objects.first()
        response = self.client.get(reverse("notices-parent", kwargs={'id_student': student.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next=/notices/{student.id}/')

    def test_logged_in_user_parent(self):
        student = Student.objects.first()
        url = reverse("notices-parent", kwargs={'id_student': student.id})
        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(url)
        form = response.context['form']
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(form, AnswerNoticeForm)
        self.assertTemplateUsed(response, 'register/notice_parent.html')

    def test_logged_in_user_different_than_parent(self):
        student = Student.objects.first()
        url = reverse("notices-parent", kwargs={'id_student': student.id})

        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

    def test_post_good_data(self):
        student = Student.objects.first()
        notice = Notice.objects.first()
        url = reverse("notices-parent", kwargs={'id_student': student.id})
        data = {'re_text': 'test content re', 'accepted': False, 'button': notice.id}
        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

    def test_post_bad_data(self):
        student = Student.objects.first()
        notice = Notice.objects.first()
        url = reverse("notices-parent", kwargs={'id_student': student.id})
        data = {'button': notice.id}
        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_post_bad_data_lack_button(self):
        student = Student.objects.first()
        notice = Notice.objects.first()
        url = reverse("notices-parent", kwargs={'id_student': student.id})
        data = {}
        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)


class NoticeParentEditViewTest(TestCase):
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
        student = Student.objects.create(year_of_birth=1988, classes=classes_new, user=test_user_2)
        Notice.objects.create(text='test content', from_user=teacher, to_user=student, accepted=False)

    def test_redirect_if_not_logged_in(self):
        notice = Notice.objects.first()
        response = self.client.get(reverse("notice-edit-parent", kwargs={'id_notice': notice.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next=/edit_notice_parent/{notice.id}/')

    def test_logged_in_user_parent(self):
        notice = Notice.objects.first()
        url = reverse("notice-edit-parent", kwargs={'id_notice': notice.id})
        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(url)
        form = response.context['form']
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(form, AnswerNoticeForm)
        self.assertTemplateUsed(response, 'register/add_notice.html')

    def test_logged_in_user_different_than_parent(self):
        notice = Notice.objects.first()
        url = reverse("notice-edit-parent", kwargs={'id_notice': notice.id})

        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

    def test_post_good_data(self):
        notice = Notice.objects.first()
        url = reverse("notice-edit-parent", kwargs={'id_notice': notice.id})
        data = {'re_text': 'test content re', 'accepted': False}
        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

    def test_post_bad_data(self):
        notice = Notice.objects.first()
        url = reverse("notice-edit-parent", kwargs={'id_notice': notice.id})
        data = {}
        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


class NoticeTeacherViewTest(TestCase):
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
        student = Student.objects.create(year_of_birth=1988, classes=classes_new, user=test_user_2)
        Notice.objects.create(text='test content', from_user=teacher, to_user=student, accepted=False)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("notices-teacher"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/teacher_notices/')

    def test_logged_in_user_teacher(self):
        url = reverse("notices-teacher")
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser3')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/notices_teacher.html')

    def test_logged_in_user_different_than_parent(self):
        url = reverse("notices-teacher")

        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)


class AdvertTeacherViewTest(TestCase):
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
        AdvertsClass.objects.create(text='test content',
                                    title='test title',
                                    author=teacher,
                                    classes=classes_new)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("adverts-teacher"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/teacher_adverts/')

    def test_logged_in_user_teacher(self):
        url = reverse("adverts-teacher")
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser3')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/advert_teacher.html')

    def test_logged_in_user_different_than_teacher(self):
        url = reverse("adverts-teacher")

        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)


class AnnouncementViewTest(TestCase):
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
        student = Student.objects.create(year_of_birth=1988, classes=classes_new, user=test_user_2)
        Announcements.objects.create(text='test content', user=test_user_2)
        Announcements.objects.create(text='test content 2', user=test_user_2)

        #second parent
        test_user_4 = User.objects.create_user(username='testuser4',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing4',
                                               last_name='user4')
        test_user_4.profile.role = 1
        test_user_4.save()
        parent2 = Parent.objects.create(user=test_user_4)

        test_user_5 = User.objects.create_user(username='testuser5',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing5',
                                               last_name='user5')
        test_user_5.profile.role = 0
        test_user_5.save()
        test_user_6 = User.objects.create_user(username='testuser6',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing6',
                                               last_name='user6')
        test_user_6.profile.role = 0
        test_user_6.save()
        student2 = Student.objects.create(year_of_birth=1988, classes=classes_new, user=test_user_5)
        student3 = Student.objects.create(year_of_birth=1988, classes=classes_new, user=test_user_6)
        parent2.students.add(student2, student3)
        parent2.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("announcements"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/announcements/')

    def test_logged_in_user_parent(self):
        url = reverse("announcements")
        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/announcements_list.html')

    def test_logged_in_user_parent_two_children(self):
        url = reverse("announcements")
        login = self.client.login(username='testuser4', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser4')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_different_than_parent(self):
        url = reverse("announcements")

        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

    def test_post_good_data(self):
        url = reverse("announcements")
        announcement = Announcements.objects.first()
        announcement2 = Announcements.objects.last()
        approved = f'read_{announcement.id}'
        approved_2 = f'deleted_{announcement2.id}'
        data = {'approved': approved}
        data2 = {'approved': approved_2}
        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, data2)
        self.assertEqual(response.status_code, 200)

    def test_post_bad_data(self):
        url = reverse("announcements")
        data = {}
        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)


class AnnouncementOnlineViewTest(TestCase):
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
        student = Student.objects.create(year_of_birth=1988, classes=classes_new, user=test_user_2)
        parent.students.add(student)
        parent.save()
        Announcements.objects.create(text='test content', user=test_user_2)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("counter"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/announcements_online/')

    def test_logged_in_user_parent(self):
        announcement = Announcements.objects.first()
        url = reverse("counter")
        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'1')

    def test_logged_in_user_different_than_parent(self):
        url = reverse("counter")

        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)


class AddEventViewTest(TestCase):
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
        student = Student.objects.create(year_of_birth=1988, classes=classes_new, user=test_user_2)
        parent.students.add(student)
        parent.save()
        subject_new = Subject(name='testSubject')
        subject_new.save()
        subject_new.classes.add(classes_new)
        subject_new.save()
        lesson = Lessons.objects.create(classes=classes_new, subject=subject_new, teacher=teacher)

        test_user_4 = User.objects.create_user(username='testuser4',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing4',
                                               last_name='user4')
        test_user_4.profile.role = 2
        test_user_4.save()
        teacher = Teacher.objects.create(user=test_user_4)

    def test_redirect_if_not_logged_in(self):
        lesson = Lessons.objects.first()
        response = self.client.get(reverse("add-event", kwargs={'id_lesson': lesson.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next=/add_events/{lesson.id}/')

    def test_logged_in_user_teacher(self):
        lesson = Lessons.objects.first()
        url = reverse("add-event", kwargs={'id_lesson': lesson.id})
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(url)
        form = response.context['form']
        self.assertIsInstance(form, AddEventForm)
        self.assertEqual(str(response.context['user']), 'testuser3')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/add_event.html')

    def test_logged_in_user_different_than_teacher(self):
        lesson = Lessons.objects.first()
        url = reverse("add-event", kwargs={'id_lesson': lesson.id})

        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser4', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

    def test_post_good_data_good_user(self):
        lesson = Lessons.objects.first()
        url = reverse("add-event", kwargs={'id_lesson': lesson.id})

        data = {'title': 'test title', 'text': 'test content', 'date_of_event': '2019-02-18'}
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

    def test_post_good_data_bad_user(self):
        lesson = Lessons.objects.first()
        url = reverse("add-event", kwargs={'id_lesson': lesson.id})

        data = {'title': 'test title', 'text': 'test content', 'date_of_event': '2019-02-18'}
        login = self.client.login(username='testuser4', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)

    def test_post_bad_data(self):
        lesson = Lessons.objects.first()
        url = reverse("add-event", kwargs={'id_lesson': lesson.id})
        data = {}
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


class EditEventViewTest(TestCase):
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
        student = Student.objects.create(year_of_birth=1988, classes=classes_new, user=test_user_2)
        parent.students.add(student)
        parent.save()
        subject_new = Subject(name='testSubject')
        subject_new.save()
        subject_new.classes.add(classes_new)
        subject_new.save()
        lesson = Lessons.objects.create(classes=classes_new, subject=subject_new, teacher=teacher)

        test_user_4 = User.objects.create_user(username='testuser4',
                                               email='a@a.com',
                                               password='testpassword',
                                               first_name='testing4',
                                               last_name='user4')
        test_user_4.profile.role = 2
        test_user_4.save()
        teacher = Teacher.objects.create(user=test_user_4)
        date_date = datetime(int(2019), int(2), int(4)).date()
        Event.objects.create(lesson=lesson, title='test title', text='test content', date_of_event=date_date)

    def test_redirect_if_not_logged_in(self):
        event = Event.objects.first()
        response = self.client.get(reverse("edit-event", kwargs={'id_event': event.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next=/edit_events/{event.id}/')

    def test_logged_in_user_teacher(self):
        event = Event.objects.first()
        url = reverse("edit-event", kwargs={'id_event': event.id})
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(url)
        form = response.context['form']
        self.assertIsInstance(form, AddEventForm)
        self.assertEqual(str(response.context['user']), 'testuser3')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/add_event.html')

    def test_logged_in_user_different_than_teacher(self):
        event = Event.objects.first()
        url = reverse("edit-event", kwargs={'id_event': event.id})

        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser4', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

    def test_post_good_data_good_user(self):
        event = Event.objects.first()
        url = reverse("edit-event", kwargs={'id_event': event.id})

        data = {'title': 'test title', 'text': 'test content', 'date_of_event': '2019-02-18'}
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

    def test_post_good_data_bad_user(self):
        event = Event.objects.first()
        url = reverse("edit-event", kwargs={'id_event': event.id})

        data = {'title': 'test title', 'text': 'test content', 'date_of_event': '2019-02-18'}
        login = self.client.login(username='testuser4', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)

    def test_post_bad_data(self):
        event = Event.objects.first()
        url = reverse("edit-event", kwargs={'id_event': event.id})
        data = {}
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


class ListEventViewTest(TestCase):
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
        student = Student.objects.create(year_of_birth=1988, classes=classes_new, user=test_user_2)
        parent.students.add(student)
        parent.save()
        subject_new = Subject(name='testSubject')
        subject_new.save()
        subject_new.classes.add(classes_new)
        subject_new.save()
        lesson = Lessons.objects.create(classes=classes_new, subject=subject_new, teacher=teacher)
        date_date = datetime(int(2019), int(2), int(4)).date()
        Event.objects.create(lesson=lesson, title='test title', text='test content', date_of_event=date_date)

    def test_redirect_if_not_logged_in(self):
        classes = Classes.objects.first()
        response = self.client.get(reverse("list-event", kwargs={'id_classes': classes.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next=/list_events/{classes.id}/')

    def test_logged_in_user_teacher(self):
        classes = Classes.objects.first()
        url = reverse("list-event", kwargs={'id_classes': classes.id})
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser3')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/events_list.html')

    def test_logged_in_user_different_than_teacher(self):
        classes = Classes.objects.first()
        url = reverse("list-event", kwargs={'id_classes': classes.id})

        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_bad_class_id(self):
        url = reverse("list-event", kwargs={'id_classes': 123465798})

        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class ListEventTeacherViewTest(TestCase):
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
        student = Student.objects.create(year_of_birth=1988, classes=classes_new, user=test_user_2)
        parent.students.add(student)
        parent.save()
        subject_new = Subject(name='testSubject')
        subject_new.save()
        subject_new.classes.add(classes_new)
        subject_new.save()
        lesson = Lessons.objects.create(classes=classes_new, subject=subject_new, teacher=teacher)
        date_date = datetime(int(2019), int(2), int(4)).date()
        Event.objects.create(lesson=lesson, title='test title', text='test content', date_of_event=date_date)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("list-teacher-event"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/list_events_teacher/')

    def test_logged_in_user_teacher(self):
        url = reverse("list-teacher-event")
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(str(response.context['user']), 'testuser3')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/events_list.html')

    def test_logged_in_user_different_than_teacher(self):
        url = reverse("list-teacher-event")

        login = self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)

        login = self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 403)
