# Generated by Django 5.0.1 on 2024-01-24 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_remove_user_request_points_outgoingrequest_turn_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outgoingrequest',
            name='game_link',
            field=models.CharField(max_length=255),
        ),
    ]
