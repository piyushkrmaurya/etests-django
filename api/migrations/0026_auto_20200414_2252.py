# Generated by Django 3.0.3 on 2020-04-14 17:22

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_auto_20200412_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='institute',
            name='contacts',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name='institute',
            name='faculty',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True),
        ),
    ]