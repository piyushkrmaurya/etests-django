# Generated by Django 2.2.1 on 2019-09-21 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='object_id',
        ),
    ]
