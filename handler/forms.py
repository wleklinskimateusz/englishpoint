from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import *


class ParentForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    surname = forms.CharField(max_length=20)
    email = forms.CharField(max_length=30, required=False)
    phone_number = PhoneNumberField(required=False)


class StudentGroup(forms.Form):
    name = forms.CharField(max_length=20)
    lesson_duration = forms.DurationField()
    amount_lessons = forms.IntegerField()


class StudentForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    surname = forms.CharField(max_length=20)
    group = forms.ModelChoiceField(StudentGroup)
    parent = forms.ModelChoiceField(Parent)
    birthday = forms.DateField(required=False)


class PaymentForm(forms.Form):
    client = forms.ModelChoiceField(Parent)
    value = forms.FloatField()
    date = forms.DateField(required=False)
    comment = forms.CharField(max_length=50, required=False)
