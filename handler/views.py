from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import *
# Create your views here.


def home(request):
    return redirect(reverse_lazy('handler:clients'))

###CLIENTS###


def clients(request):
    template_name = 'clients.html'
    context = {
        'clients': Parent.objects.all(),
    }
    return render(request, template_name, context)


def client(request, client_id):
    my_client = get_object_or_404(Parent, pk=client_id)
    template_name = 'client.html'
    kids = Student.objects.filter(parent=my_client)
    context = {
        'client': my_client,
        'kids': kids,
    }
    return render(request, template_name, context)


###STUDENTS###


def students(request):
    template_name = 'students.html'
    context = {
        'students': Student.objects.all(),
    }
    return render(request, template_name, context)


def student(request, student_id):
    my_student = get_object_or_404(Student, pk=student_id)
    template_name = 'student.html'
    context = {
        'student': my_student,
    }
    return render(request, template_name, context)


###GROUPS###


def groups(request):
    template_name = 'groups.html'
    context = {
        'groups': StudentGroup.objects.all(),
    }
    return render(request, template_name, context)


def group(request, group_id):
    my_group = get_object_or_404(StudentGroup, pk=group_id)
    template_name = 'group.html'
    context = {
        'group': my_group,
        'students': Student.objects.filter(group=my_group),
    }
    return render(request, template_name, context)


###PAYMENTS###


def payments(request):
    template_name = 'payments.html'
    context = {
        'payments': Payment.objects.all(),
    }
    return render(request, template_name, context)
