# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-16 18:07
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DjangoBaseNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('path', models.CharField(max_length=1000, verbose_name='path')),
                ('scope', models.CharField(default='miniref', max_length=1000, verbose_name='scope')),
                ('version', models.CharField(default='0.1', max_length=1000, verbose_name='schema version')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='last modified')),
                ('comment', models.TextField(blank=True, default='', verbose_name='comment')),
            ],
        ),
    ]
