# Generated by Django 2.2.12 on 2020-08-03 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounts', '0006_auto_20200727_1841'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='birth_date',
            new_name='_birth_date',
        ),
    ]