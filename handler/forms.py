from django import forms
from phonenumber_field.formfields import PhoneNumberField as Phone
from .models import Parent, StudentGroup, Student
from django.utils.timezone import now

MONTHS = [
    (1, 'Styczeń'),
    (2, 'Luty'),
    (3, 'Marzec'),
    (4, 'Kwiecień'),
    (5, 'Maj'),
    (6, 'Czerwiec'),
    (9, 'Wrzesień'),
    (10, 'Październik'),
    (11, 'Listopad'),
    (12, 'Grudzień'),
]


class DateInput(forms.DateInput):
    input_type = 'date'


class ParentForm(forms.Form):
    first_name = forms.CharField(max_length=20, label="Imię")
    surname = forms.CharField(max_length=20, label="Nazwisko")
    email = forms.CharField(max_length=30, required=False)
    phone_number = Phone(required=False, label="numer telefonu")


class StudentGroupForm(forms.Form):
    name = forms.CharField(max_length=20, label="Nazwa Grupy")
    lesson_duration = forms.IntegerField(label="Czas trwania zajęć w minutach")
    amount_lessons = forms.IntegerField(label="Ilość zajęć")


class StudentForm(forms.Form):
    first_name = forms.CharField(max_length=20, label="Imię")
    surname = forms.CharField(max_length=20, label="Nazwisko")
    group = forms.ModelChoiceField(StudentGroup.objects.all(), label="Grupa")
    parent = forms.ModelChoiceField(Parent.objects.all(), label="Rodzic")
    birthday = forms.DateField(required=False, widget=DateInput, label="Urodziny")
    first_month = forms.ChoiceField(choices=MONTHS, initial=9, label='Pierwszy miesiąc')
    monthly_payment = forms.FloatField(label="Miesięczna należność")


class PaymentForm(forms.Form):
    client = forms.ModelChoiceField(Parent.objects.all(), label='Rodzic')
    value = forms.FloatField(label="Wartość")
    date = forms.DateField(required=False, widget=DateInput, label='Data')
    comment = forms.CharField(max_length=50, required=False, label='Komentarz')

class CorrectionForm(forms.Form):
    kid = forms.ModelChoiceField(Student.objects.all(), label="Uczeń")
    value = forms.FloatField(label="Kwota")
    date = forms.DateField(required=False, widget=DateInput, label='Data')
    info = forms.CharField(max_length=50, required=False, label='Komentarz')


class AttendanceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        students = kwargs.pop('students')
        super(AttendanceForm, self).__init__(*args, **kwargs)
        self.fields['presence'] = forms.TypedMultipleChoiceField(
            choices=students,
            coerce=int,
            label="Uczniowie"
        )
    date = forms.DateTimeField(initial=now(), label="data")


class SendMailForm(forms.Form):
    subject = forms.CharField(max_length=20, label="Temat")
    message = forms.CharField(widget=forms.Textarea, label="Wiadmość")
    send_copy_to_me = forms.BooleanField(initial=True, required=False, label="Wyślij kopię do mnie")

