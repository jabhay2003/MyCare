# Generated by Django 4.1.3 on 2024-03-14 04:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0003_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='date',
            field=models.DateField(default=datetime.datetime.today, verbose_name='Date'),
        ),
    ]
