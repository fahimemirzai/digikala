# Generated by Django 2.2.12 on 2020-06-06 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounts', '0045_auto_20200606_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='order_registration_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]