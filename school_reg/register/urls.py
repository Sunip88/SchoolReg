from django.urls import path
from .views import MainView, ClassView, AddClassView, EditClassView, DetailsClassView, SubjectsView, AddSubjectView, \
    EditSubjectView, AddGradesClass, AddGradeCategoryView, StudentDetailView, TeacherPanelView, \
    TeacherSubjectsClassesView, TeacherGradesView, StudentView, PresenceView, ScheduleClasses, \
    ScheduleTeacherView, ScheduleRoomView, SchedulesView, AdvertAddView, NoticeAddView, ParentPanelView, \
    NoticeParentView, NoticeTeacherView, AdvertClassAddView, AdvertTeacherView, AdvertClassEditView, AdvertEditView, \
    NoticeEditView, NoticeParentEditView, AnnouncementView, TeacherDetailView, AnnouncementOnlineView

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
    path("edit_advert/<int:id_advert>/", AdvertEditView.as_view(), name='edit-advert'),
    path("add_advert_class/<int:id_class>/", AdvertClassAddView.as_view(), name='add-advert-class'),
    path("edit_advert_class/<int:id_advert>/", AdvertClassEditView.as_view(), name='edit-advert-class'),
    path("add_notice/<int:id_student>/", NoticeAddView.as_view(), name='add-notice'),
    path("edit_notice/<int:id_notice>/", NoticeEditView.as_view(), name='edit-notice'),
    path("notices/<int:id_student>/", NoticeParentView.as_view(), name='notices-parent'),
    path("edit_notice_parent/<int:id_notice>/", NoticeParentEditView.as_view(), name='notice-edit-parent'),
    path("teacher_notices/", NoticeTeacherView.as_view(), name='notices-teacher'),
    path("teacher_adverts/", AdvertTeacherView.as_view(), name='adverts-teacher'),
    path("announcements/", AnnouncementView.as_view(), name='announcements'),
    path("announcements_online/", AnnouncementOnlineView.as_view(), name='counter'),
    path("edit_class/<int:pk>/", EditClassView.as_view(), name='class-edit'),
    path("edit_subject/<int:pk>/", EditSubjectView.as_view(), name='subject-edit'),
    path("detailed_class/<int:pk>/", DetailsClassView.as_view(), name='class-details'),
    path("schedules/", SchedulesView.as_view(), name='schedules'),
    path("class_schedule/<int:id_class>/", ScheduleClasses.as_view(), name='class-schedule'),
    path("teacher_schedule/<int:id_teacher>/", ScheduleTeacherView.as_view(), name='teacher-schedule'),
    path("room_schedule/<int:id_room>/", ScheduleRoomView.as_view(), name='room-schedule'),
    path("detailed_class_grades/<int:subject_id>/<int:class_id>/", TeacherGradesView.as_view(), name='class-details-grades'),
    path("detailed_student/<int:pk>/", StudentDetailView.as_view(), name='student-details'),
    path("detailed_teacher/<int:pk>/", TeacherDetailView.as_view(), name='teacher-details'),
    path("add_grades/<int:id_class>/<int:id_subject>/", AddGradesClass.as_view(), name='class-grade-add'),
    path("add_presence/<int:id_class>/<int:id_schedule>/", PresenceView.as_view(), name='class-presence-add'),
]
