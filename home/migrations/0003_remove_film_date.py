# Generated by Django 5.0 on 2024-04-04 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_film_theloai'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='film',
            name='date',
        ),
    ]