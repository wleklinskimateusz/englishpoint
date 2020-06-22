from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import weekday_field

# Create your models here.


class Parent(models.Model):
    first_name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    email = models.CharField(max_length=30, null=True)
    phone_number = PhoneNumberField()


class StudentGroup(models.Model):
    name = models.CharField(max_length=20)
    lesson_time = models.DurationField()
    amount_lessons = models.IntegerField()
    #lesson1 = weekday_field.Weekday_field()


class Student(models.Model):
    first_name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)


