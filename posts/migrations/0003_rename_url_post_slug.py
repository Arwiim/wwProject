# Generated by Django 3.2.5 on 2021-07-31 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='url',
            new_name='slug',
        ),
    ]
