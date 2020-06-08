# Generated by Django 2.2.12 on 2020-06-03 07:28

import app_accounts.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounts', '0038_auto_20200602_0724'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='reciver_first_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='reciver_last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='reciver_national_code',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.MinLengthValidator(10), app_accounts.models.validate_national_code]),
        ),
    ]