# Generated by Django 5.0.4 on 2024-04-15 09:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_alter_userprofile_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='MuaGoi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tengoi', models.CharField(max_length=100)),
                ('giagoi', models.DecimalField(decimal_places=2, max_digits=10)),
                ('thoihan', models.CharField(max_length=100)),
                ('phuongthucthanhtoan', models.CharField(max_length=100)),
                ('ngaymuagoi', models.DateTimeField(auto_now_add=True)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.userprofile')),
            ],
        ),
    ]
