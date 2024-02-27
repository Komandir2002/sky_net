# ваш_проект/ваше_приложение/urls.py

from django.urls import path
from .views import add_application,show_applications,application_info,rate_application,update_application,review,planup_p

urlpatterns = [
    path('add-applications/', add_application, name='add_application_url'),
    path('show_applications/', show_applications, name='show_applications'),
    path('application_info/<slug:application_slug>/', application_info, name='add_application_info'),
    path('update_aplications/<slug:application_slug>/', update_application, name='update_application_info'),
    path('rate-application/<slug:application_slug>/', rate_application, name='rate_application'),
    path('application_info/<slug:application_slug>/review/', review, name='review'),

    path('testy/', planup_p, name='testy'),
    # Другие URL-пути вашего приложения...
]
