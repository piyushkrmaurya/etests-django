# Generated by Django 2.2.1 on 2019-10-02 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20191003_0053'),
    ]

    operations = [
        migrations.RenameField(
            model_name='test',
            old_name='ranklist',
            new_name='marks_list',
        ),
    ]
