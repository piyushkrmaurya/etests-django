# Generated by Django 3.0.3 on 2020-04-12 14:48

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='institute',
            name='centers',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True),
        ),
    ]