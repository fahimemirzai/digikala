# Generated by Django 2.2.12 on 2020-08-06 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounts', '0010_auto_20200804_0618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_accounts.Address'),
        ),
        migrations.AlterField(
            model_name='basket',
            name='deliverydate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_accounts.DeliveryDate'),
        ),
    ]
