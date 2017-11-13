# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-10 16:42
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True)),
                ('homepage', models.URLField(blank=True, null=True)),
                ('license', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gepetto_packages.License')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Repo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('url', models.URLField(unique=True)),
                ('homepage', models.URLField(blank=True, null=True)),
                ('default_branch', models.CharField(max_length=50)),
                ('open_issues', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('open_pr', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('license', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gepetto_packages.License')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gepetto_packages.Package')),
            ],
            options={
                'ordering': ('package', 'url'),
            },
        ),
        migrations.AddField(
            model_name='package',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gepetto_packages.Project'),
        ),
    ]
