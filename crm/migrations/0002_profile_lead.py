# Generated by Django 4.2.2 on 2023-06-10 01:52

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=30)),
                ('bio', models.CharField(max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.CharField(blank=True, max_length=60, null=True)),
                ('contact_num', models.IntegerField(blank=True, null=True, verbose_name='Contact Number')),
                ('touches', models.IntegerField(blank=True, null=True)),
                ('last_contacted', models.DateField(blank=True, null=True)),
                ('date_created', models.DateField(default=datetime.date.today)),
                ('status', models.CharField(blank=True, choices=[('New Lead', 'New Lead'), ('Won', 'Won'), ('Lost', 'Lost'), ('Follow Up', 'Follow Up')], max_length=20, null=True)),
                ('intent', models.CharField(blank=True, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], max_length=20, null=True)),
                ('notes', models.CharField(blank=True, max_length=200, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
