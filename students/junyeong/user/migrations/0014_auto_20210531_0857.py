# Generated by Django 3.2.3 on 2021-05-31 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_auto_20210531_0707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(max_length=45, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=30, null=True, unique=True),
        ),
    ]
