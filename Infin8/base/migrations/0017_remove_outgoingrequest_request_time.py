# Generated by Django 4.2.4 on 2024-01-27 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_incomingrequest_valid_until_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outgoingrequest',
            name='request_time',
        ),
    ]