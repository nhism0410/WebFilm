# Generated by Django 5.0.4 on 2024-04-14 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chedule', '0010_remove_tapfilm_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='tapfilm',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
