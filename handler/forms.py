from django import forms
from phonenumber_field.formfields import PhoneNumberField as Phone
from .models import Parent, StudentGroup
from django.utils.timezone import now


class DateInput(forms.DateInput):
    input_type = 'date'


class ParentForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    surname = forms.CharField(max_length=20)
    email = forms.CharField(max_length=30, required=False)
    phone_number = Phone(required=False)


class StudentGroupForm(forms.Form):
    name = forms.CharField(max_length=20)
    lesson_duration = forms.DurationField()
    amount_lessons = forms.IntegerField()


class StudentForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    surname = forms.CharField(max_length=20)
    group = forms.ModelChoiceField(StudentGroup.objects.all())
    parent = forms.ModelChoiceField(Parent.objects.all())
    birthday = forms.DateField(required=False, widget=DateInput)


class PaymentForm(forms.Form):
    client = forms.ModelChoiceField(Parent.objects.all())
    value = forms.FloatField()
    date = forms.DateField(required=False, widget=DateInput)
    comment = forms.CharField(max_length=50, required=False)


class AttendanceForm(forms.Form):
    def __init__(self, students, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)
        self.fields['presence'] = forms.TypedMultipleChoiceField(
            choices=students,
            coerce=int
        )
    date = forms.DateTimeField(initial=now())

