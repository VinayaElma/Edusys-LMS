from django.urls import path
from assignments import views as assignment_views

app_name = "assignments"

urlpatterns = [
    path('subjects/', assignment_views.SubjectsListView.as_view(), name='view_subjects'),
    path('subjects/<int:pk>/', assignment_views.SubjectsDetailView.as_view(), name='view_assignments'),
    path('subjects/<int:pk>/new/', assignment_views.AssignmentCreateView.as_view(), name='new_assignments'),
    path('subjects/<int:pk_alt>/<int:pk>/', assignment_views.AssignmentDetailView.as_view(), name='detail_assignments'),
    path('subjects/<int:pk_alt>/<int:pk>/update/', assignment_views.AssignmentUpdateView.as_view(),
         name='update_assignments'),
    path('subjects/<int:pk_alt>/<int:pk>/delete/', assignment_views.AssignmentDeleteView.as_view(),
         name='delete_assignments'),
    path('subjects/<int:pk_alt>/<int:pk>/question', assignment_views.FileUploadCreateView.as_view(),
         name='question_file_upload'),
    path('subjects/<int:pk_alt>/<int:pk_al>/<int:pk>/update', assignment_views.FileUploadUpdateView.as_view(),
         name='question_file_update'),
    path('subjects/<int:pk_alt>/<int:pk_al>/<int:pk>/submit', assignment_views.SubmissionCreateView.as_view(),
         name='new_submission'),
    path('subjects/<int:pk_alt>/<int:pk_al>/<int:pk_a>/<int:pk>/update/',
         assignment_views.SubmissionUpdateView.as_view(),
         name='update_submission'),
    path('subjects/<int:pk_alt>/<int:pk_al>/<int:pk>/answers/',
         assignment_views.AnswerListView.as_view(),
         name='view_answers'),
    path('subjects/<int:pk_alt>/<int:pk_al>/<int:pk_a>/<int:pk>/',
         assignment_views.MarkUploadView.as_view(),
         name='marks_upload'),
    path('subject/', assignment_views.SubjectListView.as_view(), name='subjects'),
    path('subject/<int:pk>/', assignment_views.MarksListView.as_view(), name='view_marks'),
    path('subject/<int:pk_alt>/<int:pk>/', assignment_views.StudentsListView.as_view(), name='list_marks'),
]
