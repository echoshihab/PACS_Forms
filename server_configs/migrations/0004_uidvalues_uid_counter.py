# Generated by Django 2.2.5 on 2019-09-28 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server_configs', '0003_uidvalues'),
    ]

    operations = [
        migrations.AddField(
            model_name='uidvalues',
            name='uid_counter',
            field=models.BigIntegerField(null=True),
        ),
    ]
