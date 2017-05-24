# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-24 07:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('file', models.ImageField(upload_to='challenges')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('key', models.CharField(max_length=256)),
                ('points', models.IntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='challenges', to='challenges.Category')),
            ],
        ),
        migrations.CreateModel(
            name='ChallengeFail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challenges.Challenge')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChallengeSolved',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challenges.Challenge')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hints', to='challenges.Challenge')),
            ],
        ),
        migrations.AddField(
            model_name='challenge',
            name='failed_by',
            field=models.ManyToManyField(related_name='failed_challenges', through='challenges.ChallengeFail', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='challenge',
            name='solved_by',
            field=models.ManyToManyField(related_name='solved_challenges', through='challenges.ChallengeSolved', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attachment',
            name='challenge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='challenges.Challenge'),
        ),
        migrations.AlterUniqueTogether(
            name='hint',
            unique_together=set([('challenge', 'text')]),
        ),
    ]
