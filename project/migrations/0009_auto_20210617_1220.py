# Generated by Django 3.2.2 on 2021-06-17 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_auto_20210617_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='effective_hours',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='remaining_hours',
            field=models.TimeField(blank=True, null=True),
        ),
    ]