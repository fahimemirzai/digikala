# Generated by Django 2.2.12 on 2020-07-25 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounts', '0003_auto_20200719_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='returningbasket',
            name='returning_date',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_accounts.ReturningDate'),
        ),
    ]
