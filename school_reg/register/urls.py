from django.urls import path
from .views import MainView, ClassView, AddClassView, EditClassView, DetailsClassView, SubjectsView, AddSubjectView, \
    EditSubjectView, AddGradesClass, AddGradeCategoryView

urlpatterns = [
    path("", MainView.as_view(), name="main"),
    path("classes/", ClassView.as_view(), name="class-view"),
    path("subjects/", SubjectsView.as_view(), name="subject-view"),
    path("add_class/", AddClassView.as_view(), name='class-add'),
    path("add_subject/", AddSubjectView.as_view(), name='subject-add'),
    path("add_grade_category/", AddGradeCategoryView.as_view(), name='add-grade-category'),
    path("edit_class/<int:pk>/", EditClassView.as_view(), name='class-edit'),
    path("edit_subject/<int:pk>/", EditSubjectView.as_view(), name='subject-edit'),
    path("detailed_class/<int:pk>/", DetailsClassView.as_view(), name='class-details'),
    path("add_grades/<int:id_class>/", AddGradesClass.as_view(), name='class-grade-add'),
]
