# Generated by Django 2.2.12 on 2020-05-01 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounts', '0008_auto_20200501_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('no active', 'no active')], max_length=10, null=True),
        ),
    ]
