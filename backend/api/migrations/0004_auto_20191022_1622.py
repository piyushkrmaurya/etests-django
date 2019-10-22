# Generated by Django 2.2.1 on 2019-10-22 10:52

import api.models
from django.db import migrations, models
import etests.storage_backends


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20191021_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionimage',
            name='file',
            field=models.ImageField(storage=etests.storage_backends.PublicMediaStorage(), upload_to='', validators=[api.models.validate_file_size]),
        ),
    ]