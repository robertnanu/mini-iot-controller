# Generated by Django 4.0.2 on 2022-02-03 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temperature', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='humidity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
