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
    path('student/<int:pk>/edit', views.StudentUpdate.as_view(), name='edit_student'),
    path('student/<int:pk>/delete', views.StudentDeleteView.as_view() , name='delete_student'),
    path('student/new', views.new_student, name='new_student'),
    path('payments', views.payments, name="payments"),
    path('payments/new', views.new_payment, name="new_payment"),
    path('corrections', views.corrections, name='corrections'),
    path('corrections/new', views.new_correction, name="new_correction"),
    path('groups', views.groups, name='groups'),
    path('groups/<int:group_id>', views.group, name='group'),
    path('groups/<int:pk>/delete', views.GroupDeleteView.as_view(), name='delete_group'),
    path('groups/<int:pk>/edit', views.GroupUpdate.as_view(), name='edit_group'),
    path('groups/new', views.new_group, name='new_group'),
    path('attendance/', views.attendance, name='attendance'),
    path('attendance/check/<int:group_id>', views.check_attendance, name='check_attendance'),
    path('years/next_year', views.next_year, name='next_year'),
    path('years/previous_year', views.previous_year, name='previous_year'),
    path('search', views.search, name="search"),

]