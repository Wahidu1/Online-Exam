# Generated by Django 5.1 on 2024-08-24 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0002_notification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='user',
            new_name='examinee',
        ),
    ]