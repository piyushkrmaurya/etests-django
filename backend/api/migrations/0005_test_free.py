# Generated by Django 2.2.1 on 2019-11-01 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20191022_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='free',
            field=models.BooleanField(default=False),
        ),
    ]
