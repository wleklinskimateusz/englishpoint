from django.urls import path

from . import views

app_name = 'handler'

urlpatterns = [
    path('', views.home, name="home"),
    path('clients', views.clients, name='clients'),
    path('clients/<int:client_id>', views.client, name='client'),
    path('clients/<int:pk>/delete', views.ClientDeleteView.as_view(), name='delete_client'),
    path('clients/new', views.new_client, name='new_client'),
    path('students', views.students, name="students"),
    path('student/<int:student_id>', views.student, name='student'),
    path('student/new', views.new_student, name='new_student'),
    path('payments', views.payments, name="payments"),
    path('payments/new', views.new_payment, name="new_payment"),
    path('groups', views.groups, name='groups'),
    path('groups/<int:group_id>', views.group, name='group'),
    path('groups/new', views.new_group, name='new_group'),
    path('attendance/', views.attendance, name='attendance'),
    path('attendance/check/<int:group_id>', views.check_attendance, name='check_attendance'),

]