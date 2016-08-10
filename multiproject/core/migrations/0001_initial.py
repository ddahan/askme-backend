# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-10 13:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('file', models.FileField(upload_to='')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Dispatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('from_address', models.CharField(max_length=1024)),
                ('to_address', models.CharField(max_length=1024)),
                ('status', models.CharField(choices=[('CREATED', 'Demande créée'), ('GENERATION_STARTED', 'Génération PDF démarée'), ('GENERATION_FINISHED', 'Génération PDF terminée')], max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=128, verbose_name='Nom')),
                ('slug', models.SlugField(max_length=128, verbose_name='Slug')),
                ('description', models.CharField(blank=True, max_length=2048, verbose_name='Description (aide)')),
                ('default_value', models.CharField(blank=True, max_length=2048, verbose_name='Défaut')),
                ('choices', models.TextField(blank=True, verbose_name='Choix')),
                ('max_size', models.PositiveIntegerField(default=2048)),
                ('field_type', models.CharField(choices=[('SHORT_TEXT', 'Short Text'), ('LONG_TEXT', 'Long Text'), ('INTEGER', 'Integer'), ('SIMPLE_CHOICE', 'Simple Choice'), ('MULTI_CHOICE', 'Multiple Choice'), ('DATE', 'Date'), ('TIME', 'Time'), ('DATETIME', 'DateTime')], max_length=256)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FieldValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('value', models.CharField(max_length=1024, verbose_name='Valeur')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LetterType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('html_template', models.FilePathField(max_length=1024, path='html_templates/', recursive=True)),
                ('default_to_address', models.CharField(max_length=1024, verbose_name='Adresse du destinataire')),
                ('description', models.CharField(max_length=1024, verbose_name='Description')),
                ('purpose', models.CharField(choices=[('RESILIATION', 'Résiliation'), ('INFORMATION', 'Information'), ('OTHER', 'Autre')], max_length=256)),
                ('url', models.CharField(blank=True, max_length=2048, verbose_name='Site officiel')),
                ('fields', models.ManyToManyField(to='core.Field')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Marque')),
                ('website', models.CharField(blank=True, max_length=2048, verbose_name='Site officiel')),
                ('logo', models.FilePathField(blank=True, path='/some/path/where/logos/will/be')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='lettertype',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Organization'),
        ),
    ]