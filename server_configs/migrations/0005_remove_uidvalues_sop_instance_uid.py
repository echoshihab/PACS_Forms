# Generated by Django 2.2.5 on 2019-09-28 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server_configs', '0004_uidvalues_uid_counter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uidvalues',
            name='sop_instance_uid',
        ),
    ]
