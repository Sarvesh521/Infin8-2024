# Generated by Django 5.0.1 on 2024-01-24 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_alter_outgoingrequest_game_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='outgoingrequest',
            name='wins',
            field=models.IntegerField(default=0),
        ),
    ]
