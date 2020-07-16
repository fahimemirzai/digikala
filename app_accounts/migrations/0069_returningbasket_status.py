# Generated by Django 2.2.12 on 2020-06-25 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounts', '0068_returningdate_returning_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='returningbasket',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('canceled', 'canceled'), ('accepted', 'accepted'), ('received', 'received')], max_length=10, null=True),
        ),
    ]
