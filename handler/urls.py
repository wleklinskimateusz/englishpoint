from django.urls import path

from . import views

app_name = 'handler'

urlpatterns = [
    path('', views.home, name='home'),
]