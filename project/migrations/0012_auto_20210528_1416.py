# Generated by Django 3.2.2 on 2021-05-28 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_alter_project_last_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
