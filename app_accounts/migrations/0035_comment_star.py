# Generated by Django 2.2.12 on 2020-05-31 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounts', '0034_auto_20200531_0807'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='star',
            field=models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1, null=True),
        ),
    ]