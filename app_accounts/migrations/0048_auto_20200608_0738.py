# Generated by Django 2.2.12 on 2020-06-08 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounts', '0047_basket_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('favorites', 'favorites'), ('pardakht', 'pardakht'), ('pardakht-shod', 'pardakht-shod'), ('delivered', 'deliverd'), ('canceled', 'canceled')], max_length=30, null=True),
        ),
    ]