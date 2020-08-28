from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('coursematerials/', include(('course_materials.urls', 'course_materials'))),
    path('announcements/', include(('announcements.urls', 'announcements'))),
    path("assignments/", include(("assignments.urls", 'assignments'))),
    path('', include('accounts.urls')),
    path("forum/", include("forum.urls")),
    path("quiz/",include("quiz.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

