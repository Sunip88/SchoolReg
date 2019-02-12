from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from register.models import Teacher, Classes, Parent, Student, Subject, Lessons, ClassRoom, WorkingHours, Schedule, \
    Grades, GradeCategory


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

    def test_post_bad_data_good_user(self):
        classes = Classes.objects.first()
        subject = Subject.objects.first()
        student = Student.objects.first()
        url = reverse("class-grade-add", kwargs={'id_class': classes.id, 'id_subject': subject.id})
        category_grade = GradeCategory.objects.first()
        data = {'category': 'bad', 'grade': 5, 'button': student.id}
        login = self.client.login(username='testuser3', password='testpassword')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

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
