# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-10 13:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lettertype',
            name='uploader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.Customer'),
        ),
        migrations.AddField(
            model_name='letter',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Customer'),
        ),
        migrations.AddField(
            model_name='letter',
            name='letter_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.LetterType'),
        ),
        migrations.AddField(
            model_name='fieldvalue',
            name='field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Field'),
        ),
        migrations.AddField(
            model_name='fieldvalue',
            name='letter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Letter'),
        ),
        migrations.AddField(
            model_name='dispatch',
            name='letter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Letter'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='dispatch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Dispatch'),
        ),
    ]