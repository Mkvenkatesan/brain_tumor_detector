# brain_tumor_detection_app/urls.py
from django.urls import path
from .views import predict_image

urlpatterns = [
    path('', predict_image, name='predict_image'),
]
