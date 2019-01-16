from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView

from .forms import AddGradeForm
from .models import Classes, Subject, Student, GradeCategory, Teacher
from django.contrib import messages


class MainView(View):

    def get(self, request):
        return render(request, 'register/main.html')


class TeacherPanelView(View):
    def get(self, request):
        teacher = Teacher.objects.filter(user_id=request.user.id)
        return render(request, 'register/teacher_view.html', {"teacher": teacher})


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
        cxt = {'students': students, 'detail_class': detail_class}
        return render(request, 'register/detail_classes.html', cxt)


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
    form_class = AddGradeForm

    def get(self, request, id_class, id_subject):
        detail_class = get_object_or_404(Classes, id=id_class)
        students = Student.objects.all()
        subject = get_object_or_404(Subject, id=id_subject)
        form = self.form_class()
        cxt = {'detail_class': detail_class, 'students': students, 'subject': subject, 'form': form}
        return render(request, 'register/detail_classes_add_grade.html', cxt)

    def post(self, request, id_class, id_subject):
        form = self.form_class(request.POST)
        detail_class = get_object_or_404(Classes, id=id_class)
        students = Student.objects.all()
        subject = get_object_or_404(Subject, id=id_subject)
        cxt = {'detail_class': detail_class, 'students': students, 'subject': subject, 'form': form}
        if form.is_valid():
            button = request.POST.get('button')
            student = get_object_or_404(Student, id=button)
            new_grade = form.save(commit=False)
            new_grade.subject = subject
            new_grade.student = student
            new_grade.save()
            messages.success(request, 'Dodano ocenę')
            return redirect('class-grade-add', id_class=id_class, id_subject=id_subject)
        return render(request, 'register/detail_classes_add_grade.html', cxt)


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
