# Generated by Django 2.2.12 on 2020-07-27 17:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounts', '0004_auto_20200725_0826'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='validation_code',
            field=models.CharField(max_length=4, null=True, validators=[django.core.validators.MinLengthValidator(4)]),
        ),
    ]