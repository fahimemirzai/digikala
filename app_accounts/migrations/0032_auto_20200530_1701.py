# Generated by Django 2.2.12 on 2020-05-30 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounts', '0031_auto_20200530_0830'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='dislike',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='like',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
