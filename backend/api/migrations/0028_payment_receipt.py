# Generated by Django 2.2.1 on 2019-09-21 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_auto_20190921_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='receipt',
            field=models.FileField(default='static/images/receipts/Invoice,pdf', null=True, upload_to='static/images/receipts/'),
        ),
    ]