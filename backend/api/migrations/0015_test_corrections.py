# Generated by Django 2.2.1 on 2019-09-06 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20190906_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='corrections',
            field=models.BooleanField(default=False),
        ),
    ]