# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-29 21:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblios', '0006_auto_20170325_0019'),
    ]

    operations = [
        migrations.CreateModel(
            name='Home',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name=b'Tytu\xc5\x82')),
                ('content', models.CharField(max_length=1000, verbose_name=b'Zawarto\xc5\x9b\xc4\x87')),
            ],
            options={
                'verbose_name': 'Home',
            },
        ),
    ]
