from django.contrib import admin
from django.urls import path, include           # ✅ Make sure 'path' is here
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse             # ✅ For default homepage

def home(request):
    return JsonResponse({"message": "Job Portal API is running!"})

urlpatterns = [
    path('', home),  # ✅ root / path added
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/jobs/', include('jobs.urls')),
    path('api/applications/', include('applications.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
