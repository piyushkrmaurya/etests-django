# Generated by Django 3.0.3 on 2020-04-05 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institute',
            name='handle',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
