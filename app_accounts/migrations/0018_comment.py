# Generated by Django 2.2.12 on 2020-05-21 15:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_accounts', '0017_auto_20200516_2026'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('write_date', models.DateField(null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('viewpoint', models.TextField(max_length=2000, null=True)),
                ('strengths', models.TextField(blank=True, max_length=1000, null=True)),
                ('weak_points', models.TextField(blank=True, max_length=1000, null=True)),
                ('buyer', models.BooleanField(default=False, null=True)),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]