# Generated by Django 2.2.1 on 2019-09-30 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_test_aits'),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('acess_code', models.IntegerField()),
                ('date_added', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='codes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
