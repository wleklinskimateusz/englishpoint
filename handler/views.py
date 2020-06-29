from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse_lazy
from .models import *
from .forms import StudentForm, StudentGroupForm, ParentForm, PaymentForm
# Create your views here.


def home(request):
    if not request.user.is_authenticated:
        return redirect('accounts/login')

    return redirect(reverse_lazy('handler:clients'))

###CLIENTS###


def clients(request):
    if not request.user.is_authenticated:
        return redirect('accounts/login')

    template_name = 'clients.html'
    context = {
        'clients': Parent.objects.all(),
    }
    return render(request, template_name, context)


def client(request, client_id):
    if not request.user.is_authenticated:
        return redirect('accounts/login')

    my_client = get_object_or_404(Parent, pk=client_id)
    template_name = 'client.html'
    kids = Student.objects.filter(parent=my_client)
    context = {
        'client': my_client,
        'kids': kids,
    }
    return render(request, template_name, context)


def new_client(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    template_name = 'form.html'
    if request.method == 'POST':
        form = ParentForm(request.POST)
        if form.is_valid():
            new = Parent()
            new.first_name = form.cleaned_data['first_name']
            new.surname = form.cleaned_data['surname']
            new.email = form.cleaned_data['email']
            new.phone_number = form.cleaned_data['phone_number']
            new.save()
            return HttpResponseRedirect(reverse_lazy('handler:clients'))
    else:
        form = ParentForm()
    context = {
        'form': form,
        'title': "Nowy Rodzic"

    }

    return render(request, template_name, context)

###STUDENTS###


def students(request):
    if not request.user.is_authenticated:
        return redirect('accounts/login')

    template_name = 'students.html'
    context = {
        'students': Student.objects.all(),
    }
    return render(request, template_name, context)


def student(request, student_id):
    if not request.user.is_authenticated:
        return redirect('accounts/login')

    my_student = get_object_or_404(Student, pk=student_id)
    template_name = 'student.html'
    context = {
        'student': my_student,
    }
    return render(request, template_name, context)


def new_student(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    template_name = 'form.html'
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            new = Student()
            new.first_name = form.cleaned_data['first_name']
            new.surname = form.cleaned_data['surname']
            new.group = form.cleaned_data['group']
            new.parent = form.cleaned_data['parent']
            new.birthday = form.cleaned_data['birthday']
            new.save()
            return HttpResponseRedirect(reverse_lazy('handler:students'))
    else:
        form = StudentForm()
    context = {
        'form': form,
        'title': "Nowe dziecko"

    }

    return render(request, template_name, context)


###GROUPS###


def groups(request):
    if not request.user.is_authenticated:
        return redirect('accounts/login')

    template_name = 'groups.html'
    context = {
        'groups': StudentGroup.objects.all(),
    }
    return render(request, template_name, context)


def group(request, group_id):
    if not request.user.is_authenticated:
        return redirect('accounts/login')

    my_group = get_object_or_404(StudentGroup, pk=group_id)
    template_name = 'group.html'
    context = {
        'group': my_group,
        'students': Student.objects.filter(group=my_group),
    }
    return render(request, template_name, context)


def new_group(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    template_name = 'form.html'
    if request.method == 'POST':
        form = StudentGroupForm(request.POST)
        if form.is_valid():
            new = StudentGroup()
            new.name = form.cleaned_data['name']
            new.lesson_duration = form.cleaned_data['lesson_duration']
            new.amount_lessons = form.cleaned_data['amount_lessons']
            new.save()
            return HttpResponseRedirect(reverse_lazy('handler:groups'))
    else:
        form = StudentGroupForm()
    context = {
        'form': form,
        'title': "Nowa grupa"

    }

    return render(request, template_name, context)


###PAYMENTS###


def payments(request):
    if not request.user.is_authenticated:
        return redirect('accounts/login')

    template_name = 'payments.html'
    context = {
        'payments': Payment.objects.all(),
    }
    return render(request, template_name, context)


def new_payment(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    template_name = 'form.html'
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            new = Payment()
            new.client = form.cleaned_data['client']
            new.value = form.cleaned_data['value']
            new.date = form.cleaned_data['date']
            new.comment = form.cleaned_data['comment']
            new.save()
            return HttpResponseRedirect(reverse_lazy('handler:payments'))
    else:
        form = PaymentForm()
    context = {
        'form': form,
        'title': "Nowa płatność"

    }

    return render(request, template_name, context)
