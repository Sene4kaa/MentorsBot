# Generated by Django 5.0.3 on 2024-03-21 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_alter_user_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='chat_id',
            field=models.BigIntegerField(),
        ),
    ]
