# Generated by Django 4.2.4 on 2024-02-11 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_remove_status_num1_remove_status_num2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='requests_left',
            field=models.IntegerField(default=15),
        ),
    ]
