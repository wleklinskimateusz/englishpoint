# Generated by Django 3.0.7 on 2020-11-27 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handler', '0004_auto_20201127_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
