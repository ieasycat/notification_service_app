# Generated by Django 3.2.13 on 2022-08-27 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_message_id_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='name',
        ),
        migrations.RemoveField(
            model_name='client',
            name='surname',
        ),
        migrations.RemoveField(
            model_name='client',
            name='unvisible_client',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='name_notification',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='unvisible_notification',
        ),
    ]