# Generated by Django 2.2.9 on 2020-01-24 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_board_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='name',
            field=models.TextField(),
        ),
    ]