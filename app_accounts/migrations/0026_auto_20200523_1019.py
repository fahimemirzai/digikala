# Generated by Django 2.2.12 on 2020-05-23 10:19

import app_accounts.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounts', '0025_auto_20200523_0705'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='newsletter_receive',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='national_code',
            field=models.CharField(max_length=10, null=True, validators=[django.core.validators.MinLengthValidator(10), app_accounts.models.validate_national_code]),
        ),
    ]
