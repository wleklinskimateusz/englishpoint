from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from .models import *
from .forms import StudentForm, StudentGroupForm, ParentForm, PaymentForm, AttendanceForm
# Create your views here.


def home(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    return redirect(reverse_lazy('handler:clients'))

###CLIENTS###


def clients(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    template_name = 'clients.html'
    context = {
        'clients': Parent.objects.all(),
    }
    return render(request, template_name, context)


def client(request, client_id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

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


class ClientDeleteView(DeleteView):
    """
    class for deleting GoGame Object
    """
    model = Parent
    template_name = 'delete.html'
    context_object_name = 'object'
    success_url = reverse_lazy('handler:clients')

###STUDENTS###


def students(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    template_name = 'students.html'
    context = {
        'students': Student.objects.all(),
    }
    return render(request, template_name, context)


def student(request, student_id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    my_student = get_object_or_404(Student, pk=student_id)
    template_name = 'student.html'
    context = {
        'student': my_student,
        'attendances': Attendance.objects.filter(student=my_student)
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
            new.monthly_payment = form.cleaned_data['monthly_payment']
            new.first_month = form.cleaned_data['first_month']
            new.save()
            return HttpResponseRedirect(reverse_lazy('handler:students'))
    else:
        form = StudentForm()
    context = {
        'form': form,
        'title': "Nowe dziecko"

    }

    return render(request, template_name, context)


class StudentDeleteView(DeleteView):
    """
    class for deleting Student Object
    """
    model = Student
    template_name = 'delete.html'
    context_object_name = 'object'
    success_url = reverse_lazy('handler:students')


###GROUPS###


def groups(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    template_name = 'groups.html'
    context = {
        'groups': StudentGroup.objects.all(),
    }
    return render(request, template_name, context)


def group(request, group_id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

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


class GroupDeleteView(DeleteView):
    """
    class for deleting Student Object
    """
    model = StudentGroup
    template_name = 'delete.html'
    context_object_name = 'object'
    success_url = reverse_lazy('handler:groups')


###PAYMENTS###


def payments(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

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


class PaymentDeleteView(DeleteView):
    """
    class for deleting Student Object
    """
    model = Payment
    template_name = 'delete.html'
    context_object_name = 'object'
    success_url = reverse_lazy('handler:payments')


###ATENDANCE###
def attendance(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    template_name = 'attendance.html'
    context = {
        'groups': StudentGroup.objects.all(),
    }
    return render(request, template_name, context)


def check_attendance(request, group_id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    template_name = 'form.html'

    studs = []
    for stud in Student.objects.filter(group_id=group_id):
        studs.append(tuple([stud.id, stud]))

    if request.method == 'POST':
        form = AttendanceForm(request.POST, students=studs)
        if form.is_valid():
            present = []
            for present_stud in form.cleaned_data['presence']:
                temp_presence = Attendance()
                temp_presence.student = Student.objects.get(pk=present_stud)
                temp_presence.present = True
                temp_presence.date = form.cleaned_data['date']
                temp_presence.save_attendance()
                temp_presence.save()
                present.append(present_stud)
            for stud in Student.objects.filter(group_id=group_id):
                if stud.id not in present:
                    temp_absence = Attendance()
                    temp_absence.student = stud
                    temp_absence.present = False
                    temp_absence.date = form.cleaned_data['date']
                    temp_absence.save_attendance()
                    temp_absence.save()

            return HttpResponseRedirect(reverse_lazy('handler:attendance'))
    else:
        form = AttendanceForm(students=studs)
    context = {
        'form': form,
        'title': "Sprawdź obecność"

    }

    return render(request, template_name, context)
