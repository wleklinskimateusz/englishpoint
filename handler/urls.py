from django.urls import path

from . import views

app_name = 'handler'

urlpatterns = [
    path('', views.home, name="home"),
    path('clients', views.clients, name='clients'),
    path('students', views.students, name="students"),
    path('payments', views.payments, name="payments"),
]