# Generated by Django 2.2.12 on 2020-06-12 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounts', '0050_auto_20200612_0745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='address',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_accounts.Address'),
        ),
    ]
