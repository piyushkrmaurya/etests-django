# Generated by Django 2.2.1 on 2019-09-25 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20190925_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institute',
            name='pincode',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
