# Generated by Django 3.2.4 on 2021-06-25 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_remove_post_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
