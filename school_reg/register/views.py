from datetime import datetime, date

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView

from .forms import AddGradeForm, PresenceForm, AddAdvertForm, AddNoticeForm, AnswerNoticeForm
from .models import Classes, Subject, Student, GradeCategory, Teacher, PresenceList, WorkingHours, Schedule, WEEKDAYS, \
    ClassRoom, Adverts, Parent, Notice
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


class MainView(View):

    def get(self, request):
        adverts = Adverts.objects.all()
        return render(request, 'register/main.html', {'adverts': adverts})


class TeacherPanelView(View):
    def get(self, request):
        teacher = Teacher.objects.get(user_id=self.request.user.id)
        educator = teacher.classes_set.all()
        if educator:
            educator = educator.first()
        return render(request, 'register/teacher_view.html', {"teacher": teacher, "educator": educator})


class ParentPanelView(View):
    def get(self, request):
        parent = Parent.objects.get(user_id=self.request.user.id)
        children = parent.students.all()
        ctx = {"parent": parent, "children": children}
        return render(request, 'register/parent_view.html', ctx)


class TeacherSubjectsClassesView(View):
    def get(self, request):
        teacher = Teacher.objects.filter(user_id=request.user.id)
        if teacher:
            teacher = teacher.first()
            subjects = teacher.subjects.all()
        else:
            subjects = []
        return render(request, 'register/teacher_class_subject.html', {'teacher': teacher, 'subjects': subjects})


class TeacherGradesView(View):
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


class StudentView(View):
    def get(self, request):
        student = Student.objects.get(user_id=self.request.user.id)
        student_class = student.classes
        ctx = {'student': student, 'student_class': student_class}
        return render(request, 'register/student_view.html', ctx)


class ClassView(View):
    def get(self, request):
        teacher = Teacher.objects.filter(user_id=request.user.id)
        if teacher:
            classes = teacher.classes_set.all()
        else:
            messages.success(request, 'Konto admin')
            classes = Classes.objects.all()
        return render(request, 'register/classes.html', {'classes': classes})


class AddClassView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'register.add_classes'
    model = Classes
    fields = '__all__'
    template_name = 'register/add_class.html'
    success_url = reverse_lazy("class-view")


class EditClassView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'register.change_classes'
    model = Classes
    fields = '__all__'
    template_name = 'register/add_class.html'
    success_url = reverse_lazy("class-view")


class DetailsClassView(View):

    def get(self, request, pk):
        detail_class = get_object_or_404(Classes, id=pk)
        students = detail_class.student_set.all()
        ctx = {'students': students, 'detail_class': detail_class}
        return render(request, 'register/detail_classes.html', ctx)


class SubjectsView(View):

    def get(self, request):
        subjects = Subject.objects.all()
        return render(request, 'register/subjects.html', {'subjects': subjects})


class AddSubjectView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'register.add_subject'
    model = Subject
    fields = '__all__'

    template_name = 'register/add_class.html'
    success_url = reverse_lazy("subject-view")

    def get_form(self, form_class=None):
        form = super(AddSubjectView, self).get_form(form_class)
        form.fields['classes'].required = False
        return form


class EditSubjectView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'register.change_subject'
    model = Subject
    fields = '__all__'
    template_name = 'register/add_class.html'
    success_url = reverse_lazy("subject-view")


class AddGradeCategoryView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'register.add_gradecategory'
    model = GradeCategory
    fields = '__all__'
    template_name = 'register/add_class.html'
    success_url = reverse_lazy("add-grade-category")


class AddGradesClass(View):
    class_form = AddGradeForm

    def get(self, request, id_class, id_subject):
        detail_class = get_object_or_404(Classes, id=id_class)
        students = Student.objects.filter(classes_id=detail_class.id)
        subject = get_object_or_404(Subject, id=id_subject)
        form = self.class_form()
        ctx = {'detail_class': detail_class, 'students': students, 'subject': subject, 'form': form}
        return render(request, 'register/detail_classes_add_grade.html', ctx)

    def post(self, request, id_class, id_subject):
        form = self.class_form(request.POST)
        detail_class = get_object_or_404(Classes, id=id_class)
        students = Student.objects.filter(classes_id=detail_class.id)
        subject = get_object_or_404(Subject, id=id_subject)
        ctx = {'detail_class': detail_class, 'students': students, 'subject': subject, 'form': form}
        if form.is_valid():
            button = request.POST.get('button')
            student = get_object_or_404(Student, id=button)
            new_grade = form.save(commit=False)
            new_grade.subject = subject
            new_grade.student = student
            new_grade.save()
            messages.success(request, 'Dodano ocenę')
            return redirect('class-grade-add', id_class=id_class, id_subject=id_subject)
        return render(request, 'register/detail_classes_add_grade.html', ctx)


class StudentDetailView(View):

    def get(self, request, pk):
        student = get_object_or_404(Student, id=pk)
        grades = student.grades_set.all()
        subjects = {}
        for g in grades:
            if g.subject.id not in subjects.keys():
                subjects[g.subject.id] = g.subject.name
        ctx = {'student': student, 'grades': grades, 'subjects': subjects}
        return render(request, 'register/student_details.html', ctx)


class PresenceView(View):
    class_form = PresenceForm

    def get(self, request, id_class, id_subject):
        detail_class = get_object_or_404(Classes, id=id_class)
        students = Student.objects.filter(classes_id=detail_class.id)
        subject = get_object_or_404(Subject, id=id_subject)
        today = datetime.now().strftime('%Y-%m-%d')
        form = self.class_form()
        ctx = {'detail_class': detail_class, 'students': students, 'subject': subject, 'form': form, 'today': today}
        return render(request, 'register/presence_check.html', ctx)

    def post(self, request, id_class, id_subject):
        form = self.class_form(request.POST)
        detail_class = get_object_or_404(Classes, id=id_class)
        students = Student.objects.filter(classes_id=detail_class.id)
        subject = get_object_or_404(Subject, id=id_subject)
        today = datetime.now().date()
        ctx = {'detail_class': detail_class, 'students': students, 'subject': subject, 'form': form}
        if form.is_valid():
            button = request.POST.get('button')
            student = get_object_or_404(Student, id=button)
            presence = form.save(commit=False)
            presence.day = today
            presence.student = student
            presence.subject = subject
            presence.save()
            messages.success(request, 'Dodano ocenę')
            return redirect('class-presence-add', id_class=id_class, id_subject=id_subject)
        return render(request, 'register/presence_check.html', ctx)


class PresenceEditView(View):
    class_form = PresenceForm

    def get(self, request, id_class, id_subject, id_student):
        detail_class = get_object_or_404(Classes, id=id_class)
        student = get_object_or_404(Student, id=id_student)
        subject = get_object_or_404(Subject, id=id_subject)
        today = datetime.now().date()
        today_str = today.strftime('%Y-%m-%d')
        presence = PresenceList.objects.filter(student_id=student.id, day=today, subject_id=subject.id).first()
        form = self.class_form(instance=presence)
        ctx = {'detail_class': detail_class, 'student': student, 'subject': subject, 'form': form, 'today': today_str}
        return render(request, 'register/presence_edit.html', ctx)

    def post(self, request, id_class, id_subject, id_student):
        detail_class = get_object_or_404(Classes, id=id_class)
        student = get_object_or_404(Student, id=id_student)
        subject = get_object_or_404(Subject, id=id_subject)
        today = datetime.now().date()
        today_str = today.strftime('%Y-%m-%d')
        presence = PresenceList.objects.filter(student_id=student.id, day=today, subject_id=subject.id).first()
        form = self.class_form(request.POST, instance=presence)
        ctx = {'detail_class': detail_class, 'student': student, 'subject': subject, 'form': form, 'today': today_str}
        if form.is_valid():
            button = request.POST.get('button')
            student = get_object_or_404(Student, id=button)
            presence = form.save(commit=False)
            presence.day = today
            presence.student = student
            presence.subject = subject
            presence.save()
            messages.success(request, 'Dodano ocenę')
            return redirect('class-presence-add', id_class=id_class, id_subject=id_subject)
        return render(request, 'register/presence_edit.html', ctx)


class SchedulesView(View):

    def get(self, request):
        teachers = Teacher.objects.all()
        classes = Classes.objects.all()
        rooms = ClassRoom.objects.all()
        ctx = {'teachers': teachers, 'classes': classes, 'rooms': rooms}
        return render(request, 'register/schedules.html', ctx)


class ScheduleClasses(View):

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


class ScheduleTeacherView(View):

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


class ScheduleRoomView(View):

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


class AdvertAddView(View):
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


class NoticeAddView(View):
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


class NoticeParentView(View):
    class_form = AnswerNoticeForm

    def get(self, request, id_student):
        form = self.class_form()
        student = get_object_or_404(Student, id=id_student)
        notices = student.notice_set.all()
        return render(request, 'register/notice_parent.html', {'student': student, 'notices': notices, 'form': form})

    def post(self, request, id_student):
        button = request.POST.get('button')
        notice = Notice.objects.get(id=button)
        student = get_object_or_404(Student, id=id_student)
        notices = student.notice_set.all()
        form = self.class_form(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Potwierdzono uwage')
            return redirect('notices', id_student=id_student)
        return render(request, 'register/notice_parent.html', {'student': student, 'notices': notices, 'form': form})


class NoticeTeacherView(View):

    def get(self, request):
        teacher = Teacher.objects.get(id=request.user.teacher.id)
        notices = teacher.notice_set.all()
        return render(request, 'register/notices_teacher.html', {'teacher': teacher, 'notices': notices})


