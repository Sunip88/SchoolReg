from PIL import Image
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from datetime import datetime
from register.models import Subject, Teacher, Classes, Student, Parent, GradeCategory, Grades, Lessons, ClassRoom, \
    WorkingHours, Schedule, PresenceList, Adverts, AdvertsClass, Notice, Announcements, Event
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
        classes = Classes.objects.all().first()
        field_label = classes._meta.get_field('educator').verbose_name
        self.assertEqual(field_label, 'educator')

    def test_name_label(self):
        classes = Classes.objects.all().first()
        field_label = classes._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_description_label(self):
        classes = Classes.objects.all().first()
        field_label = classes._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_name_max_lenght(self):
        classes = Classes.objects.all().first()
        max_length = classes._meta.get_field('name').max_length
        self.assertEqual(max_length, 32)

    def test_description_max_lenght(self):
        classes = Classes.objects.all().first()
        max_length = classes._meta.get_field('description').max_length
        self.assertEqual(max_length, 512)

    def test_object_name_is_name(self):
        classes = Classes.objects.all().first()
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
        subject = Subject.objects.all().first()
        field_label = subject._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_classes_label(self):
        subject = Subject.objects.all().first()
        field_label = subject._meta.get_field('classes').verbose_name
        self.assertEqual(field_label, 'classes')

    def test_name_max_lenght(self):
        subject = Subject.objects.all().first()
        max_length = subject._meta.get_field('name').max_length
        self.assertEqual(max_length, 128)

    def test_object_name_is_name(self):
        subject = Subject.objects.all().first()
        expected_object_name = f'{subject.name}'
        self.assertEqual(expected_object_name, str(subject))


class TeacherModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser',
                                   email='a@a.com',
                                   password='testpassword',
                                   first_name='testing',
                                   last_name='user')
        user.profile.role = 2
        teacher = Teacher.objects.create(user=user)

    def test_user_label(self):
        teacher = Teacher.objects.all().first()
        field_label = teacher._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_object_name_is_user_first_name_space_user_last_name(self):
        teacher = Teacher.objects.all().first()
        expected_object_name = f'{teacher.user.first_name} {teacher.user.last_name}'
        self.assertEqual(expected_object_name, str(teacher))


class StudentModelTest(TestCase):
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
        user2 = User.objects.create(username='testuser_student',
                                   email='a@a.com',
                                   password='testpassword',
                                   first_name='testing_student',
                                   last_name='user_student')
        user2.profile.role = 0
        student = Student.objects.create(year_of_birth=2000, classes=classes_new, user=user2)

    def test_year_of_birth_label(self):
        student = Student.objects.all().first()
        field_label = student._meta.get_field('year_of_birth').verbose_name
        self.assertEqual(field_label, 'year of birth')

    def test_classes_label(self):
        student = Student.objects.all().first()
        field_label = student._meta.get_field('classes').verbose_name
        self.assertEqual(field_label, 'classes')

    def test_user_label(self):
        student = Student.objects.all().first()
        field_label = student._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_object_name_is_user_first_name_space_user_last_name(self):
        student = Student.objects.all().first()
        expected_object_name = f'{student.user.first_name} {student.user.last_name}'
        self.assertEqual(expected_object_name, str(student))


class ParentModelTest(TestCase):
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
        user2 = User.objects.create(username='testuser_student',
                                    email='a@a.com',
                                    password='testpassword',
                                    first_name='testing_student',
                                    last_name='user_student')
        user2.profile.role = 0
        student = Student.objects.create(year_of_birth=2000, classes=classes_new, user=user2)
        user3 = User.objects.create(username='testuser_parent',
                                    email='a@a.com',
                                    password='testpassword',
                                    first_name='testing_parent',
                                    last_name='user_parent')
        parent = Parent.objects.create(user=user3)
        parent.students.add(student)
        parent.save()

    def test_user_label(self):
        parent = Parent.objects.all().first()
        field_label = parent._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_students_label(self):
        parent = Parent.objects.all().first()
        field_label = parent._meta.get_field('students').verbose_name
        self.assertEqual(field_label, 'students')

    def test_object_name_is_user_first_name_space_user_last_name(self):
        parent = Parent.objects.all().first()
        expected_object_name = f'{parent.user.first_name} {parent.user.last_name}'
        self.assertEqual(expected_object_name, str(parent))


class GradeCategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        GradeCategory.objects.create(name='test')

    def test_name_label(self):
        grade_category = GradeCategory.objects.all().first()
        field_label = grade_category._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_object_name_is_name(self):
        grade_category = GradeCategory.objects.all().first()
        expected_object_name = f'{grade_category.name}'
        self.assertEqual(expected_object_name, str(grade_category))


class GradesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = GradeCategory.objects.create(name='test')
        user = User.objects.create(username='testuser',
                                   email='a@a.com',
                                   password='testpassword',
                                   first_name='testing',
                                   last_name='user')
        user.profile.role = 2
        teacher = Teacher.objects.create(user=user)
        classes_new = Classes.objects.create(educator=teacher, name='1a', description='test')
        user2 = User.objects.create(username='testuser_student',
                                    email='a@a.com',
                                    password='testpassword',
                                    first_name='testing_student',
                                    last_name='user_student')
        user2.profile.role = 0
        student = Student.objects.create(year_of_birth=2000, classes=classes_new, user=user2)
        subject = Subject.objects.create(name='testSubject')
        subject.classes.add(classes_new)
        subject.save()
        Grades.objects.create(subject=subject, student=student, category=category, grade=3.25)

    def test_subject_label(self):
        grade = Grades.objects.all().first()
        field_label = grade._meta.get_field('subject').verbose_name
        self.assertEqual(field_label, 'subject')

    def test_student_label(self):
        grade = Grades.objects.all().first()
        field_label = grade._meta.get_field('student').verbose_name
        self.assertEqual(field_label, 'student')

    def test_category_label(self):
        grade = Grades.objects.all().first()
        field_label = grade._meta.get_field('category').verbose_name
        self.assertEqual(field_label, 'category')

    def test_grade_label(self):
        grade = Grades.objects.all().first()
        field_label = grade._meta.get_field('grade').verbose_name
        self.assertEqual(field_label, 'grade')

    def test_object_name_is_subject_student_grade(self):
        grade = Grades.objects.all().first()
        expected_object_name = f'{grade.subject.name} - {grade.student.user.first_name} {grade.student.user.last_name} - {grade.grade}'
        self.assertEqual(expected_object_name, str(grade))


class PresenceListModelTest(TestCase):
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
        user2 = User.objects.create(username='testuser_student',
                                    email='a@a.com',
                                    password='testpassword',
                                    first_name='testing_student',
                                    last_name='user_student')
        user2.profile.role = 0
        student = Student.objects.create(year_of_birth=2000, classes=classes_new, user=user2)
        subject = Subject.objects.create(name='testSubject')
        subject.classes.add(classes_new)
        subject.save()
        lesson = Lessons.objects.create(classes=classes_new, subject=subject, teacher=teacher)
        room = ClassRoom.objects.create(name="testRoom")
        time_s = datetime.strptime('8:00', '%H:%M').time()
        time_e = datetime.strptime('8:45', '%H:%M').time()
        hours = WorkingHours.objects.create(nr=1, start_time=time_s, end_time=time_e)
        schedule = Schedule.objects.create(lesson=lesson, room=room, hours=hours, weekday=1)
        date_date = datetime(int(2019), int(2), int(4)).date()
        PresenceList.objects.create(student=student, present=True, schedule=schedule, day=date_date)

    def test_day_label(self):
        presence = PresenceList.objects.all().first()
        field_label = presence._meta.get_field('day').verbose_name
        self.assertEqual(field_label, 'day')

    def test_student_label(self):
        presence = PresenceList.objects.all().first()
        field_label = presence._meta.get_field('student').verbose_name
        self.assertEqual(field_label, 'student')

    def test_present_label(self):
        presence = PresenceList.objects.all().first()
        field_label = presence._meta.get_field('present').verbose_name
        self.assertEqual(field_label, 'present')

    def test_grade_label(self):
        presence = PresenceList.objects.all().first()
        field_label = presence._meta.get_field('schedule').verbose_name
        self.assertEqual(field_label, 'schedule')

    def test_object_name_is_subject_student_grade(self):
        presence = PresenceList.objects.all().first()
        expected_object_name = f'{presence.student.user.first_name} {presence.student.user.last_name} - {presence.day} - {presence.present}'
        self.assertEqual(expected_object_name, str(presence))


class ClassRoomModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ClassRoom.objects.create(name='testRoom')

    def test_name_label(self):
        class_room = ClassRoom.objects.all().first()
        field_label = class_room._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_object_name_is_name(self):
        class_room = ClassRoom.objects.all().first()
        expected_object_name = f'{class_room.name}'
        self.assertEqual(expected_object_name, str(class_room))


class WorkingHoursModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        time_s = datetime.strptime('8:50', '%H:%M').time()
        time_e = datetime.strptime('9:35', '%H:%M').time()
        hours = WorkingHours.objects.create(nr=2, start_time=time_s, end_time=time_e)

    def test_nr_label(self):
        working_hours = WorkingHours.objects.all().first()
        field_label = working_hours._meta.get_field('nr').verbose_name
        self.assertEqual(field_label, 'nr')

    def test_start_time_label(self):
        working_hours = WorkingHours.objects.all().first()
        field_label = working_hours._meta.get_field('start_time').verbose_name
        self.assertEqual(field_label, 'start time')

    def test_end_time_label(self):
        working_hours = WorkingHours.objects.all().first()
        field_label = working_hours._meta.get_field('end_time').verbose_name
        self.assertEqual(field_label, 'end time')

    def test_object_name_is_name(self):
        working_hours = WorkingHours.objects.all().first()
        expected_object_name = f'{working_hours.start_time} - {working_hours.end_time}'
        self.assertEqual(expected_object_name, str(working_hours))


class LessonsModelTest(TestCase):
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
        lesson = Lessons.objects.create(classes=classes_new, subject=subject, teacher=teacher)

    def test_classes_label(self):
        lesson = Lessons.objects.all().first()
        field_label = lesson._meta.get_field('classes').verbose_name
        self.assertEqual(field_label, 'classes')

    def test_subject_label(self):
        lesson = Lessons.objects.all().first()
        field_label = lesson._meta.get_field('subject').verbose_name
        self.assertEqual(field_label, 'subject')

    def test_teacher_label(self):
        lesson = Lessons.objects.all().first()
        field_label = lesson._meta.get_field('teacher').verbose_name
        self.assertEqual(field_label, 'teacher')

    def test_object_name_is_subject_student_grade(self):
        lesson = Lessons.objects.all().first()
        expected_object_name = f'{lesson.classes.name} - {lesson.subject.name} - {lesson.teacher.user.last_name}'
        self.assertEqual(expected_object_name, str(lesson))


class ScheduleModelTest(TestCase):
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
        lesson = Lessons.objects.create(classes=classes_new, subject=subject, teacher=teacher)
        room = ClassRoom.objects.create(name="testRoom")
        time_s = datetime.strptime('8:00', '%H:%M').time()
        time_e = datetime.strptime('8:45', '%H:%M').time()
        hours = WorkingHours.objects.create(nr=1, start_time=time_s, end_time=time_e)
        schedule = Schedule.objects.create(lesson=lesson, room=room, hours=hours, weekday=1)

    def test_lesson_label(self):
        schedule = Schedule.objects.all().first()
        field_label = schedule._meta.get_field('lesson').verbose_name
        self.assertEqual(field_label, 'lesson')

    def test_room_label(self):
        schedule = Schedule.objects.all().first()
        field_label = schedule._meta.get_field('room').verbose_name
        self.assertEqual(field_label, 'room')

    def test_hours_label(self):
        schedule = Schedule.objects.all().first()
        field_label = schedule._meta.get_field('hours').verbose_name
        self.assertEqual(field_label, 'hours')

    def test_weekday_label(self):
        schedule = Schedule.objects.all().first()
        field_label = schedule._meta.get_field('weekday').verbose_name
        self.assertEqual(field_label, 'weekday')

    def test_object_name_is_subject_student_grade(self):
        schedule = Schedule.objects.all().first()
        expected_object_name = f'{schedule.lesson.classes.name} - {schedule.lesson.subject.name} - {schedule.lesson.teacher.user.last_name} - {schedule.room.name}'
        self.assertEqual(expected_object_name, str(schedule))


class AdvertsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser',
                                   email='a@a.com',
                                   password='testpassword',
                                   first_name='testing',
                                   last_name='user')
        user.profile.role = 2
        Adverts.objects.create(text="testing text field",
                               title='Title of test object',
                               author=user)

    def test_text_label(self):
        adverts = Adverts.objects.all().first()
        field_label = adverts._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'text')

    def test_title_label(self):
        adverts = Adverts.objects.all().first()
        field_label = adverts._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_date_label(self):
        adverts = Adverts.objects.all().first()
        field_label = adverts._meta.get_field('date').verbose_name
        self.assertEqual(field_label, 'date')

    def test_author_label(self):
        adverts = Adverts.objects.all().first()
        field_label = adverts._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_deleted_label(self):
        adverts = Adverts.objects.all().first()
        field_label = adverts._meta.get_field('deleted').verbose_name
        self.assertEqual(field_label, 'deleted')

    def test_name_max_lenght(self):
        adverts = Adverts.objects.all().first()
        max_length = adverts._meta.get_field('title').max_length
        self.assertEqual(max_length, 64)


class AdvertsClassModelTest(TestCase):
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
        AdvertsClass.objects.create(text="testing text field",
                                    title='Title of test object',
                                    author=teacher,
                                    classes=classes_new)

    def test_text_label(self):
        adverts = AdvertsClass.objects.all().first()
        field_label = adverts._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'text')

    def test_title_label(self):
        adverts = AdvertsClass.objects.all().first()
        field_label = adverts._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_date_label(self):
        adverts = AdvertsClass.objects.all().first()
        field_label = adverts._meta.get_field('date').verbose_name
        self.assertEqual(field_label, 'date')

    def test_author_label(self):
        adverts = AdvertsClass.objects.all().first()
        field_label = adverts._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_deleted_label(self):
        adverts = AdvertsClass.objects.all().first()
        field_label = adverts._meta.get_field('deleted').verbose_name
        self.assertEqual(field_label, 'deleted')

    def test_classes_label(self):
        adverts = AdvertsClass.objects.all().first()
        field_label = adverts._meta.get_field('classes').verbose_name
        self.assertEqual(field_label, 'classes')

    def test_title_max_lenght(self):
        adverts = AdvertsClass.objects.all().first()
        max_length = adverts._meta.get_field('title').max_length
        self.assertEqual(max_length, 64)


class NoticeModelTest(TestCase):
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
        user2 = User.objects.create(username='testuser_student',
                                    email='a@a.com',
                                    password='testpassword',
                                    first_name='testing_student',
                                    last_name='user_student')
        user2.profile.role = 0
        student = Student.objects.create(year_of_birth=2000, classes=classes_new, user=user2)
        Notice.objects.create(text="testing text field",
                              from_user=teacher,
                              to_user=student,
                              accepted=False)

    def test_text_label(self):
        notice = Notice.objects.all().first()
        field_label = notice._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'text')

    def test_from_user_label(self):
        notice = Notice.objects.all().first()
        field_label = notice._meta.get_field('from_user').verbose_name
        self.assertEqual(field_label, 'from user')

    def test_to_user_label(self):
        notice = Notice.objects.all().first()
        field_label = notice._meta.get_field('to_user').verbose_name
        self.assertEqual(field_label, 'to user')

    def test_accepted_label(self):
        notice = Notice.objects.all().first()
        field_label = notice._meta.get_field('accepted').verbose_name
        self.assertEqual(field_label, 'accepted')

    def test_re_text_label(self):
        notice = Notice.objects.all().first()
        field_label = notice._meta.get_field('re_text').verbose_name
        self.assertEqual(field_label, 're text')

    def test_date_label(self):
        notice = Notice.objects.all().first()
        field_label = notice._meta.get_field('date').verbose_name
        self.assertEqual(field_label, 'date')

    def test_deleted_label(self):
        notice = Notice.objects.all().first()
        field_label = notice._meta.get_field('deleted').verbose_name
        self.assertEqual(field_label, 'deleted')

    def test_text_max_lenght(self):
        notice = Notice.objects.all().first()
        max_length = notice._meta.get_field('text').max_length
        self.assertEqual(max_length, 256)

    def test_re_text_max_lenght(self):
        notice = Notice.objects.all().first()
        max_length = notice._meta.get_field('re_text').max_length
        self.assertEqual(max_length, 256)


class AnnouncementsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser',
                                   email='a@a.com',
                                   password='testpassword',
                                   first_name='testing',
                                   last_name='user')
        user.profile.role = 2
        Announcements.objects.create(text="testing text field",
                                     user=user)

    def test_text_label(self):
        announcement = Announcements.objects.all().first()
        field_label = announcement._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'text')

    def test_user_label(self):
        announcement = Announcements.objects.all().first()
        field_label = announcement._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_date_label(self):
        announcement = Announcements.objects.all().first()
        field_label = announcement._meta.get_field('date').verbose_name
        self.assertEqual(field_label, 'date')

    def test_read_label(self):
        announcement = Announcements.objects.all().first()
        field_label = announcement._meta.get_field('read').verbose_name
        self.assertEqual(field_label, 'read')

    def test_deleted_label(self):
        announcement = Announcements.objects.all().first()
        field_label = announcement._meta.get_field('deleted').verbose_name
        self.assertEqual(field_label, 'deleted')


class EventModelTest(TestCase):
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
        lesson = Lessons.objects.create(classes=classes_new, subject=subject, teacher=teacher)
        date_date = datetime(int(2019), int(2), int(4)).date()
        Event.objects.create(lesson=lesson, date_of_event=date_date, title="Title test", text="testing context")

    def test_lesson_label(self):
        event = Event.objects.all().first()
        field_label = event._meta.get_field('lesson').verbose_name
        self.assertEqual(field_label, 'lesson')

    def test_date_set_label(self):
        event = Event.objects.all().first()
        field_label = event._meta.get_field('date_set').verbose_name
        self.assertEqual(field_label, 'date set')

    def test_date_of_event_label(self):
        event = Event.objects.all().first()
        field_label = event._meta.get_field('date_of_event').verbose_name
        self.assertEqual(field_label, 'date of event')

    def test_title_label(self):
        event = Event.objects.all().first()
        field_label = event._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_text_label(self):
        event = Event.objects.all().first()
        field_label = event._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'text')

    def test_deleted_label(self):
        event = Event.objects.all().first()
        field_label = event._meta.get_field('deleted').verbose_name
        self.assertEqual(field_label, 'deleted')


class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser',
                                   email='a@a.com',
                                   password='testpassword',
                                   first_name='testing',
                                   last_name='user')
        user.profile.role = 2

    def test_user_label(self):
        profile = Profile.objects.all().first()
        field_label = profile._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_image_label(self):
        profile = Profile.objects.all().first()
        field_label = profile._meta.get_field('image').verbose_name
        self.assertEqual(field_label, 'image')

    def test_role_label(self):
        profile = Profile.objects.all().first()
        field_label = profile._meta.get_field('role').verbose_name
        self.assertEqual(field_label, 'role')

    def test_temp_password_label(self):
        profile = Profile.objects.all().first()
        field_label = profile._meta.get_field('temp_password').verbose_name
        self.assertEqual(field_label, 'temp password')

    def test_phone_label(self):
        profile = Profile.objects.all().first()
        field_label = profile._meta.get_field('phone').verbose_name
        self.assertEqual(field_label, 'phone')

    def test_temp_password_max_lenght(self):
        profile = Profile.objects.all().first()
        max_length = profile._meta.get_field('temp_password').max_length
        self.assertEqual(max_length, 32)

    def test_object_name_is_user_first_last_name(self):
        profile = Profile.objects.all().first()
        expected_object_name = f'{profile.user.first_name}, {profile.user.last_name} Profile'
        self.assertEqual(expected_object_name, str(profile))

    def test_image_size(self):
        profile = Profile.objects.all().first()
        img = Image.open(profile.image.path)
        self.assertEqual(img.height, 300)
        self.assertEqual(img.width, 300)
