from django.urls import path

from . import views

app_name = 'handler'

urlpatterns = [
    path('', views.home, name="home"),
    path('clients', views.clients, name='clients'),
    path('clients/<int:client_id>', views.client, name='client'),
    path('students', views.students, name="students"),
    path('student/<int:student_id>', views.student, name='student'),
    path('payments', views.payments, name="payments"),
    path('groups', views.groups, name='groups'),
    path('groups/<int:group_id>', views.group, name='group'),
]