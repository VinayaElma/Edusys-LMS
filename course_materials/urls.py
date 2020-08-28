from django.urls import path
from . import views

app_name = "course_materials"

urlpatterns = [
    path('',views.SubjectsListView.as_view(),name='view_subjects'),
    path('<int:pk>/',views.SubjectsDetailView.as_view(),name='view_course_materials'),
    path('teacher/<int:pk>/',views.SubjectsDetailView1.as_view(),name='view_teacher_courses'),
    path('teacher/<int:pk>/new/', views.CourseMaterialCreateView.as_view(), name='new_materials'),
    path('teacher/<int:pk_alt>/<int:pk>/delete/', views.CourseMaterialDeleteView.as_view(), name='delete_material'),
    path('teacher/<int:pk_alt>/<int:pk>/update/', views.CourseMaterialUpdateView.as_view(), name='update_materials'),
    path('<int:pk>/search/',views.SearchResultsView.as_view(), name='search_results1'),
    path('teacher/<int:pk>/search/',views.SearchResultsViews.as_view(), name='search_results_teacher'),
]