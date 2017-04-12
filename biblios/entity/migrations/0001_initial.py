# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-15 14:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Adress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[(b'N', b'Nieaktywny'), (b'A', b'Aktywny')], max_length=1, verbose_name=b'Status')),
                ('street', models.CharField(max_length=128, verbose_name=b'Ulica')),
                ('zip_code', models.CharField(default=b'00000', max_length=5, verbose_name=b'Kod pocztowy')),
                ('city', models.CharField(max_length=50, verbose_name=b'Miasto')),
                ('state', models.CharField(max_length=50, verbose_name='Wojew\xf3dztwo')),
            ],
        ),
        migrations.CreateModel(
            name='Biblioteka',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'Biblioteka', max_length=200, verbose_name=b'Nazwa instytucji')),
                ('phone', models.CharField(default=b'+48123456789', max_length=10, verbose_name=b'Telefon')),
                ('published', models.DateTimeField(verbose_name=b'Data wprowadzenia')),
                ('url', models.URLField(default=b'https://', verbose_name=b'Strona internetowa')),
                ('type', models.CharField(choices=[(b'P', b'Pbliczna'), (b'N', b'Naukowa')], max_length=1, verbose_name=b'Typ biblioteki')),
                ('chain', models.CharField(choices=[(b'P', b'Pbliczna'), (b'N', b'Naukowa')], max_length=1, verbose_name='Sie\u0107 bibliotek')),
                ('owner', models.CharField(max_length=100, verbose_name=b'Organizator')),
                ('siglum', models.CharField(default=b'WA N', max_length=15, verbose_name=b'Siglum')),
                ('notes', models.TextField(verbose_name=b'Uwagi')),
                ('slug', models.SlugField()),
                ('adres', models.ManyToManyField(to='entity.Adress')),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[(b'N', b'Nieaktywny'), (b'A', b'Aktywny')], max_length=1, verbose_name=b'Status')),
                ('email', models.EmailField(max_length=254, verbose_name=b'adres e-mail')),
            ],
        ),
        migrations.AddField(
            model_name='biblioteka',
            name='email',
            field=models.ManyToManyField(to='entity.Email'),
        ),
    ]