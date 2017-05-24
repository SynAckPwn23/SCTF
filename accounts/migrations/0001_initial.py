# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-24 07:40
from __future__ import unicode_literals

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities_light', '0006_compensate_for_0003_bytestring_bug'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            bases=(models.Model, accounts.models.StatsFromChallengesMixin),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.FileField(default='accounts/user.png', upload_to='accounts/')),
                ('job', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('website', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cities_light.Country')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Team')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, accounts.models.StatsFromChallengesMixin),
        ),
        migrations.AddField(
            model_name='team',
            name='users',
            field=models.ManyToManyField(through='accounts.UserProfile', to=settings.AUTH_USER_MODEL),
        ),
    ]
