from django.urls import path

from . import views

app_name = 'handler'

urlpatterns = [
    path('', views.home, name="home"),
    path('clients', views.clients, name='clients'),
    path('clients/<int:client_id>', views.client, name='client'),
    path('clients/<int:pk>/delete', views.ClientDeleteView.as_view(), name='delete_client'),
    path('clients/<int:pk>/edit', views.ClientUpdate.as_view(), name='client_edit'),
    path('clients/<int:client_id>/contact', views.mail_to_client, name='send_mail'),
    path('clients/new', views.new_client, name='new_client'),
    path('clients/overdues', views.clients_overdue, name='overdues'),
    path('students', views.students, name="students"),
    path('student/<int:student_id>', views.student, name='student'),
    path('student/new', views.new_student, name='new_student'),
    path('payments', views.payments, name="payments"),
    path('payments/new', views.new_payment, name="new_payment"),
    path('groups', views.groups, name='groups'),
    path('groups/<int:group_id>', views.group, name='group'),
    path('groups/<int:pk>/delete', views.GroupDeleteView.as_view(), name='delete_group'),
    path('groups/<int:pk>/edit', views.GroupUpdate.as_view(), name='edit_group'),
    path('groups/new', views.new_group, name='new_group'),
    path('attendance/', views.attendance, name='attendance'),
    path('attendance/check/<int:group_id>', views.check_attendance, name='check_attendance'),

]