# Generated by Django 2.2.1 on 2019-09-25 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
