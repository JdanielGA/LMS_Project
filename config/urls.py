# Path: config/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path(
        "", RedirectView.as_view(pattern_name="courses:course_list", permanent=False), name="home"
    ),
    path("admin/", admin.site.urls),
    path("courses/", include("apps.courses.urls", namespace="courses")),
    path("users/", include("apps.users.urls", namespace="users")),
    path("assessments/", include("apps.assessments.urls", namespace="assessments")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns

    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
