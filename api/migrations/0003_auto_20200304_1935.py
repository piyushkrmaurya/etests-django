# Generated by Django 3.0.3 on 2020-03-04 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200303_2119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('position', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('position', 'name'),
            },
        ),
        migrations.AlterModelOptions(
            name='exam',
            options={'ordering': ('position',)},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ('subject_index', 'topic_index', 'type', 'difficulty')},
        ),
        migrations.AddField(
            model_name='question',
            name='exams',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Exam'),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('position', models.IntegerField(default=0)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Subject')),
            ],
            options={
                'ordering': ('position', 'subject', 'name'),
            },
        ),
    ]
