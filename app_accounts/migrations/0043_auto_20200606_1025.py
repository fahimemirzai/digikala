# Generated by Django 2.2.12 on 2020-06-06 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounts', '0042_auto_20200606_0730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='order_registration_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]