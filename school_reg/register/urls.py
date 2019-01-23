from django.urls import path
from .views import MainView, ClassView, AddClassView, EditClassView, DetailsClassView, SubjectsView, AddSubjectView, \
    EditSubjectView, AddGradesClass, AddGradeCategoryView, StudentDetailView, TeacherPanelView, \
    TeacherSubjectsClassesView, TeacherGradesView, StudentView, PresenceView, PresenceEditView, ScheduleClasses, \
    ScheduleTeacherView, ScheduleRoomView, SchedulesView, AdvertAddView, NoticeAddView, ParentPanelView, \
    NoticeParentView, NoticeTeacherView

urlpatterns = [
    path("", MainView.as_view(), name="main"),
    path("classes/", ClassView.as_view(), name="class-view"),
    path("teacher_panel/", TeacherPanelView.as_view(), name="teacher-panel-view"),
    path("student_panel/", StudentView.as_view(), name="student-panel-view"),
    path("parent_panel/", ParentPanelView.as_view(), name="parent-panel-view"),
    path("teacher_subjects/", TeacherSubjectsClassesView.as_view(), name="teacher-subjects-view"),
    path("subjects/", SubjectsView.as_view(), name="subject-view"),
    path("add_class/", AddClassView.as_view(), name='class-add'),
    path("add_subject/", AddSubjectView.as_view(), name='subject-add'),
    path("add_grade_category/", AddGradeCategoryView.as_view(), name='add-grade-category'),
    path("add_advert/", AdvertAddView.as_view(), name='add-advert'),
    path("add_notice/<int:id_student>/", NoticeAddView.as_view(), name='add-notice'),
    path("notices/<int:id_student>/", NoticeParentView.as_view(), name='notices-parent'),
    path("teacher_notices/", NoticeTeacherView.as_view(), name='notices-teacher'),
    path("edit_class/<int:pk>/", EditClassView.as_view(), name='class-edit'),
    path("edit_subject/<int:pk>/", EditSubjectView.as_view(), name='subject-edit'),
    path("detailed_class/<int:pk>/", DetailsClassView.as_view(), name='class-details'),
    path("schedules/", SchedulesView.as_view(), name='schedules'),
    path("class_schedule/<int:id_class>/", ScheduleClasses.as_view(), name='class-schedule'),
    path("teacher_schedule/<int:id_teacher>/", ScheduleTeacherView.as_view(), name='teacher-schedule'),
    path("room_schedule/<int:id_room>/", ScheduleRoomView.as_view(), name='room-schedule'),
    path("detailed_class_grades/<int:subject_id>/<int:class_id>/", TeacherGradesView.as_view(), name='class-details-grades'),
    path("detailed_student/<int:pk>/", StudentDetailView.as_view(), name='student-details'),
    path("add_grades/<int:id_class>/<int:id_subject>/", AddGradesClass.as_view(), name='class-grade-add'),
    path("add_presence/<int:id_class>/<int:id_subject>/", PresenceView.as_view(), name='class-presence-add'),
    path("edit_presence/<int:id_class>/<int:id_subject>/<int:id_student>/", PresenceEditView.as_view(), name='class-presence-edit'),
]
