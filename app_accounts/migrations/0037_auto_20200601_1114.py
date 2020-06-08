# Generated by Django 2.2.12 on 2020-06-01 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounts', '0036_auto_20200531_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='count_dislike',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='count_like',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='most_liked',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
