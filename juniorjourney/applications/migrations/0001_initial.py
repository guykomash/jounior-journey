# Generated by Django 5.0.6 on 2024-06-11 14:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=75, verbose_name='Company')),
                ('role', models.CharField(max_length=75, verbose_name='Role')),
                ('job_description', models.TextField(verbose_name='Description')),
                ('applied_date', models.DateTimeField(auto_now_add=True, verbose_name='Applied at')),
                ('status', models.CharField(choices=[('applied', 'Applied'), ('interview', 'Interview'), ('offer', 'Offer'), ('rejected', 'Rejected')], default='applied', max_length=50, verbose_name='Status')),
                ('resume', models.FileField(upload_to='resumes/', verbose_name='Resume')),
                ('author', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-applied_date'],
            },
        ),
    ]