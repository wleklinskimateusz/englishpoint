from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import now
import weekday_field

# Create your models here.


class Parent(models.Model):
    first_name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    email = models.CharField(max_length=30, null=True)
    phone_number = PhoneNumberField()

    def __str__(self):
        return self.surname


class StudentGroup(models.Model):
    name = models.CharField(max_length=20)
    lesson_duration = models.DurationField()
    amount_lessons = models.IntegerField()


class Student(models.Model):
    first_name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.surname}"


class Payment(models.Model):
    Client = models.ForeignKey(Parent, on_delete=models.CASCADE)
    Value = models.FloatField()
    Date = models.DateField(default=now().day)
    comment = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        if self.comment:
            com = self.comment
        else:
            com = ""
        return f"{self.Client} payed {self.Date}, {com}"


