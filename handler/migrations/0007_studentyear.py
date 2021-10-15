# Generated by Django 3.0.7 on 2021-10-13 23:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('handler', '0006_auto_20211002_1501'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monthly_payment', models.FloatField()),
                ('first_month', models.IntegerField()),
                ('present', models.IntegerField(default=0)),
                ('absent', models.IntegerField(default=0)),
                ('finished', models.BooleanField(default=False)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='handler.Student')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='handler.Year')),
            ],
        ),
    ]