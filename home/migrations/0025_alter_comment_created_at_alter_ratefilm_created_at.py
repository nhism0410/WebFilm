# Generated by Django 5.0.3 on 2024-04-18 09:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_alter_comment_created_at_alter_ratefilm_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 18, 9, 39, 32, 531390, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='ratefilm',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 18, 9, 39, 32, 531390, tzinfo=datetime.timezone.utc)),
        ),
    ]
