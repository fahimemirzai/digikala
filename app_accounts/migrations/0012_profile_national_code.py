# Generated by Django 2.2.12 on 2020-05-12 06:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounts', '0011_address_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='national_code',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
