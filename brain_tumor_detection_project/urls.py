# brain_tumor_detection_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('brain_tumor_detection_app.urls')),
]
