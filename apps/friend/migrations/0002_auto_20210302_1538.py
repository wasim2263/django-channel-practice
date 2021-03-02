# Generated by Django 3.1.6 on 2021-03-02 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='user_1_connection_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='friend',
            name='user_1_update_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='friend',
            name='user_2_connection_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='friend',
            name='user_2_update_time',
            field=models.DateTimeField(null=True),
        ),
    ]
