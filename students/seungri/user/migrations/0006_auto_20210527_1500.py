# Generated by Django 3.2.3 on 2021-05-27 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20210527_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(blank=True, max_length=45, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_num',
            field=models.CharField(blank=True, max_length=45, null=True, unique=True),
        ),
    ]
