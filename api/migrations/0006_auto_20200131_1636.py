# Generated by Django 3.0.2 on 2020-01-31 11:06

from django.db import migrations, models
import etests.storage_backends


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20200130_0141'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='QuestionImage',
            new_name='Image',
        ),
        migrations.AlterModelOptions(
            name='testseriestransaction',
            options={'verbose_name_plural': 'Test Series Transactions'},
        ),
        migrations.AlterField(
            model_name='testseriestransaction',
            name='receipt',
            field=models.FileField(blank=True, null=True, storage=etests.storage_backends.PrivateMediaStorage(), upload_to=''),
        ),
    ]