# Generated by Django 2.2.12 on 2020-07-19 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='total_discount_price',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
