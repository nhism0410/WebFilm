# Generated by Django 5.0 on 2024-04-04 04:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='tenfilm',
        ),
    ]
