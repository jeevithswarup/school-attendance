from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('dashboard'), name='home'),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('accounts.dashboard_urls')),
    path('students/', include('students.urls')),
    path('attendance/', include('attendance_app.urls')),
    path('fees/', include('fees.urls')),
    path('marks/', include('marks.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
