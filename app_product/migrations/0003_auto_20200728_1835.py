# Generated by Django 2.2.12 on 2020-07-28 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_product', '0002_auto_20200728_1830'),
    ]

    operations = [
        migrations.RenameField(
            model_name='color',
            old_name='colors',
            new_name='color',
        ),
    ]
