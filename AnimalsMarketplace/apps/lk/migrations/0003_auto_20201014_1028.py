# Generated by Django 3.0.7 on 2020-10-14 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lk', '0002_profile_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, verbose_name='Фамилия'),
        ),
    ]
