from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from .forms import AddGradeForm, AddAdvertForm, AddNoticeForm, AnswerNoticeForm, AddClassAdvertForm, \
    EditAdvertForm, EditClassAdvertForm, EditNoticeForm, AddEventForm
from .models import Classes, Subject, Student, GradeCategory, Teacher, PresenceList, WorkingHours, Schedule, WEEKDAYS, \
    ClassRoom, Adverts, Parent, Notice, AdvertsClass, Announcements, Event, Lessons
from django.contrib import messages

weekdays = [
    (0, 'Nr'),
    (0, 'Godz'),
    (1, 'Poniedziałek'),
    (2, 'Wtorek'),
    (3, 'Środa'),
    (4, 'Czwartek'),
    (5, 'Piątek'),
]


def testing_func(user, role):
    if user.profile.role == role:
        return True
    return False


class MainView(LoginRequiredMixin, ListView):
    model = Adverts
    paginate_by = 10
    ordering = ['-date']
    template_name = 'register/main.html'


class TeacherPanelView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request):
        teacher = Teacher.objects.get(user_id=self.request.user.id)
        educator = teacher.classes_set.all()
        if educator:
            educator = educator.first()
        return render(request, 'register/teacher_view.html', {"teacher": teacher, "educator": educator})

    def test_func(self):
        return testing_func(self.request.user, 2)


class ParentPanelView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request):
        parent = Parent.objects.get(user_id=self.request.user.id)
        children = parent.students.all()
        ctx = {"parent": parent, "children": children}
        return render(request, 'register/parent_view.html', ctx)

    def test_func(self):
        return testing_func(self.request.user, 1)


class TeacherSubjectsClassesView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request):
        teacher = Teacher.objects.get(user_id=request.user.id)
        weekday_now = datetime.now().weekday()
        schedule_all = Schedule.objects.filter(lesson__teacher=teacher)
        schedule_now = schedule_all.filter(weekday=weekday_now + 1)
        subjects = []
        temp = []
        if schedule_all:
            for item in schedule_all:
                i = str(item.lesson.subject) + str(item.lesson.classes.name)
                if i not in temp:
                    subjects.append(item)
                    temp.append(str(item.lesson.subject) + str(item.lesson.classes.name))
        else:
            subjects = []
        ctx = {'teacher': teacher, 'subjects': subjects, 'schedule': schedule_all, 'weekday_now': weekday_now,
               'schedule_now': schedule_now}
        return render(request, 'register/teacher_class_subject.html', ctx)

    def test_func(self):
        return testing_func(self.request.user, 2)


class TeacherGradesView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, subject_id, class_id):
        subject = get_object_or_404(Subject, id=subject_id)
        student_class = get_object_or_404(Classes, id=class_id)
        students = student_class.student_set.all()
        categories = GradeCategory.objects.all()
        ctx = {'subject': subject,
               'student_class': student_class,
               'students': students,
               'categories': categories,
               'class_id': class_id}
        return render(request, 'register/teacher_class_grades.html', ctx)

    def test_func(self):
        return testing_func(self.request.user, 2)


class StudentView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request):
        student = Student.objects.get(user_id=self.request.user.id)
        student_class = student.classes
        ctx = {'student': student, 'student_class': student_class}
        return render(request, 'register/student_view.html', ctx)

    def test_func(self):
        return testing_func(self.request.user, 0)


class ClassView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Classes
    paginate_by = 25
    template_name = 'register/classes.html'
    ordering = ['educator']

    def test_func(self):
        return testing_func(self.request.user, 2)


class AddClassView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):  # delete?
    permission_required = 'register.add_classes'
    model = Classes
    fields = '__all__'
    template_name = 'register/add_class.html'
    success_url = reverse_lazy("class-view")


class EditClassView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):  # delete?
    permission_required = 'register.change_classes'
    model = Classes
    fields = '__all__'
    template_name = 'register/add_class.html'
    success_url = reverse_lazy("class-view")


class DetailsClassView(LoginRequiredMixin, View):
    def get(self, request, pk):
        adverts = AdvertsClass.objects.filter(classes_id=pk)
        detail_class = get_object_or_404(Classes, id=pk)
        students = detail_class.student_set.all()
        if not self.my_test(detail_class):
            raise PermissionDenied
        ctx = {'students': students, 'detail_class': detail_class, 'adverts': adverts}
        return render(request, 'register/detail_classes.html', ctx)

    def my_test(self, detail_class):
        user = self.request.user
        role = user.profile.role
        if role == 2:
            return True
        elif role == 0:
            if user.student in detail_class.student_set.all():
                return True
            else:
                return False
        else:
            children = user.parent.students.all()
            if children:
                for child in children:
                    if child in detail_class.student_set.all():
                        return True
            return False


class AddGradeCategoryView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = GradeCategory
    fields = '__all__'
    template_name = 'register/add_class.html'
    success_url = reverse_lazy("add-grade-category")

    def test_func(self):
        return testing_func(self.request.user, 2)


class AddGradesClass(LoginRequiredMixin, UserPassesTestMixin, View):
    class_form = AddGradeForm

    def get(self, request, id_class, id_subject):
        detail_class = get_object_or_404(Classes, id=id_class)
        students = Student.objects.filter(classes_id=detail_class.id)
        subject = get_object_or_404(Subject, id=id_subject)
        if not self.my_test(subject, detail_class):
            raise PermissionDenied
        form = self.class_form()
        ctx = {'detail_class': detail_class, 'students': students, 'subject': subject, 'form': form}
        return render(request, 'register/detail_classes_add_grade.html', ctx)

    def post(self, request, id_class, id_subject):
        form = self.class_form(request.POST)
        detail_class = get_object_or_404(Classes, id=id_class)
        students = Student.objects.filter(classes_id=detail_class.id)
        subject = get_object_or_404(Subject, id=id_subject)
        if not self.my_test(subject, detail_class):
            raise PermissionDenied
        ctx = {'detail_class': detail_class, 'students': students, 'subject': subject, 'form': form}
        if form.is_valid():
            button = request.POST.get('button')
            student = get_object_or_404(Student, id=button)
            new_grade = form.save(commit=False)
            new_grade.subject = subject
            new_grade.student = student
            new_grade.save()
            name = student.user.first_name
            surname = student.user.last_name
            text = f'''Uczen {name} {surname} otrzymal {new_grade.grade} z {new_grade.subject}.'''
            Announcements.objects.create(text=text, user=student.user)
            messages.success(request, 'Dodano ocenę')
            return redirect('class-grade-add', id_class=id_class, id_subject=id_subject)
        return render(request, 'register/detail_classes_add_grade.html', ctx)

    def test_func(self):
        return testing_func(self.request.user, 2)

    def my_test(self, subject, classes):
        teacher = Lessons.objects.filter(classes=classes, subject=subject)
        if teacher:
            teacher = teacher.first().teacher
            if self.request.user.teacher == teacher:
                return True
        return False


class TeacherDetailView(LoginRequiredMixin, DetailView):
    model = Teacher
    template_name = 'register/teacher_details.html'


class StudentDetailView(LoginRequiredMixin, View):

    def get(self, request, pk):
        student = get_object_or_404(Student, id=pk)
        if not self.my_test(student):
            raise PermissionDenied
        grades = student.grades_set.all()
        date_now = datetime.now()
        date_four_weeks = date_now - timedelta(weeks=4)
        presence = PresenceList.objects.filter(student=student, day__gte=date_four_weeks)
        subjects_all = student.classes.subject_set.all()
        subjects = {}
        for g in grades:
            if g.subject.id not in subjects.keys():
                subjects[g.subject.id] = g.subject.name
        ctx = {'student': student, 'grades': grades, 'subjects': subjects, 'presence_list': presence,
               'subject_all': subjects_all}
        return render(request, 'register/student_details.html', ctx)

    def my_test(self, student):
        user = self.request.user
        role = user.profile.role
        if role == 2:
            return True
        elif role == 0:
            if user.student == student:
                return True
            else:
                return False
        else:
            children = user.parent.students.all()
            if children:
                for child in children:
                    if child == student:
                        return True
            return False


class PresenceView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request, id_class, id_schedule):
        detail_class = get_object_or_404(Classes, id=id_class)
        students = Student.objects.filter(classes_id=detail_class.id)
        schedule = get_object_or_404(Schedule, id=id_schedule)
        today = datetime.now().strftime('%Y-%m-%d')
        if not self.my_test(schedule.lesson):
            raise PermissionDenied
        ctx = {'detail_class': detail_class, 'students': students, 'today': today, 'schedule': schedule}
        return render(request, 'register/presence_check.html', ctx)

    def post(self, request, id_class, id_schedule):
        detail_class = get_object_or_404(Classes, id=id_class)
        schedule = get_object_or_404(Schedule, id=id_schedule)
        if not self.my_test(schedule.lesson):
            raise PermissionDenied
        students = Student.objects.filter(classes_id=detail_class.id)
        today = datetime.now()
        date_formated = today.strftime('%Y-%m-%d')
        day = today.date()
        student_presence_str = request.POST.getlist('student')
        student_presence = [int(i) for i in student_presence_str]
        for student in students:
            presence = PresenceList.objects.filter(student=student,
                                                   day=day,
                                                   schedule=schedule)
            if student.id in student_presence:
                if len(presence) > 0:
                    presence = presence.first()
                    presence.present = True
                    presence.save()
                else:
                    PresenceList.objects.create(student=student,
                                                day=day,
                                                schedule=schedule,
                                                present=True)
            else:
                name = student.user.first_name
                surname = student.user.last_name
                text = f"{name} {surname} był nieobecny na {schedule.lesson.subject.name} w dniu {date_formated}"
                if len(presence) > 0:
                    presence = presence.first()
                    if presence.present:
                        Announcements.objects.create(text=text,
                                                     user=student.user)
                    presence.present = False
                    presence.save()
                else:
                    PresenceList.objects.create(student=student,
                                                day=day,
                                                schedule=schedule,
                                                present=False)
                    Announcements.objects.create(text=text,
                                                 user=student.user)

        messages.success(request, 'Zaktualizowano obecności')
        return redirect('class-presence-add', id_class=id_class, id_schedule=id_schedule)

    def test_func(self):
        return testing_func(self.request.user, 2)

    def my_test(self, lesson):
        if self.request.user.teacher == lesson.teacher:
            return True
        return False


class SchedulesView(LoginRequiredMixin, View):

    def get(self, request):
        teachers = Teacher.objects.all()
        classes = Classes.objects.all()
        rooms = ClassRoom.objects.all()
        ctx = {'teachers': teachers, 'classes': classes, 'rooms': rooms}
        return render(request, 'register/schedules.html', ctx)


class ScheduleClasses(LoginRequiredMixin, View):

    def get(self, request, id_class):
        hours = WorkingHours.objects.all()
        student_class = get_object_or_404(Classes, id=id_class)
        schedule = Schedule.objects.all()

        ctx = {'hours': hours,
               'student_class': student_class,
               'schedule': schedule,
               'weekdays': weekdays,
               'weekdays_day': WEEKDAYS}
        return render(request, 'register/schedule_class.html', ctx)


class ScheduleTeacherView(LoginRequiredMixin, View):

    def get(self, request, id_teacher):
        hours = WorkingHours.objects.all()
        teacher = get_object_or_404(Teacher, id=id_teacher)
        schedule = Schedule.objects.all()

        ctx = {'hours': hours,
               'teacher': teacher,
               'schedule': schedule,
               'weekdays': weekdays,
               'weekdays_day': WEEKDAYS}
        return render(request, 'register/schedule_class.html', ctx)


class ScheduleRoomView(LoginRequiredMixin, View):

    def get(self, request, id_room):
        hours = WorkingHours.objects.all()
        room = get_object_or_404(ClassRoom, id=id_room)
        schedule = Schedule.objects.all()

        ctx = {'hours': hours,
               'room': room,
               'schedule': schedule,
               'weekdays': weekdays,
               'weekdays_day': WEEKDAYS}
        return render(request, 'register/schedule_class.html', ctx)


class AdvertAddView(LoginRequiredMixin, UserPassesTestMixin, View):
    class_form = AddAdvertForm

    def get(self, request):
        form = self.class_form()
        return render(request, 'register/add_advert.html', {'form': form})

    def post(self, request):
        form = self.class_form(request.POST)
        if form.is_valid():
            new_advert = form.save(commit=False)
            new_advert.author = request.user
            new_advert.save()
            messages.success(request, 'Dodano ogloszenie')
            return redirect('main')
        return render(request, 'register/add_advert.html', {'form': form})

    def test_func(self):
        return testing_func(self.request.user, 2)


class AdvertEditView(LoginRequiredMixin, UserPassesTestMixin, View):
    class_form = EditAdvertForm

    def get(self, request, id_advert):
        advert_class = get_object_or_404(Adverts, id=id_advert)
        form = self.class_form(instance=advert_class)
        return render(request, 'register/add_advert.html', {'form': form, 'advert_class': advert_class})

    def post(self, request, id_advert):
        advert_class = get_object_or_404(Adverts, id=id_advert)
        form = self.class_form(request.POST, instance=advert_class)
        if form.is_valid():
            form.save()
            messages.success(request, 'Zmodyfikowano ogloszenie')
            return redirect('main')
        return render(request, 'register/add_advert.html', {'form': form})

    def test_func(self):
        return testing_func(self.request.user, 2)


class AdvertClassAddView(LoginRequiredMixin, UserPassesTestMixin, View):
    class_form = AddClassAdvertForm

    def get(self, request, id_class):
        student_class = get_object_or_404(Classes, id=id_class)
        form = self.class_form()
        return render(request, 'register/add_advert.html', {'form': form, 'student_class': student_class})

    def post(self, request, id_class):
        student_class = get_object_or_404(Classes, id=id_class)
        form = self.class_form(request.POST)
        if form.is_valid():
            new_advert = form.save(commit=False)
            new_advert.author = request.user.teacher
            new_advert.classes = student_class
            new_advert.save()
            messages.success(request, 'Dodano ogloszenie')
            return redirect('class-details', pk=id_class)
        return render(request, 'register/add_advert.html', {'form': form, 'student_class': student_class})

    def test_func(self):
        return testing_func(self.request.user, 2)


class AdvertClassEditView(LoginRequiredMixin, UserPassesTestMixin, View):
    class_form = EditClassAdvertForm

    def get(self, request, id_advert):
        advert_class = get_object_or_404(AdvertsClass, id=id_advert)
        form = self.class_form(instance=advert_class)
        return render(request, 'register/add_advert.html', {'form': form, 'advert_class': advert_class})

    def post(self, request, id_advert):
        advert_class = get_object_or_404(AdvertsClass, id=id_advert)
        form = self.class_form(request.POST, instance=advert_class)
        if form.is_valid():
            form.save()
            messages.success(request, 'Zmieniono ogloszenie')
            return redirect('adverts-teacher')
        return render(request, 'register/add_advert.html', {'form': form, 'advert_class': advert_class})

    def test_func(self):
        return testing_func(self.request.user, 2)


class NoticeAddView(LoginRequiredMixin, UserPassesTestMixin, View):
    class_form = AddNoticeForm

    def get(self, request, id_student):
        form = self.class_form()
        student = get_object_or_404(Student, id=id_student)
        return render(request, 'register/add_notice.html', {'form': form, 'student': student})

    def post(self, request, id_student):
        student = get_object_or_404(Student, id=id_student)
        form = self.class_form(request.POST)
        if form.is_valid():
            new_notice = form.save(commit=False)
            new_notice.from_user = request.user.teacher
            new_notice.to_user = student
            new_notice.save()
            messages.success(request, 'Dodano uwage')
            return redirect('student-details', pk=id_student)
        return render(request, 'register/add_notice.html', {'form': form, 'student': student})

    def test_func(self):
        return testing_func(self.request.user, 2)


class NoticeEditView(LoginRequiredMixin, UserPassesTestMixin, View):
    class_form = EditNoticeForm

    def get(self, request, id_notice):
        notice = get_object_or_404(Notice, id=id_notice)
        form = self.class_form(instance=notice)
        return render(request, 'register/add_notice.html', {'form': form, 'notice': notice})

    def post(self, request, id_notice):
        notice = get_object_or_404(Notice, id=id_notice)
        form = self.class_form(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Zmieniono uwage')
            return redirect('notices-teacher')
        return render(request, 'register/add_notice.html', {'form': form, 'notice': notice})

    def test_func(self):
        return testing_func(self.request.user, 2)


class NoticeParentView(LoginRequiredMixin, UserPassesTestMixin, View):
    class_form = AnswerNoticeForm

    def get(self, request, id_student):
        form = self.class_form()
        student = get_object_or_404(Student, id=id_student)
        notices = student.notice_set.all()
        return render(request, 'register/notice_parent.html', {'student': student, 'notices': notices, 'form': form})

    def post(self, request, id_student):
        button = request.POST.get('button')
        student = get_object_or_404(Student, id=id_student)
        notices = student.notice_set.all()
        notice = get_object_or_404(Notice, id=button)
        form = self.class_form(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Potwierdzono uwage')
            return redirect('notices-parent', id_student=id_student)
        return render(request, 'register/notice_parent.html', {'student': student, 'notices': notices, 'form': form})

    def test_func(self):
        return testing_func(self.request.user, 1)


class NoticeParentEditView(LoginRequiredMixin, UserPassesTestMixin, View):
    class_form = AnswerNoticeForm

    def get(self, request, id_notice):
        notice = get_object_or_404(Notice, id=id_notice)
        form = self.class_form(instance=notice)
        return render(request, 'register/add_notice.html', {'form': form, 'notice': notice})

    def post(self, request, id_notice):
        notice = get_object_or_404(Notice, id=id_notice)
        form = self.class_form(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Zmieniono uwage')
            return redirect('notices-parent', id_student=notice.to_user.id)
        return render(request, 'register/add_notice.html', {'form': form, 'notice': notice})

    def test_func(self):
        return testing_func(self.request.user, 1)


class NoticeTeacherView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request):
        teacher = Teacher.objects.get(id=request.user.teacher.id)
        notices = teacher.notice_set.all()
        return render(request, 'register/notices_teacher.html', {'teacher': teacher, 'notices': notices})

    def test_func(self):
        return testing_func(self.request.user, 2)


class AdvertTeacherView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request):
        adverts_global = Adverts.objects.all()
        adverts_class = AdvertsClass.objects.all()
        ctx = {'adverts_global': adverts_global, 'adverts_class': adverts_class}
        return render(request, 'register/advert_teacher.html', ctx)

    def test_func(self):
        return testing_func(self.request.user, 2)


class AnnouncementView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request):
        parent = Parent.objects.get(user_id=request.user.id)
        children = parent.students.all()
        if len(children) > 1:
            children_flag = True
        else:
            children_flag = False
        ctx = {'children': children, 'children_flag': children_flag}
        return render(request, 'register/announcements_list.html', ctx)

    def post(self, request):
        approved = request.POST.get("approved")
        if approved:
            event, id_ann = approved.split("_")
            if event == 'deleted':
                announcement = get_object_or_404(Announcements, id=id_ann)
                announcement.deleted = True
                announcement.save()
            else:
                announcement = get_object_or_404(Announcements, id=id_ann)
                announcement.read = True
                announcement.save()
            return HttpResponse('great')
        else:
            raise PermissionDenied

    def test_func(self):
        return testing_func(self.request.user, 1)


class AnnouncementOnlineView(LoginRequiredMixin, View):

    def get(self, request):
        count = 0
        if request.user.profile.role == 1:
            parent = Parent.objects.get(user_id=request.user.id)
            children = parent.students.all()
            for child in children:
                count += Announcements.objects.filter(user=child.user, read=False, deleted=False).count()
            return HttpResponse(str(count))
        else:
            raise PermissionDenied


class AddEventView(LoginRequiredMixin, UserPassesTestMixin, View):
    class_form = AddEventForm

    def get(self, request, id_lesson):
        lesson = get_object_or_404(Lessons, id=id_lesson)
        if not self.my_test(lesson):
            raise PermissionDenied
        form = self.class_form()
        return render(request, 'register/add_event.html', {'form': form, 'lesson': lesson})

    def post(self, request, id_lesson):
        lesson = get_object_or_404(Lessons, id=id_lesson)
        if not self.my_test(lesson):
            raise PermissionDenied
        form = self.class_form(request.POST)
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.lesson = lesson
            new_event.save()
            messages.success(request, "Dodano wydarzenie")
            return redirect('teacher-subjects-view')
        return render(request, 'register/add_event.html', {'form': form, 'lesson': lesson})

    def test_func(self):
        return testing_func(self.request.user, 2)

    def my_test(self, lesson):
        if lesson.teacher == self.request.user.teacher:
            return True
        return False


class EditEventView(LoginRequiredMixin, UserPassesTestMixin, View):
    class_form = AddEventForm

    def get(self, request, id_event):
        event = get_object_or_404(Event, id=id_event)
        if not self.my_test(event.lesson):
            raise PermissionDenied
        form = self.class_form(instance=event)
        return render(request, 'register/add_event.html', {'form': form, 'event': event})

    def post(self, request, id_event):
        event = get_object_or_404(Event, id=id_event)
        if not self.my_test(event.lesson):
            raise PermissionDenied
        form = self.class_form(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Edytowano wydarzenie")
            return redirect('list-event', id_classes=event.lesson.classes.id)
        return render(request, 'register/add_event.html', {'form': form, 'event': event})

    def test_func(self):
        return testing_func(self.request.user, 2)

    def my_test(self, lesson):
        if lesson.teacher == self.request.user.teacher:
            return True
        return False


class ListEventView(LoginRequiredMixin, View):

    def get(self, request, id_classes):
        date_now = datetime.now()
        classes = get_object_or_404(Classes, id=id_classes)
        events = Event.objects.filter(date_of_event__gte=date_now, lesson__classes=classes).order_by('date_of_event')
        return render(request, 'register/events_list.html', {'events': events})


class ListEventTeacherView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request):
        date_now = datetime.now()
        teacher = Teacher.objects.get(user=request.user)
        events = Event.objects.filter(date_of_event__gte=date_now, lesson__teacher=teacher).order_by('date_of_event')
        return render(request, 'register/events_list.html', {'events': events})

    def test_func(self):
        return testing_func(self.request.user, 2)
