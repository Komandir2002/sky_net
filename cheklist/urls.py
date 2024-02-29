# ваш_проект/ваше_приложение/urls.py

from django.urls import path
from .views import add_application,application_info,update_application,review

urlpatterns = [
    path('add-applications/', add_application, name='add_application_url'),
    path('application_info/<slug:application_slug>/', application_info, name='application_info'),
    path('update_aplications/<slug:application_slug>/', update_application, name='update_application'),
    path('application_info/<slug:application_slug>/review/', review, name='review'),
]
