# Generated by Django 5.0.4 on 2024-04-13 13:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_film_views_alter_comment_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='follow',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 13, 13, 19, 33, 889324, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='ratefilm',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 13, 13, 19, 33, 889324, tzinfo=datetime.timezone.utc)),
        ),
    ]
