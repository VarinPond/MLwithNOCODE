# Generated by Django 3.2.16 on 2022-11-07 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_history_loss'),
    ]

    operations = [
        migrations.AddField(
            model_name='members',
            name='table_id',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='members',
            name='user_id',
            field=models.IntegerField(default=1),
        ),
    ]