# Generated by Django 4.2.7 on 2024-05-26 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clicker_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='upgrade_level',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
