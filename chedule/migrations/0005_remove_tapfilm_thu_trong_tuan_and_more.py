# Generated by Django 4.1.7 on 2024-04-06 07:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chedule', '0004_tapfilm_thu_trong_tuan_alter_tapfilm_ngaychieu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tapfilm',
            name='thu_trong_tuan',
        ),
        migrations.AlterField(
            model_name='tapfilm',
            name='ngaychieu',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 6, 14, 32, 43, 156103)),
        ),
    ]