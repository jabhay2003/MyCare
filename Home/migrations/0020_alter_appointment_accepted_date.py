# Generated by Django 5.0.2 on 2024-03-28 13:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0019_alter_appointment_accepted_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='accepted_date',
            field=models.DateTimeField(default=datetime.datetime.today, verbose_name='Date'),
        ),
    ]
