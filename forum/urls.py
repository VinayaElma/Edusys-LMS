from django.contrib import admin
from django.urls import path

from forum import views as views

app_name = 'forum'

urlpatterns = [
    path('', views.ForumListView.as_view(), name='forum'),
    path('<code>/', views.TopicListView.as_view(), name='topics'),
    path('<code>/new/', views.NewTopicFormView.as_view(), name='new_topic'),
    path('<code>/topics/search/', views.SearchTopicResultsView.as_view(), name='search_topics'),
    path('<code>/topics/<int:pk>/', views.TopicCommentsView.as_view(), name='topic_comments'),
    path('<code>/topics/<int:pk>/edit/', views.TopicUpdateView.as_view(), name='edit_topic'),
    path('<code>/topics/<int:pk>/delete/', views.TopicDeleteView.as_view(), name='delete_topic'),
    path('<code>/topics/<int:pk>/comments/<int:comment_pk>/edit/', views.CommentEditView.as_view(), name='edit_comment'),
    path('<code>/topics/<int:pk>/comments/<int:comment_pk>/delete/', views.CommentDeleteView.as_view(), name='delete_comment'),

]
