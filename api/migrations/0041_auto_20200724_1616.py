# Generated by Django 3.0.2 on 2020-07-24 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0040_institute_extras'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institute',
            name='handle',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
