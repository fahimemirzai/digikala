# Generated by Django 2.2.12 on 2020-04-27 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounts', '0002_auto_20200427_0426'),
    ]

    operations = [
        migrations.AddField(
            model_name='basketitem',
            name='basket',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_accounts.Basket'),
        ),
    ]
