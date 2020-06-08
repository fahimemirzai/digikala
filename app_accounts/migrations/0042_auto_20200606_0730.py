# Generated by Django 2.2.12 on 2020-06-06 07:30

import app_accounts.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounts', '0041_address_reciver_cellphone'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='order_number',
            field=models.CharField(blank=True, max_length=13, null=True, validators=[django.core.validators.MinLengthValidator(13), app_accounts.models.validate_order_number]),
        ),
        migrations.AddField(
            model_name='basket',
            name='order_registration_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='basket',
            name='total_price',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='basket',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('favorites', 'favorites'), ('delivered', 'deliverd'), ('canceled', 'canceled'), ('current', 'current')], max_length=15, null=True),
        ),
    ]
