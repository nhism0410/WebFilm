# Generated by Django 5.0.4 on 2024-04-14 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chedule', '0011_tapfilm_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tapfilm',
            name='views',
        ),
        migrations.AddField(
            model_name='tapfilm',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]
