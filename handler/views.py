from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from django.forms import Form
from .models import *
from .forms import AddYearStudent, StudentForm, StudentGroupForm, ParentForm, PaymentForm, AttendanceForm, SendMailForm, CorrectionForm
from django.core.mail import send_mail
from datetime import timedelta
from django.http import JsonResponse
from django.db.models import Q


def add_context(orig: dict, search: bool = True) -> dict:
    output = orig
    output['selected_year'] = Year.get_selected()
    output['can_prev'] = output['selected_year'].starting_year != Year.objects.first().starting_year
    output['can_next'] = output['selected_year'].starting_year != Year.objects.last().starting_year
    output['searchbar'] = search
    return output


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
    year = Year.get_selected()
    clients = []
    for client in Parent.objects.all():
        if year in client.years.all():
            clients.append(client)
    context = add_context({
        'clients': clients,
        'searchbar': True
    })
    return render(request, template_name, context)


def clients_overdue(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    template_name = 'clients_overdue.html'

    overdues = []
    for parent in Parent.objects.all():
        if parent.diff_to_pay() > 0 and Year.get_selected() in parent.years.all():
            overdues.append(parent)

    if request.method == "POST":
        form = Form(request.POST)
        if form.is_valid():
            for parent in overdues:
                send_mail(
                    "EnglishPoint - zaległość",
                    f"""Dzień dobry,
uprzejmię informuję, że zalega Pan/Pani z płatnością za usługi edukacyjne firmy EnglishPoint w wysokości: {parent.diff_to_pay()}.
W razie pytań proszę o kontakt.

Wiadomość została wygenerowana automatycznie, proszę na nią nie odpowiadać.
\tEnglishPoint Tychy""",
                    "academia@englishpoint.tychy.pl",
                    [parent.email]
                )
                parent.last_mail = now().date()
                parent.save()

            return HttpResponseRedirect(reverse_lazy('handler:payments'))
    else:
        form = Form()
    context = add_context({
        'clients': overdues,
        'form': form,
    })

    return render(request, template_name, context)


def client(request, client_id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    my_client = get_object_or_404(Parent, pk=client_id)
    template_name = 'client.html'
    kids = []
    for kid in Student.objects.filter(parent=my_client):
        if Year.get_selected() in kid.years.all():
            kids.append(kid)
    context = add_context({
        'client': my_client,
        'kids': kids,
        'haventpaid': my_client.diff_to_pay() > 0,
    })
    return render(request, template_name, context)


def new_client(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    template_name = 'form.html'
    if request.method == 'POST':
        form = ParentForm(request.POST)
        if form.is_valid():
            new = Parent()
            new.save()
            new.years.add(Year.get_selected())
            new.first_name = form.cleaned_data['first_name']
            new.surname = form.cleaned_data['surname']
            new.email = form.cleaned_data['email']
            new.phone_number = form.cleaned_data['phone_number']
            new.save()
            return HttpResponseRedirect(reverse_lazy('handler:clients'))
    else:
        form = ParentForm()
    context = add_context({
        'form': form,
        'title': "Nowy Rodzic"

    })

    return render(request, template_name, context)


def mail_to_client(request, client_id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    template_name = "client.html"

    my_client = get_object_or_404(Parent, pk=client_id)
    if request.method == 'POST':
        form = SendMailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            recipients = [my_client.email]
            if form.cleaned_data['send_copy_to_me']:
                if request.user.email:
                    recipients.append(request.user.email)
            send_mail(subject, message, 'englishpointacademia@gmail.com', recipients)

            return HttpResponseRedirect(reverse_lazy('handler:clients'))
    else:
        form = SendMailForm()
    kids = Student.objects.filter(parent=my_client)
    context = add_context({
        'client': my_client,
        'kids': kids,
        'haventpaid': my_client.diff_to_pay() > 0,
        'form': form,
    })
    return render(request, template_name, context)


class ClientDeleteView(DeleteView):
    """
    class for deleting GoGame Object
    """
    model = Parent
    template_name = 'delete.html'
    context_object_name = 'object'
    success_url = reverse_lazy('handler:clients')


def client_update(request, pk):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    my_client = get_object_or_404(Parent, pk=pk)
    template_name = 'form.html'
    if request.method == 'POST':
        form = ParentForm(request.POST)
        if form.is_valid():
            my_client.first_name = form.cleaned_data['first_name']
            my_client.surname = form.cleaned_data['surname']
            my_client.email = form.cleaned_data['email']
            my_client.phone_number = form.cleaned_data['phone_number']
            my_client.save()
            return HttpResponseRedirect(reverse_lazy('handler:client', kwargs={"client_id": my_client.id}))
    else:
        form = ParentForm()
    context = add_context({
        'form': form,
        'title': "Edytuj dane"

    })

    return render(request, template_name, context)


class ClientUpdate(UpdateView):
    model = Parent
    template_name = 'form.html'
    fields = [
        'first_name',
        'surname',
        'email',
        'phone_number'
    ]

    def get_success_url(self):
        return reverse_lazy('handler:client', kwargs={'client_id': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        return add_context(super().get_context_data(**kwargs))

def add_year_client(request, parent_id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    
    parent = Parent.objects.get(parent_id)
    parent.years.add(Year.objects.filter(starting_year=2021))
    parent.save()


###STUDENTS###


def students(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    template_name = 'students.html'
    students = []
    for student in Student.objects.all():
        if Year.get_selected() in student.years.all():
            students.append(student)
    context = add_context({
        'students': students,
        'searchbar': True
    })
    return render(request, template_name, context)


def student(request, student_id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    my_student = get_object_or_404(Student, pk=student_id)
    template_name = 'student.html'
    context = add_context({
        'student': my_student,
        'studentYear': my_student.get_student_year(),
        'attendances': Attendance.objects.filter(student=my_student),
    })
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
            new.parent = form.cleaned_data['parent']
            new.birthday = form.cleaned_data['birthday']
            new.save()
            new.years.add(Year.get_selected())
            new.save()
            print("New student Saved")
            new_year = StudentYear()
            
            print("New year created")
            new_year.year = Year.get_selected()
            
            
            new_year.group = form.cleaned_data['group']
            
            new_year.monthly_payment = form.cleaned_data['monthly_payment']
            new_year.first_month = form.cleaned_data['first_month']
            new_year.student = new
            print(new_year)
            new_year.save()
            print("new year saved")
            return HttpResponseRedirect(reverse_lazy('handler:students'))
    else:
        form = StudentForm()
    context = add_context({
        'form': form,
        'title': "Nowe dziecko"

    })

    return render(request, template_name, context)


class StudentDeleteView(DeleteView):
    """
    class for deleting Student Object
    """
    model = Student
    template_name = 'delete.html'
    context_object_name = 'object'
    success_url = reverse_lazy('handler:students')


class StudentUpdate(UpdateView):
    model = Student
    template_name = 'form.html'
    fields = [
        'first_name',
        'surname',
        'parent',
        'birthday',
        'years'
    ]

    def get_success_url(self):
        return reverse_lazy('handler:student', kwargs={'student_id': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        return add_context(super().get_context_data(**kwargs))

def student_add_year(request, student_id, starting_year):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    student = Student.objects.get(student_id)
    if Year.selected_year() not in student.years.all():
        form = AddYearStudent(initial={'student': student.id})
        return render(request, 'form.html', add_context({'form': form, 'action': reverse_lazy('')}))

def student_add_year_form(request):
    form = AddYearStudent(request.POST)
    if form.is_valid():
        student = Student.objects.get(form.cleaned_data['student'])
        year = Year.objects.filter(starting_year=2021)
        student.years.add(year)
        student.save()
        student_year = StudentYear()
        student_year.student = student
        student_year.year = year
        student_year.group = form.cleaned_data['group']
        student_year.first_month = form.cleaned_data['first_month']
        student_year.monthly_payment = form.cleaned_data['monthly_payment']
        student_year.save()
        return redirect(reverse_lazy('handle:student', {'student_id': student.id}))


###GROUPS###


def groups(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    template_name = 'groups.html'
    context = add_context({
        'groups': StudentGroup.objects.filter(year=Year.get_selected()),
        'searchbar': True
    })
    return render(request, template_name, context)


def group(request, group_id):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    my_group = get_object_or_404(StudentGroup, pk=group_id)
    template_name = 'group.html'
    context = add_context({
        'group': my_group,
        'students': StudentYear.objects.filter(group=my_group),
        'minutes': my_group.lesson_duration.seconds / 60,
    })
    return render(request, template_name, context)


def new_group(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    template_name = 'form.html'
    if request.method == 'POST':
        form = StudentGroupForm(request.POST)
        if form.is_valid():
            new = StudentGroup()
            new.year = Year.get_selected()
            new.name = form.cleaned_data['name']
            new.lesson_duration = timedelta(minutes=form.cleaned_data['lesson_duration'])
            new.amount_lessons = form.cleaned_data['amount_lessons']
            new.save()
            return HttpResponseRedirect(reverse_lazy('handler:groups'))
    else:
        form = StudentGroupForm()
    context = add_context({
        'form': form,
        'title': "Nowa grupa"

    })

    return render(request, template_name, context)



class GroupDeleteView(DeleteView):
    """
    class for deleting StudentGroup Object
    """
    model = StudentGroup
    template_name = 'delete.html'
    context_object_name = 'object'
    success_url = reverse_lazy('handler:groups')


class GroupUpdate(UpdateView):
    model = StudentGroup
    template_name = 'form.html'
    fields = [
        'name',
        'lesson_duration',
        'amount_lessons',
        'year'
    ]
    extra_context = add_context({'title': "Edycja Grupy"})

    def get_success_url(self):
        return reverse_lazy('handler:group', kwargs={'group_id': self.kwargs['pk']})


###PAYMENTS###


def payments(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    template_name = 'payments.html'
    context = add_context({
        'payments': Payment.objects.filter(year=Year.get_selected()),
        'searchbar': True
    })
    return render(request, template_name, context)


def new_payment(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    template_name = 'form.html'
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            new = Payment()
            new.year = Year.get_selected()
            new.client = form.cleaned_data['client']
            new.value = form.cleaned_data['value']
            new.date = form.cleaned_data['date']
            new.comment = form.cleaned_data['comment']
            new.save()
            return HttpResponseRedirect(reverse_lazy('handler:payments'))
    else:
        form = PaymentForm()
    context = add_context({
        'form': form,
        'title': "Nowa płatność"

    })

    return render(request, template_name, context)


class PaymentDeleteView(DeleteView):
    """
    class for deleting Student Object
    """
    model = Payment
    template_name = 'delete.html'
    context_object_name = 'object'
    success_url = reverse_lazy('handler:payments')


###CORRECTION###
def corrections(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    template_name = 'corrections.html'
    context = add_context({
        'cors': Correction.objects.filter(year=Year.get_selected()),
        'searchbar': True
    })
    return render(request, template_name, context)


def new_correction(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    template_name = 'form.html'
    if request.method == 'POST':
        form = CorrectionForm(request.POST)
        if form.is_valid():
            new = Correction()
            new.year = Year.get_selected()
            new.kid = form.cleaned_data['kid']
            new.value = form.cleaned_data['value']
            new.date = form.cleaned_data['date']
            new.info = form.cleaned_data['info']
            new.save()
            return HttpResponseRedirect(reverse_lazy('handler:corrections'))
    else:
        form = CorrectionForm()
    context = add_context({
        'form': form,
        'title': "Nowa korekta"

    })

    return render(request, template_name, context)


###ATENDANCE###
def attendance(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    template_name = 'attendance.html'
    context = add_context({
        'groups': StudentGroup.objects.all(),
        'searchbar': True
    })
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
    context = add_context({
        'form': form,
        'title': "Sprawdź obecność"

    })

    return render(request, template_name, context)


def next_year(request):
    old_year = Year.get_selected()
    old_year.selected = False
    old_year.save()
    new_year = Year.objects.filter(starting_year=old_year.starting_year + 1).first()
    new_year.selected = True
    new_year.save()
    # return JsonResponse({"Success": "Year changed to next"})
    return redirect(reverse_lazy('handler:home'))


def previous_year(request):
    old_year = Year.get_selected()
    old_year.selected = False
    old_year.save()
    new_year = Year.objects.filter(starting_year=old_year.starting_year - 1).first()
    new_year.selected = True
    new_year.save()
    # return JsonResponse({"Success": "Year changed to previous"})
    return redirect(reverse_lazy('handler:home'))


def search(request):
    query = request.GET.get('search')
    if query:
        students = Student.objects.filter(Q(first_name__contains=query) | Q(surname__contains=query))
        parents = Parent.objects.filter(Q(first_name__contains=query) | Q(surname__contains=query))
        groups = StudentGroup.objects.filter(name__contains=query)
    else: 
        students, parents, groups = [], [], []

    return render(request, 'search.html', add_context({
        'students': students,
        'parents': parents,
        'groups': groups,
        }))

def update_db(request):
    year2020 = Year.objects.filter(starting_year=2020).first()
    for student in Student.objects.all():
        student.years.add(year2020)
        student_year = StudentYear()
        student_year.year = year2020
        student_year.monthly_payment = student.monthly_payment
        student_year.first_month = student.first_month
        student_year.group = student.group
        student_year.student = student
        student_year.finished = True
        student_year.save()
        student.save()
    
    for client in Parent.objects.all():
        client.years.add(year2020)
        client.save()

    for group in StudentGroup.objects.all():
        group.year = year2020
        group.save()
    
    for payment in Payment.objects.all():
        payment.year = year2020
        payment.save()

    for correction in Correction.objects.all():
        correction.year = year2020
        correction.save()

    return JsonResponse({"success": "Completed"})

