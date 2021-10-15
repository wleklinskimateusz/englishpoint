from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import now
import weekday_field

PAYMENT_DUE = 15


# Create your models here.

class Year(models.Model):
    starting_year = models.IntegerField(unique=True)
    selected = models.BooleanField(default=False)

    @staticmethod
    def get_selected():
        return Year.objects.filter(selected=True).first()

    def __str__(self):
        return f"{self.starting_year}/{self.starting_year + 1}"


class Parent(models.Model):
    first_name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    email = models.CharField(max_length=30, null=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    last_mail = models.DateField(null=True, blank=True)
    years = models.ManyToManyField(Year)

    def __str__(self):
        return f"{self.first_name} {self.surname}"

    def to_pay(self):
        output = 0
        kids = Student.objects.filter(parent=self.id)
        for kid in kids:
            if Year.get_selected() in kid.years.all():
                kid_year = kid.get_student_year()
                output += kid_year.monthly_payment * kid_year.past_months() - kid_year.corrections()
        return output

    def paid(self):
        output = 0
        payments = Payment.objects.filter(client=self.id, year=Year.get_selected())
        for payment in payments:
            output += payment.value
        return output

    def diff_to_pay(self):
        return self.to_pay() - self.paid()


class StudentGroup(models.Model):
    name = models.CharField(max_length=20)
    lesson_duration = models.DurationField()
    amount_lessons = models.IntegerField()
    year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, null=True)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    monthly_payment = models.FloatField(null=True)
    first_month = models.IntegerField(null=True)
    present = models.IntegerField(default=0)
    absent = models.IntegerField(default=0)
    years = models.ManyToManyField(Year)

    def __str__(self):
        return f"{self.first_name} {self.surname}"

    def corrections(self):
        output = 0
        for my_year in self.get_student_years():
            output += my_year.corrections()

    def get_student_years(self):
        return StudentYear.objects.filter(student=self).all()

    def get_student_year(self):
        return self.get_student_years().filter(year=Year.get_selected()).first()


class StudentYear(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    monthly_payment = models.FloatField()
    first_month = models.IntegerField()
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, null=True, blank=True)
    present = models.IntegerField(default=0)
    absent = models.IntegerField(default=0)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)

    def corrections(self):
        output = 0
        cors = Correction.objects.filter(kid=self.id, year=self.year)
        for cor in cors:
            output += cor.value
        return output

    def past_months(self):
        if self.finished:
            return 12 - self.first_month + 1 + 6
        if now().month >= 9:
            finished_months = now().month - self.first_month - 1
            if now().date().day > PAYMENT_DUE:
                finished_months += 1
        elif now().month <= 6:
            finished_months = 12 - self.first_month + now().month
            if now().date().day > PAYMENT_DUE:
                finished_months += 1
        else:
            finished_months = 13 - self.first_month + 6

        return finished_months

    def attendance(self):
        return 100 * self.present / (self.present + self.absent)

    def __str__(self) -> str:
        if not self.student or not self.year:
            return "Empty Student Year"
        return f"{self.student} in {self.year}"




class Payment(models.Model):
    client = models.ForeignKey(Parent, on_delete=models.CASCADE)
    value = models.FloatField()
    date = models.DateField(null=True, blank=True)
    comment = models.CharField(max_length=50, blank=True, null=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)

    def __str__(self):
        if self.comment:
            com = self.comment
        else:
            com = ""
        return f"{self.client} zapłacił: {self.value}zł, {self.date}, {com}"


class Attendance(models.Model):
    present = models.BooleanField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        if self.present:
            presence = "obecny"
        else:
            presence = 'nieobecny'
        return f"{self.student} był {presence}, {self.date}"

    def save_attendance(self):
        stud = Student.objects.get(pk=self.student.id)
        if self.present:
            stud.present += 1
        else:
            stud.absent += 1
        stud.save()


class Correction(models.Model):
    kid = models.ForeignKey(Student, on_delete=models.CASCADE)
    value = models.FloatField()
    date = models.DateField(null=True, blank=True)
    info = models.CharField(max_length=50, null=True, blank=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.kid} ma korektę {self.value}zł"


