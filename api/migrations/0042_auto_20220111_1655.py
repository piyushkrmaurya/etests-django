# Generated by Django 3.0.3 on 2022-01-11 11:25

import api.models
from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0041_auto_20200724_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institute',
            name='carousel',
            field=jsonfield.fields.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='institute',
            name='centers',
            field=jsonfield.fields.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='institute',
            name='contacts',
            field=jsonfield.fields.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='institute',
            name='courses',
            field=jsonfield.fields.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='institute',
            name='downloads',
            field=jsonfield.fields.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='institute',
            name='extras',
            field=jsonfield.fields.JSONField(blank=True, default=api.models.Institute.extras_default, null=True),
        ),
        migrations.AlterField(
            model_name='institute',
            name='faculty',
            field=jsonfield.fields.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='institute',
            name='faqs',
            field=jsonfield.fields.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='institute',
            name='features',
            field=jsonfield.fields.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='institute',
            name='forms',
            field=jsonfield.fields.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='institute',
            name='gallery',
            field=jsonfield.fields.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='institute',
            name='links',
            field=jsonfield.fields.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='institute',
            name='notifications',
            field=jsonfield.fields.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='institute',
            name='questions',
            field=jsonfield.fields.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='institute',
            name='settings',
            field=jsonfield.fields.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='institute',
            name='team',
            field=jsonfield.fields.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='institute',
            name='toppers',
            field=jsonfield.fields.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='tags',
            field=jsonfield.fields.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='current',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='marks',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='ranks',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='response',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='result',
            field=jsonfield.fields.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='answers',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='marks_list',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='questions',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='sections',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='stats',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=api.models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]
