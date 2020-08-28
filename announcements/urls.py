from django.urls import path
from . import views


app_name = "announcements"

urlpatterns=[
    #path('', views.home, name='home'),
    path('home/', views.home,name='home'),
    path('', views.AnnouncementListView.as_view(), name='view_announcements'),
    path('new/', views.AnnouncementCreateView.as_view(), name='new_announcements'),
    path('search/', views.SearchResultsView.as_view(), name='search_results')
]