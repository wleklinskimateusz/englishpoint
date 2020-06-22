from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import *
# Create your views here.


def home(request):
    return redirect(reverse_lazy('handler:clients'))


def clients(request):
    template_name = 'clients.html'
    context = {
        'clients': Parent.objects.all(),
    }
    return render(request, template_name, context)


def students(request):
    template_name = 'students.html'
    context = {
        'students': Student.objects.all(),
    }
    return render(request, template_name, context)


def payments(request):
    template_name = 'payments.html'
    context = {
        'payments': Payment.objects.all(),
    }
    return render(request, template_name, context)
